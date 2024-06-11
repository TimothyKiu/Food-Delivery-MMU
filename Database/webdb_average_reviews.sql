-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: webdb
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `average_reviews`
--

DROP TABLE IF EXISTS `average_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `average_reviews` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `username` varchar(255) DEFAULT NULL,
  `total_ratings` float DEFAULT NULL,
  `rating_count` int DEFAULT NULL,
  `average_rating` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `username_2` (`username`),
  UNIQUE KEY `username_3` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `average_reviews`
--

LOCK TABLES `average_reviews` WRITE;
/*!40000 ALTER TABLE `average_reviews` DISABLE KEYS */;
INSERT INTO `average_reviews` VALUES (27,'2024-05-16 14:31:05','john',37,11,3.36364),(28,'2024-05-16 14:31:05','asdas',2,1,2),(29,'2024-05-16 14:31:05','asdsa',8,2,4),(30,'2024-05-16 14:31:05','DR GRIEF',4,1,4),(31,'2024-05-16 14:31:05','superna',10,2,5),(32,'2024-05-16 14:31:05','bartholomew',12,4,3),(33,'2024-05-16 14:31:05','joh',3,1,3),(34,'2024-05-16 14:31:05','johnsada',3,1,3),(35,'2024-05-16 14:31:05','megajon',9,3,3),(36,'2024-05-16 14:31:05','adf',4,1,4),(37,'2024-05-16 14:31:05','jon1',15,7,2.14286),(44,'2024-05-16 14:59:35','reviews',10,2,5),(46,'2024-05-16 15:02:41','review1',16,6,2.66667),(57,'2024-05-23 16:32:21','runner1',67,15,4.46667),(70,'2024-05-30 09:34:16','customer1',10,2,5),(74,'2024-06-02 15:25:32','run1',23,6,3.83333),(81,'2024-06-07 17:05:30','primer1',23,6,3.83333),(88,'2024-06-07 19:17:19','run2',26,6,4.33333);
/*!40000 ALTER TABLE `average_reviews` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-12  2:44:47
