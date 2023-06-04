const chatbotForm = document.getElementById("chatbot-form");
const chatbotInput = document.getElementById("chatbot-input");
const conversationContainer = document.getElementById("conversation-container");

chatbotForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = chatbotInput.value.trim();

  if (question === "") {
    return;
  }

  const response = await fetch("/chatbot", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await response.json();
  const botMessage = data.response;

  appendMessage("user", question);
  appendMessage("bot", botMessage);

  chatbotInput.value = "";
});

function appendMessage(sender, message) {
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message", sender);
  messageContainer.textContent = message;

  conversationContainer.appendChild(messageContainer);
  conversationContainer.scrollTop = conversationContainer.scrollHeight;
}
