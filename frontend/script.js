// frontend/script.js
document.addEventListener("DOMContentLoaded", () => {
  const landingPage = document.getElementById("landing-page");
  const appModal = document.getElementById("app-modal");
  const openAppBtn = document.getElementById("open-app-btn");
  const heroDemoBtn = document.getElementById("hero-demo-btn");
  const closeAppBtn = document.getElementById("close-app-btn");
  const exitChatBtn = document.getElementById("exit-chat-btn");

  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");

  const CUSTOMER_ID = "CUST001";
  const API_BASE = "http://127.0.0.1:5000";

  // Fetch initial profile & tickets on load
  async function loadCustomerData() {
    try {
      const res = await fetch(`${API_BASE}/customer/${CUSTOMER_ID}`);
      if (res.ok) {
        const data = await res.json();
        renderSidebar(data.profile, data.tickets);
      }
    } catch (e) {
      console.warn("Could not pre-load customer info:", e);
    }
  }

  function renderSidebar(profile, tickets) {
    if (!profile) return;
    
    // Update Profile
    const profileCard = document.querySelector(".profile-card");
    if (profileCard) {
      const initials = profile.name.slice(0, 2).toUpperCase();
      profileCard.querySelector(".avatar").textContent = initials;
      profileCard.querySelector(".profile-info h3").textContent = profile.name;
      profileCard.querySelector(".cust-id").textContent = `ID: #${profile.customer_id}`;
      profileCard.querySelector(".tier-badge").innerHTML = `<i class="fa-solid fa-shield-halved"></i> ${profile.plan} Plan`;
    }

    // Update Tickets list
    if (tickets && tickets.length > 0) {
      const latest = tickets[tickets.length - 1];
      const historyItem = document.querySelector(".history-item");
      if (historyItem) {
        historyItem.querySelector(".ticket-id").textContent = `#${latest.ticket_id}`;
        historyItem.querySelector(".history-title").textContent = latest.issue;
        historyItem.querySelector(".pill").textContent = `Status: ${latest.status} (${latest.result})`;
      }
    }
  }

  const launchApp = () => {
    landingPage.classList.add("hidden");
    appModal.classList.remove("hidden");
    loadCustomerData();
  };

  const closeApp = () => {
    appModal.classList.add("hidden");
    landingPage.classList.remove("hidden");
  };

  openAppBtn.addEventListener("click", launchApp);
  heroDemoBtn.addEventListener("click", launchApp);
  closeAppBtn.addEventListener("click", closeApp);
  exitChatBtn.addEventListener("click", closeApp);

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageText = userInput.value.trim();
    if (!messageText) return;

    appendMessage(messageText, "user");
    userInput.value = "";
    const loadingMessage = appendLoadingMessage();

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: CUSTOMER_ID,
          message: messageText,
        }),
      });

      const data = await response.json();
      loadingMessage.remove();

      if (response.ok && data.reply) {
        let citation = null;
        if (data.recalled_memories && data.recalled_memories.length > 0) {
          citation = `Recalled from memory: ${data.recalled_memories[0]}`;
        }
        appendMessage(data.reply, "bot", citation);

        if (data.profile || data.tickets) {
          renderSidebar(data.profile, data.tickets);
        }
      } else {
        appendMessage(data.error || "Error processing request.", "bot");
      }
    } catch (err) {
      loadingMessage.remove();
      appendMessage("Failed to connect to backend server.", "bot");
    }
  });

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
