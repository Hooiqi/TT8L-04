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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-22 14:38:29
