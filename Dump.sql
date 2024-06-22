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

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(100) NOT NULL,
  `event_descr` text,
  `event_start` datetime NOT NULL,
  `event_end` datetime NOT NULL,
  `event_time` time NOT NULL,
  `event_duration` varchar(50) NOT NULL,
  `event_img` varchar(255) DEFAULT NULL,
  `category_id` varchar(3) NOT NULL,
  `eventvenue_id` varchar(3) NOT NULL,
  `location_details` varchar(255) NOT NULL,
  `admin_id` varchar(4) NOT NULL,
  `publish_status` varchar(45) NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`),
  KEY `admin_id` (`admin_id`),
  KEY `category_id` (`category_id`),
  KEY `eventvenue_id` (`eventvenue_id`),
  CONSTRAINT `admin_id` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  CONSTRAINT `category_id` FOREIGN KEY (`category_id`) REFERENCES `event_category` (`category_id`),
  CONSTRAINT `eventvenue_id` FOREIGN KEY (`eventvenue_id`) REFERENCES `event_venue` (`eventvenue_id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'PEAK PURSUIT: GUNUNG DATUK','Step into nature’s embrace with OARS! Come and join our latest hiking event PEAK PURSUIT: GUNUNG DATUK with us.','2024-05-26 00:00:00','2024-05-26 00:00:00','05:00:00','8 hours','event1.jpg','C03','V02','Gunung Datuk Recreational Forest, Negeri Sembilan','A004','Published','2024-05-15 16:00:00'),(2,'Adobe Workshop: Artistry Unleashed','Calling all MMU students, Are you ready to elevate your Adobe skills? Explore the realm of creation with our upcoming Artistry Unleashed workshop. Master Adobe Photoshop and Illustrator deeper as we guide you to empower yourself with the tools and techniques necessary to bring life to your ideas. Whether you’re a beginner eager to learn the basics or a seasoned pro looking to refine your skills, this workshop is going to take your skills to the next level and it’s FREE OF CHARGE!!','2024-05-26 00:00:00','2024-05-26 00:00:00','13:00:00','5 hours','event2.jpg','C01','V03','Microsoft Teams','A003','Published','2024-05-17 16:00:00'),(3,'Tech Talk: Blockchain with ICP - Become a Blockchain Expert (0 to 100)','Join ICP Malaysia for an in-depth exploration of blockchain technology and the Internet Computer Protocol.','2024-05-27 00:00:00','2024-05-27 00:00:00','19:00:00','2 hours','event3.jpg','C01','V01','Agmo Space, FCM','A001','Published','2024-05-14 16:00:00'),(4,'Stage Show \"Suffocate\"','Complex interpersonal relationships, perplexing plots that keep everyone guessing about the next scene, the ups and downs of life, and societal issues surrounding us - all filled with surprises leading to unexpected endings.\r\n\r\nThe human inner self is often influenced by a force called “emotion.”?? In the inner conflict of the heart and mind, others need to carefully make the final choices at crossroads, determining the direction they take forward.','2024-06-14 00:00:00','2024-06-14 00:00:00','20:00:00','2 hours','event4.jpg','C02','V01','Dewan Tun Canselor, Multimedia University (Cyberjaya)','A002','Published','2024-05-17 16:00:00'),(5,'CodeSprint 2024','Compete in our annual coding competition and showcase your problem-solving skills!','2024-07-15 00:00:00','2024-07-15 00:00:00','09:00:00','6 hours','event5.jpg','C01','V01','Agmo Space, FCM','A001','Published','2024-06-14 16:00:00'),(6,'Chinese Cultural Night','Immerse yourself in the rich culture of China with performances, food, and activities.','2024-08-01 00:00:00','2024-08-01 00:00:00','19:00:00','4 hours','event6.jpg','C02','V01','Dewan Tun Canselor, Multimedia University (Cyberjaya)','A002','Published','2024-06-19 16:00:00'),(7,'Outdoor Adventure: Taman Negara','Join us for an exhilarating adventure in Taman Negara, exploring the natural beauty of Malaysia.','2024-09-10 00:00:00','2024-09-10 00:00:00','06:00:00','10 hours','event7.jpg','C03','V02','Taman Negara, Pahang','A004','Published','2024-06-18 16:00:00'),(8,'SRC Town Hall Meeting','An open forum for students to discuss their concerns and suggestions with the SRC.','2024-07-20 00:00:00','2024-07-20 00:00:00','14:00:00','3 hours',NULL,'C04','V01','Dewan Tun Canselor, Multimedia University (Cyberjaya)','A003','Published','2024-06-19 16:00:00'),(9,'Mental Health Awareness Week','Join us for a series of workshops and talks focusing on mental health and well-being.','2024-08-05 00:00:00','2024-08-09 00:00:00','10:00:00','8 hours','event9.jpg','C04','V01','Dewan Tun Canselor, Multimedia University (Cyberjaya)','A003','Published','2024-06-21 16:00:00'),(10,'Career Fair 2024','Meet potential employers and learn about career opportunities in various fields.','2024-09-15 00:00:00','2024-09-15 00:00:00','09:00:00','7 hours','event10.jpg','C01','V01','Dewan Tun Canselor, Multimedia University (Cyberjaya)','A003','Published','2024-06-19 16:00:00'),(11,'Blood Donation Drive','Help save lives by donating blood. Organized in collaboration with the National Blood Bank.','2024-10-10 00:00:00','2024-10-10 00:00:00','10:00:00','6 hours','event11.jpg','C04','V01','MPH, Multimedia University (Cyberjaya)','A003','Published','2024-06-20 16:00:00'),(32,'Happy','awd xghsos cpe vsk vhhjhshv cas\r\newfvsd dcgs;vds hlfklvnelv\r\ndjsd gilfnlleounv ','2024-06-20 00:00:00','2024-06-21 00:00:00','15:00:00','5 hours',NULL,'C04','V03','Google meet','A003','Draft','2024-05-17 16:00:00'),(52,'Fun Fair','wihfq dyfdg ;cw\r\ndsdfdvckjqwd\r\n','2024-06-14 00:00:00','2024-06-18 00:00:00','23:00:00','3 hours','event52.png','C02','V01','CLC, MMU','A003','Draft','2024-05-17 16:00:00'),(53,'Play','BHDVJCBJSD,BVCRGIURBVD\r\nSDBFJKLABRGHHBVNKWFBK','2024-06-11 00:00:00','2024-06-12 00:00:00','10:34:00','3 hours','','C01','V03','Google meet','A001','Draft','2024-05-17 16:00:00'),(54,'Save the Earth','Come to save Earth','2024-06-20 00:00:00','2024-06-22 00:00:00','12:00:00','1 day','event54.jpg','C04','V02','Taman pokok','A003','Published','2024-06-14 16:00:00'),(62,'Hello World','hiiiiiiiiii','2024-06-29 00:00:00','2024-06-30 00:00:00','12:46:00','3 hours','','C04','V01','Cyberpark, MMU','A001','Draft','2024-05-17 16:00:00'),(64,'Happy','hsrtj yjs yj','2024-06-21 00:00:00','2024-06-24 00:00:00','23:10:00','5 hours','','C03','V01','Cyberpark, MMU','A004','Draft','2024-06-21 04:32:36'),(65,'Computer fair','dsfaefaewf','2024-06-21 00:00:00','2024-06-22 00:00:00','23:42:00','5 hours','','C01','V01','aeffefawg','A001','Draft','2024-06-21 04:32:36');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_category`
--

DROP TABLE IF EXISTS `event_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_category` (
  `category_id` varchar(3) NOT NULL,
  `category` varchar(30) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_category`
