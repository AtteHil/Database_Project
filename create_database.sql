--Create tables
CREATE TABLE Players (
    PlayerId INTEGER NOT NULL PRIMARY KEY,
    RoomId INTEGER DEFAULT 1,
    Name VARCHAR(30) NOT NULL,
    Health INTEGER NOT NULL,
    Damage INTEGER NOT NULL,
    ExpPoints INTEGER NOT NULL,
    Level INTEGER NOT NULL,
    UNIQUE (Name),
    CHECK (length(Name) >= 3),
    CHECK (RoomId <= Level),
    FOREIGN KEY (RoomId) REFERENCES Rooms (RoomId) ON UPDATE CASCADE
);

CREATE TABLE Rooms (
    RoomId INTEGER NOT NULL PRIMARY KEY,
    Name VARCHAR(30) NOT NULL UNIQUE,
    Level INTEGER NOT NULL
);

CREATE TABLE EnemiesInTheRooms (
    RoomId INTEGER NOT NULL,
    EnemyId INTEGER NOT NULL,
    FOREIGN KEY (RoomId) REFERENCES Rooms (RoomId) ON UPDATE CASCADE,
    FOREIGN KEY (EnemyId) REFERENCES Enemies (EnemyId) ON UPDATE CASCADE
);

CREATE TABLE Enemies (
    EnemyId INTEGER NOT NULL PRIMARY KEY,
    ItemId INTEGER,
    Type VARCHAR(30) NOT NULL,
    Health INTEGER NOT NULL,
    Damage INTEGER NOT NULL,
    Level INTEGER NOT NULL,
    FOREIGN KEY (ItemId) REFERENCES Items (ItemId) ON UPDATE CASCADE    
);

CREATE TABLE Inventory (
    PlayerID INTEGER NOT NULL,
    WeaponSlot INTEGER,
    ArmorSlot INTEGER,
    FOREIGN KEY (WeaponSlot) REFERENCES Items (ItemId) ON UPDATE CASCADE,
    FOREIGN KEY (ArmorSlot) REFERENCES Items (ItemId) ON UPDATE CASCADE,
    FOREIGN KEY (PlayerID) REFERENCES Players (PlayerID) ON UPDATE CASCADE
);

CREATE TABLE Items (
    ItemId INTEGER NOT NULL PRIMARY KEY,
    ItemType VARCHAR(30) NOT NULL,
    Health INTEGER,
    Damage INTEGER,
    Level INTEGER NOT NULL
);

--Inserting default values
INSERT INTO Players
VALUES 
    ( 1, 3, 'Fox', 20, 5, 5, 3),
    (2,1,'Kitty', 15, 4, 8, 2),
    (3,1,'Rumpali', 10, 3, 3, 1),
    (4,3,'Pog', 25, 7, 14, 4),
    (5,5,'Pedestrian', 30, 8, 19, 5);

INSERT INTO Rooms 
VALUES
    (1,'Catacomb',1),
    (2,'Dungeon',2),
    (3,'Tomb',3),
    (4,'Haunted House',4),
    (5,'Elite Catacomb',5);

INSERT INTO EnemiesInTheRooms 
VALUES
    (1,1),
    (2,2),
    (2,3),
    (3,4),
    (4,4),
    (4,5),
    (5,1),
    (5,6);

INSERT INTO Enemies 
VALUES
    (1,NULL,'Skeleton',5,1,1),
    (2,NULL,'Spider',8,9,2),
    (3,1,'Bear',15,2,2),
    (4,2,'Ghost  ',15,4,3),
    (5,NULL,'Decoy',1,0,1),
    (6,3,'Elite Skeleton',30,4,5);

INSERT INTO Items 
VALUES
    (1,'Claw Dagger',NULL,5,2),
    (2,'Spectral Armor',5,NULL,3),
    (3,'Iron Sword',NULL,8,6),
    (4,'AdminArmor',9999,NULL,1),
    (5,'AdminWeapon',NULL,9999,1);

INSERT INTO Inventory 
VALUES
    (1,1,2),
    (2,1,NULL),
    (3,NULL,NULL),
    (4,1,2),
    (5,3,2);