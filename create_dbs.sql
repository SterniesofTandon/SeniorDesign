CREATE TABLE user(
	username varchar(50),
	password varchar(50),
    anon_code varchar(50),
    first_name varchar(50),
	last_name varchar(50),
    address varchar(50),
    phone_number varchar(50),
	card_number varchar(50),
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
        FOREIGN KEY (pID) REFERENCES Order (pID),
        FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE Order (
        pID INT AUTO_INCREMENT,
        postingDate DATETIME,
        filePath VARCHAR(255),
        caption VARCHAR(1000),
        poster VARCHAR(32),
        -- PRIMARY KEY (pID),
        -- FOREIGN KEY (poster) REFERENCES user (username)
);

CREATE TABLE Follow(
        follower VARCHAR(32),
        followee VARCHAR(32),
        followStatus INT,
        PRIMARY KEY (follower, followee),
        FOREIGN KEY (follower) REFERENCES user (username),
        FOREIGN KEY (followee) REFERENCES user (username)
);

'''
-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Nov 27, 2021 at 09:47 PM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `flaskdemo`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `anon_code` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `anon_code`, `first_name`, `last_name`, `address`, `phone_number`, `card_number`) VALUES
('customer1', 'vibe', NULL, NULL, NULL, NULL, NULL, NULL),
('luizaTest', 'syrup', NULL, NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

  '''