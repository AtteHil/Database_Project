# Here is the interface for using the database
import sqlite3
db = sqlite3.connect('game_database.sqlite')
cur = db.cursor()


def initializeDB():
    try:
        f = open("create_database.sql", "r")
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
        print("\nMenu options: (1-5 are queries)")
        print("1: ")
        print("2: See all rooms player have cleared.")
        print("3: ")
        print("4: ")
        print("5: ")
        print("6: Search players stats with name.")
        print("7: Insert, update or delete items")
        print("0: Quit")
        userInput = input("What do you want to do? ")

        if userInput == "1":
            pass
        elif userInput == "2":
            clearedRooms()
        elif userInput == "3":
            pass
        elif userInput == "4":
            pass
        elif userInput == "5":
            pass
        elif userInput == "6":
            searchPlayerStats()
        elif userInput == "7":
            modifyData()
        elif userInput == "0":
            print("Ending software...")
        else:
            print("Didn't quite get that.\nGive your choice again.")
    db.close()
    return


def searchPlayerStats():
    player_name = input("Give player name: ")
    cur.execute("SELECT * FROM Players WHERE Name=?;", [player_name])
    result = cur.fetchone()
    if result == None:
        print("No such player.")
        return
    for i in result:
        print(i)
    return


def clearedRooms():
    cur.execute(
        "SELECT Players.Name, GROUP_CONCAT(Rooms.Name,',') FROM Players JOIN Rooms ON Players.Level<Rooms.Level GROUP BY Players.Name;")
    result = cur.fetchall()

    for i in result:
        print(i, "\n")
    return


def modifyData():
    print("Here you can insert, update or delete players.")
    choice = input(''''What you want to do?
        1) Insert new player
        2) Update existing player
        3) Delete existing player
        your choice: ''')
    if choice == "1":
        player_name = input("Player name: ")
        cur.execute("SELECT COUNT(*) FROM Players;")
        count = cur.fetchone()
        try:
            cur.execute("INSERT INTO Players(PlayerId,Name) VALUES (?,?);",
                        (count[0]+1, player_name))
        except:
            print("Your name needs to be atleast 3 characters long.")


main()
