CREATE DATABASE movielens;
GO

USE movielens;
GO

CREATE TABLE movies(
    MovieID INT PRIMARY KEY,
    Title NVARCHAR(100),
    Genres NVARCHAR(100) 
);

CREATE TABLE users(
    UserID INT PRIMARY KEY,
    Gender CHAR(1),
    Age INT,
    Occupation INT,
    Zip-code VARCHAR
);

CREATE TABLE ratings(
    UserID INT,
    MovieID INT,
    Rating INT,
    Timestamp BIGINT,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (MovieID) REFERENCES movies(MovieID)
);

BULK INSERT movies
FROM '/var/opt/mssql/app/data/movies.csv'
WITH (
    FIELDTERMINATOR = '::',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    TABLOCK
);

BULK INSERT users
FROM '/var/opt/mssql/app/data/users.csv'
WITH (
    FIELDTERMINATOR = '::',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    TABLOCK
);

BULK INSERT ratings
FROM '/var/opt/mssql/app/data/users.csv'
WITH (
    FIELDTERMINATOR = '::',
    ROWTERMINATOR = '\n',
    FIRSTROW = 1,
    TABLOCK
);

GO