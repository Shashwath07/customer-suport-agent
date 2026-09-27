/* =========================================================
   CUSTOMER SUPPORT AI AGENT
   Frontend JavaScript
   ========================================================= */


/* ================= CONFIGURATION ================= */

const API_URL = "/api/chat";


/* ================= DOM ELEMENTS ================= */

const customerIdInput =
    document.getElementById("customer-id");

const loadCustomerButton =
    document.getElementById("load-customer-btn");

const customerDisplay =
    document.getElementById("customer-display");

const messageInput =
    document.getElementById("message-input");

const sendButton =
    document.getElementById("send-btn");

const clearChatButton =
    document.getElementById("clear-chat-btn");

const chatMessages =
    document.getElementById("chat-messages");

const typingIndicator =
    document.getElementById("typing-indicator");

const memoryList =
    document.getElementById("memory-list");

const memoryStatus =
    document.getElementById("memory-status");


/* ================= APPLICATION STATE ================= */

let currentCustomerId =
    customerIdInput.value.trim();

let isSending = false;


/* ================= INITIALIZATION ================= */

document.addEventListener("DOMContentLoaded", () => {

    updateCustomerDisplay();

    messageInput.focus();

});


/* ================= CUSTOMER ================= */

function getCustomerId() {

    return customerIdInput.value
        .trim()
        .toUpperCase();

}


function updateCustomerDisplay() {

    currentCustomerId = getCustomerId();

    if (!currentCustomerId) {

        customerDisplay.textContent =
            "Customer: Not selected";

        setMemoryStatus(
            "Waiting for customer",
            false
        );

        return;
    }

    customerDisplay.textContent =
        `Customer: ${currentCustomerId}`;

    setMemoryStatus(
        `Memory ready for ${currentCustomerId}`,
        true
    );

}


function loadCustomer() {

    const customerId =
        getCustomerId();

    if (!customerId) {

        showError(
            "Please enter a customer ID first."
        );

        customerIdInput.focus();

        return;
    }

    currentCustomerId =
        customerId;

    updateCustomerDisplay();

    clearMemoryList();

    addSystemMessage(
        `Customer ${customerId} loaded. You can now start a support conversation.`
    );

    messageInput.focus();

}


/* ================= SEND MESSAGE ================= */

async function sendMessage() {

    if (isSending) {
        return;
    }

    const message =
        messageInput.value.trim();

    const customerId =
        getCustomerId();


    if (!customerId) {

        showError(
            "Please enter a customer ID."
        );

        customerIdInput.focus();

        return;
    }


    if (!message) {

        messageInput.focus();

        return;
    }


    currentCustomerId =
        customerId;


    /* Display user's message */

    addUserMessage(message);


    /* Clear input */

    messageInput.value = "";

    autoResizeTextarea();


    /* Start loading state */

    setSendingState(true);

    showTypingIndicator();


    try {

        const result =
            await callChatAPI(
                customerId,
                message
            );


        hideTypingIndicator();


        if (!result.success) {

            addErrorMessage(
                result.error ||
                "The server could not process your request."
            );

            return;
        }


        /* Display AI response */

        addAIMessage(
            result.response ||
            "I received your message, but no response was generated."
        );


        /* Update recalled memory */

        updateMemoryPanel(
            result.used_memory || []
        );


    } catch (error) {

        console.error(
            "Chat API error:",
            error
        );


        hideTypingIndicator();


        addErrorMessage(
            "Unable to connect to the support server. Please check that the backend is running."
        );

    } finally {

        setSendingState(false);

        messageInput.focus();

    }

}


/* ================= API CALL ================= */

async function callChatAPI(
    customerId,
    message
) {

    const response =
        await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    customer_id:
                        customerId,

                    message:
                        message

                })

            }
        );


    let data;

    try {

        data =
            await response.json();

    } catch {

        throw new Error(
            "Invalid response received from server."
        );

    }


    if (!response.ok) {

        throw new Error(
            data.error ||
            `Server returned status ${response.status}.`
        );

    }


    return data;

}


/* ================= ADD USER MESSAGE ================= */

function addUserMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message user-message";


    messageElement.innerHTML = `

        <div class="avatar user-avatar">
            YOU
        </div>

        <div class="message-content">

            <div class="message-name">
                You
            </div>

            <div class="message-bubble"></div>

            <div class="message-time">
                ${getCurrentTime()}
            </div>

        </div>

    `;


    const bubble =
        messageElement.querySelector(
            ".message-bubble"
        );


    bubble.textContent =
        message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* ================= ADD AI MESSAGE ================= */

function addAIMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message ai-message";


    messageElement.innerHTML = `

        <div class="avatar ai-avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                SupportAI
            </div>

            <div class="message-bubble"></div>

            <div class="message-time">
                ${getCurrentTime()}
            </div>

        </div>

    `;


    const bubble =
        messageElement.querySelector(
            ".message-bubble"
        );


    bubble.textContent =
        message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* ================= SYSTEM MESSAGE ================= */

function addSystemMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message ai-message";


    messageElement.innerHTML = `

        <div class="avatar ai-avatar">
            AI
        </div>

        <div class="message-content">

            <div class="message-name">
                SupportAI
            </div>

            <div class="message-bubble"></div>

            <div class="message-time">
                ${getCurrentTime()}
            </div>

        </div>

    `;


    messageElement
        .querySelector(".message-bubble")
        .textContent = message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* ================= ERROR MESSAGE ================= */

function addErrorMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message ai-message error-message";


    messageElement.innerHTML = `

        <div class="avatar ai-avatar">
            !
        </div>

        <div class="message-content">

            <div class="message-name">
                SupportAI
            </div>

            <div class="message-bubble"></div>

            <div class="message-time">
                ${getCurrentTime()}
            </div>

        </div>

    `;


    messageElement
        .querySelector(".message-bubble")
        .textContent = message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* ================= SHOW ERROR ================= */

function showError(message) {

    addErrorMessage(message);

}


/* ================= MEMORY PANEL ================= */

function updateMemoryPanel(memories) {

    memoryList.innerHTML = "";


    if (
        !Array.isArray(memories) ||
        memories.length === 0
    ) {

        memoryList.innerHTML = `

            <div class="empty-memory">

                <div class="empty-memory-icon">
                    🧠
                </div>

                <h3>
                    No relevant memories
                </h3>

                <p>
                    No customer memories were
                    returned for this message.
                </p>

            </div>

        `;


        setMemoryStatus(
            "No relevant memory found",
            false
        );

        return;
    }


    memories.forEach(
        (memory, index) => {

            const memoryElement =
                document.createElement("div");

            memoryElement.className =
                "memory-item";


            memoryElement.innerHTML = `

                <div class="memory-item-header">

                    <span class="memory-item-icon">
                        🧠
                    </span>

                    <span class="memory-item-label">
                        Recalled Memory ${index + 1}
                    </span>

                </div>

                <div class="memory-item-text"></div>

            `;


            memoryElement
                .querySelector(
                    ".memory-item-text"
                )
                .textContent =
                    formatMemory(memory);


            memoryList.appendChild(
                memoryElement
            );

        }
    );


    setMemoryStatus(
        `${memories.length} memory item(s) recalled`,
        true
    );

}


/* ================= MEMORY FORMAT ================= */

function formatMemory(memory) {

    if (
        typeof memory === "string"
    ) {

        return memory;

    }


    if (
        memory &&
        typeof memory === "object"
    ) {

        if (memory.text) {
            return memory.text;
        }

        if (memory.content) {
            return memory.content;
        }

        try {

            return JSON.stringify(
                memory,
                null,
                2
            );

        } catch {

            return String(memory);

        }

    }


    return String(memory);

}


/* ================= CLEAR MEMORY ================= */

function clearMemoryList() {

    memoryList.innerHTML = `

        <div class="empty-memory">

            <div class="empty-memory-icon">
                🧠
            </div>

            <h3>
                No memories yet
            </h3>

            <p>
                Customer memories will appear here
                when the AI recalls useful information.
            </p>

        </div>

    `;


    setMemoryStatus(
        `Memory ready for ${currentCustomerId}`,
        true
    );

}


/* ================= MEMORY STATUS ================= */

function setMemoryStatus(
    text,
    active
) {

    memoryStatus.innerHTML = `

        <span class="memory-status-dot"></span>

        <span>
            ${escapeHTML(text)}
        </span>

    `;


    if (active) {

        memoryStatus.classList.add(
            "active"
        );

    } else {

        memoryStatus.classList.remove(
            "active"
        );

    }

}


/* ================= TYPING INDICATOR ================= */

function showTypingIndicator() {

    typingIndicator.classList.remove(
        "hidden"
    );

    scrollChatToBottom();

}


function hideTypingIndicator() {

    typingIndicator.classList.add(
        "hidden"
    );

}


/* ================= SENDING STATE ================= */

function setSendingState(sending) {

    isSending =
        sending;

    sendButton.disabled =
        sending;

    messageInput.disabled =
        sending;

    loadCustomerButton.disabled =
        sending;

}


/* ================= CLEAR CHAT ================= */

function clearChat() {

    chatMessages.innerHTML = "";

    clearMemoryList();

    addSystemMessage(
        `Chat cleared for ${currentCustomerId}. How can I help you?`
    );

}


/* ================= TEXTAREA ================= */

function autoResizeTextarea() {

    messageInput.style.height =
        "auto";


    const newHeight =
        Math.min(
            messageInput.scrollHeight,
            130
        );


    messageInput.style.height =
        `${newHeight}px`;

}


/* ================= SCROLL ================= */

function scrollChatToBottom() {

    requestAnimationFrame(() => {

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

    });

}


/* ================= TIME ================= */

function getCurrentTime() {

    return new Date()
        .toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );

}


/* ================= HTML ESCAPE ================= */

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;

}


/* ================= EVENT LISTENERS ================= */


/* Send button */

sendButton.addEventListener(
    "click",
    sendMessage
);


/* Load customer */

loadCustomerButton.addEventListener(
    "click",
    loadCustomer
);


/* Clear chat */

clearChatButton.addEventListener(
    "click",
    clearChat
);


/* Enter key */

messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* Resize textarea */

messageInput.addEventListener(
    "input",
    autoResizeTextarea
);


/* Customer ID input */

customerIdInput.addEventListener(
    "input",
    () => {

        customerIdInput.value =
            customerIdInput.value
                .toUpperCase();

    }
);


/* Customer ID Enter key */

customerIdInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            loadCustomer();

        }

    }
);
