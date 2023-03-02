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
        print("5: tulosta lista")
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
            printTable("Inventory")
        elif userInput == "6":
            player_name = input("Give player name: ")
            searchPlayerStats(player_name)
        elif userInput == "7":
            modifyData()
            # db.commit()
        elif userInput == "0":
            print("Ending software...")
        else:
            print("Didn't quite get that.\nGive your choice again.")
    db.close()
    return


def searchPlayerStats(player_name):
    cur.execute("SELECT * FROM Players WHERE Name=?;", [player_name])
    result = cur.fetchone()
    if result == None:
        print("No such player.")
        return
    print(f'''Name {result[2]}
    is in room: {result[1]}
    Health: {result[3]}
    Damage: {result[4]}
    Experience points: {result[5]}
    Level: {result[6]}''')
    return


def clearedRooms():
    cur.execute(
        "SELECT Players.Name, GROUP_CONCAT(Rooms.Name,',') FROM Players JOIN Rooms ON Players.Level>Rooms.Level GROUP BY Players.Name;")
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
            cur.execute(
                "INSERT INTO Inventory(PlayerId) VALUES (?);", (count[0]+1,))
            print("New player created.")
            return
        except:
            print("Your name needs to be between 3 and 30 caharacters.")

    elif choice == "2":
        player_name = input("Player name: ")
        print("Current stats are")
        searchPlayerStats(player_name)
        data = input(
            "Give new stats in form (Name, Health, Damage, Level): ")

        try:
            insert_data = data.split(", ")
            cur.execute("UPDATE Players SET Name=?, Health=?, Damage=?, Level=? WHERE Name=?;",
                        (insert_data[0], insert_data[1], insert_data[2], insert_data[3], player_name))

            print("Update done!")
            return
        except:
            print("Something went wrong")

    elif choice == "3":
        player_name = input("Give player name you want to delete: ")
        try:
            cur.execute("DELETE FROM Inventory WHERE playerId = (SELECT PlayerId from Players WHERE Name = ?);", [
                        player_name])
            cur.execute("DELETE FROM Players WHERE Name=?", [player_name])
            print("Player succesfully deleted!")
            return
        except:
            print("Player was not found and therefore not deleted.")
    else:
        print("Try again.")


def printTable(table_name):
    cur.execute(f"SELECT * FROM {table_name};")
    result = cur.fetchall()
    for i in result:
        print(i)


main()
