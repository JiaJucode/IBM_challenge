import sqlite3
from backend.utils.language_model import sentence_similarity

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
            cls._instance.connection = sqlite3.connect('backend/database.db')
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
         # Search response table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Search (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT,
                frequency Integer,
                summarized_response TEXT
            );
        ''')

        # Chats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                searches TEXT
            );
        ''')

        # Messages table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                role TEXT CHECK(role IN ('system', 'user', 'assistant')),
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES Chats (id)
            );
        ''')

        self.connection.commit()

    def create_chat(self, title: str, commit=True):
        self.cursor.execute('''
            INSERT INTO Chats (title)
            VALUES (?,);
        ''', (title,))
        if commit:
            self.connection.commit()

        chat_id = self.cursor.lastrowid
        return chat_id
    
    def update_chat(self, chat_id, summarized_search_results=None, commit=True):
        if summarized_search_results:
            # Modify search results and increment frequency
            self.cursor.execute('''
                Update Chats set frequency=frequency+1, summarized_search_results=? where id=? 
            ''', (summarized_search_results, chat_id))
        else:
            # Increment results only
            self.cursor.execute('''
                Update Chats set frequency=frequency+1 where id=? 
            ''', (chat_id))
        if commit:
            self.connection.commit()

    def get_chat(self, chat_id):
        '''
        Get chat and all its messages by chat ID.
        '''

        # Get chat
        self.cursor.execute('''
            SELECT * FROM Chats WHERE id = ?;
        ''', (chat_id,))
        chat = self.cursor.fetchone()

        if chat is None:
            return {'chat': None, 'messages': None}

        # Get messages
        self.cursor.execute('''
            SELECT role, content, timestamp
            FROM Messages WHERE chat_id = ?
            ORDER BY timestamp ASC;
        ''', (chat_id,))
        messages = self.cursor.fetchall()

        return {'chat': chat, 'messages': messages}

        
    def get_chats(self):
        '''
        Get high level info for all chats.
        Returns a list of chat informations
        '''
        self.cursor.execute('''
            SELECT * FROM Chats;
        ''')
        chats = self.cursor.fetchall()
        return chats
    
    def recent_chats(self, num):
        '''Get an overview of the latest n chats
        '''
        self.cursor.execute('''
            SELECT id, title FROM Chats order by id DESC limit ?;
        ''', (num,))
        chats = self.cursor.fetchall()
        return chats
    
    def similar_chats(self, title:str, similar_threshold=0.9):
        '''Find through all chat titles similar to input message
        '''
        chats = self.get_chats()
        similar_scores = sentence_similarity(title, [chat[1] for chat in chats])
        similar_chats = []
        for c in range(len(chats)):
            sim = similar_scores[c]
            if sim >= similar_threshold:
                similar_chats.append((chats[c], sim))
        similar_chats.sort(key=lambda entry: entry[1], reverse=True)
        return similar_chats
    
    def similar_search(self, term:str, similar_threshold=0.9):
        '''Find through all chat titles similar to input message
        '''
        pass

    def add_message(self, chat_id, role, content, commit=True):
        self.cursor.execute('''
            INSERT INTO Messages (chat_id, role, content)
            VALUES (?, ?, ?);
        ''', (chat_id, role, content))

        if commit:
            self.connection.commit()

        message_id = self.cursor.lastrowid

        return message_id

# Test database without persisting data
if __name__ == "__main__":

    print("Starting database tests...")

    # Without context manager
    # chat_db = ChatsDatabase()

    # chat_id = chat_db.create_chat(search_query="foo", summarized_search_results="foo bar baz", commit=False)
    # print("Created chat with ID:", chat_id)

    # chat = chat_db.get_chat(chat_id)
    # print("Fetched chat after creating 1 chat:", chat)

    # chat_db.add_message(chat_id, role="system", content="system message", commit=False)
    # chat_db.add_message(chat_id, role="user", content="user message 0", commit=False)
    # chat_db.add_message(chat_id, role="assistant", content="assistant message 0", commit=False)
    # chat_db.add_message(chat_id, role="user", content="user message 1", commit=False)
    # chat_db.add_message(chat_id, role="assistant", content="assistant message 1", commit=False)

    # messages = chat_db.get_chat_history(chat_id=chat_id)
    # print("Fetched messages:", messages)

    # chat_db.create_chat(search_query="bar", summarized_search_results="bar baz foo")
    # chat_db.create_chat(search_query="baz", summarized_search_results="baz foo bar")

    # chats = chat_db.get_chats()
    # print("Fetched chats after creating 3 chats:", chats)

    # chat_db.close()

    # using context manager
    with ChatsDatabase() as chat_db:
        chat_id = chat_db.create_chat(
            search_query="foo", summarized_search_results="foo bar baz")
        print("Created chat with ID:", chat_id)

        chat = chat_db.get_chat(chat_id)
        print("Fetched chat after creating 1 chat:", chat)

        chat_db.add_message(chat_id, role="system", content="system message")
        chat_db.add_message(chat_id, role="user", content="user message 0")
        chat_db.add_message(chat_id, role="assistant",
                            content="assistant message 0")
        chat_db.add_message(chat_id, role="user", content="user message 1")
        chat_db.add_message(chat_id, role="assistant",
                            content="assistant message 1")

        messages = chat_db.get_chat_history(chat_id=chat_id)
        print("Fetched messages:", messages)

        chat_db.create_chat(search_query="bar",
                            summarized_search_results="bar baz foo")
        chat_db.create_chat(search_query="baz",
                            summarized_search_results="baz foo bar")

        chats = chat_db.get_chats()
        print("Fetched chats after creating 3 chats:", chats)
