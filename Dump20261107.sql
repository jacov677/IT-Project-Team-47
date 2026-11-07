-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: wil_placement_management
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `accounts_coordinator`
--

DROP TABLE IF EXISTS `accounts_coordinator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_coordinator` (
  `coordinator_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `department` varchar(120) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`coordinator_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_coordinator_user_id_6fea830b_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_coordinator`
--

LOCK TABLES `accounts_coordinator` WRITE;
/*!40000 ALTER TABLE `accounts_coordinator` DISABLE KEYS */;
INSERT INTO `accounts_coordinator` VALUES (1,'','','','2026-11-06 21:44:37.054431',3),(2,'','','','2026-11-06 21:44:37.065799',4),(3,'Amanda','Naidoo','IT','2026-11-07 21:12:56.535022',15),(4,'Sibusiso','Mkhize','IT','2026-11-07 21:12:56.951145',16),(5,'Priya','Pillay','IT','2026-11-07 21:12:57.364973',17);
/*!40000 ALTER TABLE `accounts_coordinator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_employerprofile`
--

DROP TABLE IF EXISTS `accounts_employerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_employerprofile` (
  `employer_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `contact_number` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `organisation_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_employerpro_organisation_id_a14f7e50_fk_organisat` (`organisation_id`),
  CONSTRAINT `accounts_employerpro_organisation_id_a14f7e50_fk_organisat` FOREIGN KEY (`organisation_id`) REFERENCES `organisations_hostorganization` (`organisation_id`),
  CONSTRAINT `accounts_employerprofile_user_id_90741f2a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_employerprofile`
--

LOCK TABLES `accounts_employerprofile` WRITE;
/*!40000 ALTER TABLE `accounts_employerprofile` DISABLE KEYS */;
INSERT INTO `accounts_employerprofile` VALUES (1,'Percy','Mthembu','HR Manager','','2026-11-07 21:13:00.677322',1,21),(2,'Emma','Williams','HR Manager','','2026-11-07 21:13:01.093991',2,22),(3,'David','Brown','HR Manager','','2026-11-07 21:13:01.510495',3,23),(4,'Zinhle','Ngcobo','HR Manager','','2026-11-07 21:13:01.923063',4,24),(5,'Mark','Taylor','HR Manager','','2026-11-07 21:13:02.336978',5,25);
/*!40000 ALTER TABLE `accounts_employerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_mentor`
--

DROP TABLE IF EXISTS `accounts_mentor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_mentor` (
  `mentor_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `contact_number` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `organisation_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`mentor_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_mentor_organisation_id_d459fe56_fk_organisat` (`organisation_id`),
  CONSTRAINT `accounts_mentor_organisation_id_d459fe56_fk_organisat` FOREIGN KEY (`organisation_id`) REFERENCES `organisations_hostorganization` (`organisation_id`),
  CONSTRAINT `accounts_mentor_user_id_200b98d0_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_mentor`
--

LOCK TABLES `accounts_mentor` WRITE;
/*!40000 ALTER TABLE `accounts_mentor` DISABLE KEYS */;
INSERT INTO `accounts_mentor` VALUES (1,'','','','','2026-11-06 22:05:19.433249',1,5),(2,'','','','','2026-11-06 22:05:19.453478',2,6),(3,'John','Smith','Senior Developer','0820000000','2026-11-07 21:12:59.426262',3,18),(4,'Lerato','Molefe','Senior Developer','0820000000','2026-11-07 21:12:59.839956',4,19),(5,'Kyle','Peters','Senior Developer','0820000000','2026-11-07 21:13:00.263708',5,20);
/*!40000 ALTER TABLE `accounts_mentor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_student`
--

DROP TABLE IF EXISTS `accounts_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_student` (
  `student_number` varchar(30) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `qualification` varchar(120) NOT NULL,
  `contact_number` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`student_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_student_user_id_683c461a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_student`
--

LOCK TABLES `accounts_student` WRITE;
/*!40000 ALTER TABLE `accounts_student` DISABLE KEYS */;
INSERT INTO `accounts_student` VALUES ('STU2026001','','','','','2026-11-06 22:17:45.664772',7),('STU2026002','','','','','2026-11-06 22:17:45.679998',8),('STU2026003','','','','','2026-11-06 22:17:45.701950',9),('STU2026004','','','','','2026-11-06 22:17:45.723157',10),('STU2026005','','','','','2026-11-06 22:17:45.743184',11),('STU2026006','Thabiso','Molefe','Diploma in IT','0820000006','2026-11-07 21:13:06.857762',26),('STU2026007','Nomusa','Dlamini','Diploma in Software Development','0820000007','2026-11-07 21:13:07.272391',27),('STU2026008','Kabelo','Mokoena','Diploma in IT','0820000008','2026-11-07 21:13:07.684491',28),('STU2026009','Fatima','Ahmed','Diploma in Networking','0820000009','2026-11-07 21:13:08.107250',29),('STU2026010','Sanele','Ngubane','Diploma in IT','0820000010','2026-11-07 21:13:08.523523',30);
/*!40000 ALTER TABLE `accounts_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `accounts_user_email_b2644a56_uniq` (`email`),
  KEY `accounts_user_role_57e97df0` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (3,'pbkdf2_sha256$1000000$s4eJyXhxENcNc41gLe7Q7t$loMLPsJKOiNc65iiUxItQEtTJgO+GenkLfb0fqTSlZg=',NULL,0,'thandi@test.co.za','Thandi','Mokoena','thandi@test.co.za',0,1,'2026-11-06 21:44:37.037879','2026-11-06 21:44:37.038429','COORDINATOR','2026-11-07 21:12:55.198453'),(4,'pbkdf2_sha256$1000000$ZVqSxr7hO1lJ2dlp1iemxI$AEfInWxPMYT6jlD4k0ur9DHPZ7CRYs79rymE8Q+ygTA=',NULL,0,'nkule@test.co.za','Nkule','Zuma','nkule@test.co.za',0,1,'2026-11-06 21:44:37.059912','2026-11-06 21:44:37.060143','COORDINATOR','2026-11-07 21:12:56.075019'),(5,'pbkdf2_sha256$1000000$tQCwUQ5ePG4BDJRQfvsR30$ADVjszASPQ6tUgydQgS2g3EyvvSMshSs5RB/iDSJ2fs=',NULL,0,'sipho@test.co.za','Sipho','Dube','sipho@test.co.za',0,1,'2026-11-06 21:44:37.070382','2026-11-06 21:44:37.070584','MENTOR','2026-11-07 21:12:58.186356'),(6,'pbkdf2_sha256$1000000$F5YZiwzDQ6zbaQv643fNeE$rXtgcdFck2g/qwnSfzyGynG6k9sOo4t7QiLaRPqEapU=',NULL,0,'naledi@test.co.za','Naledi','Khumalo','naledi@test.co.za',0,1,'2026-11-06 22:05:19.443589','2026-11-06 22:05:19.444172','MENTOR','2026-11-07 21:12:59.006585'),(7,'pbkdf2_sha256$1000000$q8ll8cHVqVDlblsRCd25AY$KzPFadqPw+5r8kxTOFCFPCxooXK3lP7kZJbizkr29Fk=',NULL,0,'ayesha@test.co.za','Ayesha','Khan','ayesha@test.co.za',0,1,'2026-11-06 22:05:19.461856','2026-11-06 22:05:19.462249','STUDENT','2026-11-07 21:13:03.157584'),(8,'pbkdf2_sha256$1000000$S6QN94b4rIXKuwojy4EbfG$u5+c6POM/ovfe/c7WrqLbcVuUeUjl+N4pBP4aWl2Fdk=',NULL,0,'lwazi@test.co.za','Lwazi','Ndlovu','lwazi@test.co.za',0,1,'2026-11-06 22:05:19.486078','2026-11-06 22:05:19.486470','STUDENT','2026-11-07 21:13:03.982458'),(9,'pbkdf2_sha256$1000000$M0hkb7EDMx424kEjMBdlu1$KuPzep/VZRE7DG5/NGZ8BvW8Paf9ZQ7XH+KDNHy8R84=',NULL,0,'risto@test.co.za','Mkhayaristo','Cele','risto@test.co.za',0,1,'2026-11-06 22:17:45.690340','2026-11-06 22:17:45.691258','STUDENT','2026-11-07 21:13:04.803784'),(10,'pbkdf2_sha256$1000000$LX47c50rYDzLRmWvV42CXw$NLQ5ZT3a9K5TNhCAgBbGXzqxBJ6722/ajDI+xOOvmWk=',NULL,0,'bongani@test.co.za','Bongani','Zulu','bongani@test.co.za',0,1,'2026-11-06 22:17:45.712637','2026-11-06 22:17:45.713082','STUDENT','2026-11-07 21:13:05.624764'),(11,'pbkdf2_sha256$1000000$ZWsgGHn5jpVlb0I5KlWTnW$F8Gluups5utHHh1QTOAyDwGaA+ZFayTt/XGlOGrQOrM=',NULL,0,'zanele@test.co.za','Zanele','Mthembu','zanele@test.co.za',0,1,'2026-11-06 22:17:45.732629','2026-11-06 22:17:45.733076','STUDENT','2026-11-07 21:13:06.445044'),(14,'pbkdf2_sha256$1000000$5PHt4CcBx6EnpHYHLkI4VD$3T/DXp/2XR470q2W+QmtZip0Gco4uCmJGStEjKaBhgI=',NULL,1,'admin@test.co.za','Admin','User','admin@test.co.za',1,1,'2026-11-07 14:47:18.657467','2026-11-07 14:47:18.657691','ADMIN','2026-11-07 21:12:54.318311'),(15,'pbkdf2_sha256$1000000$PDS99NO5Beupso9Swgj4tY$Kah0rzCBnkf55Ig0aMsvzWZ7qh94jGeW7kxSW87fUoM=',NULL,0,'amanda@test.co.za','Amanda','Naidoo','amanda@test.co.za',0,1,'2026-11-07 21:12:56.077628','2026-11-07 21:12:56.077755','COORDINATOR','2026-11-07 21:12:56.532302'),(16,'pbkdf2_sha256$1000000$vIbFkis3vpj0ulY8qxaGYn$MzZyjg0i6pX68vrDP7rMVG+kNkCqXDqpLj42IUFn93U=',NULL,0,'sibusiso@test.co.za','Sibusiso','Mkhize','sibusiso@test.co.za',0,1,'2026-11-07 21:12:56.536624','2026-11-07 21:12:56.536738','COORDINATOR','2026-11-07 21:12:56.948942'),(17,'pbkdf2_sha256$1000000$227Fh9aYCUfA5UguiWNlYL$r/vzrRpXT5BoUdTJXZUFtK8coNC+fyUADino+L4QAz0=',NULL,0,'priya@test.co.za','Priya','Pillay','priya@test.co.za',0,1,'2026-11-07 21:12:56.952506','2026-11-07 21:12:56.952608','COORDINATOR','2026-11-07 21:12:57.363173'),(18,'pbkdf2_sha256$1000000$MRsOnYOGTCZvoMYxu9KhZo$uBjCaWWV7oBiQHRSL3we67wBDS6GI9KZrqv2IIcta80=',NULL,0,'john@test.co.za','John','Smith','john@test.co.za',0,1,'2026-11-07 21:12:59.009366','2026-11-07 21:12:59.009617','MENTOR','2026-11-07 21:12:59.424256'),(19,'pbkdf2_sha256$1000000$06TwS74BuubTqSfk974Ciy$9P+uu4kAINH97/dpqtRFnzCk1xsUHJnjTWozE2Xja7Q=',NULL,0,'lerato@test.co.za','Lerato','Molefe','lerato@test.co.za',0,1,'2026-11-07 21:12:59.428386','2026-11-07 21:12:59.428498','MENTOR','2026-11-07 21:12:59.838067'),(20,'pbkdf2_sha256$1000000$3ZJwknC0DRQ5maqJpVe1GI$WagZ3W8iOA2FnBl6c3Emc+0L3Ti5ZLDBFKiSnLtJhtY=',NULL,0,'kyle@test.co.za','Kyle','Peters','kyle@test.co.za',0,1,'2026-11-07 21:12:59.842125','2026-11-07 21:12:59.842229','MENTOR','2026-11-07 21:13:00.261881'),(21,'pbkdf2_sha256$1000000$fdbtmbivyzWm6UojEdpz6t$IzXo/qIktbwc4OuD+eBMNezn8sIFTWhdMOTTWaOTrjQ=',NULL,0,'percy@test.co.za','Percy','Mthembu','percy@test.co.za',0,1,'2026-11-07 21:13:00.264968','2026-11-07 21:13:00.265069','EMPLOYER','2026-11-07 21:13:00.674862'),(22,'pbkdf2_sha256$1000000$O7L3C3Secz39EahkT5dBZQ$pBYkK4qtvn1V2De1y6vEbYk8Cc27LdZCfPeIfJfrJWQ=',NULL,0,'emma@test.co.za','Emma','Williams','emma@test.co.za',0,1,'2026-11-07 21:13:00.678608','2026-11-07 21:13:00.678716','EMPLOYER','2026-11-07 21:13:01.089281'),(23,'pbkdf2_sha256$1000000$YRt754vyezf8k6NIm50kt9$Pr4lHGCdUzF/3QWfhPZx/DSVAqbvHlfy/cL4S6cJBC4=',NULL,0,'david@test.co.za','David','Brown','david@test.co.za',0,1,'2026-11-07 21:13:01.095512','2026-11-07 21:13:01.095681','EMPLOYER','2026-11-07 21:13:01.508692'),(24,'pbkdf2_sha256$1000000$cnAP0NEbV6eHFwUaPmX1fa$KhIfmNt+2Jn8YGjKkAp8z2tcgDZd819Lh9FuY/8L4XQ=',NULL,0,'zinhle@test.co.za','Zinhle','Ngcobo','zinhle@test.co.za',0,1,'2026-11-07 21:13:01.511698','2026-11-07 21:13:01.511798','EMPLOYER','2026-11-07 21:13:01.921206'),(25,'pbkdf2_sha256$1000000$0QYpyR5SkG2E8xaP1Hupz5$oCxHij9rfV1OTec5amOOQSBe/XvOPH/zMmtbZjxoddg=',NULL,0,'mark@test.co.za','Mark','Taylor','mark@test.co.za',0,1,'2026-11-07 21:13:01.924727','2026-11-07 21:13:01.924866','EMPLOYER','2026-11-07 21:13:02.335190'),(26,'pbkdf2_sha256$1000000$Vb02LSfgHXRpZaAqFWrgHI$4SIgNS5FTQqlkW2M3Ra9i93lfLMfQZdbk7LzZFEofvM=',NULL,0,'thabiso@test.co.za','Thabiso','Molefe','thabiso@test.co.za',0,1,'2026-11-07 21:13:06.447434','2026-11-07 21:13:06.447543','STUDENT','2026-11-07 21:13:06.855834'),(27,'pbkdf2_sha256$1000000$74K5AbMOWyg1kHWeKCAO3O$6uAig/a2AWN51SAV3pO+48fePiBY8m2h/ucgnagDKck=',NULL,0,'nomusa@test.co.za','Nomusa','Dlamini','nomusa@test.co.za',0,1,'2026-11-07 21:13:06.859528','2026-11-07 21:13:06.859636','STUDENT','2026-11-07 21:13:07.270638'),(28,'pbkdf2_sha256$1000000$SVCFxYh2JV2j7rhEpiiSt4$TBGplvapZ4Oom06hgubn9VI8zsRof9biQ/l2VHa9iv8=',NULL,0,'kabelo@test.co.za','Kabelo','Mokoena','kabelo@test.co.za',0,1,'2026-11-07 21:13:07.273727','2026-11-07 21:13:07.273838','STUDENT','2026-11-07 21:13:07.682550'),(29,'pbkdf2_sha256$1000000$5lwfi0ycGJA6AgDFgQrvzJ$BKSTnKbeHCiwqA1WKI8rKRZARVdzZOhJq6LXF4tcHic=',NULL,0,'fatima@test.co.za','Fatima','Ahmed','fatima@test.co.za',0,1,'2026-11-07 21:13:07.685739','2026-11-07 21:13:07.685848','STUDENT','2026-11-07 21:13:08.105501'),(30,'pbkdf2_sha256$1000000$XHRCV7lFQ7N5kfiCuKhlaJ$TuSB2TV/HeVl+8VETv9oYwANEWNdR5bPK6PKpyay60k=',NULL,0,'sanele@test.co.za','Sanele','Ngubane','sanele@test.co.za',0,1,'2026-11-07 21:13:08.108646','2026-11-07 21:13:08.108754','STUDENT','2026-11-07 21:13:08.521654');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessment`
--

DROP TABLE IF EXISTS `assessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` decimal(5,2) DEFAULT NULL,
  `feedback` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `assessed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `mentor_id` int DEFAULT NULL,
  `placement_id` bigint NOT NULL,
  `student_id` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assessment_mentor_id_2dff3a02_fk_accounts_mentor_mentor_id` (`mentor_id`),
  KEY `assessment_placement_id_948bd152_fk_placement_id` (`placement_id`),
  KEY `assessment_student_id_fe7b9396_fk_accounts_` (`student_id`),
  CONSTRAINT `assessment_mentor_id_2dff3a02_fk_accounts_mentor_mentor_id` FOREIGN KEY (`mentor_id`) REFERENCES `accounts_mentor` (`mentor_id`),
  CONSTRAINT `assessment_placement_id_948bd152_fk_placement_id` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`),
  CONSTRAINT `assessment_student_id_fe7b9396_fk_accounts_` FOREIGN KEY (`student_id`) REFERENCES `accounts_student` (`student_number`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment`
--

LOCK TABLES `assessment` WRITE;
/*!40000 ALTER TABLE `assessment` DISABLE KEYS */;
INSERT INTO `assessment` VALUES (1,80.00,'Good progress for Ayesha','SUBMITTED',NULL,'2026-11-06 22:17:45.857283','2026-11-06 22:17:45.857337',1,1,'STU2026001'),(2,81.00,'Good progress for Lwazi','SUBMITTED',NULL,'2026-11-06 22:22:18.591358','2026-11-06 22:22:18.591409',2,2,'STU2026002'),(3,82.00,'Good progress for Mkhayaristo','SUBMITTED',NULL,'2026-11-06 22:22:18.733893','2026-11-06 22:22:18.733950',1,3,'STU2026003'),(4,83.00,'Good progress for Bongani','SUBMITTED',NULL,'2026-11-06 22:22:18.845892','2026-11-06 22:22:18.845941',2,4,'STU2026004'),(5,84.00,'Good progress for Zanele','SUBMITTED',NULL,'2026-11-06 22:22:18.957789','2026-11-06 22:22:18.957839',1,5,'STU2026005'),(6,82.00,'Good progress for Mkhayaristo','SUBMITTED',NULL,'2026-11-07 21:13:08.561913','2026-11-07 21:13:08.561929',3,6,'STU2026003'),(7,83.00,'Good progress for Bongani','SUBMITTED',NULL,'2026-11-07 21:13:08.583442','2026-11-07 21:13:08.583456',4,7,'STU2026004'),(8,84.00,'Good progress for Zanele','SUBMITTED',NULL,'2026-11-07 21:13:08.603551','2026-11-07 21:13:08.603566',5,8,'STU2026005'),(9,80.00,'Good progress for Thabiso','SUBMITTED',NULL,'2026-11-07 21:13:08.624269','2026-11-07 21:13:08.624285',1,9,'STU2026006'),(10,81.00,'Good progress for Nomusa','SUBMITTED',NULL,'2026-11-07 21:13:08.642632','2026-11-07 21:13:08.642646',2,10,'STU2026007'),(11,82.00,'Good progress for Kabelo','SUBMITTED',NULL,'2026-11-07 21:13:08.660482','2026-11-07 21:13:08.660497',3,11,'STU2026008'),(12,83.00,'Good progress for Fatima','SUBMITTED',NULL,'2026-11-07 21:13:08.679513','2026-11-07 21:13:08.679526',4,12,'STU2026009'),(13,84.00,'Good progress for Sanele','SUBMITTED',NULL,'2026-11-07 21:13:08.698010','2026-11-07 21:13:08.698023',5,13,'STU2026010');
/*!40000 ALTER TABLE `assessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assessment_result`
--

DROP TABLE IF EXISTS `assessment_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assessment_result` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `final_mark` int NOT NULL,
  `outcome` varchar(20) NOT NULL,
  `assessed_at` datetime(6) NOT NULL,
  `coordinator_id` int NOT NULL,
  `placement_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `placement_id` (`placement_id`),
  KEY `assessments_assessme_coordinator_id_2b3a9780_fk_accounts_` (`coordinator_id`),
  CONSTRAINT `assessments_assessme_coordinator_id_2b3a9780_fk_accounts_` FOREIGN KEY (`coordinator_id`) REFERENCES `accounts_coordinator` (`coordinator_id`),
  CONSTRAINT `assessments_assessme_placement_id_6342d6bb_fk_placement` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assessment_result`
--

LOCK TABLES `assessment_result` WRITE;
/*!40000 ALTER TABLE `assessment_result` DISABLE KEYS */;
INSERT INTO `assessment_result` VALUES (1,80,'PASS','2026-11-06 22:22:18.491703',1,1),(2,81,'PASS','2026-11-06 22:22:18.609488',1,2),(3,82,'PASS','2026-11-06 22:22:18.752479',2,3),(4,83,'PASS','2026-11-06 22:22:18.864295',1,4),(5,84,'PASS','2026-11-06 22:22:18.978472',2,5),(6,82,'PASS','2026-11-07 21:13:08.565907',3,6),(7,83,'PASS','2026-11-07 21:13:08.586920',4,7),(8,84,'PASS','2026-11-07 21:13:08.606411',5,8),(9,80,'PASS','2026-11-07 21:13:08.627144',1,9),(10,81,'PASS','2026-11-07 21:13:08.645286',2,10),(11,82,'PASS','2026-11-07 21:13:08.664090',3,11),(12,83,'PASS','2026-11-07 21:13:08.682978',4,12),(13,84,'PASS','2026-11-07 21:13:08.701006',5,13);
/*!40000 ALTER TABLE `assessment_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(50) NOT NULL,
  `table_name` varchar(50) NOT NULL,
  `record_id` int DEFAULT NULL,
  `details` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `audit_log_user_id_a1b3392d_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `audit_log_user_id_a1b3392d_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add coordinator',7,'add_coordinator'),(26,'Can change coordinator',7,'change_coordinator'),(27,'Can delete coordinator',7,'delete_coordinator'),(28,'Can view coordinator',7,'view_coordinator'),(29,'Can add employer profile',8,'add_employerprofile'),(30,'Can change employer profile',8,'change_employerprofile'),(31,'Can delete employer profile',8,'delete_employerprofile'),(32,'Can view employer profile',8,'view_employerprofile'),(33,'Can add mentor',9,'add_mentor'),(34,'Can change mentor',9,'change_mentor'),(35,'Can delete mentor',9,'delete_mentor'),(36,'Can view mentor',9,'view_mentor'),(37,'Can add student',10,'add_student'),(38,'Can change student',10,'change_student'),(39,'Can delete student',10,'delete_student'),(40,'Can view student',10,'view_student'),(41,'Can add host organization',11,'add_hostorganization'),(42,'Can change host organization',11,'change_hostorganization'),(43,'Can delete host organization',11,'delete_hostorganization'),(44,'Can view host organization',11,'view_hostorganization'),(45,'Can add document',12,'add_document'),(46,'Can change document',12,'change_document'),(47,'Can delete document',12,'delete_document'),(48,'Can view document',12,'view_document'),(49,'Can add placement',13,'add_placement'),(50,'Can change placement',13,'change_placement'),(51,'Can delete placement',13,'delete_placement'),(52,'Can view placement',13,'view_placement'),(53,'Can add logbook entry',14,'add_logbookentry'),(54,'Can change logbook entry',14,'change_logbookentry'),(55,'Can delete logbook entry',14,'delete_logbookentry'),(56,'Can view logbook entry',14,'view_logbookentry'),(57,'Can add assessment',15,'add_assessment'),(58,'Can change assessment',15,'change_assessment'),(59,'Can delete assessment',15,'delete_assessment'),(60,'Can view assessment',15,'view_assessment'),(61,'Can add report',16,'add_report'),(62,'Can change report',16,'change_report'),(63,'Can delete report',16,'delete_report'),(64,'Can view report',16,'view_report'),(65,'Can add evaluation',17,'add_evaluation'),(66,'Can change evaluation',17,'change_evaluation'),(67,'Can delete evaluation',17,'delete_evaluation'),(68,'Can view evaluation',17,'view_evaluation'),(69,'Can add assessment result',18,'add_assessmentresult'),(70,'Can change assessment result',18,'change_assessmentresult'),(71,'Can delete assessment result',18,'delete_assessmentresult'),(72,'Can view assessment result',18,'view_assessmentresult'),(73,'Can add audit log',19,'add_auditlog'),(74,'Can change audit log',19,'change_auditlog'),(75,'Can delete audit log',19,'delete_auditlog'),(76,'Can view audit log',19,'view_auditlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (19,'accounts','auditlog'),(7,'accounts','coordinator'),(8,'accounts','employerprofile'),(9,'accounts','mentor'),(10,'accounts','student'),(6,'accounts','user'),(1,'admin','logentry'),(15,'assessments','assessment'),(18,'assessments','assessmentresult'),(17,'assessments','evaluation'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(14,'logbook','logbookentry'),(11,'organisations','hostorganization'),(12,'placements','document'),(13,'placements','placement'),(16,'reports','report'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'organisations','0001_initial','2026-11-04 14:32:39.848826'),(2,'contenttypes','0001_initial','2026-11-04 14:32:39.877917'),(3,'contenttypes','0002_remove_content_type_name','2026-11-04 14:32:39.941995'),(4,'auth','0001_initial','2026-11-04 14:32:40.161191'),(5,'auth','0002_alter_permission_name_max_length','2026-11-04 14:32:40.204759'),(6,'auth','0003_alter_user_email_max_length','2026-11-04 14:32:40.210164'),(7,'auth','0004_alter_user_username_opts','2026-11-04 14:32:40.215481'),(8,'auth','0005_alter_user_last_login_null','2026-11-04 14:32:40.221112'),(9,'auth','0006_require_contenttypes_0002','2026-11-04 14:32:40.224051'),(10,'auth','0007_alter_validators_add_error_messages','2026-11-04 14:32:40.229860'),(11,'auth','0008_alter_user_username_max_length','2026-11-04 14:32:40.235209'),(12,'auth','0009_alter_user_last_name_max_length','2026-11-04 14:32:40.241204'),(13,'auth','0010_alter_group_name_max_length','2026-11-04 14:32:40.258740'),(14,'auth','0011_update_proxy_permissions','2026-11-04 14:32:40.265195'),(15,'auth','0012_alter_user_first_name_max_length','2026-11-04 14:32:40.271549'),(16,'accounts','0001_initial','2026-11-04 14:32:40.500058'),(17,'accounts','0002_user_created_at_user_role_user_updated_at_and_more','2026-11-04 14:32:41.048143'),(18,'admin','0001_initial','2026-11-04 14:32:41.168064'),(19,'admin','0002_logentry_remove_auto_add','2026-11-04 14:32:41.187040'),(20,'admin','0003_logentry_add_action_flag_choices','2026-11-04 14:32:41.200620'),(21,'sessions','0001_initial','2026-11-04 14:32:41.231865'),(22,'accounts','0003_alter_user_created_at','2026-11-05 08:07:17.414863'),(23,'placements','0001_initial','2026-11-05 12:20:10.686428'),(24,'logbook','0001_initial','2026-11-05 12:30:21.504762'),(25,'placements','0002_rename_doc_type_document_document_type_and_more','2026-11-05 16:49:10.940536'),(26,'assessments','0001_initial','2026-11-05 16:56:30.307557'),(27,'reports','0001_initial','2026-11-05 17:09:05.928988'),(28,'assessments','0002_assessmentresult_evaluation','2026-11-05 20:51:34.225287'),(29,'accounts','0004_auditlog','2026-11-05 21:00:55.300430'),(30,'assessments','0003_alter_assessmentresult_coordinator_and_more','2026-11-06 22:20:25.270112');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `document_type` varchar(20) NOT NULL,
  `file_path` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `placement_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `document_placement_id_9873ca60_fk_placement_id` (`placement_id`),
  CONSTRAINT `document_placement_id_9873ca60_fk_placement_id` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
INSERT INTO `document` VALUES (1,'CV - Ayesha','CV','placement_documents/cv.txt','2026-11-06 22:17:45.774417',1),(2,'Contract - Ayesha','CONTRACT','','2026-11-06 22:17:45.801438',1),(3,'CV - Lwazi','CV','placement_documents/cv_Ku67af1.txt','2026-11-06 22:22:18.527232',2),(4,'Contract - Lwazi','CONTRACT','','2026-11-06 22:22:18.547641',2),(5,'CV - Mkhayaristo','CV','placement_documents/cv_WgvYXek.txt','2026-11-06 22:22:18.670151',3),(6,'Contract - Mkhayaristo','CONTRACT','','2026-11-06 22:22:18.689756',3),(7,'CV - Bongani','CV','placement_documents/cv_NtIrbA4.txt','2026-11-06 22:22:18.785780',4),(8,'Contract - Bongani','CONTRACT','','2026-11-06 22:22:18.804950',4),(9,'CV - Zanele','CV','placement_documents/cv_eYFc94y.txt','2026-11-06 22:22:18.898177',5),(10,'Contract - Zanele','CONTRACT','','2026-11-06 22:22:18.917967',5),(11,'CV - Mkhayaristo','CV','placement_documents/cv_iEn7z7B.txt','2026-11-07 21:13:08.549990',6),(12,'Contract - Mkhayaristo','CONTRACT','','2026-11-07 21:13:08.554140',6),(13,'CV - Bongani','CV','placement_documents/cv_ZoTdznY.txt','2026-11-07 21:13:08.572550',7),(14,'Contract - Bongani','CONTRACT','','2026-11-07 21:13:08.576273',7),(15,'CV - Zanele','CV','placement_documents/cv_zbF1ozz.txt','2026-11-07 21:13:08.593492',8),(16,'Contract - Zanele','CONTRACT','','2026-11-07 21:13:08.596998',8),(17,'CV - Thabiso','CV','placement_documents/cv_qu0WZW2.txt','2026-11-07 21:13:08.613383',9),(18,'Contract - Thabiso','CONTRACT','','2026-11-07 21:13:08.617186',9),(19,'CV - Nomusa','CV','placement_documents/cv_sCAWCgg.txt','2026-11-07 21:13:08.632241',10),(20,'Contract - Nomusa','CONTRACT','','2026-11-07 21:13:08.636177',10),(21,'CV - Kabelo','CV','placement_documents/cv_GsrsB0C.txt','2026-11-07 21:13:08.650170',11),(22,'Contract - Kabelo','CONTRACT','','2026-11-07 21:13:08.653751',11),(23,'CV - Fatima','CV','placement_documents/cv_1o5bTUQ.txt','2026-11-07 21:13:08.669533',12),(24,'Contract - Fatima','CONTRACT','','2026-11-07 21:13:08.673300',12),(25,'CV - Sanele','CV','placement_documents/cv_KM0iglb.txt','2026-11-07 21:13:08.688368',13),(26,'Contract - Sanele','CONTRACT','','2026-11-07 21:13:08.691848',13);
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS `evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` int NOT NULL,
  `feedback` longtext NOT NULL,
  `evaluation_date` date NOT NULL,
  `mentor_id` int NOT NULL,
  `placement_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assessments_evaluati_mentor_id_a7826a38_fk_accounts_` (`mentor_id`),
  KEY `assessments_evaluation_placement_id_290215f3_fk_placement_id` (`placement_id`),
  CONSTRAINT `assessments_evaluati_mentor_id_a7826a38_fk_accounts_` FOREIGN KEY (`mentor_id`) REFERENCES `accounts_mentor` (`mentor_id`),
  CONSTRAINT `assessments_evaluation_placement_id_290215f3_fk_placement_id` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation`
--

LOCK TABLES `evaluation` WRITE;
/*!40000 ALTER TABLE `evaluation` DISABLE KEYS */;
INSERT INTO `evaluation` VALUES (1,80,'Strong work ethic','2026-11-07',1,1),(2,81,'Strong work ethic','2026-11-07',2,2),(3,82,'Strong work ethic','2026-11-07',1,3),(4,83,'Strong work ethic','2026-11-07',2,4),(5,84,'Strong work ethic','2026-11-07',1,5),(6,82,'Strong work ethic','2026-11-07',3,6),(7,83,'Strong work ethic','2026-11-07',4,7),(8,84,'Strong work ethic','2026-11-07',5,8),(9,80,'Strong work ethic','2026-11-07',1,9),(10,81,'Strong work ethic','2026-11-07',2,10),(11,82,'Strong work ethic','2026-11-07',3,11),(12,83,'Strong work ethic','2026-11-07',4,12),(13,84,'Strong work ethic','2026-11-07',5,13);
/*!40000 ALTER TABLE `evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logbook_entry`
--

DROP TABLE IF EXISTS `logbook_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logbook_entry` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `hours_worked` decimal(4,2) NOT NULL,
  `activities` longtext NOT NULL,
  `skills_learned` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `mentor_feedback` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `placement_id` bigint NOT NULL,
  `student_id` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logbook_entry_placement_id_c90db175_fk_placement_id` (`placement_id`),
  KEY `logbook_entry_student_id_b378bc83_fk_accounts_` (`student_id`),
  CONSTRAINT `logbook_entry_placement_id_c90db175_fk_placement_id` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`),
  CONSTRAINT `logbook_entry_student_id_b378bc83_fk_accounts_` FOREIGN KEY (`student_id`) REFERENCES `accounts_student` (`student_number`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logbook_entry`
--

LOCK TABLES `logbook_entry` WRITE;
/*!40000 ALTER TABLE `logbook_entry` DISABLE KEYS */;
INSERT INTO `logbook_entry` VALUES (1,'2026-11-07',8.00,'Day 1: Worked on Software Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','DRAFT','','2026-11-06 22:17:45.818422','2026-11-06 22:17:45.818478',1,'STU2026001'),(2,'2026-11-06',8.00,'Day 2: Worked on Software Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:17:45.831533','2026-11-06 22:17:45.831601',1,'STU2026001'),(3,'2026-11-05',8.00,'Day 3: Worked on Software Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:17:45.843409','2026-11-06 22:17:45.843460',1,'STU2026001'),(4,'2026-11-07',8.00,'Day 1: Worked on IT Support Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','DRAFT','','2026-11-06 22:22:18.557682','2026-11-06 22:22:18.557728',2,'STU2026002'),(5,'2026-11-06',8.00,'Day 2: Worked on IT Support Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.568413','2026-11-06 22:22:18.568461',2,'STU2026002'),(6,'2026-11-05',8.00,'Day 3: Worked on IT Support Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.581103','2026-11-06 22:22:18.581168',2,'STU2026002'),(7,'2026-11-07',8.00,'Day 1: Worked on Data Analyst Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','DRAFT','','2026-11-06 22:22:18.701079','2026-11-06 22:22:18.701129',3,'STU2026003'),(8,'2026-11-06',8.00,'Day 2: Worked on Data Analyst Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.711647','2026-11-06 22:22:18.711702',3,'STU2026003'),(9,'2026-11-05',8.00,'Day 3: Worked on Data Analyst Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.723285','2026-11-06 22:22:18.723334',3,'STU2026003'),(10,'2026-11-07',8.00,'Day 1: Worked on Network Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','DRAFT','','2026-11-06 22:22:18.814958','2026-11-06 22:22:18.815006',4,'STU2026004'),(11,'2026-11-06',8.00,'Day 2: Worked on Network Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.825726','2026-11-06 22:22:18.825772',4,'STU2026004'),(12,'2026-11-05',8.00,'Day 3: Worked on Network Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.835851','2026-11-06 22:22:18.835899',4,'STU2026004'),(13,'2026-11-07',8.00,'Day 1: Worked on Web Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','DRAFT','','2026-11-06 22:22:18.927212','2026-11-06 22:22:18.927257',5,'STU2026005'),(14,'2026-11-06',8.00,'Day 2: Worked on Web Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.938011','2026-11-06 22:22:18.938056',5,'STU2026005'),(15,'2026-11-05',8.00,'Day 3: Worked on Web Dev Intern tasks, standup, fixed bugs','Django, MySQL, Teamwork','SUBMITTED','','2026-11-06 22:22:18.947850','2026-11-06 22:22:18.947925',5,'STU2026005'),(16,'2026-11-07',8.00,'Day 1: Worked on Data Analyst Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.556182','2026-11-07 21:13:08.556195',6,'STU2026003'),(17,'2026-11-06',8.00,'Day 2: Worked on Data Analyst Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.557971','2026-11-07 21:13:08.557984',6,'STU2026003'),(18,'2026-11-05',8.00,'Day 3: Worked on Data Analyst Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.559672','2026-11-07 21:13:08.559686',6,'STU2026003'),(19,'2026-11-07',8.00,'Day 1: Worked on Network Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.578160','2026-11-07 21:13:08.578173',7,'STU2026004'),(20,'2026-11-06',8.00,'Day 2: Worked on Network Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.579802','2026-11-07 21:13:08.579842',7,'STU2026004'),(21,'2026-11-05',8.00,'Day 3: Worked on Network Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.581651','2026-11-07 21:13:08.581669',7,'STU2026004'),(22,'2026-11-07',8.00,'Day 1: Worked on Web Dev Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.598726','2026-11-07 21:13:08.598741',8,'STU2026005'),(23,'2026-11-06',8.00,'Day 2: Worked on Web Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.600397','2026-11-07 21:13:08.600410',8,'STU2026005'),(24,'2026-11-05',8.00,'Day 3: Worked on Web Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.601985','2026-11-07 21:13:08.601998',8,'STU2026005'),(25,'2026-11-07',8.00,'Day 1: Worked on Backend Dev Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.618826','2026-11-07 21:13:08.618839',9,'STU2026006'),(26,'2026-11-06',8.00,'Day 2: Worked on Backend Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.620652','2026-11-07 21:13:08.620667',9,'STU2026006'),(27,'2026-11-05',8.00,'Day 3: Worked on Backend Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.622530','2026-11-07 21:13:08.622545',9,'STU2026006'),(28,'2026-11-07',8.00,'Day 1: Worked on Frontend Dev Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.637652','2026-11-07 21:13:08.637664',10,'STU2026007'),(29,'2026-11-06',8.00,'Day 2: Worked on Frontend Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.639302','2026-11-07 21:13:08.639317',10,'STU2026007'),(30,'2026-11-05',8.00,'Day 3: Worked on Frontend Dev Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.641191','2026-11-07 21:13:08.641204',10,'STU2026007'),(31,'2026-11-07',8.00,'Day 1: Worked on Cloud Support Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.655391','2026-11-07 21:13:08.655407',11,'STU2026008'),(32,'2026-11-06',8.00,'Day 2: Worked on Cloud Support Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.657195','2026-11-07 21:13:08.657209',11,'STU2026008'),(33,'2026-11-05',8.00,'Day 3: Worked on Cloud Support Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.658882','2026-11-07 21:13:08.658895',11,'STU2026008'),(34,'2026-11-07',8.00,'Day 1: Worked on QA Testing Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.674941','2026-11-07 21:13:08.674954',12,'STU2026009'),(35,'2026-11-06',8.00,'Day 2: Worked on QA Testing Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.676496','2026-11-07 21:13:08.676510',12,'STU2026009'),(36,'2026-11-05',8.00,'Day 3: Worked on QA Testing Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.678035','2026-11-07 21:13:08.678047',12,'STU2026009'),(37,'2026-11-07',8.00,'Day 1: Worked on Cyber Security Intern tasks','Django, MySQL, Teamwork','DRAFT','','2026-11-07 21:13:08.693288','2026-11-07 21:13:08.693300',13,'STU2026010'),(38,'2026-11-06',8.00,'Day 2: Worked on Cyber Security Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.694898','2026-11-07 21:13:08.694911',13,'STU2026010'),(39,'2026-11-05',8.00,'Day 3: Worked on Cyber Security Intern tasks','Django, MySQL, Teamwork','SUBMITTED','','2026-11-07 21:13:08.696544','2026-11-07 21:13:08.696557',13,'STU2026010');
/*!40000 ALTER TABLE `logbook_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organisations_hostorganization`
--

DROP TABLE IF EXISTS `organisations_hostorganization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organisations_hostorganization` (
  `organisation_id` int NOT NULL AUTO_INCREMENT,
  `organisation_name` varchar(150) NOT NULL,
  `registration_number` varchar(80) DEFAULT NULL,
  `industry` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `contact_email` varchar(150) NOT NULL,
  `contact_number` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`organisation_id`),
  UNIQUE KEY `registration_number` (`registration_number`),
  KEY `org_name_idx` (`organisation_name`),
  KEY `org_industry_idx` (`industry`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organisations_hostorganization`
--

LOCK TABLES `organisations_hostorganization` WRITE;
/*!40000 ALTER TABLE `organisations_hostorganization` DISABLE KEYS */;
INSERT INTO `organisations_hostorganization` VALUES (1,'Tech Solutions Durban',NULL,'','','','',1,'2026-11-06 22:05:19.383578','2026-11-06 22:05:19.383694'),(2,'EThekwini Municipality IT',NULL,'','','','',1,'2026-11-06 22:05:19.396476','2026-11-06 22:05:19.396531'),(3,'Nedbank Tech Hub',NULL,'','','','',1,'2026-11-06 22:05:19.408737','2026-11-06 22:05:19.408793'),(4,'DUT Innovation Hub',NULL,'IT','Durban','info@test.co.za','',1,'2026-11-07 21:12:53.883297','2026-11-07 21:12:53.883347'),(5,'Capitec Durban Tech',NULL,'IT','Durban','info@test.co.za','',1,'2026-11-07 21:12:53.886940','2026-11-07 21:12:53.886957');
/*!40000 ALTER TABLE `organisations_hostorganization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `placement`
--

DROP TABLE IF EXISTS `placement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `placement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `coordinator_id` int DEFAULT NULL,
  `mentor_id` int DEFAULT NULL,
  `organisation_id` int NOT NULL,
  `student_id` varchar(30) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `placement_coordinator_id_84d876c1_fk_accounts_` (`coordinator_id`),
  KEY `placement_mentor_id_14a0a206_fk_accounts_mentor_mentor_id` (`mentor_id`),
  KEY `placement_organisation_id_c45dfdf2_fk_organisat` (`organisation_id`),
  KEY `placement_student_id_fecaec5c_fk_accounts_student_student_number` (`student_id`),
  CONSTRAINT `placement_coordinator_id_84d876c1_fk_accounts_` FOREIGN KEY (`coordinator_id`) REFERENCES `accounts_coordinator` (`coordinator_id`),
  CONSTRAINT `placement_mentor_id_14a0a206_fk_accounts_mentor_mentor_id` FOREIGN KEY (`mentor_id`) REFERENCES `accounts_mentor` (`mentor_id`),
  CONSTRAINT `placement_organisation_id_c45dfdf2_fk_organisat` FOREIGN KEY (`organisation_id`) REFERENCES `organisations_hostorganization` (`organisation_id`),
  CONSTRAINT `placement_student_id_fecaec5c_fk_accounts_student_student_number` FOREIGN KEY (`student_id`) REFERENCES `accounts_student` (`student_number`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placement`
--

LOCK TABLES `placement` WRITE;
/*!40000 ALTER TABLE `placement` DISABLE KEYS */;
INSERT INTO `placement` VALUES (1,'Software Dev Intern','WIL Placement - Software Dev Intern','2026-10-08','2027-04-06','APPROVED','2026-11-06 22:17:45.758165','2026-11-06 22:17:45.758195',1,1,1,'STU2026001','2026-11-06 22:17:45.749679'),(2,'IT Support Intern','WIL Placement - IT Support Intern','2026-10-08','2027-04-06','ACTIVE','2026-11-06 22:22:18.515256','2026-11-06 22:22:18.515283',1,2,2,'STU2026002','2026-11-06 22:22:18.510067'),(3,'Data Analyst Intern','WIL Placement - Data Analyst Intern','2026-10-08','2027-04-06','PENDING','2026-11-06 22:22:18.657163','2026-11-06 22:22:18.657208',2,1,1,'STU2026003',NULL),(4,'Network Intern','WIL Placement - Network Intern','2026-10-08','2027-04-06','COMPLETED','2026-11-06 22:22:18.773474','2026-11-06 22:22:18.773503',1,2,3,'STU2026004','2026-11-06 22:22:18.768947'),(5,'Web Dev Intern','WIL Placement - Web Dev Intern','2026-10-08','2027-04-06','ACTIVE','2026-11-06 22:22:18.887160','2026-11-06 22:22:18.887187',2,1,2,'STU2026005','2026-11-06 22:22:18.882124'),(6,'Data Analyst Intern','WIL Placement - Data Analyst Intern','2026-10-08','2027-04-06','PENDING','2026-11-07 21:13:08.546884','2026-11-07 21:13:08.546901',3,3,3,'STU2026003',NULL),(7,'Network Intern','WIL Placement - Network Intern','2026-10-08','2027-04-06','COMPLETED','2026-11-07 21:13:08.569673','2026-11-07 21:13:08.569680',4,4,4,'STU2026004','2026-11-07 21:13:08.568392'),(8,'Web Dev Intern','WIL Placement - Web Dev Intern','2026-10-08','2027-04-06','ACTIVE','2026-11-07 21:13:08.590754','2026-11-07 21:13:08.590763',5,5,5,'STU2026005','2026-11-07 21:13:08.589225'),(9,'Backend Dev Intern','WIL Placement - Backend Dev Intern','2026-10-08','2027-04-06','APPROVED','2026-11-07 21:13:08.611762','2026-11-07 21:13:08.611770',1,1,1,'STU2026006','2026-11-07 21:13:08.610425'),(10,'Frontend Dev Intern','WIL Placement - Frontend Dev Intern','2026-10-08','2027-04-06','ACTIVE','2026-11-07 21:13:08.630464','2026-11-07 21:13:08.630471',2,2,2,'STU2026007','2026-11-07 21:13:08.629336'),(11,'Cloud Support Intern','WIL Placement - Cloud Support Intern','2026-10-08','2027-04-06','PENDING','2026-11-07 21:13:08.648506','2026-11-07 21:13:08.648520',3,3,3,'STU2026008',NULL),(12,'QA Testing Intern','WIL Placement - QA Testing Intern','2026-10-08','2027-04-06','COMPLETED','2026-11-07 21:13:08.668018','2026-11-07 21:13:08.668025',4,4,4,'STU2026009','2026-11-07 21:13:08.666656'),(13,'Cyber Security Intern','WIL Placement - Cyber Security Intern','2026-10-08','2027-04-06','ACTIVE','2026-11-07 21:13:08.686690','2026-11-07 21:13:08.686697',5,5,5,'STU2026010','2026-11-07 21:13:08.685570');
/*!40000 ALTER TABLE `placement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `summary` longtext NOT NULL,
  `file_path` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `coordinator_id` int DEFAULT NULL,
  `placement_id` bigint NOT NULL,
  `student_id` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_coordinator_id_2e4b1fcc_fk_accounts_` (`coordinator_id`),
  KEY `report_placement_id_86eb0419_fk_placement_id` (`placement_id`),
  KEY `report_student_id_c0e9dc01_fk_accounts_student_student_number` (`student_id`),
  CONSTRAINT `report_coordinator_id_2e4b1fcc_fk_accounts_` FOREIGN KEY (`coordinator_id`) REFERENCES `accounts_coordinator` (`coordinator_id`),
  CONSTRAINT `report_placement_id_86eb0419_fk_placement_id` FOREIGN KEY (`placement_id`) REFERENCES `placement` (`id`),
  CONSTRAINT `report_student_id_c0e9dc01_fk_accounts_student_student_number` FOREIGN KEY (`student_id`) REFERENCES `accounts_student` (`student_number`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,'Software Dev Intern - Final Report','PLACEMENT','Report for Ayesha at Tech Solutions Durban - APPROVED','','SUBMITTED',NULL,'2026-11-06 22:22:18.504434','2026-11-06 22:22:18.504495',1,1,'STU2026001'),(2,'IT Support Intern - Final Report','PLACEMENT','Report for Lwazi at EThekwini Municipality IT - ACTIVE','','SUBMITTED',NULL,'2026-11-06 22:22:18.620632','2026-11-06 22:22:18.620704',1,2,'STU2026002'),(3,'Data Analyst Intern - Final Report','PLACEMENT','Report for Mkhayaristo at Tech Solutions Durban - PENDING','','SUBMITTED',NULL,'2026-11-06 22:22:18.762102','2026-11-06 22:22:18.762158',2,3,'STU2026003'),(4,'Network Intern - Final Report','PLACEMENT','Report for Bongani at Nedbank Tech Hub - COMPLETED','','SUBMITTED',NULL,'2026-11-06 22:22:18.876237','2026-11-06 22:22:18.876286',1,4,'STU2026004'),(5,'Web Dev Intern - Final Report','PLACEMENT','Report for Zanele at EThekwini Municipality IT - ACTIVE','','SUBMITTED',NULL,'2026-11-06 22:22:18.988108','2026-11-06 22:22:18.988158',2,5,'STU2026005'),(6,'Data Analyst Intern - Final Report','PLACEMENT','Report for Mkhayaristo at Nedbank Tech Hub','','SUBMITTED',NULL,'2026-11-07 21:13:08.567880','2026-11-07 21:13:08.567895',3,6,'STU2026003'),(7,'Network Intern - Final Report','PLACEMENT','Report for Bongani at DUT Innovation Hub','','SUBMITTED',NULL,'2026-11-07 21:13:08.588654','2026-11-07 21:13:08.588669',4,7,'STU2026004'),(8,'Web Dev Intern - Final Report','PLACEMENT','Report for Zanele at Capitec Durban Tech','','SUBMITTED',NULL,'2026-11-07 21:13:08.609769','2026-11-07 21:13:08.609787',5,8,'STU2026005'),(9,'Backend Dev Intern - Final Report','PLACEMENT','Report for Thabiso at Tech Solutions Durban','','SUBMITTED',NULL,'2026-11-07 21:13:08.628790','2026-11-07 21:13:08.628806',1,9,'STU2026006'),(10,'Frontend Dev Intern - Final Report','PLACEMENT','Report for Nomusa at EThekwini Municipality IT','','SUBMITTED',NULL,'2026-11-07 21:13:08.646798','2026-11-07 21:13:08.646812',2,10,'STU2026007'),(11,'Cloud Support Intern - Final Report','PLACEMENT','Report for Kabelo at Nedbank Tech Hub','','SUBMITTED',NULL,'2026-11-07 21:13:08.666129','2026-11-07 21:13:08.666145',3,11,'STU2026008'),(12,'QA Testing Intern - Final Report','PLACEMENT','Report for Fatima at DUT Innovation Hub','','SUBMITTED',NULL,'2026-11-07 21:13:08.685007','2026-11-07 21:13:08.685022',4,12,'STU2026009'),(13,'Cyber Security Intern - Final Report','PLACEMENT','Report for Sanele at Capitec Durban Tech','','SUBMITTED',NULL,'2026-11-07 21:13:08.702573','2026-11-07 21:13:08.702588',5,13,'STU2026010');
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-07 23:50:32
