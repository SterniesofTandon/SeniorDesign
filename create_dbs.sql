CREATE TABLE user(
	username varchar(30),
	pwd varchar(30),
    anon_code varchar(256),
    first_name varchar(30),
	last_name varchar(30),
    addr varchar(30),
    phone_number varchar(15),
	card_number varchar(30),
	PRIMARY KEY(anon_code)
);

CREATE TABLE userE(
    anon_code varchar(256),
    first_nameE VARBINARY(256),
	last_nameE VARBINARY(256),
    addrE VARBINARY(256),
    phone_numberE VARBINARY(256),
	card_numberE VARBINARY(256),
    PRIMARY KEY (anon_code),
    FOREIGN KEY (anon_code) REFERENCES user(anon_code)
);

CREATE TABLE blog(
	blog_post varchar(500),
	username varchar(50),
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	FOREIGN KEY (username) REFERENCES user(anon_code)
);

CREATE TABLE belongTo(
  username varchar(32),
  groupName varchar(32),
  groupCreator varchar(32)
)

CREATE TABLE Orders (
        pID VARCHAR(256),
        postingDate DATETIME,
        filePath VARCHAR(255),
        caption VARCHAR(1000),
        poster VARCHAR(256),
        PRIMARY KEY (pID),
        FOREIGN KEY (poster) REFERENCES user (anon_code)
);

CREATE TABLE ReactTo (
        anon_code VARCHAR(256),
        pID VARCHAR(256),
        reactionTime DATETIME,
        comment VARCHAR(1000),    
	    PRIMARY KEY (reactionTime),
        FOREIGN KEY (pID) REFERENCES Orders (pID),
        FOREIGN KEY (anon_code) REFERENCES user (anon_code)
);

CREATE TABLE OrdersE (
        pID VARCHAR(256),
        postingDate DATETIME,
        filePath VARCHAR(255),
        caption VARCHAR(1000),
        posterE VARCHAR(256),
        PRIMARY KEY (postingDate),
        FOREIGN KEY (pID) REFERENCES Orders (pID),
        FOREIGN KEY (posterE) REFERENCES user (anon_code)
);

CREATE TABLE Follow(
        follower VARCHAR(32),
        followee VARCHAR(32),
        followStatus INT,
        PRIMARY KEY (follower, followee)
);

-- CREATE TABLE csr(
-- 	username varchar(50),
-- 	pwd varchar(50),
--     first_name varchar(50),
-- 	last_name varchar(50),
-- 	PRIMARY KEY(username)
-- );