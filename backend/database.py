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
        # User credentials
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                credential TEXT
            );
        ''')

        # Search response table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Search (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user INTEGER,
                search_term TEXT,
                mode TEXT CHECK(mode IN ('Google maps', 'Google search')),
                frequency INTEGER,
                summarized_response TEXT,
                FOREIGN KEY (user) REFERENCES Users (id)
            );
        ''')

        # Chats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user Integer,
                title TEXT,
                search_list TEXT,
                FOREIGN KEY (user) REFERENCES Users (id)
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

    def create_chat(self, uid, title: str, commit=True):
        self.cursor.execute('''
            INSERT INTO Chats (user, title)
            VALUES (?,?);
        ''', (uid, title))
        if commit:
            self.connection.commit()

        chat_id = self.cursor.lastrowid
        return chat_id
    
    def _find_search_terms(self, search_ids):
        self.cursor.execute(f'''
            Select id, search_term, mode from Search where id in {tuple(search_ids)}
        ''')
        searches = self.cursor.fetchall()
        search_keys = ["id, search_term, mode"]
        return [{search_keys[i]: search[i] for i in range(len(search_keys))} for search in searches]

    def get_chat(self, chat_id):
        '''
        Get chat and all its messages by chat ID.
        '''

        # Get chat
        self.cursor.execute('''
            SELECT * FROM Chats WHERE id = ?;
        ''', (chat_id,))
        chat = self.cursor.fetchone()
        search_ids = chat[2]

        if chat is None:
            return {'chat': None, 'messages': None}
        else:
            keys = ["id", "title"]
            chat = {keys[i]: chat[i] for i in range(len(keys))}

        # Get messages
        self.cursor.execute('''
            SELECT role, content, timestamp
            FROM Messages WHERE chat_id = ?
            ORDER BY timestamp ASC;
        ''', (chat_id,))
        messages = self.cursor.fetchall()
        keys = ["role", "content", "timestamp"]
        messages = {keys[i]: messages[i] for i in range(len(keys))}
        searches = self._find_search_terms(search_ids)

        return {'chat': chat, 'messages': messages, "searches": searches}
    
    def chat_add_search(self, chat_id, new_search_ids:list, commit=True):
        self.cursor.execute('''
            SELECT search_list FROM Chats WHERE id = ?;
        ''', (chat_id,))
        searches:str = self.cursor.fetchone()[0]
        if not searches:
            searches = ""
        # 'search_list' entry of Chats stores a list of search ids in comma separated strings
        search_list = searches.split(",")
        new_searches = ""

        for i in new_search_ids:
            if i in search_list:
                # Move the same search id to the end of the list
                search_list.remove(i)
            search_list.append(i)
        
        for i in search_list:
            new_searches += f"{i},"
        new_searches = new_searches[:-1]

        self.cursor.execute('''
            Update Chats set search_list = ? where id = ?;
        ''', (chat_id, new_searches))

        if commit:
            self.connection.commit()
        return search_list
    
    def chat_user(self, chat_id):
         self.cursor.execute('''
            Select user from Chats where id = ?;
        ''', (chat_id, ))
         return self.cursor.fetchone()[0]

    def get_chats(self, uid, num=0) -> list[dict]:
        '''
        Get high level info for all chats or recent n chats.
        Returns a list of chat informations
        '''
        if not num:
            # Return all chats
            try:
                self.cursor.execute('''
                    SELECT * FROM Chats where user = ?;
                ''', (uid,))
            except:
                # chat not found 
                # TODO: maybe return some error message here
                return []
        else:
            try:
                # Return recent {num} chats
                self.cursor.execute('''
                    SELECT * FROM Chats where user = ? order by id DESC limit ?;
                ''', (uid, num))
            except:
                # chat not found 
                # TODO: maybe return some error message here
                return []
        entries = self.cursor.fetchall()
        chat_keys = ["id", "title"]
        chats = []
        for entry in entries:
            if entry[2]:
                search_ids = entry[2].split(",")
                chat = {chat_keys[i]: entry[i] for i in range(len(chat_keys))}
                chat["search_list"] = self._find_search_terms(search_ids)
        return chats
    
    def similar_chats(self, uid, title:str, similar_threshold=0.9):
        '''Find through all chat titles similar to input message
        '''
        chats = self.get_chats(uid)
        similar_scores = sentence_similarity(title, [chat["title"] for chat in chats])
        sim_chats = []
        for c in range(len(chats)):
            sim = similar_scores[c]
            if sim >= similar_threshold:
                chats[c]["similarity"] = sim
                sim_chats.append(chats[c])
        sim_chats.sort(key=lambda chat: chat["similarity"], reverse=True)
        return sim_chats
    
    def similar_searches(self, uid, term:str, mode:str, similar_threshold=0.9):
        '''Find through all search history with similar search terms, include respnse
        '''
        self.cursor.execute('''
            SELECT id, search_term, summarized_response FROM Search WHERE mode=? and user = ?;
        ''', (mode,uid))
        searches = self.cursor.fetchall()
        similar_scores = sentence_similarity(term, [search[1] for search in searches])
        sim_searches = []
        keys = ["id", "search_term", "summarized_response"]
        for c in range(len(searches)):
            sim = similar_scores[c]
            if sim >= similar_threshold:
                search = {keys[i]: searches[c][i] for i in range(len(keys))}
                search["similarity"] = sim
                sim_searches.append(search)
        sim_searches.sort(key=lambda search: search["similarity"], reverse=True)
        return sim_searches

    def add_message(self, chat_id, role, content, commit=True):
        self.cursor.execute('''
            INSERT INTO Messages (chat_id, role, content)
            VALUES (?, ?, ?);
        ''', (chat_id, role, content))

        if commit:
            self.connection.commit()

        message_id = self.cursor.lastrowid
        return message_id
    
    def add_search(self, uid="", term="", mode="", response="", id=None, commit=True):
        if id is None:
            # Add new search terms and response
            self.cursor.execute('''
                INSERT INTO Search (search_term, mode, summarized_response, frequency, user)
                VALUES (?, ?, ?, ?, ?);
            ''', (term, mode, response, 1, uid))
            
        else:
            if not response:
                # Use cached search and increment frequency
                self.cursor.execute('''
                    Update Search set frequency=frequency+1 where id=?
                ''', (id,))
            else:
                # Update cache with new response and increment frequency
                self.cursor.execute('''
                    Update Search set frequency=frequency+1, summarized_response=? where id=?
                ''', (response, id))

        if commit:
            self.connection.commit()
        return self.cursor.lastrowid
    
    def login_register(self, uid, name, pwd):
        if uid:
            self.cursor.execute('''
                Select * from Users where id = ?;
            ''', (uid,))
            user = self.cursor.fetchone()
            if user and user[2] == pwd:
                # user id exists and password correct, return user id
                return user[0]
            else:
                return ""
        else:
            # No user id provided, register new user and return id
            self.cursor.execute('''
                INSERT INTO Users (name, credential)
                VALUES (?, ?);
            ''', (name, pwd))
            return self.cursor.lastrowid
        
    def get_username(self, uid):
        self.cursor.execute('''
                Select name from Users where id = ?;
            ''', (uid,))
        return self.cursor.fetchone()[0]

            




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
