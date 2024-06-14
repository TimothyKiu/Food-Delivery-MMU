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
-- Table structure for table `confirmedorders`
--

DROP TABLE IF EXISTS `confirmedorders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `confirmedorders` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `runnerName` varchar(255) DEFAULT NULL,
  `customerName` varchar(255) DEFAULT NULL,
  `orderCompleted` tinyint(1) DEFAULT NULL,
  `orderList` varchar(255) DEFAULT NULL,
  `restaurant` varchar(255) DEFAULT NULL,
  `customerLocation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=410 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `confirmedorders`
--

LOCK TABLES `confirmedorders` WRITE;
/*!40000 ALTER TABLE `confirmedorders` DISABLE KEYS */;
INSERT INTO `confirmedorders` VALUES (240,'run2','cus3',1,'asdas','Deen\'s',NULL),(249,'run2','john',1,'s','Deen\'s',NULL),(250,'run2','cus3',1,'asd','Deen\'s',NULL),(253,'run1','run1',1,'asdasd','Deen\'s','asdasd'),(264,'run691','tester99',1,'asd','Deen\'s','asdz'),(265,'rok1','lok1',1,'CUS1','Deen\'s','CUS1'),(266,'rok1','lok1',1,'CUS1','Deen\'s','CUS1'),(281,'run1','lok2',1,'zx','Deen\'s','zx'),(282,'rok1','lok2',1,'zx','Deen\'s','zx'),(286,'rok1','rok',1,'122121','Deen\'s','121212'),(287,'rok1','newcus1',1,'111','Deen\'s','11'),(288,'rok1','newcus1',1,NULL,NULL,'placeholder'),(289,'rok1','grok',1,NULL,NULL,'placeholder'),(290,'rok1','grok2',1,NULL,NULL,'placeholder'),(291,'rok1','grok3',1,NULL,NULL,'placeholder'),(292,'rok1','grok3',1,NULL,NULL,'placeholder'),(293,'rok1','grok4',1,NULL,NULL,'placeholder'),(294,'rok1','grok5',1,NULL,NULL,'placeholder'),(295,'rok1','grok6',1,NULL,NULL,'placeholder'),(296,'rok1','grok7',1,'x','Deen\'s','x'),(297,'rok1','tok1',1,'Chicken','Deen\'s','nigga222'),(298,'rok1','rat1',1,'23','Deen\'s','23'),(299,'rok1','rat1',1,'23','Deen\'s','23'),(300,'rok1','rat2',1,'zx','Deen\'s','zx'),(301,'rok1','rat2',1,'zx','Deen\'s','zx'),(302,'rok1','rat2',1,'zx','Deen\'s','zx'),(303,'rok1','rat2',1,'zx','Deen\'s','zx'),(304,'rok1','fat1',1,'x','Deen\'s','z'),(305,'rok1','fat',1,'Chicken','Deen\'s','nigga222'),(306,'rok1','fatt',1,'x','Deen\'s','x'),(309,'rok1','fat',1,'Chicken','Deen\'s','nigga222'),(314,'rok1','tat',1,'asd','Deen\'s','asd'),(315,'rok1','rat6',1,'Chicken','Deen\'s','nigga222'),(317,'rok1','1rrr',1,'bigchicken','Deen\'s','asd'),(322,'rok1','grok',1,'11','Deen\'s','11'),(323,'rok1','grok2',1,'121','Deen\'s','121'),(324,'rok1','grok4',1,'x','Deen\'s','x'),(325,'rok1','grok5',1,'grok5','Deen\'s','moses69'),(326,'rok1','grok6',1,'zx','Deen\'s','zx'),(327,'rok1','grok7',1,'x','Deen\'s','x'),(328,'rok1','tok1',1,'Chicken','Deen\'s','nigga222'),(329,'rok1','fat1',1,'x','Deen\'s','z'),(330,'rok1','rat6',1,'Chicken','Deen\'s','nigga222'),(331,'rok1','11r',1,'Chicken','Deen\'s','nigga222'),(332,'rok1','1rrr',1,'bigchicken','Deen\'s','asd'),(333,'rok1','2rr',1,'asd','Deen\'s','asd'),(334,'rok1','3rr',1,'Chicken','Deen\'s','nigga222'),(335,'rok1','axe',1,'asd','Deen\'s','asd'),(337,'rok1','thefirstavengers',1,'thefirstavengers','Deen\'s','thefirstavengers'),(344,'rok1','gree1',1,'asd','Deen\'s','asd'),(346,'run1','thefirstavengers1',1,'asd','Deen\'s','sd'),(347,'run1','ass1',1,'ass','Deen\'s','ass'),(348,'run1','cr1',1,'asd','Deen\'s','asd'),(349,'run1','cr2',1,'asd','Deen\'s','asd'),(350,'run1','cr3',1,'asd','Deen\'s','asd'),(351,'run1','gree1',1,'asd','Deen\'s','asd'),(352,'run1','gra1',1,'asd','Deen\'s','asd'),(355,'run1','grammar',1,'asd','Deen\'s','asd'),(358,'run1','kupkup',1,'asd','Deen\'s','asd'),(361,'run1','greek',1,'asd','Deen\'s','asd'),(363,'run1','green1',1,'asd','Deen\'s','asd'),(364,'run1','gremlin',1,'asd','Deen\'s','asd'),(365,'run1','123b',1,'asd','Deen\'s','asd'),(366,'run1','tits',1,'ads','Deen\'s','asd'),(367,'run1','tits',1,'ads','Deen\'s','asd'),(368,'run1','tits',1,'ads','Deen\'s','ads'),(369,'run1','tits',1,'asd','Deen\'s','asd'),(371,'run1','kupkup',1,'asd','Deen\'s','asd'),(375,'run1','tits',1,'asd','Deen\'s','asd'),(376,'run1','gremlin',1,'asd','Deen\'s','asd'),(384,'joer1','customer1',NULL,'111','Deen\'s','11'),(386,'run1','asd13',1,'asd','Deen\'s','asd');
/*!40000 ALTER TABLE `confirmedorders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-15  6:29:17
