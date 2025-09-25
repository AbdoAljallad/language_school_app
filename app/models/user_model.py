"""
User Model
---------
Represents a user in the system and provides methods for user-related operations.
"""

from app.utils.database import execute_query, execute_transaction, get_connection
from app.utils.crypto import hash_password, verify_password
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_CHATS_FILE = _DATA_DIR / "chats.json"

def _ensure_data_dir():
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

def _load_chats_json() -> Dict[str, Any]:
    _ensure_data_dir()
    if not _CHATS_FILE.exists():
        return {"next_chat_id": 1, "next_message_id": 1, "chats": []}
    try:
        with _CHATS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"next_chat_id": 1, "next_message_id": 1, "chats": []}

def _save_chats_json(data: Dict[str, Any]) -> bool:
    _ensure_data_dir()
    try:
        with _CHATS_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def _next_chat_id(data: Dict[str, Any]) -> int:
    nid = data.get("next_chat_id", 1)
    data["next_chat_id"] = nid + 1
    return nid

def _next_message_id(data: Dict[str, Any]) -> int:
    nid = data.get("next_message_id", 1)
    data["next_message_id"] = nid + 1
    return nid

logger = logging.getLogger(__name__)

_CHAT_META_SUPPORTED = None

def _db_supports_chat_meta() -> bool:
    """
    Detect whether the DB chat_messages table contains edited/deleted columns.
    Cache the result in _CHAT_META_SUPPORTED.
    """
    global _CHAT_META_SUPPORTED
    if _CHAT_META_SUPPORTED is not None:
        return _CHAT_META_SUPPORTED
    try:
        # try a lightweight read that references one of the new columns
        # If the column is missing this will raise and we catch it.
        execute_query("SELECT edited FROM chat_messages LIMIT 1", fetch=True)
        _CHAT_META_SUPPORTED = True
    except Exception:
        _CHAT_META_SUPPORTED = False
    return _CHAT_META_SUPPORTED

