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
    first_nameE varchar(256) CHARACTER SET utf8mb4 NOT NULL,
	last_nameE varchar(256),
    addrE varchar(256),
    phone_numberE varchar(256),
	card_numberE varchar(256),
    FOREIGN KEY (anon_code) REFERENCES user(anon_code)
);

CREATE TABLE csr(
	username varchar(50),
	pwd varchar(50),
    first_name varchar(50),
	last_name varchar(50),
	PRIMARY KEY(username)
);

CREATE TABLE blog(
	blog_post varchar(500),
	username varchar(50),
	ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	FOREIGN KEY (username) REFERENCES user(username)
);

CREATE TABLE belongTo(
  username varchar(32),
  groupName varchar(32),
  groupCreator varchar(32)
)

CREATE TABLE ReactTo (
        username VARCHAR(32),
        pID INT,
        reactionTime DATETIME,
        comment VARCHAR(1000),    
	    PRIMARY KEY (reactionTime),
        FOREIGN KEY (pID) REFERENCES Orders (pID),
        FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE Orders (
        pID INT AUTO_INCREMENT,
        postingDate DATETIME,
        filePath VARCHAR(255),
        caption VARCHAR(1000),
        poster VARCHAR(32),
        PRIMARY KEY (pID),
        FOREIGN KEY (poster) REFERENCES user (username)
);

CREATE TABLE Follow(
        follower VARCHAR(32),
        followee VARCHAR(32),
        followStatus INT,
        PRIMARY KEY (follower, followee),
        FOREIGN KEY (follower) REFERENCES user (username),
        FOREIGN KEY (followee) REFERENCES user (username)
);