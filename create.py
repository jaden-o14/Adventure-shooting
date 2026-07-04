import sqlite3

#database function is being created
def createDB():
    try:
        dbfile = "user.db"
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()

        sql =  """CREATE TABLE IF NOT EXISTS userList \
        (uID INTEGER PRIMARY KEY AUTOINCREMENT, \
        Username TEXT NOT NULL, \
        Password TEXT NOT NULL)"""

        # Leaderboard table
        sql_leaderboard = """CREATE TABLE IF NOT EXISTS leaderboard (
                          lID INTEGER PRIMARY KEY AUTOINCREMENT,
                          uID INTEGER NOT NULL,
                          Score INTEGER DEFAULT 0,
                          FOREIGN KEY (uID) REFERENCES userList (uID))"""

        


        conn.execute(sql)
        conn.execute(sql_leaderboard)
        conn.commit()
        print("successfully created a new database")
        
    except sqlite3.DatabaseError as e:
        print("there was an error: " + str(e))
        conn.rollback()

    finally:
        conn.close()

createDB()
