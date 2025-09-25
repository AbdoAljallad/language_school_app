from typing import List, Dict, Any
from app.models.user_model import User

class Chat:
    """
    Chat model wrapper.
    Provides a single place to call chat-related functionality (delegates to User helpers).
    """
    @staticmethod
    def get_chats(user_id: int) -> List[Dict[str, Any]]:
        """Return list of chats for a user."""
        return User.get_chats(user_id)

    @staticmethod
    def get_or_create_chat(user1_id: int, user2_id: int) -> int:
        """Return existing chat id between two users or create it."""
        return User.get_or_create_chat(user1_id, user2_id)

    @staticmethod
    def get_messages(chat_id: int, limit: int = 200, after_id: int = None) -> List[Dict[str, Any]]:
        """Return messages for a chat."""
        return User.get_messages(chat_id, limit=limit, after_id=after_id)

    @staticmethod
    def send_message(chat_id: int, sender_id: int, text: str) -> bool:
        """Send a message in a chat."""
        return User.send_message(chat_id, sender_id, text)

    @staticmethod
    def edit_message(message_id: int, user_id: int, new_text: str) -> bool:
        """Edit a message (sender only)."""
        return User.edit_message(message_id, user_id, new_text)

    @staticmethod
    def delete_message(message_id: int, user_id: int) -> bool:
        """Delete (mark) a message (sender only)."""
        return User.delete_message(message_id, user_id)

    @staticmethod
    def mark_messages_read(chat_id: int, user_id: int) -> bool:
        """Mark messages read for a user."""
        return User.mark_messages_read(chat_id, user_id)
