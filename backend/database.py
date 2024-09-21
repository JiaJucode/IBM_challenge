import sqlite3
from utils.language_model import sentence_similarity    

class Database:
    _instance = None

    @classmethod
    def __dict_factory(cls, cursor, row):
        '''
        Converts sqlite3 row to dictionary
        '''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect('backend/database.db', check_same_thread=False)
            cls._instance.connection.row_factory = cls.__dict_factory
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance._create_tables()
        return cls._instance

    def __enter__(self):
        '''
        For context manager (with block)
        '''
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''
        For context manager (with block)
        '''
        self.close()

    def _create_tables(self):
        '''
        Create tables in the database
        '''
        raise NotImplementedError('Subclasses must implement this method')

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


class ChatsDatabase(Database):

    def _create_tables(self):

        # Chats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Chats (
                chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT
            );
        ''')

        # Messages table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                role TEXT CHECK(role IN ('system', 'user', 'assistant')),
                content TEXT,
                FOREIGN KEY (chat_id) REFERENCES Chats (id)
            );
        ''')

        self.connection.commit()

    def create_chat(self, uid, title: str, commit=True):
        self.cursor.execute('''
            INSERT INTO Chats (title)
            VALUES (?);
        ''', (title,))
        if commit:
            self.connection.commit()

        chat_id = self.cursor.lastrowid
        return chat_id

    def get_chat(self, chat_id):
        '''
        Get chat and all its messages by chat ID.
        '''

        # Get chat
        self.cursor.execute('''
            SELECT role, content 
            FROM Messages WHERE chat_id = ?;
        ''', (chat_id,))
        return self.cursor.fetchall()

    def get_chats(self, uid):
        '''
        Get all chats by user ID.
        Ignore user ID for now.
        '''
        self.cursor.execute('''
            SELECT chat_id, title
            FROM Chats''')
        return self.cursor.fetchall()

    def add_message(self, chat_id, role, content, commit=True):
        self.cursor.execute('''
            INSERT INTO Messages (chat_id, role, content)
            VALUES (?, ?, ?);
        ''', (chat_id, role, content))

        if commit:
            self.connection.commit()

        message_id = self.cursor.lastrowid
        return message_id

db = ChatsDatabase()
cursor = db.cursor
# print all tables
cursor.execute(" SELECT role, content FROM Messages Where chat_id = 1")
print(cursor.fetchall())