
// Utility to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Fetch all conversations for the user
async function loadConversations(conversationList, chatMessages) {
  try {
    const response = await fetch('/api/conversations/');
    if (!response.ok) throw new Error('Failed to fetch conversations');
    const conversations = await response.json();

    // Clear existing list but keep the header and button
    const header = conversationList.querySelector('.d-flex');
    conversationList.innerHTML = '';
    if(header) {
      conversationList.appendChild(header);
    }


    conversations.forEach(conv => {
      const convElement = document.createElement('a');
      convElement.href = '#';
      convElement.className = 'list-group-item list-group-item-action';
      convElement.dataset.conversationId = conv.id;
      convElement.textContent = `Conversation ${conv.id} (${new Date(conv.created_at).toLocaleString()})`;
      conversationList.appendChild(convElement);
    });
  } catch (error) {
    chatMessages.innerHTML = '<p class="text-danger text-center">Could not load conversations.</p>';
  }
}

// Fetch messages for a given conversation
async function loadMessages(conversationId, chatMessages, messageInput, sendButton) {
  chatMessages.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

  // Highlight active conversation
  document.querySelectorAll('#conversation-list .list-group-item-action').forEach(el => {
      el.classList.remove('active');
  });
  const activeConversationElement = document.querySelector(`[data-conversation-id="${conversationId}"]`);
  if (activeConversationElement) {
    activeConversationElement.classList.add('active');
  }


  try {
    const response = await fetch(`/api/conversations/${conversationId}/messages/`);
    if (!response.ok) throw new Error('Failed to fetch messages');
    const messages = await response.json();

    chatMessages.innerHTML = '';
    if (messages.length === 0) {
        chatMessages.innerHTML = '<p class="text-center text-muted">No messages yet. Send one to start!</p>';
    } else {
      messages.forEach(message => addMessageToChat(message, chatMessages));
    }

    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
  } catch (error) {
    chatMessages.innerHTML = '<p class="text-danger text-center">Could not load messages.</p>';
  }
  return conversationId;
}

// Add a single message to the chat window
function addMessageToChat(message, chatMessages) {
  if (chatMessages.querySelector('.text-center')) {
      chatMessages.innerHTML = ''; // Clear placeholder text
  }
  const messageWrapper = document.createElement('div');
  messageWrapper.className = `message ${message.sender}-message`;

  const messageDiv = document.createElement('div');
  messageDiv.className = 'content';
  messageDiv.textContent = message.content;

  messageWrapper.appendChild(messageDiv);
  chatMessages.appendChild(messageWrapper);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle new message submission
async function handleMessageSubmit(e, messageInput, sendButton, activeConversationId, csrftoken, chatMessages) {
  e.preventDefault();
  const messageText = messageInput.value.trim();
  if (!messageText || !activeConversationId) return;

  messageInput.value = '';
  messageInput.disabled = true;
  sendButton.disabled = true;

  // Display user message immediately
  addMessageToChat({ sender: 'user', content: messageText }, chatMessages);

  try {
    const response = await fetch(`/api/conversations/${activeConversationId}/send_message/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ message: messageText }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to send message');
    }

    const aiMessage = await response.json();
    addMessageToChat(aiMessage, chatMessages);

  } catch (error) {
    addMessageToChat({ sender: 'ai', content: `Error: ${error.message}` }, chatMessages);
  } finally {
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
  }
}

// Handle clicking on a conversation
async function handleConversationClick(e, chatMessages, messageInput, sendButton, activeConversation) {
  if (e.target && e.target.matches('.list-group-item-action')) {
    e.preventDefault();
    const conversationId = e.target.dataset.conversationId;
    activeConversation.id = await loadMessages(conversationId, chatMessages, messageInput, sendButton);
  }
}

// Handle creating a new conversation
async function handleNewConversation(csrftoken, conversationList, chatMessages, messageInput, sendButton, activeConversation) {
  try {
      const response = await fetch('/api/conversations/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
          },
      });
      if (!response.ok) throw new Error('Failed to create conversation');
      const newConversation = await response.json();
      await loadConversations(conversationList, chatMessages); // Refresh list
      activeConversation.id = await loadMessages(newConversation.id, chatMessages, messageInput, sendButton); // Load the new empty conversation
  } catch (error) {
      alert('Could not create a new conversation.');
  }
}


document.addEventListener('DOMContentLoaded', () => {
  const conversationList = document.getElementById('conversation-list');
  const chatMessages = document.getElementById('chat-messages');
  const messageForm = document.getElementById('message-form');
  const messageInput = document.getElementById('message-input');
  const sendButton = messageForm.querySelector('button');
  const newConversationBtn = document.getElementById('new-conversation-btn');
  const createChatSettingForm = document.getElementById('setting-form');

  const activeConversation = { id: null };
  const csrftoken = getCookie('csrftoken');

  messageForm.addEventListener('submit', (e) => handleMessageSubmit(e, messageInput, sendButton, activeConversation.id, csrftoken, chatMessages));
  conversationList.addEventListener('click', (e) => handleConversationClick(e, chatMessages, messageInput, sendButton, activeConversation));
  newConversationBtn.addEventListener('click', () => handleNewConversation(csrftoken, conversationList, chatMessages, messageInput, sendButton, activeConversation));

  createChatSettingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("submit settings form");
    try {
      const response = await fetch('/api/chat-setting/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
          'reply_style': "test-reply-style",
          'tone': "test-tone",
          'model': "gpt-3.5-turbo",
          'pre_constructed_prompt': "test pre-constructed prompt",
          'created_at': "2023-10-01T00:00:00Z",
          'updated_at': "2023-10-01T00:00:00Z"
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create chat settings');
      }
      const newConversation = await response.json();
      await loadConversations(conversationList, chatMessages); // Refresh list
      activeConversation.id = await loadMessages(newConversation.id, chatMessages, messageInput, sendButton); // Load the new empty conversation
    } catch (error) {
      alert('Could not create a new conversation.');
    }

  })

  // Initial load
  loadConversations(conversationList, chatMessages);
});
