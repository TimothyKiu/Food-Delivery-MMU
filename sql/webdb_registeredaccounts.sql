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
  `registered_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(255) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registeredaccounts`
--

LOCK TABLES `registeredaccounts` WRITE;
/*!40000 ALTER TABLE `registeredaccounts` DISABLE KEYS */;
INSERT INTO `registeredaccounts` VALUES ('2024-05-07 07:43:47','Joseph1','moses69','Customer',NULL,NULL),('2024-05-08 16:21:22','john','x','Customer','xxx','zzzz'),('2024-05-11 15:27:37','hasher','scrypt:32768:8:1$wvYFy8sFS1w11mpW$d594b5d970c31d44eb3ae1451ddb79941bed2aeafb4ecb47f3e2259ec6da92847755932c1411763b487e646e821958434c33ea4cfa382aa88f041dd565a5efda','Customer',NULL,NULL),('2024-05-11 15:29:38','hasher1','scrypt:32768:8:1$6nk9QRysDo8hm5B3$1a711afec5dbb8cca5597b2f0fcb614ea0e8d247c18538ac6ee1f0bf5275b325c03d977b4765005a255e185c3b1732f1cb05fcf39085581be66a462705ccf8e6','Runner',NULL,NULL),('2024-05-16 09:27:04','john1','scrypt:32768:8:1$IFxlNbNp5Zg4SYrX$281ab71bde735d23d5a3467a5098fa5b8ee2ee7c02cd2b536b1662d3ab3abcfff95a398f949266174bc19481b5ff3ffb9771eee912bc7f0634e899c5de9eed53','Customer',NULL,'0980932840932'),('2024-05-16 09:32:42','dasijodias','scrypt:32768:8:1$XpCN7ROwucswuorM$1aff2cb3b3044f15e838bb3f1ec8ec1080b067ca59620f29df4317f92b4287422ef035ddc89d53682ba92c4f93d749e8a9d7bf49794bd60d49f8df8197802c7b','Customer',NULL,NULL),('2024-05-16 10:49:16','jon1','scrypt:32768:8:1$vh8OcELaDLN5wnxW$564fec21c517321daabc4c162b5975d4a178050c01384df570a3fe62d4c97525d1b059f36c10f08bcb1306b2a206078063c586fa869739d43a67c37e57ba8599','Customer','Jon','013222269'),('2024-05-16 14:59:06','reviews','scrypt:32768:8:1$MHsHBJ0g2rPPglgl$b18cc6d3cad050fe8b8d62cece261d093d62bde4f1e1f5bd31d75c1778b3a51e1aa2c8c466efe44f3e8fd368a999c55ca6499b8e105d0cec199f1876693b5878','Customer',NULL,NULL),('2024-05-16 15:02:21','review1','scrypt:32768:8:1$tV37jW1XtFt23uH9$7b1def98f3b0c3349a66009a594cac6f37cd6bf8fc8254a39b9886e0f64f12c2128440511839f5ba9898a1c5a90bf398b7aa229a11edf1b8d6f2ddf99d3c586b','Customer',NULL,NULL),('2024-05-23 11:28:01','joe1','scrypt:32768:8:1$lvrxnVFcuDBXo2rH$1e0cb94e07ec72c2b9316b9a3467ede6cbb999fdc6de65331f3bad90a563dcede8362a233acfd5082d1bc83f5723a15222919e9ec89e54266c793391128ca832','Customer',NULL,NULL),('2024-05-23 14:41:52','runner1','scrypt:32768:8:1$6lUnHNB07OuPu9vb$03d5ef344bf18af2557bac6f00420ddc514a587bc8882fd4afc7bd62e69ec94c2563f545bb48f391185d40893ab335cfd6b67a1fe45dd8f7ec6050b2b7f7b2b6','Runner',NULL,NULL),('2024-05-23 15:38:35','idk','scrypt:32768:8:1$vAFKiln0MILals1X$e394214ddec7ea437d102b43b4de6dfe0edca741e1185497c9883060c935b119a3276d3bc9f6a4c4eb356a32358d12cbaa6527ee5e1a25848ae37dcda6a021f0','Customer',NULL,NULL),('2024-05-24 20:31:10','joeswanson','scrypt:32768:8:1$hIjtdRcHxl0a2X7v$4f7f0950a1793a6974406db979040ec3aed48d0f1d84bda6573a743b9ed3385da09a44d899c5018c2df18db5404c3ac8be6f7753a77fad75d9cfb0cd006025e8','Customer',NULL,NULL),('2024-05-26 21:08:15','jon232','scrypt:32768:8:1$yaIUxWmT8eedJ6Am$7f7fc105ff8d6ea10b594c320c3af86074f5c2427b5851e3f155bcc4efca36234e34ab695c562aa818bafb6f204124a15d297136af305a93dd9d3e0da91efedf','Customer',NULL,NULL),('2024-05-26 21:31:01','cus1','scrypt:32768:8:1$i662sv4FT2scpTro$69062aff1cfb8c2ad09e1e0b1d7a943ab87c0f54c528f9b83f19bfd67b41c18acc6ef985e2e91642c6d86857e9ff0de1494e2955a206d49c08e0e1333fdc2206','Customer',NULL,NULL),('2024-05-26 21:31:35','cus2','scrypt:32768:8:1$goOeAWUGuFn9PuJx$cd22c81def1dc6b5718aa14bf90c5a52be129b41a1969468bb51d2662995eeadaf68ece9471bb867064e619812ae5eeeedfdc5f60f106ef742f37797d28f8a11','Customer',NULL,NULL),('2024-05-26 21:37:13','c1','scrypt:32768:8:1$jbtBcOpSpmIZDrrH$eb8b560bfb2c3911e02a5b1fcb0d5ff4ec32f68600d26a6f853353f55782f467e5792d03f213f0e8f9648b76b698934ffcd74ea0826a0189ac76f4532e452fcb','Customer',NULL,NULL),('2024-05-26 21:39:29','c2','scrypt:32768:8:1$2up2EL0d3D2pGhQz$1e622bfd504f9954332d6d0d47a69f216b26e808ef8f1891cac5458dfa9dbd14599b5c61206f37aed8bb5036fd3a3d1f999d6bd3f1794a1647e35852e2dd7c08','Customer',NULL,NULL),('2024-05-26 21:52:11','c3','scrypt:32768:8:1$9zTLrMjbo7AOZrHA$f061c6593cddcae76907054722b80aa5082fb6970b34b3259ac9649776f334a70e65ceb9af0e7bf083e1520a7fa5b8afa366e10ed67ad83458d7d5f00e0e6242','Customer',NULL,NULL),('2024-05-26 22:03:15','c4','scrypt:32768:8:1$OxDVehR3S6W3uZeo$ba96ba1c1f20512c52cd64d2bab63d9507a06c9308623e33b3b83cacfdf87dee460d0642ea4f9d85d3af29ec13392b5a5b4492a78454255550d336cfb6c46c94','Customer',NULL,NULL),('2024-05-26 22:09:22','c5','scrypt:32768:8:1$PV5pDZ8Faaj1ukKx$fdc684aaa9895ee8b3e1539a879c8c53ef4006bfb8b710b49c19963c4a8b520bb190368df7698412083390fa8e685156cf55a6c4bf41f66f953bafea944e82a2','Customer',NULL,NULL),('2024-05-26 22:11:12','c6','scrypt:32768:8:1$XYvWMr0k2Ju5tqMj$3ba1393dd0994d94abee9f6c238ed00a2643339ec4321666279adfcad5a262ed27372510dfae7891c7917030eb9cddd02b9cf90ac3de7b3327a41bf2b85ccb32','Customer',NULL,NULL),('2024-05-26 22:12:22','c7','scrypt:32768:8:1$6MWW9oFHk4RnFcJB$9e0505580342d9a145f9145c726bcf944fd838f5570abeae81d202a4aa69b9f372d8d7cd982255f39c48c9ed61fabfcc8fcbf75c5d9b3a0c8fac085c934dd38b','Customer',NULL,NULL),('2024-05-26 22:16:08','c8','scrypt:32768:8:1$XAZtrqzcDb0x0xyM$c436d8d8029af513439b7ad996749b8c22f222db7dd9c0138042225dde163e9941b7367bdb590b2cf94e1c2c2a675829dfe6c41bc1778ead54242ce7fcc6ced7','Customer',NULL,NULL),('2024-05-26 22:16:33','a1','scrypt:32768:8:1$rbORPGi8Il10cYM0$c4e68fa8536ed0175dd3d936dd315171b30857ea3bc4cc68afefab1cf5026d52269ec7a8ca94aafc538043d8cee5daa79a1d2e3af40706a48c69f7f6550ef4b7','Customer',NULL,NULL),('2024-05-26 22:19:27','a2','scrypt:32768:8:1$2AIv8M5o6K71oirY$517fceb7b6cd45fc3db477171e7e8e01aee8d43116f391660a031af39f962484cfe1477a0927c050314065d55c225ecf56e632ce76866c94e54c72e53f0a22c0','Customer',NULL,NULL),('2024-05-26 22:31:55','a4','scrypt:32768:8:1$yVdfNDTXcsMOeMqS$e73187b019caf04046a4de797369da857998e3ee83c98c31db05a63a227ddd1dda9772c2151e0f55c6f2f42f0674cbbc3c16f2ecfea81f318f3f583dce9aedf9','Customer',NULL,NULL),('2024-05-26 22:33:41','z1','scrypt:32768:8:1$7BlHvyNIaICaycmG$749adbf0c465ca5ed1e2fb580213267ed33be77326de1f7d6d77eead5b226836ff8d1095c7f2a79e91c76fb06e225d24f009a19c1f1c3728f603886f072fecce','Customer',NULL,NULL),('2024-05-26 22:35:34','1','scrypt:32768:8:1$ChTs8DT97nwp1Z48$7d7b95e0a6278b1bb4d8b032cfd8a0d479bff6adc236970d40d9df19dc30387a59a75ad45b69dd18578186c7b60d27c4014e0c8508e231634257c2c21183ba66','Customer',NULL,NULL),('2024-05-27 04:46:12','2','scrypt:32768:8:1$FwxhwbLJkAjOBKk7$26ac6b2bf69298e191d1f9f56e0ca614f1eaf66f1a9fa51c7d36e747f3ae364c44c70029b2a6d920d7b3344eda34e429444ea6f166968ec6d6d660fe72c54e4c','Customer',NULL,NULL),('2024-05-27 05:02:44','3','scrypt:32768:8:1$Iw1sJV8nXCdYLwD3$a4485f67906f95fd122cee7d764226539a2874cc7288c315ab3636a03068c6fd4c53c5d6f824478f673909ecbcc306460526be92fb75879700e2e5f60c8165bf','Customer',NULL,NULL),('2024-05-27 05:16:29','q','scrypt:32768:8:1$XZ943ecGk5yqo2e3$4fb8157c3667d2d67d215f946ea992abf6f8555f0c96744f17cffab57dc511be4a6685b92c8c2568f93b3c5926371f2497888146567a40e1951fcb5d17913cc6','Customer',NULL,NULL),('2024-05-27 05:16:38','12','scrypt:32768:8:1$nY2NI2l0tVwcB4li$d0355244d479cecf128b22f3bd139254fc0f83f1a8f2882be8f57b33afd97b089b19b95424784c78e485b4d672dc6b5649ced148c3f93162968abe0ed19c3008','Customer',NULL,NULL),('2024-05-27 05:24:23','xd','scrypt:32768:8:1$KKKeLgFVLo2eSS5V$967274f5603acdf493fde4937de89145b13885c0821426ed9aeb28abb842ec26f5ae706b923ec60e53e78bd1151da4abc4f8e857291d9030dca1b6abae4a91cf','Customer',NULL,NULL);
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

-- Dump completed on 2024-05-30 15:28:33