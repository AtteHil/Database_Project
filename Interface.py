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
        print("1: See all rooms player have cleared.")
        print("2: Players with progress")
        print("3: Equipment on players")
        print("4: Enemies with nothing in hand")
        print("5: Enemies in each room")
        print("6: Search players stats with name.")
        print("7: Insert, update or delete items")
        print("0: Quit")
        userInput = input("What do you want to do? ")

        if userInput == "1":
            clearedRooms()
        elif userInput == "2":
            playersWithProgress()
        elif userInput == "3":
            equipmentLists()
        elif userInput == "4":
            enemiesWithNothing()
        elif userInput == "5":
            enemiesInRooms()
        elif userInput == "6":
            player_name = input("Give player name: ")
            searchPlayerStats(player_name)
        elif userInput == "7":
            modifyData()
            db.commit()
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
        return -1
    print(f'''Name {result[2]}
    is in room: {result[1]}
    Health: {result[3]}
    Damage: {result[4]}
    Experience points: {result[5]}
    Level: {result[6]}''')
    return 1


def clearedRooms():
    cur.execute(
        "SELECT Players.Name, GROUP_CONCAT(Rooms.Name,',') FROM Players JOIN Rooms ON Players.Level>Rooms.Level GROUP BY Players.Name;")
    result = cur.fetchall()
    for i in result:
        print(i)
    return


def equipmentLists():
    cur.execute(
        "SELECT Players.Name, Inventory.WeaponSlot, Inventory.Armorslot FROM Inventory INNER JOIN Players ON Inventory.PlayerId=Players.PlayerId;")
    result = cur.fetchall()
    print("Player name, Weapon, Armor")
    for i in result:
        print(i)
    return


def enemiesInRooms():
    cur.execute("SELECT Rooms.Name, GROUP_CONCAT(Enemies.Type, ',') FROM EnemiesInTheRooms INNER JOIN Rooms ON EnemiesInTheRooms.RoomId=Rooms.RoomId INNER JOIN Enemies ON EnemiesInTheRooms.EnemyId=Enemies.EnemyId GROUP BY Rooms.Name;")
    result = cur.fetchall()
    for i in result:
        print(i)
    return


def enemiesWithNothing():
    cur.execute(
        "SELECT Enemies.Type, Enemies.Level FROM Enemies WHERE ItemId IS NULL;")
    result = cur.fetchall()
    print("Enemy type, Enemy level.")
    for i in result:
        print(i)
    return


def playersWithProgress():
    cur.execute(
        "SELECT Players.Name, Players.ExpPoints, Players.Level FROM Players WHERE Players.Level>1 OR Players.ExpPoints>1;")
    result = cur.fetchall()
    print("Player name, experience, level")
    for i in result:
        print(i)
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
            cur.execute("INSERT INTO Players(Name) VALUES (?);",[player_name])
            playerId=cur.execute("SELECT PlayerId FROM Players WHERE Name=?;",[player_name]).fetchone()
            cur.execute("INSERT INTO Inventory(PlayerId) VALUES (?);", playerId)
            print("New player created.")
            return
        except sqlite3.IntegrityError as err:
            if err.args == ("UNIQUE constraint failed: Players.Name",):
                print("Name already exists.")
            elif err.args == ("CHECK constraint failed: length(Name) >= 3",):
                print("Your name needs to be between 3 and 30 caharacters.")
            else:
                print("Something went wrong.")
        except:
                print("Something went wrong.")

    elif choice == "2":
        player_name = input("Player name: ")
        print("Current stats are")
        number = searchPlayerStats(player_name)
        if number == -1:
            return
        data = input(
            "Give new stats in form Name, Health, Damage, Level: ")

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


main()
