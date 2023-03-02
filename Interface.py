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
        print(userInput)
        if userInput == "1":

        elif userInput == "2":
            clearedRooms()

        elif userInput == "3":

        elif userInput == "4":

        elif userInput == "5":

        elif userInput == "6":
            searchPlayerStats()
        elif userInput == "0":
            print("Ending software...")
        else:
            print("Didn't quite get that.\nGive your choice again.")
    db.close()
    return


def searchPlayerStats():
    player_name = input("Give player name: ")
    cur.execute(f"SELECT * FROM Player WHERE Player_name='?';", (player_name,))
    result = cur.fetchone()
    for i in result:
        print(i, "\n")
    return


def clearedRooms():
    player_name = input("Give player name: ")
    cur.execute(
        "SELECT * FROM Rooms r INNER JOIN Player p ON r.level < p.level WHERE p.name='?';", (player_name,))
    result = cur.fetchall()
    for i in result:
        print(i, "\n")
    return


def modifyData():
    player_name = input("Give player name: ")
    choice = -1
    while (choice != 0):
        choice = input('''What you want to do?
            1) Insert new item
            2) Update old item to new
            3) Delete item''')
        if choice == 1:
            Weapon = input('''What weapon you want to use?
                1) Iron Sword
                2) Claw Dagger
                3) Spectral Armor
                your choice: ''')
