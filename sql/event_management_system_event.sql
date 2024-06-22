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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-22 14:38:28