--

LOCK TABLES `event_category` WRITE;
/*!40000 ALTER TABLE `event_category` DISABLE KEYS */;
INSERT INTO `event_category` VALUES ('C01','Academic'),('C02','Entertainments'),('C03','Sports'),('C04','Others');
/*!40000 ALTER TABLE `event_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_venue`
--

DROP TABLE IF EXISTS `event_venue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_venue` (
  `eventvenue_id` varchar(3) NOT NULL,
  `location` varchar(10) NOT NULL,
  PRIMARY KEY (`eventvenue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_venue`
--

LOCK TABLES `event_venue` WRITE;
/*!40000 ALTER TABLE `event_venue` DISABLE KEYS */;
INSERT INTO `event_venue` VALUES ('V01','On campus'),('V02','Off campus'),('V03','Online');
/*!40000 ALTER TABLE `event_venue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_status`
--

DROP TABLE IF EXISTS `member_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_status` (
  `mstatus_id` int NOT NULL,
  `mstatus_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`mstatus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_status`
--

LOCK TABLES `member_status` WRITE;
/*!40000 ALTER TABLE `member_status` DISABLE KEYS */;
INSERT INTO `member_status` VALUES (1,'Pending'),(2,'Accept'),(3,'Reject');
/*!40000 ALTER TABLE `member_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership`
--

DROP TABLE IF EXISTS `membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership` (
  `membership_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `admin_id` varchar(4) NOT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `mstatus_id` int NOT NULL,
  PRIMARY KEY (`membership_id`),
  KEY `membership_ibfk_1` (`user_id`),
  KEY `membership_ibfk_2` (`admin_id`),
  KEY `status_id_idx` (`mstatus_id`),
  CONSTRAINT `membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `membership_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `mstatus_id` FOREIGN KEY (`mstatus_id`) REFERENCES `member_status` (`mstatus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership`
--

LOCK TABLES `membership` WRITE;
/*!40000 ALTER TABLE `membership` DISABLE KEYS */;
INSERT INTO `membership` VALUES (1,'1221107001','A001','2024-03-31 16:00:00',2),(2,'1221107001','A004','2024-06-21 15:18:36',1),(3,'1221107002','A001','2024-04-01 16:00:00',2),(4,'1221107555','A001','2024-06-22 04:52:05',1),(5,'1221109001','A001','2024-04-02 16:00:00',2),(30,'1221109001','A002','2024-06-20 04:35:43',3),(33,'1221109001','A002','2024-06-21 09:27:17',1);
/*!40000 ALTER TABLE `membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `ticket_type` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `member_discount` decimal(10,2) NOT NULL,
  `max_quantity` int NOT NULL,
  `start_sale` datetime NOT NULL,
  `end_sale` datetime NOT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`),
  CONSTRAINT `ticket_chk_1` CHECK ((`price` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10000089 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (10000001,4,'Early bird',20.00,17.00,200,'2024-04-11 00:00:00','2024-05-21 00:00:00'),(10000002,4,'Normal',23.00,20.00,300,'2024-04-11 00:00:00','2024-06-08 00:00:00'),(10000003,1,'General',30.00,25.00,50,'2024-05-14 00:00:00','2024-05-21 00:00:00'),(10000004,2,'Normal',0.00,0.00,100,'2024-05-18 00:00:00','2024-05-25 00:00:00'),(10000006,3,'Normal',0.00,0.00,100,'2024-05-18 00:00:00','2024-05-26 00:00:00'),(10000007,5,'Early bird',10.00,8.00,100,'2024-06-01 00:00:00','2024-07-01 00:00:00'),(10000008,5,'Standard',15.00,12.00,200,'2024-06-01 00:00:00','2024-07-10 00:00:00'),(10000009,6,'Regular',5.00,3.00,300,'2024-06-15 00:00:00','2024-07-30 00:00:00'),(10000010,6,'VIP',20.00,18.00,50,'2024-07-01 00:00:00','2024-07-30 00:00:00'),(10000011,7,'General',50.00,45.00,100,'2024-08-01 00:00:00','2024-09-05 00:00:00'),(10000012,7,'Student',40.00,35.00,100,'2024-08-01 00:00:00','2024-09-05 00:00:00'),(10000078,32,'General',12.00,10.00,122,'2024-06-05 00:00:00','2024-06-07 00:00:00'),(10000079,52,'General',12.00,12.00,12,'2024-06-10 00:00:00','2024-06-11 00:00:00'),(10000080,52,'VIP',20.00,20.00,1,'2024-06-16 00:00:00','2024-06-17 00:30:00'),(10000081,52,'Silver',11.00,11.00,2,'2024-06-17 00:00:00','2024-06-18 00:30:00'),(10000083,54,'General',0.00,0.00,40,'2024-06-16 12:00:00','2024-06-30 12:00:00'),(10000085,53,'General',1211.00,1200.00,121,'2024-06-11 00:00:00','2024-06-12 00:00:00'),(10000086,62,'General',23.00,16.00,1,'2024-06-21 21:45:00','2024-06-22 21:45:00'),(10000088,64,'Student',243.00,324.00,3242,'2024-06-21 23:11:00','2024-06-22 23:11:00');
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(10) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `user_email` varchar(39) NOT NULL,
  `user_phone` varchar(11) NOT NULL,
  `user_pwd` varchar(60) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('1221101111','Emma','1221101111@student.mmu.edu.my','0129801231','$2b$12$vG3xp76yDmJJh82b64oGKOWybb.wItBZOKaex2bk.wceJuNCGdoq2'),('1221107001','Amy','1221107001@student.mmu.edu.my','0123334444','$2b$12$H3/2kFd24eDytd.3r9F6X.5Hf6ABtAjUUgZQnZYIt6HKH9B2IUkdy'),('1221107002','Mary','1221107002@student.mmu.edu.my','0178910112','$2b$12$qrMiNPOzlTUnptvHyjDhuuabsZ64of4AY042//91Fitl/H.kY.cyC'),('1221107111','Ali','1221107111@student.mmu.edu.my','0129801231','$2b$12$8OkERj9dNucRobF1P8rUrehg/NSK8e0wJg02C.jTIOdY7UxNvJOgG'),('1221107555','Patrick','1221107555@student.mmu.edu.my','0112233444','$2b$12$EFP/zrDUNUDKBRXS9gjcyOYIsnCnIXP9JljD6EnleHhwhEyGjSMMG'),('1221108011','Wendy','1221108011@student.mmu.edu.my','0124456667','$2b$12$LAaMh9htXhXmNz5vPhGDtehF03cc5DoT2VXSYDozTFZgeJeY2fNB6'),('1221108222','pioyi','1221108222@student.mmu.edu.my','0129801231','$2b$12$p3vngwvnLPg/es/DZB0eB.sszBWugNhTcVkagM8H3ZqODjiQ5rbaK'),('1221108678','John','1221108678@student.mmu.edu.my','0121234567','$2b$12$vCYbXg5Mnl05cCqtjfcDMeV2UnKEdGJS3.ODO.0d/bryO2liv4MUW'),('1221109001','Ken','1221109001@student.mmu.edu.my','0129801231','$2b$12$/SLes6I4zzAGwyC93m0/sO3Nmdt5dPxEc6dszDQR8znCD9jNI0UBe'),('1221109333','Caroline','1221109333@student.mmu.edu.my','0175678910','$2b$12$eQ3pMkXr9UPsam0GzASGBOuwMMVOGHv4AMCji7P1xvlqwICuIwiVW'),('1221109456','Jack','1221109456@student.mmu.edu.my','0123478299','$2b$12$zsk7Jay6c1H6woEy9Ibzq.bP7SjCXCobbcbB9w59xB2n5PtTPo.ey'),('1221111111','Lili','1221111111@student.mmu.edu.my','0129801231','$2b$12$yUC97TRSdcucEIv95tJBU.P4T7aNqpCZyoa5RzQrpSDKjbbsisJeC'),('1222323232','Barbie','1222323232@student.mmu.edu.my','0123456789','$2b$12$1AJGDI7F90B6iWqrK9hocezklB22Ks8jFd62NK2V25kjkOeM8bwTe');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_order`
--

DROP TABLE IF EXISTS `user_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_order` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `ticket_id` int NOT NULL,
  `order_date` datetime NOT NULL,
  `order_quantity` int NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `invoice` varchar(255) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  KEY `ticket_id_idx` (`ticket_id`),
  CONSTRAINT `ticket_id` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`),
  CONSTRAINT `user_order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_order`
--

LOCK TABLES `user_order` WRITE;
/*!40000 ALTER TABLE `user_order` DISABLE KEYS */;
INSERT INTO `user_order` VALUES (1,'1221107001',10000002,'2024-04-11 19:08:39',1,23.00,'5cb3282fd9'),(2,'1221107002',10000001,'2024-04-12 11:06:30',1,20.00,'a6e8a7bf3b'),(5,'1221108678',10000006,'2024-05-19 18:42:52',1,0.00,'Free'),(6,'1221107001',10000080,'2024-06-17 18:42:52',1,20.00,'928ebhbds1'),(7,'1221109001',10000006,'2024-05-19 18:42:52',1,0.00,'Free'),(14,'1221109001',10000083,'2024-06-22 15:35:28',1,0.00,'Free');
/*!40000 ALTER TABLE `user_order` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-22 19:52:18
