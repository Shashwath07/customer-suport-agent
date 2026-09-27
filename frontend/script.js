/* =========================================================
   CUSTOMER SUPPORT AI AGENT
   FRONTEND JAVASCRIPT
   ========================================================= */


/* =========================================================
   CONFIGURATION
   ========================================================= */

const API_URL = "/api/chat";
const HEALTH_URL = "/api/health";


/* =========================================================
   DOM ELEMENTS
   ========================================================= */

const customerIdInput =
    document.getElementById("customer-id");

const loadCustomerButton =
    document.getElementById("load-customer-btn");

const customerDisplay =
    document.getElementById("customer-display");

const customerInfo =
    document.getElementById("customer-info");

const customerName =
    document.getElementById("customer-name");

const customerIdDisplay =
    document.getElementById("customer-id-display");

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

const memoryStatusText =
    document.getElementById("memory-status-text");

const connectionStatus =
    document.getElementById("connection-status");

const connectionText =
    document.getElementById("connection-text");


/* =========================================================
   APPLICATION STATE
   ========================================================= */

let currentCustomerId =
    customerIdInput.value.trim().toUpperCase();

let isSending = false;


/* =========================================================
   INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        updateCustomerDisplay();

        await checkBackendConnection();

        messageInput.focus();

    }
);


/* =========================================================
   BACKEND CONNECTION
   ========================================================= */

async function checkBackendConnection() {

    try {

        const response =
            await fetch(
                HEALTH_URL
            );


        const data =
            await response.json();


        if (
            response.ok &&
            data.success
        ) {

            setConnectionStatus(
                true,
                "AI Online"
            );

        } else {

            setConnectionStatus(
                false,
                "Server Error"
            );

        }

    } catch (error) {

        console.error(
            "Backend health check failed:",
            error
        );


        setConnectionStatus(
            false,
            "Backend Offline"
        );

    }

}


function setConnectionStatus(
    online,
    text
) {

    connectionText.textContent =
        text;


    connectionStatus.classList.remove(
        "online",
        "offline"
    );


    if (online) {

        connectionStatus.classList.add(
            "online"
        );

    } else {

        connectionStatus.classList.add(
            "offline"
        );

    }

}


/* =========================================================
   CUSTOMER
   ========================================================= */

function getCustomerId() {

    return customerIdInput
        .value
        .trim()
        .toUpperCase();

}


function updateCustomerDisplay() {

    currentCustomerId =
        getCustomerId();


    if (!currentCustomerId) {

        customerDisplay.textContent =
            "Customer: Not selected";


        customerInfo.classList.add(
            "hidden"
        );


        setMemoryStatus(
            "Waiting for customer",
            false
        );


        return;
    }


    customerDisplay.textContent =
        `Customer: ${currentCustomerId}`;


    customerIdDisplay.textContent =
        currentCustomerId;

}


function loadCustomer() {

    const customerId =
        getCustomerId();


    if (!customerId) {

        addErrorMessage(
            "Please enter a customer ID."
        );

        customerIdInput.focus();

        return;
    }


    currentCustomerId =
        customerId;


    updateCustomerDisplay();


    customerInfo.classList.add(
        "hidden"
    );


    clearMemoryList();


    addSystemMessage(
        `Customer ${customerId} selected. You can now start a support conversation.`
    );


    setMemoryStatus(
        `Memory ready for ${customerId}`,
        true
    );


    messageInput.focus();

}


/* =========================================================
   SEND MESSAGE
   ========================================================= */

async function sendMessage() {

    if (isSending) {
        return;
    }


    const message =
        messageInput.value.trim();


    const customerId =
        getCustomerId();


    /* -------------------------------
       Validate customer
       ------------------------------- */

    if (!customerId) {

        addErrorMessage(
            "Please enter a customer ID."
        );

        customerIdInput.focus();

        return;
    }


    /* -------------------------------
       Validate message
       ------------------------------- */

    if (!message) {

        messageInput.focus();

        return;
    }


    currentCustomerId =
        customerId;


    /* -------------------------------
       Display user message
       ------------------------------- */

    addUserMessage(
        message
    );


    /* -------------------------------
       Clear input
       ------------------------------- */

    messageInput.value = "";

    autoResizeTextarea();


    /* -------------------------------
       Loading state
       ------------------------------- */

    setSendingState(
        true
    );

    showTypingIndicator();


    try {

        /* ---------------------------
           Call backend
           --------------------------- */

        const result =
            await callChatAPI(
                customerId,
                message
            );


        hideTypingIndicator();


        /* ---------------------------
           Backend failure
           --------------------------- */

        if (!result.success) {

            addErrorMessage(
                result.error ||
                "The server could not process the request."
            );

            return;
        }


        /* ---------------------------
           Update customer information
           --------------------------- */

        if (result.customer_name) {

            customerName.textContent =
                result.customer_name;

            customerIdDisplay.textContent =
                result.customer_id;

            customerInfo.classList.remove(
                "hidden"
            );

        }


        /* ---------------------------
           Display AI response
           --------------------------- */

        addAIMessage(
            result.response ||
            "No response was generated."
        );


        /* ---------------------------
           Update recalled memories
           --------------------------- */

        updateMemoryPanel(
            result.used_memory || []
        );


        /* ---------------------------
           Update memory state
           --------------------------- */

        if (
            result.memory_saved === true
        ) {

            setMemoryStatus(
                "Memory updated from conversation",
                true
            );

        }


    } catch (error) {

        console.error(
            "Chat API error:",
            error
        );


        hideTypingIndicator();


        addErrorMessage(
            "Unable to connect to the backend. Make sure the Flask server is running."
        );


    } finally {

        setSendingState(
            false
        );

        messageInput.focus();

    }

}


