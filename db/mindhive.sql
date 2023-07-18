-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: mindhive
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `activity_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `activity_name` varchar(45) NOT NULL,
  `Project_project_id` int(10) unsigned NOT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`activity_id`),
  UNIQUE KEY `activity_id_UNIQUE` (`activity_id`),
  KEY `fk_Activity_Project1_idx` (`Project_project_id`),
  CONSTRAINT `fk_Activity_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (1,'Actividad1',1,0),(2,'Actividad2',1,0),(3,'Actividad1',2,0),(4,'Actividad 3',1,0),(5,'Actividad 4',1,0),(6,'Actividad 5',1,0),(7,'Actividad',1,0),(8,'Actividad de prueba`',3,0);
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcement`
--

DROP TABLE IF EXISTS `announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `announcement` (
  `announcement_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `announcement_name` varchar(45) NOT NULL,
  `announcement_description` text NOT NULL,
  `ANNOUNCEMENT_DATE` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `User_uid` int(10) unsigned NOT NULL,
  `Project_project_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`announcement_id`),
  UNIQUE KEY `announcement_id_UNIQUE` (`announcement_id`),
  KEY `fk_Announcement_User1_idx` (`User_uid`),
  KEY `fk_Announcement_Project1_idx` (`Project_project_id`),
  CONSTRAINT `fk_Announcement_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Announcement_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcement`
--

LOCK TABLES `announcement` WRITE;
/*!40000 ALTER TABLE `announcement` DISABLE KEYS */;
INSERT INTO `announcement` VALUES (1,'Anuncio1','Anuncio de prueba\r\n','2023-07-17 00:32:58',1,1),(2,'Anuncio1','peeppe','2023-07-17 01:42:36',1,2),(3,'Anuncio2','descripcion','2023-07-18 01:01:48',3,3);
/*!40000 ALTER TABLE `announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_message`
--

DROP TABLE IF EXISTS `chat_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chat_message` (
  `chat_message_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `chat_message` text NOT NULL,
  `CHAT_MESSAGE_DATE` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `User_uid` int(10) unsigned NOT NULL,
  `Group_Chat_group_chat_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`chat_message_id`),
  UNIQUE KEY `chat_message_id_UNIQUE` (`chat_message_id`),
  KEY `fk_Chat_Message_User1_idx` (`User_uid`),
  KEY `fk_Chat_Message_Group_Chat1_idx` (`Group_Chat_group_chat_id`),
  CONSTRAINT `fk_Chat_Message_Group_Chat1` FOREIGN KEY (`Group_Chat_group_chat_id`) REFERENCES `group_chat` (`group_chat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Chat_Message_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_message`
--

LOCK TABLES `chat_message` WRITE;
/*!40000 ALTER TABLE `chat_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `comment_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `comment_content` varchar(45) NOT NULL,
  `COMMENT_DATE` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `User_uid` int(10) unsigned NOT NULL,
  `Announcement_announcement_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `comment_id_UNIQUE` (`comment_id`),
  KEY `fk_Comment_User1_idx` (`User_uid`),
  KEY `fk_Comment_Announcement1_idx` (`Announcement_announcement_id`),
  CONSTRAINT `fk_Comment_Announcement1` FOREIGN KEY (`Announcement_announcement_id`) REFERENCES `announcement` (`announcement_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comment_User1` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'Comentario de prueba 1\r\n','2023-07-17 00:38:55',1,1),(2,'comentario1\r\n','2023-07-17 01:42:59',1,2),(3,'Eso esta malo','2023-07-17 01:45:01',2,1),(4,'Hola','2023-07-17 21:52:32',1,1),(5,'commentario','2023-07-18 01:01:54',3,3);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_chat`
--

DROP TABLE IF EXISTS `group_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_chat` (
  `group_chat_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`group_chat_id`),
  UNIQUE KEY `group_chat_id_UNIQUE` (`group_chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_chat`
--

LOCK TABLES `group_chat` WRITE;
/*!40000 ALTER TABLE `group_chat` DISABLE KEYS */;
INSERT INTO `group_chat` VALUES (1),(2),(3);
/*!40000 ALTER TABLE `group_chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `project_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project_title` varchar(45) NOT NULL,
  `project_description` text NOT NULL,
  `starting_date` date NOT NULL,
  `ending_date` date NOT NULL,
  `shareable_code` varchar(45) NOT NULL,
  `User_project_creator` int(10) unsigned NOT NULL,
  `Group_Chat_group_chat_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `project_id_UNIQUE` (`project_id`),
  UNIQUE KEY `shareable_code_UNIQUE` (`shareable_code`),
  KEY `fk_Project_User1_idx` (`User_project_creator`),
  KEY `fk_Project_Group_Chat1_idx` (`Group_Chat_group_chat_id`),
  CONSTRAINT `fk_Project_Group_Chat1` FOREIGN KEY (`Group_Chat_group_chat_id`) REFERENCES `group_chat` (`group_chat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Project_User1` FOREIGN KEY (`User_project_creator`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'Proyecto de Prueba 1','Proyecto de prueba para mindhive','2023-07-10','2023-07-20','2883',1,1),(2,'Proyecto2','descripcion2','2023-07-02','2023-08-05','5903',1,2),(3,'Proyecto de prueba 2','prueba','2023-07-02','2023-07-28','5998',3,3);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `user_creation_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `uid_UNIQUE` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Juan Barreto','arroz@gmail.com','3b330640de95da414535d23b7097ce1bf7992b2b','2023-07-17 00:32:07'),(2,' Cedeno','cedeno@gmail.com','3b330640de95da414535d23b7097ce1bf7992b2b','2023-07-17 01:43:47'),(3,'Juan  Barreto','jdbarretog@hotmail.com','3b330640de95da414535d23b7097ce1bf7992b2b','2023-07-18 01:00:26');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_has_project`
--

DROP TABLE IF EXISTS `user_has_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_has_project` (
  `User_uid` int(10) unsigned NOT NULL,
  `Project_project_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`User_uid`,`Project_project_id`),
  KEY `fk_User_has_Project_Project1_idx` (`Project_project_id`),
  KEY `fk_User_has_Project_User_idx` (`User_uid`),
  CONSTRAINT `fk_User_has_Project_Project1` FOREIGN KEY (`Project_project_id`) REFERENCES `project` (`project_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_has_Project_User` FOREIGN KEY (`User_uid`) REFERENCES `user` (`uid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_has_project`
--

LOCK TABLES `user_has_project` WRITE;
/*!40000 ALTER TABLE `user_has_project` DISABLE KEYS */;
INSERT INTO `user_has_project` VALUES (1,1),(1,2),(2,1),(3,3);
/*!40000 ALTER TABLE `user_has_project` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-17 22:01:02
