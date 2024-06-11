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
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `review_text` text,
  `rating_given` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (8,'john','asdasd',5,'2024-05-09 11:21:01'),(9,'john','asdasd',1,'2024-05-09 11:21:09'),(10,'asdas','dsada',2,'2024-05-09 11:33:22'),(11,'asdsa','asdas',4,'2024-05-09 11:36:00'),(12,'asdsa','asdas',4,'2024-05-09 11:36:01'),(13,'DR GRIEF','asdas',4,'2024-05-09 11:36:22'),(14,'john','asd',5,'2024-05-09 11:39:09'),(15,'john','asd',5,'2024-05-09 11:40:26'),(16,'superna','asd',5,'2024-05-09 11:46:59'),(17,'superna','asd',5,'2024-05-09 11:47:38'),(18,'bartholomew','asd',5,'2024-05-09 11:50:29'),(19,'bartholomew','asd',3,'2024-05-09 11:52:41'),(20,'bartholomew','asd',3,'2024-05-09 11:53:27'),(21,'joh','asd',3,'2024-05-09 11:53:37'),(22,'john','asd',3,'2024-05-09 11:53:37'),(23,'johnsada','asd',3,'2024-05-09 11:57:42'),(24,'megajon','asd',3,'2024-05-09 11:58:12'),(25,'megajon','asd',3,'2024-05-09 11:58:30'),(26,'megajon','asd',3,'2024-05-09 11:59:14'),(27,'adf','adf',4,'2024-05-09 12:01:45'),(28,'john','asd',5,'2024-05-09 12:14:04'),(29,'john','asd',5,'2024-05-09 16:09:57'),(30,'john','asdsa',1,'2024-05-09 17:18:53'),(31,'john','asdsa',1,'2024-05-09 17:21:02'),(32,'jon1','x',5,'2024-05-16 11:10:02'),(33,'jon1','test',1,'2024-05-16 14:35:17'),(34,'jon1','test34324',5,'2024-05-16 14:37:05'),(35,'reviews','Gay runner',5,'2024-05-16 14:59:35'),(36,'reviews','Gay runnerx',5,'2024-05-16 15:00:47'),(37,'review1','Gay runner!',5,'2024-05-16 15:02:41'),(38,'review1','Shit runner!',5,'2024-05-16 15:02:52'),(39,'review1','Garbage runner',1,'2024-05-16 15:42:02'),(40,'review1','Garbage runner',1,'2024-05-16 15:42:44'),(41,'jon1','jon1 ate all my food',1,'2024-05-16 16:08:36'),(42,'jon1','He punched my mom',1,'2024-05-16 16:08:59'),(43,'jon1','Dipshit runner literally spilled all my damn curry sauce all over the bag, if I could I would give him zero stars. Ban this punk immediately!',1,'2024-05-16 21:20:41'),(44,'jon1','Dipshit runner literally spilled all my damn curry sauce all over the bag, if I could I would give him zero stars. Ban this punk immediately!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',1,'2024-05-16 21:20:57'),(45,'review1','XXXXXXZ',3,'2024-05-16 21:28:47'),(46,'review1','1 Star.',1,'2024-05-20 06:13:40'),(47,'bartholomew','sdsjsaoidasoidjaoida',1,'2024-05-23 08:54:39'),(48,'runner1','Awesome!',5,'2024-05-23 16:32:21'),(49,'runner1','Does this work??',5,'2024-05-23 16:49:38'),(50,'runner1','xx',5,'2024-05-23 16:59:32'),(51,'runner1','poop service',1,'2024-05-24 20:33:42'),(52,'runner1','x',5,'2024-05-26 22:24:56'),(53,'runner1','1',5,'2024-05-26 22:36:06'),(54,'runner1','xxxxxNICE!',5,'2024-05-27 05:03:12'),(55,'runner1','xxxxxNICE!',5,'2024-05-27 05:03:31'),(56,'runner1','xxxxxNICE!',5,'2024-05-27 05:05:01'),(57,'runner1','x',5,'2024-05-27 05:05:18'),(58,'runner1','x',5,'2024-05-27 05:08:10'),(59,'runner1','x',5,'2024-05-27 05:23:41'),(60,'runner1','xd',5,'2024-05-27 05:24:51'),(61,'customer1','GREETIngs.',5,'2024-05-30 09:34:16'),(62,'customer1','zxx',5,'2024-05-30 14:36:26'),(63,'runner1','New design test',5,'2024-05-30 15:25:43'),(64,'runner1','zzz',1,'2024-05-30 15:46:29'),(65,'run1','Xxxx',5,'2024-06-02 15:25:32'),(66,'run1','z',2,'2024-06-02 15:26:39'),(67,'run1','',1,'2024-06-05 16:25:35'),(68,'run1','dsaohdoas',5,'2024-06-05 16:57:13'),(69,'run1','finaltest',5,'2024-06-06 05:58:24'),(70,'run1','x',5,'2024-06-06 06:24:55'),(71,'john','rating',5,'2024-06-06 09:07:09'),(72,'primer1','TEST RUN LETS GO!',5,'2024-06-07 17:05:30'),(73,'primer1','xxx',3,'2024-06-07 17:06:36'),(74,'primer1','x',5,'2024-06-07 17:15:41'),(75,'john','x',1,'2024-06-07 17:20:28'),(76,'primer1','x',4,'2024-06-07 17:27:32'),(77,'primer1','xxx',2,'2024-06-07 18:00:33'),(78,'primer1','joe2',4,'2024-06-07 18:00:52'),(79,'run2','x',2,'2024-06-07 19:17:19'),(80,'run2','sdaas',5,'2024-06-10 17:43:45'),(81,'run2','dfdg',5,'2024-06-10 17:44:35'),(82,'run2','run2 gay',5,'2024-06-10 21:28:35'),(83,'run2','tessss',5,'2024-06-11 09:20:46'),(84,'run2','XXX',4,'2024-06-11 18:43:48');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
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
