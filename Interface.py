# Here is the interface for using the database
import sqlite3
db = sqlite3.connect('DATABASENAME')
cur = db.cursor()


def initializeDB():
    try:
        f = open("sqlcommands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring += line
        cur.executescript(commandstring)
    except sqlite3.OperationalError:
        print("Database exists, skip initialization")
    except:
        print("No SQL file to be used for initialization")


def main():
    initializeDB()
    userInput = -1
    while (userInput != "0"):
        print("\nMenu options:")
        print("1: ")
        print("2: ")
        print("3: ")
        print("4: ")
        print("5: ")
        print("6: ")
        print("0: Quit")
        userInput = input("What do you want to do? ")
        print(userInput)
        if userInput == "1":
            searchPlayerStats()
        if userInput == "2":
            clearedRooms()
        if userInput == "3":

        if userInput == "4":

        if userInput == "5":

        if userInput == "6":

        if userInput == "0":
            print("Ending software...")
    db.close()
    return


def searchPlayerStats():
    player_name = input("Give player name: ")
    cur.execute(f"SELECT * FROM Player WHERE Player_name='{player_name}';")
    result = cur.fetchone()
    for i in result:
        print(i, "\n")
    return


def clearedRooms():
    player_name = input("Give player name: ")
    cur.execute(
        f"SELECT * FROM Rooms r INNER JOIN Player p ON r.level < p.level WHERE p.name='{player_name}';")
    result = cur.fetchall()
    for i in result:
        print(i, "\n")
    return
