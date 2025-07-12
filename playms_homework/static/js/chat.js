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
    console.log("load messages");
    console.log(chatMessages)
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
// Handle creating a new conversation
document.addEventListener('DOMContentLoaded', () => {
  // Add debugging to check if elements exist
  console.log('DOM loaded, checking elements...');

  const conversationList = document.getElementById('conversation-list');
  const chatMessages = document.getElementById('chat-messages');
  const messageForm = document.getElementById('message-form');
  const messageInput = document.getElementById('message-input');
  const sendButton = messageForm ? messageForm.querySelector('button') : null;
  const newConversationBtn = document.getElementById('new-conversation-btn');
  const createChatSettingForm = document.getElementById('setting-form');

  // Debug logging
  console.log('conversationList:', conversationList);
  console.log('chatMessages:', chatMessages);
  console.log('messageForm:', messageForm);
  console.log('messageInput:', messageInput);
  console.log('sendButton:', sendButton);
  console.log('newConversationBtn:', newConversationBtn);
  console.log('createChatSettingForm:', createChatSettingForm);

  // If chatMessages is still null, try waiting a bit longer
  if (!chatMessages) {
    console.error('chatMessages element not found! Retrying...');
    setTimeout(() => {
      const retryChateMessages = document.getElementById('chat-messages');
      console.log('Retry chatMessages:', retryChateMessages);
      if (retryChateMessages) {
        // Re-initialize with found element
        initializeChatApp(retryChateMessages, conversationList, messageForm, messageInput, sendButton, newConversationBtn, createChatSettingForm);
      }
    }, 100);
    return;
  }

  initializeChatApp(chatMessages, conversationList, messageForm, messageInput, sendButton, newConversationBtn, createChatSettingForm);
});

function initializeChatApp(chatMessages, conversationList, messageForm, messageInput, sendButton, newConversationBtn, createChatSettingForm) {
  const activeConversation = { id: null };
  const csrftoken = getCookie('csrftoken');

  if (messageForm) {
    messageForm.addEventListener('submit', (e) => handleMessageSubmit(e, messageInput, sendButton, activeConversation.id, csrftoken, chatMessages));
  }

  if (conversationList) {
    conversationList.addEventListener('click', async (e) => {
        if (e.target && e.target.matches('.list-group-item-action')) {
            e.preventDefault();
            const conversationId = e.target.dataset.conversationId;
            activeConversation.id = await loadMessages(conversationId, chatMessages, messageInput, sendButton);
        }
    });
  }

  if (newConversationBtn) {
    newConversationBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/conversations/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
            });
            if (!response.ok) {
                throw new Error('Failed to create conversation');
            }
            const newConversation = await response.json();
            await loadConversations(conversationList, chatMessages);
            activeConversation.id = await loadMessages(newConversation.id, chatMessages, messageInput, sendButton);
        } catch (error) {
            alert('Could not create a new conversation.');
        }
    });
  }

  // Add event listener for Save Settings button in modal
  const saveSettingsBtn = document.getElementById('save-settings-btn');
  if (saveSettingsBtn) {
    saveSettingsBtn.addEventListener('click', async () => {
      console.log("save settings button clicked");
      try {
        const response = await fetch('/api/chat-setting/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
              'reply_style': document.getElementById('ai-style').value,
              'tone': document.getElementById('ai-tone').value,
              'model': document.getElementById('ai-model').value,
              'pre_constructed_prompt':  document.getElementById('pre-construction').value,
              'api_key': document.getElementById('api-key').value,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to save chat settings');
        }
        const result = await response.json();
        alert('Settings saved successfully!');

        // Close the modal after successful save
        const settingsModal = bootstrap.Modal.getInstance(document.getElementById('settingsModal'));
        if (settingsModal) {
          settingsModal.hide();
        }
      } catch (error) {
        alert('Could not save settings: ' + error.message);
      }
    });
  }

  // Add event listener for Settings modal show event to load current settings
  const settingsModal = document.getElementById('settingsModal');
  if (settingsModal) {
    settingsModal.addEventListener('show.bs.modal', async () => {
      console.log("Settings modal opening, loading current settings...");
      try {
        const response = await fetch('/api/chat-setting/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
          }
        });

        if (response.ok) {
          const settings = await response.json();
          console.log("Loaded settings:", settings);

          // Fill the form with current settings
          if (settings.reply_style) {
            document.getElementById('ai-style').value = settings.reply_style;
          }
          if (settings.tone) {
            document.getElementById('ai-tone').value = settings.tone;
          }
          if (settings.model) {
            document.getElementById('ai-model').value = settings.model;
          }
          if (settings.pre_constructed_prompt) {
            document.getElementById('pre-construction').value = settings.pre_constructed_prompt;
          }
          if (settings.api_key) {
            document.getElementById('api-key').value = settings.api_key;
          }
        } else if (response.status === 404) {
          // User has no settings yet, keep default values
          console.log("No existing settings found, using defaults");
        } else {
          throw new Error('Failed to load settings');
        }
      } catch (error) {
        console.error('Could not load settings:', error.message);
        // Keep default values if loading fails
      }
    });
  }

  // Keep the original form submit handler as backup (if needed)
  if (createChatSettingForm) {
    createChatSettingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      // This will now be triggered by the Save Settings button click
    });
  }

  // Initial load
  if (conversationList && chatMessages) {
    loadConversations(conversationList, chatMessages);
  }
}
