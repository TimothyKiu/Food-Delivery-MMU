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
-- Table structure for table `registeredaccounts`
--

DROP TABLE IF EXISTS `registeredaccounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registeredaccounts` (
  `registered_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(255) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`registered_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registeredaccounts`
--

LOCK TABLES `registeredaccounts` WRITE;
/*!40000 ALTER TABLE `registeredaccounts` DISABLE KEYS */;
INSERT INTO `registeredaccounts` VALUES ('2024-05-31 07:54:07','jon1','scrypt:32768:8:1$YLo29xAVCcp3f8Y4$8e02bb566f017d668b7ae4790499533d6e277b13ab0d0922c02ac35d133b40ae0ca9f6440383e1220e75fa86cb84b93d83034e64c47ed364ddd37835a9de2e1d','Customer',NULL,NULL),('2024-05-31 07:55:09','run1','scrypt:32768:8:1$WFo0Nz8cvGLNwULF$3100a608443b8ae38becbb44df48691d8f9021ad4a69cd77fe66f8977c6b8f921bdeb7f73738188ee80c6624f5eb5a13a221964f5483906e785ea2b88fd77a0c','Runner',NULL,NULL),('2024-06-06 05:57:42','john','scrypt:32768:8:1$ImZcEPdW5HKYnv8N$4688e4fc234935d39d342a4f87677790bec9a7e9dd363425b61dd2cbf6b679b43a3942a0d82c5ac7b91e7b28f036a9386c80495b8ccc78c5c263004af0c51c48','Customer',NULL,NULL),('2024-06-06 09:05:44','testcustomer','scrypt:32768:8:1$qo0OKL2y464WHAnC$b993cfd6420ee8a7e0180af705cb9a3eb00ddf8cdd7539e6fbd08a7629b3be6ca25e3b0c35a767752fa1595d6b7fd528520c835822fe451388ecc4730eae897c','Customer',NULL,NULL),('2024-06-07 15:57:59','primer','scrypt:32768:8:1$UC7Ha2UAB1WcF1fD$21ac33a5fb11c142811380672d452a65851d22271a0c759a5752b38b61b596bf0b37de5e5addb03909528b74ae740907a1e4274d52ba5a7ee4bb561e1fb81e2e','Runner',NULL,NULL),('2024-06-07 16:01:02','primer1','scrypt:32768:8:1$whjromnQn4IsRkQt$90db99c03f30c0c3f58c976585ba88bb807700eaf3fcfd0c24fba3b434db51ca02ffab3e82bc0e0bf01f3c2d154ba953be2fa8000e1dc3f1c2709171b248fdc9','Runner',NULL,NULL),('2024-06-07 16:23:01','rick','scrypt:32768:8:1$6z4DVqmtDTqWarNM$3a94dd00933521c6bcabc9558c03ed8ee3e3b23baebd4cae1ed8a43313477459b9c8f48537c105d2400839bf3561e26ba35b323789b2b69169bbfc832232b7d3','Runner',NULL,NULL),('2024-06-07 16:49:44','xxxx','scrypt:32768:8:1$0sJjWmTtsl2phn33$c14f2ff7c2ea71f65a33d69559f37c5e72b69e8faadca1e38eb0777a8de337271ed8651b38b766f21a60d19b13fea0da781fd43a5b5af0869c3ade2020ad4918','Runner',NULL,NULL),('2024-06-07 17:17:30','testcustomer2','scrypt:32768:8:1$O4l9EifoWNps7OK6$52d4c315100c284015b7237bf9578927d9e1398bda59ec88c65ac8117c26311894302ebfc9c9107a931d9f4efc50271dc1602d09c86ed85d164214fbce3adb1f','Customer',NULL,NULL),('2024-06-07 17:29:51','qssada','scrypt:32768:8:1$iqcysUHCv6EuGkyU$f0ba2c58abdcc750860fbab0fc1f8b10dd7eeb9ad2ca41f04a08213eb6d04263012227b8fc4e114f09602e3520d710c9f524bc01720f19f1e5e474a1def2a8e4','Customer',NULL,NULL),('2024-06-07 19:03:35','run2','scrypt:32768:8:1$0nBnQR0i5iqxW1db$be868bb67f3db6a347402e123db88a381d3e2b800f65566be32dd7f9f6d508a0d73e579d35132a2a9ca2206a68a7614f7ec0d8dc7756c7677bb902360505a75b','Runner','asdas','111111'),('2024-06-07 19:03:57','cus2','scrypt:32768:8:1$uLKvFFFQG6FMs5ri$a7e69954dbd9794cd85cc25fd0977aa324298914691b8d209ad385cb162375954675ef8b64f6210002518aba07c975ab4fc3917c13a6cf4019325250361e8b71','Customer','x',NULL),('2024-06-09 00:56:23','joe1','scrypt:32768:8:1$3DtBpWmENndJRdpV$2eee87dcc8b7a0250042d97e2ed41b6cbf9fa9b29dccebf333bb693064487a6a4d3e829b2e48fa677966c4f1548b11b36eb272ad23ac93aaf74e953784e1f7ef','Customer',NULL,NULL),('2024-06-09 12:34:45','cjoe','scrypt:32768:8:1$OuwyIKwYooVWkopa$79ed1e8520c34b01a32aa57369ce69788ace9e9777a185b56eda3f554a4719bd540863799c350836344b82db3f08564c59cb1d3b4e0187a32625351f7b19fc08','Customer',NULL,NULL),('2024-06-09 12:53:57','c1','scrypt:32768:8:1$M5yqaPtsZJd253i4$e0c6af6c5d14b7b2eb4e608dba6c909296ba002af10bd204bfd194e05f8baaf7fb3d6146bfe95ce2e0f244a1c2e329913073d3cd219fe66d43b3c08cdbf8f2ed','Customer',NULL,NULL),('2024-06-09 18:16:48','cus3','scrypt:32768:8:1$MgpC4u5sf3YiKGi8$93386aa14ce2e5208c4052d8d0146d4b31c87bf11a56bf4c5ad0340e0a3003eee9d92f566368f99c90be26c0beb42488d0549dae338aa9d2d48e4936901c6d6d','Customer','adasda',NULL),('2024-06-10 22:37:18','tester69','scrypt:32768:8:1$NPN225t2ggE4vyZn$8ad86c2ce64317047d6cd8ecf612bf0770c08abee2e0e42f69422f2f8e5562eb4fdee48e625ff8ef5aa9b7d8d4b66b79595681b2c88ae2c23e4bc3367f06af47','Customer',NULL,NULL),('2024-06-10 22:45:09','dsaojdaio','scrypt:32768:8:1$mz8c5EbtAL5mZQz5$0319c1085f6fa408b5d57579d1bb077543ecb59c06f3f81aaac5f28465f32e85e5a4a1dbe79001fc276ac4e403f691243be47ead16c91703981d1cb6d1e08ae8','Customer',NULL,NULL);
/*!40000 ALTER TABLE `registeredaccounts` ENABLE KEYS */;
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