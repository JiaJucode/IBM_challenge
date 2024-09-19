import sqlite3


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

        # Chats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_query TEXT,
                summarized_search_results TEXT
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

    def create_chat(self, search_query, summarized_search_results, commit=True):

        self.cursor.execute('''
            INSERT INTO Chats (search_query, summarized_search_results)
            VALUES (?, ?);
        ''', (search_query, summarized_search_results))

        if commit:
            self.connection.commit()

        chat_id = self.cursor.lastrowid

        return chat_id

    def get_chat(self, chat_id):
        self.cursor.execute('''
            SELECT * FROM Chats WHERE id = ?;
        ''', (chat_id,))
        chat = self.cursor.fetchone()
        return chat

    def get_chats(self):
        self.cursor.execute('''
            SELECT * FROM Chats;
        ''')
        chats = self.cursor.fetchall()
        return chats

    def add_message(self, chat_id, role, content, commit=True):
        self.cursor.execute('''
            INSERT INTO Messages (chat_id, role, content)
            VALUES (?, ?, ?);
        ''', (chat_id, role, content))

        if commit:
            self.connection.commit()

        message_id = self.cursor.lastrowid

        return message_id

    def get_chat_messages(self, chat_id):
        self.cursor.execute('''
            SELECT * FROM Messages WHERE chat_id = ?
            ORDER BY timestamp ASC;
        ''', (chat_id,))
        messages = self.cursor.fetchall()

        return messages


class SearchResponseDatabase(Database):

    def _create_tables(self):

        # Search Responses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Search (
                search_term TEXT PRIMARY KEY,
                frequency INTEGER,
                response TEXT
            );
        ''')
        self.connection.commit()

    def add_search(self, term, response=""):
        entry = self.cursor.execute('''
            SELECT frequency, response FROM Search WHERE search_term = ?;
        ''', (term,)).fetchone()

        if entry and entry[0]:
            # cache hit, increment frequency and return cached response
            self.cursor.execute('''
                UPDATE Search SET frequency = frequency + 1 WHERE search_term = ?;
            ''', (term,))
            updated = True
        else:
            # no matching history, create new one
            self.cursor.execute('''
                INSERT INTO Search (search_term, frequency, response)
                VALUES (?, ?, ?);
            ''', (term, 1, response))
            updated = False

        self.connection.commit()

        return updated


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

    # messages = chat_db.get_chat_messages(chat_id=chat_id)
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

        messages = chat_db.get_chat_messages(chat_id=chat_id)
        print("Fetched messages:", messages)

        chat_db.create_chat(search_query="bar",
                            summarized_search_results="bar baz foo")
        chat_db.create_chat(search_query="baz",
                            summarized_search_results="baz foo bar")

        chats = chat_db.get_chats()
        print("Fetched chats after creating 3 chats:", chats)
