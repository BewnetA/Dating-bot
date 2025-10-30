import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from config import config
import os

class Database:
    def __init__(self):
        self.conn = self.get_connection()
        self.create_tables()
        self.create_payment_tables()
        self.migrate_tables()
    
    def get_connection(self):
        """Get PostgreSQL database connection"""
        try:
            # Get database URL from environment variable (for production)
            database_url = os.getenv('DATABASE_URL')
            
            if database_url:
                # For Heroku and other cloud providers
                conn = psycopg2.connect(database_url, sslmode='require')
            else:
                # For local development
                conn = psycopg2.connect(
                    host=config.DB_HOST,
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    port=config.DB_PORT
                )
            
            logging.info("✅ Connected to PostgreSQL database")
            return conn
        except Exception as e:
            logging.error(f"❌ Error connecting to database: {e}")
            raise
    
    def create_tables(self):
        """Create necessary tables for the bot"""
        cursor = self.conn.cursor()
        
        # Users table with all possible columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
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
                coins INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Likes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                liked_user_id BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (liked_user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                UNIQUE(user_id, liked_user_id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                from_user_id BIGINT,
                to_user_id BIGINT,
                message_text TEXT,
                message_type VARCHAR(20) DEFAULT 'text',
                media_file_id TEXT,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (to_user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        # Blocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                blocked_user_id BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (blocked_user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                UNIQUE(user_id, blocked_user_id)
            )
        ''')
        
        # Complaints table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                reported_user_id BIGINT,
                complaint_type TEXT,
                complaint_text TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (reported_user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
        cursor.close()
    
    def migrate_tables(self):
        """Add missing columns to existing tables"""
        cursor = self.conn.cursor()
        
        # Check and add missing columns to users table
        columns_to_check = [
            ('last_name', 'TEXT'),
            ('language', 'TEXT'),
            ('phone', 'TEXT'),
            ('age', 'INTEGER'),
            ('gender', 'TEXT'),
            ('religion', 'TEXT'),
            ('city', 'TEXT'),
            ('latitude', 'REAL'),
            ('longitude', 'REAL'),
            ('bio', 'TEXT'),
            ('photos', 'TEXT'),
            ('is_active', 'BOOLEAN'),
            ('coins', 'INTEGER')
        ]
        
        for column_name, column_type in columns_to_check:
            try:
                cursor.execute(f'''
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name='users' AND column_name='{column_name}'
                        ) THEN
                            ALTER TABLE users ADD COLUMN {column_name} {column_type};
                        END IF;
                    END $$;
                ''')
                logging.info(f"Checked/added column {column_name} to users table")
            except Exception as e:
                logging.warning(f"Could not add column {column_name}: {e}")
        
        self.conn.commit()
        cursor.close()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str = ""):
        """Add new user to database"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, last_name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            ''', (user_id, username, first_name, last_name))
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            self.conn.rollback()
        finally:
            cursor.close()
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data by user_id"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None
        finally:
            cursor.close()
    
    def get_users_for_matching(self, user_id: int, gender: str) -> List[Dict[str, Any]]:
        """Get potential matches for a user (opposite gender, not liked/blocked/swiped)"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Get opposite gender
        opposite_gender = "female" if gender.lower() == "male" else "male"
        
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                WHERE u.gender = %s 
                AND u.user_id != %s
                AND u.is_active = TRUE
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = %s
                )
                AND u.user_id NOT IN (
                    SELECT liked_user_id FROM likes WHERE user_id = %s
                )
                AND u.photos IS NOT NULL
                AND u.bio IS NOT NULL
                AND u.photos != '[]'
                AND u.bio != ''
            ''', (opposite_gender, user_id, user_id, user_id))
            
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting matches: {e}")
            return []
        finally:
            cursor.close()
    
    def add_like(self, user_id: int, liked_user_id: int) -> bool:
        """Add a like between users"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO likes (user_id, liked_user_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, liked_user_id) DO NOTHING
            ''', (user_id, liked_user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding like: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    def add_message(self, from_user_id: int, to_user_id: int, message_content: str, message_type: str = "text", media_file_id: str = None):
        """Add message to database with type and media file ID support"""
        cursor = self.conn.cursor()
        query = """
        INSERT INTO messages (from_user_id, to_user_id, message_text, message_type, media_file_id, created_at)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        try:
            cursor.execute(query, (from_user_id, to_user_id, message_content, message_type, media_file_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding message: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    def add_block(self, user_id: int, blocked_user_id: int) -> bool:
        """Block a user"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO blocks (user_id, blocked_user_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, blocked_user_id) DO NOTHING
            ''', (user_id, blocked_user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding block: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def get_user_likes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get users who liked the current user"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                INNER JOIN likes l ON u.user_id = l.user_id
                WHERE l.liked_user_id = %s
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = %s
                )
                AND u.is_active = TRUE
            ''', (user_id, user_id))
            
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting user likes: {e}")
            return []
        finally:
            cursor.close()

    def get_mutual_likes(self, user_id: int) -> List[Dict[str, Any]]:
        """Get mutual matches (users who liked each other)"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT u.* FROM users u
                WHERE u.user_id IN (
                    SELECT l1.user_id FROM likes l1
                    INNER JOIN likes l2 ON l1.user_id = l2.liked_user_id AND l1.liked_user_id = l2.user_id
                    WHERE l1.liked_user_id = %s
                )
                AND u.user_id NOT IN (
                    SELECT blocked_user_id FROM blocks WHERE user_id = %s
                )
                AND u.is_active = TRUE
            ''', (user_id, user_id))
            
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting mutual likes: {e}")
            return []
        finally:
            cursor.close()

    def add_complaint(self, user_id: int, complaint_type: str, complaint_text: str, reported_user_id: int = None) -> bool:
        """Add a user complaint to database"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO complaints (user_id, reported_user_id, complaint_type, complaint_text)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, reported_user_id, complaint_type, complaint_text))
            
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding complaint: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_user_account(self, user_id: int) -> bool:
        """Delete user account and all associated data"""
        cursor = self.conn.cursor()
        try:
            # PostgreSQL handles CASCADE deletion automatically due to foreign key constraints
            cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error deleting user account: {e}")
            return False
        finally:
            cursor.close()

    def update_user_language(self, user_id: int, language: str) -> bool:
        """Update user's preferred language"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE users SET language = %s WHERE user_id = %s
            ''', (language, user_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating language: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
        
    def get_user_likes_count(self, user_id: int) -> int:
        """Get count of how many people liked the user"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM likes 
                WHERE liked_user_id = %s
            ''', (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error getting user likes count: {e}")
            return 0
        finally:
            cursor.close()

    def get_user_matches_count(self, user_id: int) -> int:
        """Get count of user's mutual matches"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT COUNT(*) FROM (
                    SELECT l1.user_id FROM likes l1
                    INNER JOIN likes l2 ON l1.user_id = l2.liked_user_id AND l1.liked_user_id = l2.user_id
                    WHERE l1.liked_user_id = %s
                ) AS matches
            ''', (user_id,))
            return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error getting user matches count: {e}")
            return 0
        finally:
            cursor.close()

    def get_user_coins(self, user_id: int) -> int:
        """Get user's coin balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT coins FROM users WHERE user_id = %s', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logging.error(f"Error getting user coins: {e}")
            return 0
        finally:
            cursor.close()

    def add_user_coins(self, user_id: int, coins: int) -> bool:
        """Add coins to user's balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET coins = coins + %s 
                WHERE user_id = %s
            ''', (coins, user_id))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error adding user coins: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def deduct_user_coins(self, user_id: int, coins: int) -> bool:
        """Deduct coins from user's balance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET coins = coins - %s 
                WHERE user_id = %s AND coins >= %s
            ''', (coins, user_id, coins))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error deducting user coins: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def create_payment_tables(self):
        """Create payment-related tables"""
        cursor = self.conn.cursor()
        
        # Payments table for tracking payment requests
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                package_name TEXT,
                coins_amount INTEGER,
                price REAL,
                status TEXT DEFAULT 'pending', -- pending, approved, rejected
                screenshot_file_id TEXT,
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                processed_by BIGINT,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
        cursor.close()

    def add_payment_request(self, user_id: int, package_name: str, coins_amount: int, price: float, screenshot_file_id: str) -> int:
        """Add a new payment request"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO payments (user_id, package_name, coins_amount, price, screenshot_file_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (user_id, package_name, coins_amount, price, screenshot_file_id))
            
            payment_id = cursor.fetchone()[0]
            self.conn.commit()
            return payment_id
        except Exception as e:
            logging.error(f"Error adding payment request: {e}")
            self.conn.rollback()
            return -1
        finally:
            cursor.close()

    def get_payment_request(self, payment_id: int) -> Optional[Dict[str, Any]]:
        """Get payment request by ID"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT p.*, u.first_name, u.username 
                FROM payments p
                LEFT JOIN users u ON p.user_id = u.user_id
                WHERE p.id = %s
            ''', (payment_id,))
            
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error getting payment request: {e}")
            return None
        finally:
            cursor.close()

    def update_payment_status(self, payment_id: int, status: str, admin_id: int, notes: str = None) -> bool:
        """Update payment status (approve/reject)"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                UPDATE payments 
                SET status = %s, processed_at = CURRENT_TIMESTAMP, processed_by = %s, admin_notes = %s
                WHERE id = %s
            ''', (status, admin_id, notes, payment_id))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating payment status: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def get_pending_payments(self) -> List[Dict[str, Any]]:
        """Get all pending payment requests"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute('''
                SELECT p.*, u.first_name, u.username 
                FROM payments p
                LEFT JOIN users u ON p.user_id = u.user_id
                WHERE p.status = 'pending'
                ORDER BY p.created_at DESC
            ''')
            
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error getting pending payments: {e}")
            return []
        finally:
            cursor.close()
    
    def update_user_profile(self, user_id: int, **kwargs):
        """Update user profile with any provided fields"""
        if not kwargs:
            return False
            
        cursor = self.conn.cursor()
        try:
            # Build the SET clause dynamically based on provided kwargs
            set_parts = []
            values = []
            
            for key, value in kwargs.items():
                set_parts.append(f"{key} = %s")
                values.append(value)
            
            values.append(user_id)
            set_clause = ", ".join(set_parts)
            
            cursor.execute(f"""
                UPDATE users SET {set_clause} 
                WHERE user_id = %s
            """, values)
            self.conn.commit()
            logging.info(f"✅ Updated user {user_id} profile with: {kwargs}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Error updating user profile: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

db = Database()