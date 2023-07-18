-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 25, 2023 at 06:21 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mindhive`
--
CREATE DATABASE IF NOT EXISTS `mindhive` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mindhive`;

-- --------------------------------------------------------

--
-- Table structure for table `activity`
--

CREATE TABLE IF NOT EXISTS `activity` (
  `activity_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `activity_name` varchar(45) NOT NULL,
  `Project_project_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`activity_id`),
  UNIQUE KEY `activity_id_UNIQUE` (`activity_id`),
  KEY `fk_Activity_Project1_idx` (`Project_project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `activity`:
--   `Project_project_id`
--       `project` -> `project_id`
--

-- --------------------------------------------------------

--
-- Table structure for table `announcement`
--

CREATE TABLE IF NOT EXISTS `announcement` (
  `announcement_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `announcement_name` varchar(45) NOT NULL,
  `announcement_description` text NOT NULL,
  `announcement_Date` date NOT NULL,
  `User_uid` int(10) UNSIGNED NOT NULL,
  `Project_project_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`announcement_id`),
  UNIQUE KEY `announcement_id_UNIQUE` (`announcement_id`),
  KEY `fk_Announcement_User1_idx` (`User_uid`),
  KEY `fk_Announcement_Project1_idx` (`Project_project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `announcement`:
--   `Project_project_id`
--       `project` -> `project_id`
--   `User_uid`
--       `user` -> `uid`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat_message`
--

CREATE TABLE IF NOT EXISTS `chat_message` (
  `chat_message_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `chat_message` text NOT NULL,
  `chat_message_date` date NOT NULL,
  `User_uid` int(10) UNSIGNED NOT NULL,
  `Group_Chat_group_chat_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`chat_message_id`),
  UNIQUE KEY `chat_message_id_UNIQUE` (`chat_message_id`),
  KEY `fk_Chat_Message_User1_idx` (`User_uid`),
  KEY `fk_Chat_Message_Group_Chat1_idx` (`Group_Chat_group_chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `chat_message`:
--   `Group_Chat_group_chat_id`
--       `group_chat` -> `group_chat_id`
--   `User_uid`
--       `user` -> `uid`
--

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE IF NOT EXISTS `comment` (
  `comment_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `comment_content` varchar(45) NOT NULL,
  `comment_date` date NOT NULL,
  `User_uid` int(10) UNSIGNED NOT NULL,
  `Announcement_announcement_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `comment_id_UNIQUE` (`comment_id`),
  KEY `fk_Comment_User1_idx` (`User_uid`),
  KEY `fk_Comment_Announcement1_idx` (`Announcement_announcement_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `comment`:
--   `Announcement_announcement_id`
--       `announcement` -> `announcement_id`
--   `User_uid`
--       `user` -> `uid`
--

-- --------------------------------------------------------

--
-- Table structure for table `group_chat`
--

CREATE TABLE IF NOT EXISTS `group_chat` (
  `group_chat_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`group_chat_id`),
  UNIQUE KEY `group_chat_id_UNIQUE` (`group_chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `group_chat`:
--

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE IF NOT EXISTS `project` (
  `project_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_title` varchar(45) NOT NULL,
  `project_description` text NOT NULL,
  `starting_date` date NOT NULL,
  `ending_date` date NOT NULL,
  `shareable_code` varchar(45) NOT NULL,
  `User_uid` int(10) UNSIGNED NOT NULL,
  `Group_Chat_group_chat_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `project_id_UNIQUE` (`project_id`),
  UNIQUE KEY `shareable_code_UNIQUE` (`shareable_code`),
  KEY `fk_Project_User1_idx` (`User_uid`),
  KEY `fk_Project_Group_Chat1_idx` (`Group_Chat_group_chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `project`:
--   `Group_Chat_group_chat_id`
--       `group_chat` -> `group_chat_id`
--   `User_uid`
--       `user` -> `uid`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `uid` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `user_creation_date` date NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `uid_UNIQUE` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `user`:
--

-- --------------------------------------------------------

--
-- Table structure for table `user_has_project`
--

CREATE TABLE IF NOT EXISTS `user_has_project` (
  `User_uid` int(10) UNSIGNED NOT NULL,
  `Project_project_id` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`User_uid`,`Project_project_id`),
  KEY `fk_User_has_Project_Project1_idx` (`Project_project_id`),
  KEY `fk_User_has_Project_User_idx` (`User_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- RELATIONSHIPS FOR TABLE `user_has_project`:
--   `Project_project_id`
--       `project` -> `project_id`
--   `User_uid`
--       `user` -> `uid`
--

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity`
--
ALTER TABLE `activity`
  ADD CONSTRAINT `fk_Activity_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `announcement`
--
ALTER TABLE `announcement`
  ADD CONSTRAINT `fk_Announcement_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Announcement_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `chat_message`
--
ALTER TABLE `chat_message`
  ADD CONSTRAINT `fk_Chat_Message_Group_Chat1` FOREIGN KEY (`Group_Chat_group_chat_id`) REFERENCES `group_chat` (`group_chat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Chat_Message_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `fk_Comment_Announcement1` FOREIGN KEY (`Announcement_announcement_id`) REFERENCES `announcement` (`announcement_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Comment_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `project`
--
ALTER TABLE `project`
  ADD CONSTRAINT `fk_Project_Group_Chat1` FOREIGN KEY (`Group_Chat_group_chat_id`) REFERENCES `group_chat` (`group_chat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Project_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `user_has_project`
--
ALTER TABLE `user_has_project`
  ADD CONSTRAINT `fk_User_has_Project_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_User_has_Project_User` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION;


--
-- Metadata
--
USE `phpmyadmin`;

--
-- Metadata for table activity
--

--
-- Metadata for table announcement
--

--
-- Metadata for table chat_message
--

--
-- Metadata for table comment
--

--
-- Metadata for table group_chat
--

--
-- Metadata for table project
--

--
-- Metadata for table user
--

--
-- Metadata for table user_has_project
--

--
-- Metadata for database mindhive
--
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
