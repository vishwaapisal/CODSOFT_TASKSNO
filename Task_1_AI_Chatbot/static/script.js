const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatLog = document.getElementById("chatLog");

function escapeHTML(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function addMessage(message, type = "bot") {
  if (!chatLog) return;

  const messageRow = document.createElement("div");
  messageRow.className = `message ${type}`;

  const prefix = document.createElement("span");
  prefix.className = "prefix";
  prefix.textContent = type === "user" ? "you@codsoft:~$" : "bot@codsoft:~$";

  const text = document.createElement("span");
  text.className = "text";
  text.innerHTML = escapeHTML(message);

  messageRow.appendChild(prefix);
  messageRow.appendChild(text);
  chatLog.appendChild(messageRow);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function showTyping() {
  if (!chatLog) return;

  const existingTyping = document.getElementById("typingMessage");
  if (existingTyping) return;

  const typingRow = document.createElement("div");
  typingRow.className = "message bot typing";
  typingRow.id = "typingMessage";

  const prefix = document.createElement("span");
  prefix.className = "prefix";
  prefix.textContent = "bot@codsoft:~$";

  const text = document.createElement("span");
  text.className = "text";
  text.textContent = "typing...";

  typingRow.appendChild(prefix);
  typingRow.appendChild(text);
  chatLog.appendChild(typingRow);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function removeTyping() {
  const typingMessage = document.getElementById("typingMessage");
  if (typingMessage) {
    typingMessage.remove();
  }
}

async function sendMessage(message) {
  if (!message || !message.trim()) return;

  addMessage(message, "user");
  userInput.value = "";
  showTyping();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    setTimeout(() => {
      removeTyping();
      addMessage(data.response, "bot");
    }, 500);
  } catch (error) {
    removeTyping();
    addMessage("Sorry, something went wrong. Please try again.", "bot");
    console.error(error);
  }
}

if (chatForm && userInput) {
  chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage(userInput.value);
  });
}
