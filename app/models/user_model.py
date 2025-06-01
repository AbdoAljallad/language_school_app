"""
User Model
---------
Represents a user in the system and provides methods for user-related operations.
"""

from app.utils.database import execute_query, execute_transaction
from app.utils.crypto import hash_password, verify_password

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
        # Handle database column name mapping
        user_id = data.get('user_id') or data.get('id')
        
        # Create full_name from first_name and last_name if needed
        full_name = data.get('full_name')
        if not full_name and data.get('first_name') and data.get('last_name'):
            full_name = f"{data.get('first_name')} {data.get('last_name')}"
            
        is_active = data.get('is_active')
        if is_active is None and data.get('active') is not None:
            is_active = data.get('active')
            
        user = cls(
            user_id=user_id,
            username=data.get('username'),
            email=data.get('email'),
            full_name=full_name,
            user_type=data.get('user_type'),
            language_level=data.get('language_level'),
            profile_image=data.get('profile_image'),
            phone=data.get('phone'),
            address=data.get('address'),
            is_active=is_active
        )
        
        # Add first_name and last_name as separate attributes
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
        """
        Authenticate a user with plaintext password.
        
        Args:
            username (str): Username.
            password (str): Password.
        
        Returns:
            User: User object if authentication succeeds, None otherwise.
        """
        # Enhanced debugging
        print(f"Attempting to authenticate user: {username} with plaintext password")
        
        # Step 1: First check if user exists regardless of password
        check_query = "SELECT * FROM users WHERE username = %s"
        user_exists = execute_query(check_query, (username,), fetch=True)
        
        if user_exists:
            print(f"User '{username}' exists in database.")
            print(f"Found user data: {user_exists[0]}")
            stored_password = user_exists[0].get('password')
            print(f"Stored password is: '{stored_password}'")
            print(f"Comparing with provided password using plaintext comparison")
        else:
            print(f"User '{username}' not found in database!")
            return None
        
        # Step 2: Try authentication
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        print(f"Executing query: {query} with params: {(username, password)}")
        result = execute_query(query, (username, password), fetch=True)
        
        # Step 3: Process results
        if result and len(result) > 0:
            user_data = result[0]
            print(f"Authentication successful for user: {username}")
            print(f"User data: {user_data}")
            
            # Update last login time - using id instead of user_id to match database schema
            update_query = "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            execute_query(update_query, (user_data.get('id'),), commit=True)
            
            return User.from_dict(user_data)
        else:
            print(f"Authentication failed for user: {username} - password mismatch")
            
            # Try direct string comparison for debugging
            if stored_password == password:
                print("NOTE: Direct string comparison matches, but SQL query failed!")
            else:
                print(f"Direct string comparison also fails: '{stored_password}' != '{password}'")
            
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
    def create(username, password, email, full_name, user_type, language_level=None, 
               profile_image=None, phone=None, address=None, is_active=True):
        """
        Create a new user with plaintext password.
        
        Args:
            username (str): Username.
            password (str): Password.
            email (str): Email address.
            full_name (str): Full name.
            user_type (str): User type (admin, teacher, student).
            language_level (str, optional): Language proficiency level. Defaults to None.
            profile_image (str, optional): Profile image path. Defaults to None.
            phone (str, optional): Phone number. Defaults to None.
            address (str, optional): Address. Defaults to None.
            is_active (bool, optional): Whether the user is active. Defaults to True.
        
        Returns:
            User: User object if creation succeeds, None otherwise.
        """
        # Check if username or email already exists
        if User.get_by_username(username) or User.get_by_email(email):
            return None
        
        # Split full_name into first_name and last_name
        first_name, last_name = full_name.split(' ', 1) if full_name and ' ' in full_name else (full_name, '')
        
        # Store password directly (plaintext)
        plaintext_password = password
        
        # Insert the new user
        query = """
            INSERT INTO users 
            (username, password, email, first_name, last_name, user_type, language_level, 
             profile_image, phone, address, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            username, plaintext_password, email, first_name, last_name, user_type, language_level,
            profile_image, phone, address, is_active
        )
        result = execute_query(query, params, commit=True)
        
        if result is not None and result > 0:
            # Get the last inserted ID
            query = "SELECT LAST_INSERT_ID() as id"
            id_result = execute_query(query, fetch=True)
            
            if id_result and len(id_result) > 0:
                user_id = id_result[0].get('id')
                return User.get_by_id(user_id)
        return None
    
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
        
        Args:
            notification_id (int): Notification ID.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
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