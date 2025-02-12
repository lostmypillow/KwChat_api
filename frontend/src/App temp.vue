<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { nextTick } from "vue";
import axios from "axios";
const chatContainer = ref(null);
const username = ref(""); // User's name
const isLoggedIn = ref(false);
const isReceiver = ref(false);
const receiver = ref("user2"); // Receiver's name
const message = ref(""); // Message input
const messages = ref([]); // Message history
let ws = null;
const confirmReceiver = () => {
  isReceiver.value = true;
  scrollToBottom();
  console.log("scroll?");
};

// Fetch message history from FastAPI
const fetchMessages = async () => {
  try {
    const response = await axios.get("http://localhost:8000/messages");
    messages.value = response.data;
  } catch (error) {
    console.error("Failed to fetch messages:", error);
  } finally {
  }
};

// Connect to WebSocket
const connectWebSocket = () => {
  isLoggedIn.value = true;
  fetchMessages();
  if (!username.value) {
    alert("Please enter a username first!");
    return;
  }

  ws = new WebSocket(`ws://localhost:8000/ws/${username.value}`);

  ws.onopen = () => console.log("Connected to WebSocket");

  ws.onmessage = (event) => {
    const newMessage = JSON.parse(event.data);
    messages.value.push(newMessage);
    scrollToBottom();
  };

  ws.onclose = () => console.log("WebSocket disconnected");
};

// Send message via WebSocket
const sendMessage = () => {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    alert("WebSocket is not connected!");
    return;
  }

  if (!message.value || !receiver.value) {
    alert("Enter a message and receiver!");
    return;
  }

  const msg = {
    sender: username.value,
    receiver: receiver.value,
    message: message.value,
  };

  ws.send(JSON.stringify(msg));
  messages.value.push(msg);
  message.value = "";
  scrollToBottom();
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  });
};
const messageRefs = ref([]);
watch(messages, scrollToBottom);
const isScrolled = ref(false); // Flag to track if the user has scrolled
const scrollTimeout = ref(null); // To store the timeout reference

// Detect scroll position and update the flag
const handleScroll = () => {
  isScrolled.value = true; // Set the flag to true as soon as the user starts scrolling

  // Clear any existing timeout when the user scrolls
  if (scrollTimeout.value) {
    clearTimeout(scrollTimeout.value);
  }

  // Set a timeout to hide the overlay after 2 seconds of no scrolling
  scrollTimeout.value = setTimeout(() => {
    isScrolled.value = false;
  }, 2000); // 2000 ms = 2 seconds
};

// Attach the scroll event listener on mount
onMounted(() => {
  if (chatContainer.value) {
    chatContainer.value.addEventListener("scroll", handleScroll);
  }
});
const scrollToMessage = (index) => {
  nextTick(() => {
    if (messageRefs.value[index]) {
      messageRefs.value[index].scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    }
  });
};

onBeforeUnmount(() => {
  if (ws) ws.close();
  if (chatContainer.value) {
    chatContainer.value.removeEventListener("scroll", handleScroll);
  }
});
</script>
<template>
  <div class="h-svh flex flex-col">
    <!-- Navbar -->
    <div class="navbar bg-base-100">
      <div class="flex-1">
        <a class="btn btn-ghost text-xl">MeowChat</a>
      </div>
      <div class="flex items-center gap-2">
         <!-- Username Input -->
        <span>From:</span>
   
        <input
          class="input input-bordered"
          v-model="username"
          placeholder="Enter your username"
          autofocus
          @keyup.enter="connectWebSocket"
          :disabled="isLoggedIn"
        />
        
        
      </div>
    </div>
<div class="flex flex-row grow min-h-0">
  <ul class="menu menu-lg bg-base-200 rounded-box w-56">
    <li class="menu-title">Chats</li>
  <li><a @click="confirmReceiver">user2</a></li>
  <li><a>Item 2</a></li>
  <li><a>Item 3</a></li>
</ul>
   <!-- Main Content (Expands Fully) -->
    <div class="flex flex-col grow min-h-0 px-4 pb-4 gap-2">
     

      <!-- Chat Messages (Now Scrolls Properly) -->
      <div
        v-if="isLoggedIn && isReceiver"
        class="grow flex flex-col overflow-y-auto p-4 w-full"
        ref="chatContainer"
      >
        <span
          @click="scrollToMessage(4)"
          class="absolute top-35 left-1/2 indicator-item badge badge-primary z-1000"
          >new</span
        >

        <div
          v-for="(message, index) in messages"
          :key="message.timestamp"
          :class="[
            message.sender === username ? 'chat-end' : 'chat-start',
            'chat',
          ]"
          :ref="(el) => (messageRefs[index] = el)"
        >
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img
                alt="User avatar"
                src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
              />
            </div>
          </div>
          <div class="chat-header">
            {{ message.sender }}
            <time class="text-xs opacity-50">{{ message.timestamp }}</time>
          </div>
          <div class="chat-bubble">{{ message.message }}</div>
          <div
            v-if="message.sender === username"
            class="chat-footer opacity-50"
          >
            Delivered
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div
        v-if="isLoggedIn && isReceiver && messages.length > 0"
        class="flex gap-4"
      >
        <input
          class="input input-bordered"
          v-model="message"
          placeholder="Type a message"
          @keyup.enter="sendMessage"
        />
        <button class="btn btn-primary" @click="sendMessage">Send</button>
      </div>
    </div>
    <!-- Main Content END -->
</div>
   
  </div>
</template>
