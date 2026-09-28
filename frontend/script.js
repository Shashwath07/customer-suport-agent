document.addEventListener("DOMContentLoaded", () => {
  // Page Navigation Elements
  const landingPage = document.getElementById("landing-page");
  const appModal = document.getElementById("app-modal");
  const openAppBtn = document.getElementById("open-app-btn");
  const heroDemoBtn = document.getElementById("hero-demo-btn");
  const closeAppBtn = document.getElementById("close-app-btn");
  const exitChatBtn = document.getElementById("exit-chat-btn");

  const launchApp = () => {
    landingPage.classList.add("hidden");
    appModal.classList.remove("hidden");
  };

  const closeApp = () => {
    appModal.classList.add("hidden");
    landingPage.classList.remove("hidden");
  };

  openAppBtn.addEventListener("click", launchApp);
  heroDemoBtn.addEventListener("click", launchApp);
  closeAppBtn.addEventListener("click", closeApp);
  exitChatBtn.addEventListener("click", closeApp);

  // Chat Elements
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");

  // Consistent Customer ID aligned with mock backend
  const CUSTOMER_ID = "cust1";

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const messageText = userInput.value.trim();
    if (!messageText) return;

    appendMessage(messageText, "user");
    userInput.value = "";

    const loadingMessage = appendLoadingMessage();

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: CUSTOMER_ID,
          message: messageText,
        }),
      });

      const data = await response.json();
      loadingMessage.remove();

      // Aligned with backend output keys: reply & recalled_memories
      if (response.ok && data.reply) {
        let citation = null;
        if (data.recalled_memories && data.recalled_memories.length > 0) {
          citation = `Recalled: ${data.recalled_memories[0]}`;
          updateSidebarMemory(data.recalled_memories[0]);
        }
        appendMessage(data.reply, "bot", citation);
      } else {
        appendMessage(
          data.error || "I encountered an error looking up customer memory history.",
          "bot"
        );
      }
    } catch (error) {
      loadingMessage.remove();
      appendMessage(
        "Could not connect to the backend server. Ensure backend/app.py is running on port 5000.",
        "bot"
      );
    }
  });

  function updateSidebarMemory(memoryText) {
    const historyTitle = document.querySelector(".history-title");
    if (historyTitle) {
      historyTitle.textContent = memoryText;
    }
  }

  function appendMessage(text, sender, citation = null) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", `${sender}-message`);

    const icon = sender === "bot" ? "fa-robot" : "fa-user";
    const name = sender === "bot" ? "Hindsight Agent" : "You";

    let citationHTML = citation
      ? `<div class="memory-citation"><i class="fa-solid fa-microchip"></i> ${citation}</div>`
      : "";

    msgDiv.innerHTML = `
      <div class="message-avatar"><i class="fa-solid ${icon}"></i></div>
      <div class="message-bubble">
        <div class="message-sender">${name} <span class="time">Just now</span></div>
        <div class="message-text">${text}</div>
        ${citationHTML}
      </div>
    `;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgDiv;
  }

  function appendLoadingMessage() {
    const loadingDiv = document.createElement("div");
    loadingDiv.classList.add("message", "bot-message");
    loadingDiv.innerHTML = `
      <div class="message-avatar"><i class="fa-solid fa-robot"></i></div>
      <div class="message-bubble">
        <div class="message-text" style="color: #9ca3af;">
          <i class="fa-solid fa-spinner fa-spin"></i> Querying Hindsight memory store...
        </div>
      </div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingDiv;
  }
});