class User:
    """
    User model representing a user in the system.
    Handles plaintext password storage as requested.
    """
    
    def __init__(self, user_id=None, username=None, email=None, full_name=None, 
                 user_type=None, language_level=None, profile_image=None, 
                 phone=None, address=None, is_active=True):
        """
        Initialize a User object.
        
        Args:
            user_id (int, optional): User ID. Defaults to None.
            username (str, optional): Username. Defaults to None.
            email (str, optional): Email address. Defaults to None.
            full_name (str, optional): Full name. Defaults to None.
            user_type (str, optional): User type (admin, teacher, student). Defaults to None.
            language_level (str, optional): Language proficiency level. Defaults to None.
            profile_image (str, optional): Profile image path. Defaults to None.
            phone (str, optional): Phone number. Defaults to None.
            address (str, optional): Address. Defaults to None.
            is_active (bool, optional): Whether the user is active. Defaults to True.
        """
        # Add id as alias for user_id for compatibility
        self.id = user_id
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.user_type = user_type
        self.language_level = language_level
        self.profile_image = profile_image
        self.phone = phone
        self.address = address
        self.is_active = is_active
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User object from a dictionary.
        
        Args:
            data (dict): Dictionary containing user data.
        
        Returns:
            User: A User object.
        """
        # Handle different ID field names
        user_id = data.get('user_id') or data.get('id')
        
        user = cls(
            user_id=user_id,  # This will set both id and user_id
            username=data.get('username'),
            email=data.get('email'),
            full_name=data.get('full_name'),
            user_type=data.get('user_type'),
            language_level=data.get('language_level'),
            profile_image=data.get('profile_image'),
            phone=data.get('phone'),
            address=data.get('address'),
            is_active=data.get('is_active')
        )
        
        # Ensure both first_name and last_name are set
        user.first_name = data.get('first_name', '')
        user.last_name = data.get('last_name', '')
        
        return user
    
    def to_dict(self):
        """
        Convert the User object to a dictionary.
        
        Returns:
            dict: Dictionary representation of the User object.
        """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'user_type': self.user_type,
            'language_level': self.language_level,
            'profile_image': self.profile_image,
            'phone': self.phone,
            'address': self.address,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_by_id(user_id):
        """
        Get a user by ID.
        
        Args:
            user_id (int): User ID.
        
        Returns:
            User: User object if found, None otherwise.
        """
        query = "SELECT * FROM users WHERE id = %s"  # Using 'id' instead of 'user_id'
        result = execute_query(query, (user_id,), fetch=True)
        
        if result and len(result) > 0:
            return User.from_dict(result[0])
        return None
    
    @staticmethod
    def get_by_username(username):
        """
        Get a user by username.
        
        Args:
            username (str): Username.
        
        Returns:
            User: User object if found, None otherwise.
        """
        query = "SELECT * FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=True)
        
        if result and len(result) > 0:
            return User.from_dict(result[0])
        return None
    
    @staticmethod
    def get_by_email(email):
        """
        Get a user by email.
        
        Args:
            email (str): Email address.
        
        Returns:
            User: User object if found, None otherwise.
        """
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,), fetch=True)
        
        if result and len(result) > 0:
            return User.from_dict(result[0])
        return None
    
    @staticmethod
    def get_all():
        """
        Get all users.
        
        Returns:
            list: List of User objects.
        """
        query = "SELECT * FROM users"
        result = execute_query(query, fetch=True)
        
        if result:
            return [User.from_dict(user_data) for user_data in result]
        return []
    
    @staticmethod
    def get_by_type(user_type):
        """
        Get users by type.
        
        Args:
            user_type (str): User type (admin, teacher, student).
        
        Returns:
            list: List of User objects.
        """
        query = "SELECT * FROM users WHERE user_type = %s"
        result = execute_query(query, (user_type,), fetch=True)
        
        if result:
            return [User.from_dict(user_data) for user_data in result]
        return []
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user."""
        try:
            # Check user credentials
            query = """
                SELECT id, username, first_name, last_name, email, user_type, active 
                FROM users 
                WHERE username = %s AND password = %s AND active = 1
            """
            result = execute_query(query, (username, password), fetch=True)
            
            if result and len(result) > 0:
                user_data = result[0]
                # Convert user_type to lowercase for consistent comparison
                user_data['user_type'] = user_data['user_type'].lower() if user_data['user_type'] else None
                return User.from_dict(user_data)
                
            return None
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    def save(self):
        """
        Save the user to the database.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if self.user_id:
            # Update existing user - split full_name into first_name and last_name
            first_name, last_name = self.full_name.split(' ', 1) if self.full_name and ' ' in self.full_name else (self.full_name, '')
            
            query = """
                UPDATE users 
                SET username = %s, email = %s, first_name = %s, last_name = %s, user_type = %s, 
                    language_level = %s, profile_image = %s, phone = %s, 
                    address = %s, active = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            params = (
                self.username, self.email, first_name, last_name, self.user_type,
                self.language_level, self.profile_image, self.phone,
                self.address, self.is_active, self.user_id
            )
            result = execute_query(query, params, commit=True)
            return result is not None and result > 0
        else:
            # Insert new user - split full_name into first_name and last_name
            first_name, last_name = self.full_name.split(' ', 1) if self.full_name and ' ' in self.full_name else (self.full_name, '')
            
            query = """
                INSERT INTO users 
                (username, email, first_name, last_name, user_type, language_level, 
                 profile_image, phone, address, active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.username, self.email, first_name, last_name, self.user_type,
                self.language_level, self.profile_image, self.phone,
                self.address, self.is_active
            )
            result = execute_query(query, params, commit=True)
            
            if result is not None and result > 0:
                # Get the last inserted ID
                query = "SELECT LAST_INSERT_ID() as id"
                id_result = execute_query(query, fetch=True)
                
                if id_result and len(id_result) > 0:
                    self.user_id = id_result[0].get('id')
                    return True
            return False
    
    @staticmethod
    def create(username, password, email, full_name, user_type):
        """Create a new user."""
        try:
            # Split full name into first and last name
            name_parts = full_name.split(maxsplit=1)
            if len(name_parts) < 2:
                return None
            
            first_name, last_name = name_parts[0], name_parts[1]
            
            db = get_connection()
            cursor = db.cursor(dictionary=True)
            
            query = """
                INSERT INTO users 
                (username, password, email, first_name, last_name, user_type, active)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
            """
            cursor.execute(query, (username, password, email, first_name, last_name, user_type))
            db.commit()
            
            # Get the created user
            user_id = cursor.lastrowid
            user = User.get_by_id(user_id)
            
            return user
            
        except Exception as e:
            logger.exception("Error creating user: %s", str(e))
            if 'db' in locals():
                db.rollback()
            return None
            
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    def update_password(self, new_password):
        """
        Update the user's password (plaintext).
        
        Args:
            new_password (str): New password.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if not self.user_id:
            return False
        
        # Update the password (stored as plaintext)
        query = "UPDATE users SET password = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        params = (new_password, self.user_id)
        result = execute_query(query, params, commit=True)
        
        return result is not None and result > 0
    
    def delete(self):
        """
        Delete the user.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if not self.user_id:
            return False
        
        query = "DELETE FROM users WHERE id = %s"
        result = execute_query(query, (self.user_id,), commit=True)
        
        return result is not None and result > 0
    
    def get_courses(self):
        """
        Get the courses the user is enrolled in or teaching.
        
        Returns:
            list: List of course dictionaries.
        """
        if not self.user_id:
            return []
        
        if self.user_type == 'student':
            # Get courses the student is enrolled in
            query = """
                SELECT c.* FROM courses c
                JOIN student_courses sc ON c.course_id = sc.course_id
                WHERE sc.student_id = %s
            """
        elif self.user_type == 'teacher':
            # Get courses the teacher is teaching
            query = "SELECT * FROM courses WHERE teacher_id = %s"
        else:
            # Admin can see all courses
            query = "SELECT * FROM courses"
        
        result = execute_query(query, (self.user_id,), fetch=True)
        
        return result if result else []
    
    def get_notifications(self, unread_only=False):
        """
        Get the user's notifications.
        
        Args:
            unread_only (bool, optional): Whether to get only unread notifications. Defaults to False.
        
        Returns:
            list: List of notification dictionaries.
        """
        if not self.user_id:
            return []
        
        if unread_only:
            query = """
                SELECT * FROM notifications 
                WHERE user_id = %s AND read_status = 0
                ORDER BY created_at DESC
            """
        else:
            query = """
                SELECT * FROM notifications 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
        
        result = execute_query(query, (self.user_id,), fetch=True)
        
        return result if result else []
    
    def mark_notification_as_read(self, notification_id):
        """
        Mark a notification as read.
        """
        if not self.user_id:
            return False
        query = """
            UPDATE notifications 
            SET read_status = 1, read_at = CURRENT_TIMESTAMP
            WHERE notification_id = %s AND user_id = %s
        """
        result = execute_query(query, (notification_id, self.user_id), commit=True)
        return result is not None and result > 0

    # ----------------------
    # Chat / Messaging helpers (DB-first, JSON fallback)
    # Controller code can call User.get_chats(user_id) etc.
    @staticmethod
    def get_chats(user_id: int) -> List[Dict[str, Any]]:
        """Return list of chats for user_id. Try DB first; on failure, use JSON store."""
        if not user_id:
            return []
        # Try DB
        try:
            # Use ANY_VALUE for non-aggregated user columns so query works with ONLY_FULL_GROUP_BY
            query = """
                SELECT
                    c.id AS chat_id,
                    CASE WHEN c.user1_id = %s THEN c.user2_id ELSE c.user1_id END AS other_user_id,
                    ANY_VALUE(u.username) AS other_username,
                    ANY_VALUE(u.first_name) AS first_name,
                    ANY_VALUE(u.last_name) AS last_name,
                    SUBSTRING_INDEX(GROUP_CONCAT(m.message ORDER BY m.sent_at DESC SEPARATOR '||__||'), '||__||', 1) AS last_message,
                    MAX(m.sent_at) AS last_at,
                    SUM(CASE WHEN m.read_status = 0 AND m.sender_id != %s THEN 1 ELSE 0 END) AS unread_count
                FROM chats c
                LEFT JOIN users u ON u.id = CASE WHEN c.user1_id = %s THEN c.user2_id ELSE c.user1_id END
                LEFT JOIN chat_messages m ON m.chat_id = c.id
                WHERE c.user1_id = %s OR c.user2_id = %s
                GROUP BY c.id
                ORDER BY last_at DESC
            """
            # parameters: user_id used in CASE, in SUM, in LEFT JOIN CASE, and twice in WHERE
            rows = execute_query(query, (user_id, user_id, user_id, user_id, user_id), fetch=True) or []
            return rows
        except Exception:
            # Fallback to JSON file
            data = _load_chats_json()
            chats_out = []
            for c in data.get("chats", []):
                if int(c.get("user1_id")) == int(user_id) or int(c.get("user2_id")) == int(user_id):
                    other_id = c["user2_id"] if int(c["user1_id"]) == int(user_id) else c["user1_id"]
                    last_msg = None
                    last_at = None
                    unread = 0
                    msgs = c.get("messages", [])
                    if msgs:
                        last = msgs[-1]
                        last_msg = last.get("message")
                        last_at = last.get("sent_at")
                        for m in msgs:
                            if m.get("sender_id") != user_id and user_id not in m.get("read_by", []):
                                unread += 1
                    # try to fetch user fields
                    try:
                        u = User.get_by_id(other_id)
                        other_username = u.username if u else None
                        first_name = getattr(u, "first_name", "")
                        last_name = getattr(u, "last_name", "")
                    except Exception:
                        other_username = None
                        first_name = ""
                        last_name = ""
                    chats_out.append({
                        "chat_id": c.get("id"),
                        "other_user_id": other_id,
                        "other_username": other_username,
                        "first_name": first_name,
                        "last_name": last_name,
                        "last_message": last_msg,
                        "last_at": last_at,
                        "unread_count": unread
                    })
            # sort by last_at (most recent first)
            chats_out.sort(key=lambda x: x.get("last_at") or "", reverse=True)
            return chats_out

    @staticmethod
    def get_or_create_chat(user1_id: int, user2_id: int) -> int:
        """Return existing chat id between two users or create it (DB or JSON fallback)."""
        if not user1_id or not user2_id:
            return None
        # DB attempt
        try:
            q = "SELECT id FROM chats WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s) LIMIT 1"
            r = execute_query(q, (user1_id, user2_id, user2_id, user1_id), fetch=True)
            if r and len(r) > 0:
                return r[0].get("id")
            insert_q = "INSERT INTO chats (user1_id, user2_id) VALUES (%s, %s)"
            execute_query(insert_q, (user1_id, user2_id), commit=True)
            last = execute_query("SELECT LAST_INSERT_ID() as id", fetch=True)
            return last[0].get("id") if last else None
        except Exception:
            # JSON fallback
            data = _load_chats_json()
            for c in data.get("chats", []):
                a = int(c.get("user1_id"))
                b = int(c.get("user2_id"))
                if (a == int(user1_id) and b == int(user2_id)) or (a == int(user2_id) and b == int(user1_id)):
                    return c.get("id")
            # create new chat
            cid = _next_chat_id(data)
            chat_obj = {"id": cid, "user1_id": int(user1_id), "user2_id": int(user2_id), "messages": []}
            data.setdefault("chats", []).append(chat_obj)
            _save_chats_json(data)
            return cid

    @staticmethod
    def get_messages(chat_id: int, limit: int = 200, after_id: int = None) -> List[Dict[str, Any]]:
        """Return list of messages for chat_id ordered asc. DB-first, JSON fallback."""
        if not chat_id:
            return []
        # Try DB first; select columns depending on DB support
        try:
            if _db_supports_chat_meta():
                if after_id:
                    q = ("SELECT id, chat_id, sender_id, message, edited, edited_at, deleted, deleted_at, "
                         "read_status, sent_at FROM chat_messages WHERE chat_id = %s AND id > %s ORDER BY sent_at ASC LIMIT %s")
                    params = (chat_id, after_id, limit)
                else:
                    q = ("SELECT id, chat_id, sender_id, message, edited, edited_at, deleted, deleted_at, "
                         "read_status, sent_at FROM chat_messages WHERE chat_id = %s ORDER BY sent_at ASC LIMIT %s")
                    params = (chat_id, limit)
            else:
                if after_id:
                    q = "SELECT id, chat_id, sender_id, message, read_status, sent_at FROM chat_messages WHERE chat_id = %s AND id > %s ORDER BY sent_at ASC LIMIT %s"
                    params = (chat_id, after_id, limit)
                else:
                    q = "SELECT id, chat_id, sender_id, message, read_status, sent_at FROM chat_messages WHERE chat_id = %s ORDER BY sent_at ASC LIMIT %s"
                    params = (chat_id, limit)
            rows = execute_query(q, params, fetch=True) or []
            return rows
        except Exception:
            # Fallback to JSON file if DB unavailable or query fails
            data = _load_chats_json()
            chat = next((c for c in data.get("chats", []) if int(c.get("id")) == int(chat_id)), None)
            if not chat:
                return []
            msgs = chat.get("messages", [])
            if after_id:
                msgs = [m for m in msgs if int(m.get("id", 0)) > int(after_id)]
            return msgs[-limit:] if limit else msgs

    @staticmethod
    def send_message(chat_id: int, sender_id: int, text: str) -> bool:
        """Insert a chat message (DB-first, JSON fallback)."""
        if not chat_id or not sender_id or not text:
            return False
        # try DB insert
        try:
            q = "INSERT INTO chat_messages (chat_id, sender_id, message, read_status) VALUES (%s, %s, %s, 0)"
            execute_query(q, (chat_id, sender_id, text), commit=True)
            try:
                execute_query("UPDATE chats SET updated_at = CURRENT_TIMESTAMP WHERE id = %s", (chat_id,), commit=True)
            except Exception:
                pass
            return True
        except Exception:
            data = _load_chats_json()
            chat = next((c for c in data.get("chats", []) if int(c.get("id")) == int(chat_id)), None)
            if not chat:
                return False
            mid = _next_message_id(data)
            sent_at = datetime.utcnow().isoformat()
            msg = {
                "id": mid,
                "sender_id": int(sender_id),
                "message": text,
                "sent_at": sent_at,
                "read_by": [int(sender_id)],
                "edited": False,
                "edited_at": None,
                "deleted": False,
                "deleted_at": None,
                "read_status": False
            }
            chat.setdefault("messages", []).append(msg)
            saved = _save_chats_json(data)
            return saved

    @staticmethod
    def edit_message(message_id: int, user_id: int, new_text: str) -> bool:
        """Allow the sender to edit their message. Returns True on success."""
        if not message_id or not user_id or new_text is None:
            return False
        # Try DB
        try:
            r = execute_query("SELECT sender_id FROM chat_messages WHERE id = %s", (message_id,), fetch=True)
            if not r:
                return False
            if int(r[0].get("sender_id")) != int(user_id):
                return False
            # Try rich update first, fallback to simple update if server lacks columns
            try:
                execute_query("UPDATE chat_messages SET message = %s, edited = 1, edited_at = CURRENT_TIMESTAMP WHERE id = %s",
                              (new_text, message_id), commit=True)
            except Exception as ex:
                # If edited column missing, fallback to updating only message
                if "Unknown column" in str(ex) or "edited" in str(ex).lower():
                    execute_query("UPDATE chat_messages SET message = %s WHERE id = %s", (new_text, message_id), commit=True)
                else:
                    raise
            return True
        except Exception:
            # JSON fallback
            data = _load_chats_json()
            changed = False
            for c in data.get("chats", []):
                for m in c.get("messages", []):
                    if int(m.get("id")) == int(message_id):
                        if int(m.get("sender_id")) != int(user_id):
                            return False
                        m["message"] = new_text
                        m["edited"] = True
                        m["edited_at"] = datetime.utcnow().isoformat()
                        changed = True
                        break
                if changed:
                    break
            if changed:
                return _save_chats_json(data)
            return False

    @staticmethod
    def delete_message(message_id: int, user_id: int) -> bool:
        """Allow the sender to mark their message as deleted. Returns True on success."""
        if not message_id or not user_id:
            return False
        # Try DB
        try:
            r = execute_query("SELECT sender_id FROM chat_messages WHERE id = %s", (message_id,), fetch=True)
            if not r:
                return False
            if int(r[0].get("sender_id")) != int(user_id):
                return False
            # Try rich delete first; if columns missing, fall back to blanking message only
            try:
                execute_query("UPDATE chat_messages SET deleted = 1, deleted_at = CURRENT_TIMESTAMP, message = '' WHERE id = %s",
                              (message_id,), commit=True)
            except Exception as ex:
                if "Unknown column" in str(ex) or "deleted" in str(ex).lower():
                    execute_query("UPDATE chat_messages SET message = '' WHERE id = %s", (message_id,), commit=True)
                else:
                    raise
            return True
        except Exception:
            # JSON fallback
            data = _load_chats_json()
            changed = False
            for c in data.get("chats", []):
                for m in c.get("messages", []):
                    if int(m.get("id")) == int(message_id):
                        if int(m.get("sender_id")) != int(user_id):
                            return False
                        m["deleted"] = True
                        m["deleted_at"] = datetime.utcnow().isoformat()
                        m["message"] = ""
                        changed = True
                        break
                if changed:
                    break
            if changed:
                return _save_chats_json(data)
            return False