const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");

let userMessage;
const API_KEY = "AIzaSyAjgynltiF_SVDedXyDVyyqaqtbDGm7Dpk";
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // create a chat <li> elment with passed message and className 
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing"? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

const generateResponse = (incomingChatLi) => {
    const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${API_KEY}`
    const messageElement = incomingChatLi.querySelector("p");

    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            contents: [{ 
                role: "user", 
                parts: [{ text: userMessage }] 
            }] 
        }),
    };
    
    // send POST request to API, get response
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        messageElement.textContent = data.candidates[0].content.parts[0].text
    }).catch((error) => {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if(!userMessage) return;
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;
 
    //append the user's message to the chatbox
    chatbox.appendChild(createChatLi (userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        //display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi ("Thinking...", "incoming")
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    //Adjust the heihgt of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // if enter is pressed without shift key and the window width is 
    // greater than 800px handle the chat    
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));








// const generateResponse = (incomingChatLi, userMessage) => {
//     const API_URL = 'http://127.0.0.1:8080/generate_response'; // Flask endpoint
//     const messageElement = incomingChatLi.querySelector("p");

//     const requestOptions = {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ message: userMessage }),
//     };

//     fetch(API_URL, requestOptions)
//         .then(res => res.json())
//         .then(data => {
//             messageElement.textContent = data.response || "No response";
//         })
//         .catch(error => {
//             messageElement.classList.add("error");
//             messageElement.textContent = "Oops! Something went wrong.";
//         })
//         .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
// };



// document.getElementById("send-btn").addEventListener("click", () => {
//     const chatbox = document.querySelector(".chatbox");
//     const textarea = document.querySelector(".chat-input textarea");
//     const userMessage = textarea.value.trim();

//     if (userMessage) {
//         // Append user message to chatbox
//         const userChatLi = document.createElement("li");
//         userChatLi.className = "chat outgoing";
//         userChatLi.innerHTML = `<p>${userMessage}</p>`;
//         chatbox.appendChild(userChatLi);

//         // Append bot's response placeholder
//         const botChatLi = document.createElement("li");
//         botChatLi.className = "chat incoming";
//         botChatLi.innerHTML = `
//             <span class="material-symbols-outlined">smart_toy</span>
//             <p>Typing...</p>
//         `;
//         chatbox.appendChild(botChatLi);

//         // Call the function to get bot response
//         generateResponse(botChatLi, userMessage);

//         // Clear the textarea
//         textarea.value = "";
//     }
// });
