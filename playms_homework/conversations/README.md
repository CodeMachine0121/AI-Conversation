# Conversations App

This app provides a conversation management system with AI responses. It follows a three-layer architecture to ensure separation of concerns and maintainability.

## Architecture

The app is structured according to a three-layer architecture:

1. **Presentation Layer**: Handles HTTP requests and responses
   - `presentation/views.py`: Contains API views for handling HTTP requests
   - `presentation/serializers.py`: Serializes and deserializes data for the API

2. **Business Logic Layer**: Contains the core business logic
   - `business_logic/services.py`: Provides services for conversation management

3. **Data Access Layer**: Handles data storage and retrieval
   - `data_access/repositories.py`: Provides repositories for database access
   - `data_access/ai_proxy.py`: Provides a proxy for AI service interaction

## Models

- `Conversation`: Represents a conversation session between a user and the AI
  - Fields: user, status, created_at, updated_at
  
- `Message`: Represents a message within a conversation
  - Fields: conversation, sender, content, timestamp

## API Endpoints

The app provides the following API endpoints:

- `GET /api/conversations/`: List all conversations for the current user
- `POST /api/conversations/`: Create a new conversation
- `GET /api/conversations/{id}/`: Retrieve a specific conversation
- `POST /api/conversations/{id}/close/`: Close a conversation
- `POST /api/conversations/{id}/reopen/`: Reopen a closed conversation
- `GET /api/conversations/{id}/messages/`: List all messages in a conversation
- `POST /api/conversations/{id}/send_message/`: Send a message to the AI and get a response

## Admin Interface

The app provides a Django Admin interface for managing conversations and messages. This allows business users to:

- View and filter conversations by user, status, and date
- View messages within conversations
- See message content and metadata

## Extensibility

The app is designed to be extensible:

1. **AI Service**: The `AIProxy` class can be extended to support different AI models or services
2. **Business Logic**: The service layer can be extended to support more complex business rules
3. **API**: New endpoints can be added to support additional features

## Usage

To use the app, make API requests to the provided endpoints. For example:

1. Create a new conversation:
   ```
   POST /api/conversations/
   ```

2. Send a message to the AI:
   ```
   POST /api/conversations/{id}/send_message/
   {
     "message": "Hello, AI!"
   }
   ```

3. Retrieve conversation messages:
   ```
   GET /api/conversations/{id}/messages/
   ```