/* =========================================================
   CHAT API
   ========================================================= */

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

    } catch (error) {

        throw new Error(
            "The backend returned an invalid response."
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


/* =========================================================
   ADD USER MESSAGE
   ========================================================= */

function addUserMessage(
    message
) {

    const messageElement =
        document.createElement(
            "div"
        );


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


/* =========================================================
   ADD AI MESSAGE
   ========================================================= */

function addAIMessage(
    message
) {

    const messageElement =
        document.createElement(
            "div"
        );


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


/* =========================================================
   SYSTEM MESSAGE
   ========================================================= */

function addSystemMessage(
    message
) {

    const messageElement =
        document.createElement(
            "div"
        );


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
        .querySelector(
            ".message-bubble"
        )
        .textContent = message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* =========================================================
   ERROR MESSAGE
   ========================================================= */

function addErrorMessage(
    message
) {

    const messageElement =
        document.createElement(
            "div"
        );


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
        .querySelector(
            ".message-bubble"
        )
        .textContent = message;


    chatMessages.appendChild(
        messageElement
    );


    scrollChatToBottom();

}


/* =========================================================
   MEMORY PANEL
   ========================================================= */

function updateMemoryPanel(
    memories
) {

    memoryList.innerHTML =
        "";


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
                    Hindsight did not return relevant
                    memories for this message.
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
        (
            memory,
            index
        ) => {

            const memoryElement =
                document.createElement(
                    "div"
                );


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


            const textElement =
                memoryElement.querySelector(
                    ".memory-item-text"
                );


            textElement.textContent =
                formatMemory(
                    memory
                );


            memoryList.appendChild(
                memoryElement
            );

        }
    );


    setMemoryStatus(
        `${memories.length} relevant memory item(s) recalled`,
        true
    );

}


/* =========================================================
   FORMAT MEMORY
   ========================================================= */

function formatMemory(
    memory
) {

    if (
        typeof memory === "string"
    ) {

        return memory;

    }


    if (
        memory &&
        typeof memory === "object"
    ) {

        if (
            memory.text
        ) {

            return memory.text;

        }


        if (
            memory.content
        ) {

            return memory.content;

        }


        try {

            return JSON.stringify(
                memory,
                null,
                2
            );

        } catch {

            return String(
                memory
            );

        }

    }


    return String(
        memory
    );

}


/* =========================================================
   CLEAR MEMORY
   ========================================================= */

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
                Relevant customer memories will
                appear here when recalled.
            </p>

        </div>

    `;


    setMemoryStatus(
        `Memory ready for ${currentCustomerId}`,
        true
    );

}


/* =========================================================
   MEMORY STATUS
   ========================================================= */

function setMemoryStatus(
    text,
    active
) {

    memoryStatusText.textContent =
        text;


    memoryStatus.classList.remove(
        "active"
    );


    if (active) {

        memoryStatus.classList.add(
            "active"
        );

    }

}


/* =========================================================
   TYPING INDICATOR
   ========================================================= */

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


/* =========================================================
   SENDING STATE
   ========================================================= */

function setSendingState(
    sending
) {

    isSending =
        sending;


    sendButton.disabled =
        sending;


    messageInput.disabled =
        sending;


    loadCustomerButton.disabled =
        sending;


    clearChatButton.disabled =
        sending;

}


/* =========================================================
   CLEAR CHAT
   ========================================================= */

function clearChat() {

    chatMessages.innerHTML =
        "";


    clearMemoryList();


    customerInfo.classList.add(
        "hidden"
    );


    addSystemMessage(
        `Chat cleared for ${currentCustomerId || "the selected customer"}. How can I help you?`
    );


    messageInput.focus();

}


/* =========================================================
   TEXTAREA RESIZE
   ========================================================= */

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


/* =========================================================
   SCROLL CHAT
   ========================================================= */

function scrollChatToBottom() {

    requestAnimationFrame(
        () => {

            chatMessages.scrollTop =
                chatMessages.scrollHeight;

        }
    );

}


/* =========================================================
   TIME
   ========================================================= */

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


/* =========================================================
   EVENT LISTENERS
   ========================================================= */


/* Send */

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


/* Enter = Send
   Shift + Enter = New line
*/

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


/* Customer ID uppercase */

customerIdInput.addEventListener(
    "input",
    () => {

        customerIdInput.value =
            customerIdInput.value
                .toUpperCase();

    }
);


/* Customer ID Enter */

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
