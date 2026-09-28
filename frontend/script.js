document.addEventListener("DOMContentLoaded", () => {
  // Page Navigation Elements
  const landingPage = document.getElementById("landing-page");
  const appModal = document.getElementById("app-modal");
  const openAppBtn = document.getElementById("open-app-btn");
  const heroDemoBtn = document.getElementById("hero-demo-btn");
  const closeAppBtn = document.getElementById("close-app-btn");
  const exitChatBtn = document.getElementById("exit-chat-btn");
  const clearChatBtn = document.getElementById("clear-chat-btn");

  // Chat Interface Elements
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const chatMessages = document.getElementById("chat-messages");

  // Relative API URL: works seamlessly whether hosted locally or via Codespaces
  const API_BASE = "";

  // Persistent User Session ID in browser storage
  let customerId = localStorage.getItem("hindsight_user_id");
  if (!customerId) {
    customerId = "CUST-" + Math.floor(1000 + Math.random() * 9000);
    localStorage.setItem("hindsight_user_id", customerId);
  }

  // Pre-load customer details & tickets from memory/database
  async function loadCustomerData() {
    try {
      const res = await fetch(`${API_BASE}/customer/${customerId}`);
      if (res.ok) {
        const data = await res.json();
        renderSidebar(data.profile, data.tickets);
        if (data.profile && data.profile.name && data.profile.name !== "Guest User") {
          resetChatThread(data.profile.name);
          return;
        }
      }
    } catch (e) {
      console.warn("Could not pre-load customer info:", e);
    }
    resetChatThread(null);
  }

  function renderSidebar(profile, tickets) {
    if (!profile) return;

    // Update Profile Card
    const profileCard = document.querySelector(".profile-card");
    if (profileCard) {
      const initials = (profile.name || "GU").slice(0, 2).toUpperCase();
      profileCard.querySelector(".avatar").textContent = initials;
      profileCard.querySelector(".profile-info h3").textContent = profile.name || "Guest User";
      profileCard.querySelector(".cust-id").textContent = `ID: #${profile.customer_id || customerId}`;
      profileCard.querySelector(".tier-badge").innerHTML = `<i class="fa-solid fa-shield-halved"></i> ${profile.plan || "Standard"} Plan`;
    }

    // Update Tickets block
    if (tickets && tickets.length > 0) {
      const latest = tickets[tickets.length - 1];
      const historyItem = document.querySelector(".history-item");
      if (historyItem) {
        historyItem.querySelector(".ticket-id").textContent = `#${latest.ticket_id}`;
        historyItem.querySelector(".history-title").textContent = latest.issue;
        const pill = historyItem.querySelector(".pill");
        if (pill) {
          pill.textContent = `Status: ${latest.status} (${latest.result})`;
        }
      }
    }
  }

  function resetChatThread(userName = null) {
    chatMessages.innerHTML = "";
    const greeting = userName
      ? `Welcome back, ${userName}! I still have your details and context saved in Hindsight memory. How can I assist you today?`
      : "Hello! I've loaded your workspace context. Tell me your name or describe your issue, and I'll retain it across your sessions.";

    appendMessage(greeting, "bot");
  }

  // Navigation Event Handlers
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

  // Clear Chat Button Logic (Tests memory retention after wiping DOM messages)
  if (clearChatBtn) {
    clearChatBtn.addEventListener("click", () => {
      loadCustomerData();
    });
  }

  // Submit Chat Message
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
          customer_id: customerId,
          message: messageText,
        }),
      });

      const data = await response.json();
      loadingMessage.remove();

      if (response.ok && data.reply) {
        let citation = null;
        if (data.recalled_memories && data.recalled_memories.length > 0) {
          citation = `Recalled from Hindsight: ${data.recalled_memories[0]}`;
        }
        appendMessage(data.reply, "bot", citation);

        if (data.profile || data.tickets) {
          renderSidebar(data.profile, data.tickets);
        }
      } else {
        appendMessage(
          data.error || "I encountered an error looking up customer memory history.",
          "bot"
        );
      }
    } catch (error) {
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
