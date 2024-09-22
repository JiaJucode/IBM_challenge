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

        # Search response table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Search (
                search_id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT,
                message INTEGER
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
    
    def add_search(self, term, msgid, commit=True):
        self.cursor.execute('''
            INSERT INTO Search (search_term, message)
            VALUES (?, ?);
        ''', (term, msgid))

        if commit:
            self.connection.commit()

    def get_searches(self, chat_id=None):
        if chat_id is not None:
            self.cursor.execute('''
                Select search_term, content as response from Search inner join Messages on 
                    message=message_id AND chat_id = ?
            ''', (chat_id,))
        else:
            self.cursor.execute('''
                Select search_term, content as response from Search inner join Messages on 
                    message=message_id
            ''')

        return self.cursor.fetchall()

if __name__ == "__main__":
    db = ChatsDatabase()
    cursor = db.cursor
    # print all tables
    # cursor.execute(" SELECT role, content FROM Messages Where chat_id = 1")
    for i in [1,2,5]:
        db.add_search(f"search {i}", i, False)
    # print(cursor.execute("select * from Search").fetchall())
    print(db.get_searches())
    # print(cursor.fetchall())