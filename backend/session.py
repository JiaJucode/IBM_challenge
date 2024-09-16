import sqlite3

class Database:
    def __init__(self, db_path:str) -> None:
        self.name = db_path

    def start(self):
        self.connection = sqlite3.connect(self.name)

    def __call__(self, query):
        return self.connection.execute(query)

    def create_history_table(self):
        self("drop table if exists History")
        self("create table History (search_term TEXT, frequency INTEGER, response TEXT)")

    def add_history(self, term, response=""):
        entry = self(f"select frequency, response from History where search_term='{term}'").fetchone()
        if entry and entry[0]:
            # cache hit, increment frequency and return cached response
            self(f"update History set frequency={int(entry[0])+1} where search_term='{term}'")
            return entry[1]
        else:
            # no matching history, create new one
            self(f"insert into History (search_term, frequency, response) values ('{term}', 1, '{response}')")

    def save_exit(self):
        self.connection.commit()
        self.connection.close()

class Session:
    def __init__(self) -> None:
        pass

# try out database
if __name__ == "__main__":
    db = Database("backend/data.db")
    db.start()
    db.create_history_table()
    for term, response in [("book flight ticket", "Etihad Airways"), ("find a shopping center", "Dubai Mall")]:
        db.add_history(term, response)
    print(1, db("select * from History").fetchall())
    for term, response in [("book flight ticket", ""), ("how to solve numpy error", "stackoverflow website")]:
        db.add_history(term, response)
    print(2, db("select * from History").fetchall())
    db.connection.close()
    