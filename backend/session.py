import sqlite3
import json

example_chat = [
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
            "questions",
            '''blablbalsdfl absldfblab sl fbalsfbflabs ldffblabs dflbas fhjkasdf kjj askdf hjk sahkjf gasdgf
            blablbals dflabsl dfblabslfbal sfbfl absldf fblabsd flbasfh jkasdf kjjas dfhjksah kjfgasdgf
            blablbals dflabsldf blab slfbalsf bflabsldffblab sdflb asf hjka sdfkjjaskdf hjksa hkjfgasdgf
            blablbalsdf labsldf blabslfbalsf bflabsldffblabsdflbasfhjkasdfkjjas kdfhj ksahkjfgasdgf
            blablbalsdflabsldfbl absl fbalsfbflabsldff blabsdflbasfhj kas dfkjjas kdfhjksah kjfgasdgf
            blablbal sdfl absldfblab slfbalsfbflabsl ff blabsdflb asfh jkasdfkjjaskdfhjk sahkjfgasdgf''',
    ]

class Session:
    def __init__(self) -> None:
        pass

class Database:
    # Base class for all databases
    def __init__(self, db_path="backend/data.db") -> None:
        self.name = db_path

    def start(self):
        self.connection = sqlite3.connect(self.name)

    def __call__(self, query):
        return self.connection.execute(query)

    def create_table(self):
        pass

    def save_exit(self):
        self.connection.commit()
        self.connection.close()

class SearchResponseDatabase(Database):
    def create_table(self):
        self("create table if not exists Search (search_term TEXT, frequency INTEGER, response TEXT)")

    def add_search(self, term, response=""):
        entry = self(f"select frequency, response from Search where search_term='{term}'").fetchone()
        if entry and entry[0]:
            # cache hit, increment frequency and return cached response
            self(f"update Search set frequency={int(entry[0])+1} where search_term='{term}'")
            return entry[1]
        else:
            # no matching history, create new one
            self(f"insert into Search (search_term, frequency, response) values ('{term}', 1, '{response}')")

# feel free to restructure the code
# TODO: user authentication
# TODO: redesign for fast adding and lazy loading
class ChatHistoryDatabase(Database):
    def start(self) -> None:
        self.next_chat_ID = 0
        self.next_user_ID = 0
        super().start()

    def create_table(self):
        self(
            '''create table if not exists UserChats (
                user_ID INTEGER,
                chat_ID INTEGER,
                chat_name TEXT,
                PRIMARY KEY (user_ID, chat_ID)
                )'''
        )
        # messages are stored as json strings
        self(
            '''create table if not exists ChatHistory (
                chat_ID INTEGER PRIMARY KEY,
                messages TEXT
                )'''
        )

    def get_next_chat_ID(self):
        self.next_chat_ID += 1
        return self.next_chat_ID
    
    def get_next_user_ID(self):
        self.next_user_ID += 1
        return self.next_user_ID

    def add_message(self, chat_ID, new_message):
        # get the chat history
        chat_history = self(f"select messages from ChatHistory where chat_ID={chat_ID}").fetchone()
        if not chat_history:
            raise KeyError("Chat ID does not exist")
        try:
            json_chat_history = json.loads(chat_history[0]) if len(chat_history[0]) > 0 else []
        except json.JSONDecodeError:
            print("history is corrupted")
            json_chat_history = []
        json_chat_history.append(new_message)
        chat_history_str = json.dumps(json_chat_history)
        self(f"UPDATE ChatHistory SET messages='{chat_history_str}' where chat_ID={chat_ID}")

    def add_chat(self, user_ID, chat_ID, chat_name=""):
        self(f"INSERT OR IGNORE INTO UserChats (user_ID, chat_ID, chat_name) VALUES ({user_ID}, {chat_ID}, '{chat_name}')")
        self(f"INSERT OR IGNORE INTO ChatHistory (chat_ID, messages) VALUES ({chat_ID}, '')")

    def get_chat_history(self, chat_ID):
        return self(f"select messages from ChatHistory where chat_ID={chat_ID}").fetchone()

    def get_user_chats(self, user_ID):
        return self(f"select chat_ID, chat_name from UserChats where user_ID={user_ID}").fetchall()

# try out database
if __name__ == "__main__":
    db = SearchResponseDatabase()
    db.start()
    db.create_table()
    for term, response in [("book flight ticket", "Etihad Airways"), ("find a shopping center", "Dubai Mall")]:
        db.add_search(term, response)
    print(1, db("select * from Search").fetchall())
    for term, response in [("book flight ticket", ""), ("how to solve numpy error", "stackoverflow website")]:
        db.add_search(term, response)
    print(2, db("select * from Search").fetchall())
    db.connection.close()

    db = ChatHistoryDatabase()
    db.start()
    db.create_table()
    db.add_chat(1, 1, "test chat")
    for message in example_chat:
        db.add_message(1, message)
    print(json.loads(db.get_chat_history(1)[0]))
    db.connection.close()


    