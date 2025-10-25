import sqlite3
import logging
from typing import List, Dict, Any, Optional
from config import config

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.DB_NAME, check_same_thread=False)
        self.create_tables()
        self.create_payment_tables()
        self.migrate_tables()
    
    def create_tables(self):
        """Create necessary tables for the bot"""
        cursor = self.conn.cursor()
        
        # Users table with all possible columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language TEXT DEFAULT 'english',
                phone TEXT,
                age INTEGER,
                gender TEXT,
                religion TEXT,
                city TEXT,
                latitude REAL,
                longitude REAL,
                bio TEXT,
                photos TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Likes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                liked_user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (liked_user_id) REFERENCES users (user_id),
                UNIQUE(user_id, liked_user_id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER,
                to_user_id INTEGER,
                message_text TEXT,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users (user_id),
                FOREIGN KEY (to_user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Blocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                blocked_user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (blocked_user_id) REFERENCES users (user_id),
                UNIQUE(user_id, blocked_user_id)
            )
        ''')
        
        # Complaints table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reported_user_id INTEGER,
                complaint_type TEXT,
                complaint_text TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (reported_user_id) REFERENCES users (user_id)
            )
        ''')
        
        self.conn.commit()
    
    def migrate_tables(self):
        """Add missing columns to existing tables"""
        cursor = self.conn.cursor()
        
        # Check if columns exist and add them if they don't
        columns_to_add = [
            ('last_name', 'TEXT'),
            ('language', 'TEXT DEFAULT "english"'),
            ('phone', 'TEXT'),
            ('age', 'INTEGER'),
            ('gender', 'TEXT'),
            ('religion', 'TEXT'),
            ('city', 'TEXT'),
            ('latitude', 'REAL'),
            ('longitude', 'REAL'),
            ('bio', 'TEXT'),
            ('photos', 'TEXT'),
            ('is_active', 'BOOLEAN DEFAULT TRUE'),
            ('coins', 'INTEGER DEFAULT 0')  # Add coins to users table
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_type}')
                logging.info(f"Added column {column_name} to users table")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e):
                    logging.warning(f"Could not add column {column_name}: {e}")
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str = ""):
        """Add new user to database"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            # If there's still an issue with columns, try without last_name
            if "no column named last_name" in str(e):
                cursor.execute('''
                    INSERT OR IGNORE INTO users (user_id, username, first_name)
                    VALUES (?, ?, ?)
                ''', (user_id, username, first_name))
                self.conn.commit()
            else:
                raise e
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data by user_id"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if row:
            return dict(zip(columns, row))
        return None
    
    def get_users_for_matching(self, user_id: int, gender: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get potential matches for a user (opposite gender, not liked/blocked)"""
        cursor = self.conn.cursor()
        
        # Get opposite gender
        opposite_gender = "female" if gender.lower() == "male" else "male"
        
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                WHERE u.gender = ? 
                AND u.user_id != ?
                AND u.is_active = TRUE
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = ?
                )
                AND u.photos IS NOT NULL
                AND u.bio IS NOT NULL
                LIMIT ?
            ''', (opposite_gender, user_id, user_id, limit))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logging.error(f"Error getting matches: {e}")
            return []
    
    def add_like(self, user_id: int, liked_user_id: int) -> bool:
        """Add a like between users"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO likes (user_id, liked_user_id)
                VALUES (?, ?)
            ''', (user_id, liked_user_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            logging.error(f"Error adding like: {e}")
            return False
    
    def add_message(self, from_user_id: int, to_user_id: int, message_text: str) -> bool:
        """Add a message between users"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO messages (from_user_id, to_user_id, message_text)
                VALUES (?, ?, ?)
            ''', (from_user_id, to_user_id, message_text))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding message: {e}")
            return False
    
    def add_block(self, user_id: int, blocked_user_id: int) -> bool:
        """Block a user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO blocks (user_id, blocked_user_id)
                VALUES (?, ?)
            ''', (user_id, blocked_user_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            logging.error(f"Error adding block: {e}")
            return False

    def get_user_likes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get users who liked the current user"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                INNER JOIN likes l ON u.user_id = l.user_id
                WHERE l.liked_user_id = ?
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = ?
                )
                AND u.is_active = TRUE
            ''', (user_id, user_id))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logging.error(f"Error getting user likes: {e}")
            return []

    def get_mutual_likes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get mutual matches (users who liked each other)"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                WHERE u.user_id IN (
                    SELECT l1.user_id FROM likes l1
                    INNER JOIN likes l2 ON l1.user_id = l2.liked_user_id AND l1.liked_user_id = l2.user_id
                    WHERE l1.liked_user_id = ?
                )
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = ?
                )
                AND u.is_active = TRUE
            ''', (user_id, user_id))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logging.error(f"Error getting mutual likes: {e}")
            return []

    def add_complaint(self, user_id: int, complaint_type: str, complaint_text: str, reported_user_id: int = None) -> bool:
        """Add a user complaint to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO complaints (user_id, reported_user_id, complaint_type, complaint_text)
                VALUES (?, ?, ?, ?)
            ''', (user_id, reported_user_id, complaint_type, complaint_text))
            
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding complaint: {e}")
            return False

    def delete_user_account(self, user_id: int) -> bool:
        """Delete user account and all associated data"""
        try:
            cursor = self.conn.cursor()
            
            # Start transaction
            cursor.execute('BEGIN TRANSACTION')
            
            # Delete user data from all tables
            cursor.execute('DELETE FROM likes WHERE user_id = ? OR liked_user_id = ?', (user_id, user_id))
            cursor.execute('DELETE FROM messages WHERE from_user_id = ? OR to_user_id = ?', (user_id, user_id))
            cursor.execute('DELETE FROM blocks WHERE user_id = ? OR blocked_user_id = ?', (user_id, user_id))
            cursor.execute('DELETE FROM complaints WHERE user_id = ? OR reported_user_id = ?', (user_id, user_id))
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error deleting user account: {e}")
            return False

    def update_user_language(self, user_id: int, language: str) -> bool:
        """Update user's preferred language"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE users SET language = ? WHERE user_id = ?
            ''', (language, user_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating language: {e}")
            return False
        
    # Add these methods to your Database class in database.py

    def get_user_likes_count(self, user_id: int) -> int:
        """Get count of how many people liked the user"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM likes 
                WHERE liked_user_id = ?
            ''', (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error getting user likes count: {e}")
            return 0

    def get_user_matches_count(self, user_id: int) -> int:
        """Get count of user's mutual matches"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM (
                    SELECT l1.user_id FROM likes l1
                    INNER JOIN likes l2 ON l1.user_id = l2.liked_user_id AND l1.liked_user_id = l2.user_id
                    WHERE l1.liked_user_id = ?
                )
            ''', (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error getting user matches count: {e}")
            return 0

    def get_user_coins(self, user_id: int) -> int:
        """Get user's coin balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.error(f"Error getting user coins: {e}")
            return 0

    def add_user_coins(self, user_id: int, coins: int) -> bool:
        """Add coins to user's balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET coins = coins + ? 
                WHERE user_id = ?
            ''', (coins, user_id))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding user coins: {e}")
            return False

    def deduct_user_coins(self, user_id: int, coins: int) -> bool:
        """Deduct coins from user's balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET coins = coins - ? 
                WHERE user_id = ? AND coins >= ?
            ''', (coins, user_id, coins))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deducting user coins: {e}")
            return False

    def set_user_coins(self, user_id: int, coins: int) -> bool:
        """Set user's coin balance to specific amount"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO user_coins (user_id, coins) 
                VALUES (?, ?)
                ON CONFLICT(user_id) 
                DO UPDATE SET coins = ?, updated_at = CURRENT_TIMESTAMP
            ''', (user_id, coins, coins))
            
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error setting user coins: {e}")
            return False

    def create_payment_tables(self):
        """Create payment-related tables"""
        cursor = self.conn.cursor()
        
        # Payments table for tracking payment requests
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                package_name TEXT,
                coins_amount INTEGER,
                price REAL,
                status TEXT DEFAULT 'pending', -- pending, approved, rejected
                screenshot_file_id TEXT,
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                processed_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        self.conn.commit()

    def add_payment_request(self, user_id: int, package_name: str, coins_amount: int, price: float, screenshot_file_id: str) -> int:
        """Add a new payment request"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO payments (user_id, package_name, coins_amount, price, screenshot_file_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, package_name, coins_amount, price, screenshot_file_id))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"Error adding payment request: {e}")
            return -1

    def get_payment_request(self, payment_id: int) -> Optional[Dict[str, Any]]:
        """Get payment request by ID"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT p.*, u.first_name, u.username 
                FROM payments p
                LEFT JOIN users u ON p.user_id = u.user_id
                WHERE p.id = ?
            ''', (payment_id,))
            
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            
            if row:
                return dict(zip(columns, row))
            return None
        except Exception as e:
            logging.error(f"Error getting payment request: {e}")
            return None

    def update_payment_status(self, payment_id: int, status: str, admin_id: int, notes: str = None) -> bool:
        """Update payment status (approve/reject)"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE payments 
                SET status = ?, processed_at = CURRENT_TIMESTAMP, processed_by = ?, admin_notes = ?
                WHERE id = ?
            ''', (status, admin_id, notes, payment_id))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating payment status: {e}")
            return False

    def get_pending_payments(self) -> List[Dict[str, Any]]:
        """Get all pending payment requests"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT p.*, u.first_name, u.username 
                FROM payments p
                LEFT JOIN users u ON p.user_id = u.user_id
                WHERE p.status = 'pending'
                ORDER BY p.created_at DESC
            ''')
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Error getting pending payments: {e}")
            return []
    
    def update_user_profile(self, user_id: int, **kwargs):
        """Update user profile with any provided fields"""
        if not kwargs:
            return False
            
        try:
            # Build the SET clause dynamically based on provided kwargs
            set_parts = []
            values = []
            
            for key, value in kwargs.items():
                set_parts.append(f"{key} = ?")
                values.append(value)
            
            values.append(user_id)
            set_clause = ", ".join(set_parts)
            
            # Use the same pattern as other methods: create cursor from self.conn
            cursor = self.conn.cursor()
            cursor.execute(f"""
                UPDATE users SET {set_clause} 
                WHERE user_id = ?
            """, values)
            self.conn.commit()
            print(f"✅ Updated user {user_id} profile with: {kwargs}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating user profile: {e}")
            return False

db = Database()