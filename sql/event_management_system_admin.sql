-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: event_management_system
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `admin_id` varchar(4) NOT NULL,
  `admin_name` varchar(100) NOT NULL,
  `admin_email` varchar(100) NOT NULL,
  `admin_phone` varchar(11) NOT NULL,
  `admin_pwd` varchar(50) NOT NULL,
  `admin_descr` text,
  `stripe_public_key` varchar(255) NOT NULL,
  `stripe_secret_key` varchar(255) NOT NULL,
  `admin_img` varchar(255) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_email` (`admin_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('A001','MMU IT Society','itsocietymmu@gmail.com','0111239999','it123','Faculty-based club of Faculty of Computing & Informatics by MMU Cyberjaya Student','pk_test_51PMWarFeLdpgIRLCQdaDneDpcOxMLWM2vMtAI8CAAMvwl1gRrOMTgouy5HWvthCAjjsDayhkgpcj4OG6armC6bKC00oZh8R1VY','sk_test_51PMWarFeLdpgIRLCcD1YhpdSwJESnWBcMmxvtFXvlx9aEfh11QwoCY3eaSMi43B7Ho1BBIld9qMDAaCRIsVbUZpw00lInyAKH0','A001.jpg'),('A002','MMU Chinese Language Society','mmuclsc@gmail.com','0128887777','clsc888','Chinese Language Society','pk_test_51PTQtEA3Fs8xmmiICs4teZCkX1JRvmgXd1GM8ea26644o1zXFUwah4HclHpoeC8zLdxn9rQDiNZjG1f1MtvqPrWw00NTV5u3CZ','sk_test_51PTQtEA3Fs8xmmiI69Ty0wXUsFgz2zxCwliC3hZIdrsdMeSOP7YcZXXT03nuxxhQy8sanqO2Ra1CiG4azi1kbMGR00qOKPEcgm','A002.jpg'),('A003','MMU Students\' Representative Council','mmusrc@gmail.com','0129876543','mmu1stchoice','By the students, For the students','pk_test_51PMWarFeLdpgIRLCQdaDneDpcOxMLWM2vMtAI8CAAMvwl1gRrOMTgouy5HWvthCAjjsDayhkgpcj4OG6armC6bKC00oZh8R1VY','sk_test_51PMWarFeLdpgIRLCcD1YhpdSwJESnWBcMmxvtFXvlx9aEfh11QwoCY3eaSMi43B7Ho1BBIld9qMDAaCRIsVbUZpw00lInyAKH0','A003.jpg'),('A004','MMU OARS','mmuoars@gmail.com','01783935463','iloveoutdoor','Outdoor Activities & Recretional Society','pk_test_51PMWarFeLdpgIRLCQdaDneDpcOxMLWM2vMtAI8CAAMvwl1gRrOMTgouy5HWvthCAjjsDayhkgpcj4OG6armC6bKC00oZh8R1VY','sk_test_51PMWarFeLdpgIRLCcD1YhpdSwJESnWBcMmxvtFXvlx9aEfh11QwoCY3eaSMi43B7Ho1BBIld9qMDAaCRIsVbUZpw00lInyAKH0','A004.jpg');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-22 14:38:28
