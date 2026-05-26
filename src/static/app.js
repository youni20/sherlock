class Queue {
    constructor() {
        this.items = [];
    }
    enqueue(item) {
        this.items.push(item);
    }
    dequeue() {
        return this.isEmpty() ? null : this.items.shift();
    }
    peek() {
        return this.isEmpty() ? null : this.items[0];
    }
    isEmpty() {
        return this.items.length === 0;
    }
    remove(item) {
        const i = this.items.indexOf(item);
        if (i >= 0) this.items.splice(i, 1);
    }
    clear() {
        this.items = [];
    }
}


const questionQueue = new Queue();
let isProcessing = false;


function addQueueItem(question) {
    const entry = document.createElement("li");
    entry.className = "queue_item";
    const questionText = document.createElement("span");
    questionText.textContent = question;
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "queue_remove";
    removeButton.textContent = "×";
    entry.appendChild(questionText);
    entry.appendChild(removeButton);
    document.getElementById("queue_list").appendChild(entry);

    const queuedQuestion = { text: question, entry };
    questionQueue.enqueue(queuedQuestion);

    removeButton.addEventListener("click", () => {
        questionQueue.remove(queuedQuestion);
        entry.remove();
    });
}


function addMessage(text, role) {
    const bubble = document.createElement("p");
    bubble.className = `msg ${role}`;
    bubble.textContent = text;
    document.getElementById("chat_box").appendChild(bubble);
    return bubble;
}


async function processQueue() {
    isProcessing = true;
    while (!questionQueue.isEmpty()) {
        const queuedQuestion = questionQueue.dequeue();
        queuedQuestion.entry.remove();
        addMessage(`You: ${queuedQuestion.text}`, "user");
        const loadingBubble = addMessage("Agent: ...", "agent");
        const response = await fetch("/get_answer", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: queuedQuestion.text }) });
        const data = await response.json();
        const noEvidence = "I don't have enough evidence to answer that.";
        loadingBubble.textContent = data.answer === noEvidence
            ? `Agent: ${data.answer}`
            : `Agent: ${data.answer} (Source: ${data.sources})`;
    }
    isProcessing = false;
}

document.getElementById("question_form").addEventListener("submit", (e) => {
    e.preventDefault();
    const question = document.getElementById("question").value.trim();

    if (question === "/clear") {
        document.getElementById("chat_box").innerHTML = "";
        document.getElementById("queue_list").innerHTML = "";
        questionQueue.clear();
        document.getElementById("question_form").reset();
        return;
    }

    if (!question) return;
    addQueueItem(question);
    document.getElementById("question_form").reset();
    if (!isProcessing) processQueue();
});

document.getElementById("upload_file").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append("file", document.getElementById("file_upload").files[0]);

    const response = await fetch("/ingest_file", {
        method: "POST",
        body: data,
    });
    console.log(await response.json());
});
