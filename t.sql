-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: databaseDemo2
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (7,'分析结果管理_一般'),(8,'分析结果管理_高级'),(5,'实验项目信息管理_一般'),(6,'实验项目信息管理_高级'),(9,'所有模块_一般'),(10,'所有模块_高级'),(3,'样本库信息管理_一般'),(4,'样本库信息管理_高级'),(1,'病历信息管理_一般'),(2,'病历信息管理_高级');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=384 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,17),(2,1,18),(3,1,19),(4,1,20),(9,1,61),(10,1,62),(11,1,63),(12,1,64),(13,1,67),(14,1,68),(15,1,69),(16,1,70),(17,1,73),(18,1,74),(19,1,75),(20,1,76),(21,1,79),(22,1,80),(23,1,81),(24,1,82),(25,1,85),(26,1,86),(27,1,87),(28,1,88),(5,1,145),(6,1,146),(7,1,147),(8,1,148),(29,2,17),(30,2,18),(31,2,19),(32,2,20),(41,2,61),(42,2,62),(43,2,63),(44,2,64),(45,2,65),(46,2,66),(47,2,67),(48,2,68),(49,2,69),(50,2,70),(51,2,71),(52,2,72),(53,2,73),(54,2,74),(55,2,75),(56,2,76),(57,2,77),(58,2,78),(59,2,79),(60,2,80),(61,2,81),(62,2,82),(63,2,83),(64,2,84),(65,2,85),(66,2,86),(67,2,87),(68,2,88),(69,2,89),(70,2,90),(33,2,145),(34,2,146),(35,2,147),(36,2,148),(37,2,153),(38,2,154),(39,2,155),(40,2,156),(71,3,17),(72,3,18),(73,3,19),(74,3,20),(79,3,91),(80,3,92),(81,3,93),(82,3,94),(83,3,97),(84,3,98),(85,3,99),(86,3,100),(87,3,103),(88,3,104),(89,3,105),(90,3,106),(91,3,109),(92,3,110),(93,3,111),(94,3,112),(75,3,145),(76,3,146),(77,3,147),(78,3,148),(95,4,17),(96,4,18),(97,4,19),(98,4,20),(107,4,91),(108,4,92),(109,4,93),(110,4,94),(111,4,95),(112,4,96),(113,4,97),(114,4,98),(115,4,99),(116,4,100),(117,4,101),(118,4,102),(119,4,103),(120,4,104),(121,4,105),(122,4,106),(123,4,107),(124,4,108),(125,4,109),(126,4,110),(127,4,111),(128,4,112),(129,4,113),(130,4,114),(99,4,145),(100,4,146),(101,4,147),(102,4,148),(103,4,153),(104,4,154),(105,4,155),(106,4,156),(137,5,17),(138,5,18),(143,5,19),(144,5,20),(139,5,115),(140,5,116),(141,5,117),(142,5,118),(145,5,121),(146,5,122),(147,5,123),(148,5,124),(150,5,127),(131,5,128),(132,5,129),(133,5,130),(134,5,145),(136,5,146),(135,5,147),(149,5,148),(156,6,17),(157,6,18),(158,6,19),(159,6,20),(168,6,115),(169,6,116),(170,6,117),(171,6,118),(172,6,119),(173,6,120),(174,6,121),(175,6,122),(176,6,123),(177,6,124),(178,6,125),(179,6,126),(180,6,127),(151,6,128),(152,6,129),(153,6,130),(154,6,131),(155,6,132),(160,6,145),(161,6,146),(162,6,147),(163,6,148),(164,6,153),(165,6,154),(166,6,155),(167,6,156),(189,7,17),(190,7,18),(191,7,19),(192,7,20),(181,7,133),(182,7,134),(183,7,135),(184,7,136),(185,7,139),(186,7,140),(187,7,141),(188,7,142),(193,7,145),(194,7,146),(195,7,147),(196,7,148),(381,7,157),(209,8,17),(210,8,18),(211,8,19),(212,8,20),(197,8,133),(198,8,134),(199,8,135),(200,8,136),(201,8,137),(202,8,138),(203,8,139),(204,8,140),(205,8,141),(206,8,142),(207,8,143),(208,8,144),(213,8,145),(214,8,146),(215,8,147),(216,8,148),(217,8,153),(218,8,154),(219,8,155),(220,8,156),(382,8,157),(232,9,17),(233,9,18),(234,9,19),(235,9,20),(240,9,61),(241,9,62),(242,9,63),(243,9,64),(244,9,67),(245,9,68),(246,9,69),(247,9,70),(248,9,73),(249,9,74),(250,9,75),(251,9,76),(252,9,79),(253,9,80),(254,9,81),(255,9,82),(256,9,85),(257,9,86),(258,9,87),(259,9,88),(260,9,91),(261,9,92),(262,9,93),(263,9,94),(264,9,97),(265,9,98),(266,9,99),(267,9,100),(268,9,103),(269,9,104),(270,9,105),(271,9,106),(272,9,109),(273,9,110),(274,9,111),(275,9,112),(276,9,115),(277,9,116),(278,9,117),(279,9,118),(280,9,121),(281,9,122),(282,9,123),(283,9,124),(284,9,127),(221,9,128),(222,9,129),(223,9,130),(224,9,133),(225,9,134),(226,9,135),(227,9,136),(228,9,139),(229,9,140),(230,9,141),(231,9,142),(236,9,145),(237,9,146),(238,9,147),(239,9,148),(383,9,157),(285,10,17),(286,10,18),(287,10,19),(288,10,20),(289,10,61),(290,10,62),(291,10,63),(292,10,64),(293,10,65),(294,10,66),(295,10,67),(296,10,68),(297,10,69),(298,10,70),(299,10,71),(300,10,72),(301,10,73),(302,10,74),(303,10,75),(304,10,76),(305,10,77),(306,10,78),(307,10,79),(308,10,80),(309,10,81),(310,10,82),(311,10,83),(312,10,84),(313,10,85),(314,10,86),(315,10,87),(316,10,88),(317,10,89),(318,10,90),(319,10,91),(320,10,92),(321,10,93),(322,10,94),(323,10,95),(324,10,96),(325,10,97),(326,10,98),(327,10,99),(328,10,100),(329,10,101),(330,10,102),(331,10,103),(332,10,104),(333,10,105),(334,10,106),(335,10,107),(336,10,108),(337,10,109),(338,10,110),(339,10,111),(340,10,112),(341,10,113),(342,10,114),(343,10,115),(344,10,116),(345,10,117),(346,10,118),(347,10,119),(348,10,120),(349,10,121),(350,10,122),(351,10,123),(352,10,124),(353,10,125),(354,10,126),(355,10,127),(356,10,128),(357,10,129),(358,10,130),(359,10,131),(360,10,132),(361,10,133),(362,10,134),(363,10,135),(364,10,136),(365,10,137),(366,10,138),(367,10,139),(368,10,140),(369,10,141),(370,10,142),(371,10,143),(372,10,144),(373,10,145),(374,10,146),(375,10,147),(376,10,148),(377,10,153),(378,10,154),(379,10,155),(380,10,156);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add crontab',6,'add_crontabschedule'),(22,'Can change crontab',6,'change_crontabschedule'),(23,'Can delete crontab',6,'delete_crontabschedule'),(24,'Can view crontab',6,'view_crontabschedule'),(25,'Can add interval',7,'add_intervalschedule'),(26,'Can change interval',7,'change_intervalschedule'),(27,'Can delete interval',7,'delete_intervalschedule'),(28,'Can view interval',7,'view_intervalschedule'),(29,'Can add periodic task',8,'add_periodictask'),(30,'Can change periodic task',8,'change_periodictask'),(31,'Can delete periodic task',8,'delete_periodictask'),(32,'Can view periodic task',8,'view_periodictask'),(33,'Can add periodic tasks',9,'add_periodictasks'),(34,'Can change periodic tasks',9,'change_periodictasks'),(35,'Can delete periodic tasks',9,'delete_periodictasks'),(36,'Can view periodic tasks',9,'view_periodictasks'),(37,'Can add task state',10,'add_taskmeta'),(38,'Can change task state',10,'change_taskmeta'),(39,'Can delete task state',10,'delete_taskmeta'),(40,'Can view task state',10,'view_taskmeta'),(41,'Can add saved group result',11,'add_tasksetmeta'),(42,'Can change saved group result',11,'change_tasksetmeta'),(43,'Can delete saved group result',11,'delete_tasksetmeta'),(44,'Can view saved group result',11,'view_tasksetmeta'),(45,'Can add task',12,'add_taskstate'),(46,'Can change task',12,'change_taskstate'),(47,'Can delete task',12,'delete_taskstate'),(48,'Can view task',12,'view_taskstate'),(49,'Can add worker',13,'add_workerstate'),(50,'Can change worker',13,'change_workerstate'),(51,'Can delete worker',13,'delete_workerstate'),(52,'Can view worker',13,'view_workerstate'),(53,'Can add group object permission',14,'add_groupobjectpermission'),(54,'Can change group object permission',14,'change_groupobjectpermission'),(55,'Can delete group object permission',14,'delete_groupobjectpermission'),(56,'Can view group object permission',14,'view_groupobjectpermission'),(57,'Can add user object permission',15,'add_userobjectpermission'),(58,'Can change user object permission',15,'change_userobjectpermission'),(59,'Can delete user object permission',15,'delete_userobjectpermission'),(60,'Can view user object permission',15,'view_userobjectpermission'),(61,'Can add 基本临床信息表',16,'add_clinicalinfo'),(62,'Can change 基本临床信息表',16,'change_clinicalinfo'),(63,'Can delete 基本临床信息表',16,'delete_clinicalinfo'),(64,'Can view 基本临床信息表',16,'view_clinicalinfo'),(65,'Can bulk delete 基本临床信息表',16,'bulk_delete_ClinicalInfo'),(66,'Can bulk update 基本临床信息表',16,'bulk_update_ClinicalInfo'),(67,'Can add 随访信息表',17,'add_followupinfo'),(68,'Can change 随访信息表',17,'change_followupinfo'),(69,'Can delete 随访信息表',17,'delete_followupinfo'),(70,'Can view 随访信息表',17,'view_followupinfo'),(71,'Can bulk delete 随访信息表',17,'bulk_delete_FollowupInfo'),(72,'Can bulk update 随访信息表',17,'bulk_update_FollowupInfo'),(73,'Can add 肝癌生化检测结果信息表',18,'add_liverbiocheminfo'),(74,'Can change 肝癌生化检测结果信息表',18,'change_liverbiocheminfo'),(75,'Can delete 肝癌生化检测结果信息表',18,'delete_liverbiocheminfo'),(76,'Can view 肝癌生化检测结果信息表',18,'view_liverbiocheminfo'),(77,'Can bulk delete 肝癌生化检测结果信息表',18,'bulk_delete_LiverBiochemInfo'),(78,'Can bulk update 肝癌生化检测结果信息表',18,'bulk_update_LiverBiochemInfo'),(79,'Can add 肝癌病理报告信息表',19,'add_liverpathologicalinfo'),(80,'Can change 肝癌病理报告信息表',19,'change_liverpathologicalinfo'),(81,'Can delete 肝癌病理报告信息表',19,'delete_liverpathologicalinfo'),(82,'Can view 肝癌病理报告信息表',19,'view_liverpathologicalinfo'),(83,'Can bulk delete 肝癌病理报告信息表',19,'bulk_delete_LiverPathologicalInfo'),(84,'Can bulk update 肝癌病理报告信息表',19,'bulk_update_LiverPathologicalInfo'),(85,'Can add 肝癌肿瘤标志物检测结果信息表',20,'add_livertmdinfo'),(86,'Can change 肝癌肿瘤标志物检测结果信息表',20,'change_livertmdinfo'),(87,'Can delete 肝癌肿瘤标志物检测结果信息表',20,'delete_livertmdinfo'),(88,'Can view 肝癌肿瘤标志物检测结果信息表',20,'view_livertmdinfo'),(89,'Can bulk delete 肝癌肿瘤标志物检测结果信息表',20,'bulk_delete_LiverTMDInfo'),(90,'Can bulk update 肝癌肿瘤标志物检测结果信息表',20,'bulk_update_LiverTMDInfo'),(91,'Can add 样本核酸使用记录表',21,'add_dnausagerecordinfo'),(92,'Can change 样本核酸使用记录表',21,'change_dnausagerecordinfo'),(93,'Can delete 样本核酸使用记录表',21,'delete_dnausagerecordinfo'),(94,'Can view 样本核酸使用记录表',21,'view_dnausagerecordinfo'),(95,'Can bulk delete 样本核酸使用记录表',21,'bulk_delete_DNAUsageRecordInfo'),(96,'Can bulk update 样本核酸使用记录表',21,'bulk_update_DNAUsageRecordInfo'),(97,'Can add 样本提取表',22,'add_extractinfo'),(98,'Can change 样本提取表',22,'change_extractinfo'),(99,'Can delete 样本提取表',22,'delete_extractinfo'),(100,'Can view 样本提取表',22,'view_extractinfo'),(101,'Can bulk delete 样本提取表',22,'bulk_delete_ExtractInfo'),(102,'Can bulk update 样本提取表',22,'bulk_update_ExtractInfo'),(103,'Can add 样本信息表',23,'add_sampleinfo'),(104,'Can change 样本信息表',23,'change_sampleinfo'),(105,'Can delete 样本信息表',23,'delete_sampleinfo'),(106,'Can view 样本信息表',23,'view_sampleinfo'),(107,'Can bulk delete 样本信息表',23,'bulk_delete_SampleInfo'),(108,'Can bulk update 样本信息表',23,'bulk_update_SampleInfo'),(109,'Can add 样本库存信息表',24,'add_sampleinventoryinfo'),(110,'Can change 样本库存信息表',24,'change_sampleinventoryinfo'),(111,'Can delete 样本库存信息表',24,'delete_sampleinventoryinfo'),(112,'Can view 样本库存信息表',24,'view_sampleinventoryinfo'),(113,'Can bulk delete 样本库存信息表',24,'bulk_delete_SampleInventoryInfo'),(114,'Can bulk update 样本库存信息表',24,'bulk_update_SampleInventoryInfo'),(115,'Can add 甲基化捕获文库信息表',25,'add_methycaptureinfo'),(116,'Can change 甲基化捕获文库信息表',25,'change_methycaptureinfo'),(117,'Can delete 甲基化捕获文库信息表',25,'delete_methycaptureinfo'),(118,'Can view 甲基化捕获文库信息表',25,'view_methycaptureinfo'),(119,'Can bulk delete 甲基化捕获文库信息表',25,'bulk_delete_MethyCaptureInfo'),(120,'Can bulk update 甲基化捕获文库信息表',25,'bulk_update_MethyCaptureInfo'),(121,'Can add 甲基化建库表',26,'add_methylibraryinfo'),(122,'Can change 甲基化建库表',26,'change_methylibraryinfo'),(123,'Can delete 甲基化建库表',26,'delete_methylibraryinfo'),(124,'Can view 甲基化建库表',26,'view_methylibraryinfo'),(125,'Can bulk delete 甲基化建库表',26,'bulk_delete_MethyLibraryInfo'),(126,'Can bulk update 甲基化建库表',26,'bulk_update_MethyLibraryInfo'),(127,'Can add 甲基化pooling表',27,'add_methypoolinginfo'),(128,'Can change 甲基化pooling表',27,'change_methypoolinginfo'),(129,'Can delete 甲基化pooling表',27,'delete_methypoolinginfo'),(130,'Can view 甲基化pooling表',27,'view_methypoolinginfo'),(131,'Can bulk delete 甲基化pooling表',27,'bulk_delete_MethyPoolingInfo'),(132,'Can bulk update 甲基化pooling表',27,'bulk_update_MethyPoolingInfo'),(133,'Can add 样本甲基化检测测序质控表',28,'add_methyqcinfo'),(134,'Can change 样本甲基化检测测序质控表',28,'change_methyqcinfo'),(135,'Can delete 样本甲基化检测测序质控表',28,'delete_methyqcinfo'),(136,'Can view 样本甲基化检测测序质控表',28,'view_methyqcinfo'),(137,'Can bulk delete 样本甲基化检测测序质控表',28,'bulk_delete_SequencingInfo'),(138,'Can bulk update 样本甲基化检测测序质控表',28,'bulk_update_SequencingInfo'),(139,'Can add 测序登记表',29,'add_sequencinginfo'),(140,'Can change 测序登记表',29,'change_sequencinginfo'),(141,'Can delete 测序登记表',29,'delete_sequencinginfo'),(142,'Can view 测序登记表',29,'view_sequencinginfo'),(143,'Can bulk delete 测序登记表',29,'bulk_delete_SequencingInfo'),(144,'Can bulk update 测序登记表',29,'bulk_update_SequencingInfo'),(145,'Can add 数据库增删改记录表',30,'add_databaserecord'),(146,'Can change 数据库增删改记录表',30,'change_databaserecord'),(147,'Can delete 数据库增删改记录表',30,'delete_databaserecord'),(148,'Can view 数据库增删改记录表',30,'view_databaserecord'),(149,'Can add 用户',31,'add_userinfo'),(150,'Can change 用户',31,'change_userinfo'),(151,'Can delete 用户',31,'delete_userinfo'),(152,'Can view 用户',31,'view_userinfo'),(153,'Can add 上传文件信息表',32,'add_uploadfile'),(154,'Can change 上传文件信息表',32,'change_uploadfile'),(155,'Can delete 上传文件信息表',32,'delete_uploadfile'),(156,'Can view 上传文件信息表',32,'view_uploadfile'),(157,'Can access 高级功能',32,'access_Advance');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_hidden_23fd02dc` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_hidden_593cfc24` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_用户信息表_index` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_用户信息表_index` FOREIGN KEY (`user_id`) REFERENCES `用户信息表` (`index`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2020-07-02 03:19:27.634903','1','病历信息管理_一般',1,'[{\"added\": {}}]',3,3),(2,'2020-07-02 03:20:00.755886','2','病历信息管理_高级',1,'[{\"added\": {}}]',3,3),(3,'2020-07-02 03:20:55.286455','3','样本库信息管理_一般',1,'[{\"added\": {}}]',3,3),(4,'2020-07-02 03:21:18.518246','4','样本库信息管理_高级',1,'[{\"added\": {}}]',3,3),(5,'2020-07-02 03:22:05.598799','5','实验项目信息管理_一般',1,'[{\"added\": {}}]',3,3),(6,'2020-07-02 03:22:46.258596','6','实验项目信息管理_高级',1,'[{\"added\": {}}]',3,3),(7,'2020-07-02 03:23:45.704427','7','分析结果管理_一般',1,'[{\"added\": {}}]',3,3),(8,'2020-07-02 03:24:08.910748','8','分析结果管理_高级',1,'[{\"added\": {}}]',3,3),(9,'2020-07-02 03:26:06.442588','9','所有模块_一般',1,'[{\"added\": {}}]',3,3),(10,'2020-07-02 03:26:42.910799','10','所有模块_高级',1,'[{\"added\": {}}]',3,3),(11,'2020-07-02 03:55:05.325092','7','分析结果管理_一般',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,3),(12,'2020-07-02 03:55:14.596776','8','分析结果管理_高级',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,3),(13,'2020-07-02 09:50:37.623743','9','所有模块_一般',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,3);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(32,'ADVANCE','uploadfile'),(3,'auth','group'),(2,'auth','permission'),(21,'BIS','dnausagerecordinfo'),(22,'BIS','extractinfo'),(23,'BIS','sampleinfo'),(24,'BIS','sampleinventoryinfo'),(4,'contenttypes','contenttype'),(6,'djcelery','crontabschedule'),(7,'djcelery','intervalschedule'),(8,'djcelery','periodictask'),(9,'djcelery','periodictasks'),(10,'djcelery','taskmeta'),(11,'djcelery','tasksetmeta'),(12,'djcelery','taskstate'),(13,'djcelery','workerstate'),(16,'EMR','clinicalinfo'),(17,'EMR','followupinfo'),(18,'EMR','liverbiocheminfo'),(19,'EMR','liverpathologicalinfo'),(20,'EMR','livertmdinfo'),(14,'guardian','groupobjectpermission'),(15,'guardian','userobjectpermission'),(25,'LIMS','methycaptureinfo'),(26,'LIMS','methylibraryinfo'),(27,'LIMS','methypoolinginfo'),(28,'SEQ','methyqcinfo'),(29,'SEQ','sequencinginfo'),(5,'sessions','session'),(30,'USER','databaserecord'),(31,'USER','userinfo');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'ADVANCE','0001_initial','2020-07-02 03:14:01.113342'),(2,'BIS','0001_initial','2020-07-02 03:14:01.377942'),(3,'BIS','0002_auto_20200701_1417','2020-07-02 03:14:01.399608'),(4,'BIS','0003_auto_20200702_1100','2020-07-02 03:14:01.420627'),(5,'BIS','0004_auto_20200702_1112','2020-07-02 03:14:01.440892'),(6,'EMR','0001_initial','2020-07-02 03:14:01.595304'),(7,'EMR','0002_auto_20200701_1417','2020-07-02 03:14:01.830994'),(8,'EMR','0003_auto_20200702_1100','2020-07-02 03:14:01.887195'),(9,'EMR','0004_auto_20200702_1112','2020-07-02 03:14:01.941867'),(10,'LIMS','0001_initial','2020-07-02 03:14:02.029401'),(11,'LIMS','0002_auto_20200701_1417','2020-07-02 03:14:02.205005'),(12,'LIMS','0003_auto_20200702_1100','2020-07-02 03:14:02.239624'),(13,'LIMS','0004_auto_20200702_1112','2020-07-02 03:14:02.276097'),(14,'SEQ','0001_initial','2020-07-02 03:14:02.578601'),(15,'SEQ','0002_auto_20200701_1417','2020-07-02 03:14:02.751599'),(16,'SEQ','0003_auto_20200702_1100','2020-07-02 03:14:02.778906'),(17,'SEQ','0004_auto_20200702_1112','2020-07-02 03:14:02.809308'),(18,'contenttypes','0001_initial','2020-07-02 03:14:02.831887'),(19,'contenttypes','0002_remove_content_type_name','2020-07-02 03:14:02.876233'),(20,'auth','0001_initial','2020-07-02 03:14:02.913495'),(21,'auth','0002_alter_permission_name_max_length','2020-07-02 03:14:02.987163'),(22,'auth','0003_alter_user_email_max_length','2020-07-02 03:14:02.993974'),(23,'auth','0004_alter_user_username_opts','2020-07-02 03:14:03.000817'),(24,'auth','0005_alter_user_last_login_null','2020-07-02 03:14:03.009089'),(25,'auth','0006_require_contenttypes_0002','2020-07-02 03:14:03.011519'),(26,'auth','0007_alter_validators_add_error_messages','2020-07-02 03:14:03.017990'),(27,'auth','0008_alter_user_username_max_length','2020-07-02 03:14:03.025042'),(28,'auth','0009_alter_user_last_name_max_length','2020-07-02 03:14:03.032067'),(29,'USER','0001_initial','2020-07-02 03:14:03.107339'),(30,'USER','0002_auto_20200701_1906','2020-07-02 03:14:03.184180'),(31,'USER','0003_auto_20200701_1923','2020-07-02 03:14:03.193943'),(32,'USER','0004_auto_20200701_1943','2020-07-02 03:14:03.221045'),(33,'USER','0005_auto_20200701_2020','2020-07-02 03:14:03.229958'),(34,'USER','0006_auto_20200702_0926','2020-07-02 03:14:03.291769'),(35,'admin','0001_initial','2020-07-02 03:14:03.316348'),(36,'admin','0002_logentry_remove_auto_add','2020-07-02 03:14:03.359776'),(37,'admin','0003_logentry_add_action_flag_choices','2020-07-02 03:14:03.373791'),(38,'auth','0010_alter_group_name_max_length','2020-07-02 03:14:03.391559'),(39,'auth','0011_update_proxy_permissions','2020-07-02 03:14:03.422539'),(40,'djcelery','0001_initial','2020-07-02 03:14:03.557520'),(41,'guardian','0001_initial','2020-07-02 03:14:03.703050'),(42,'guardian','0002_generic_permissions_index','2020-07-02 03:14:03.838873'),(43,'sessions','0001_initial','2020-07-02 03:14:03.850940'),(44,'ADVANCE','0002_auto_20200702_1154','2020-07-02 03:54:25.139235'),(45,'USER','0007_auto_20200703_1800','2020-07-03 10:01:01.228501');
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
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` (`crontab_id`),
  KEY `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` (`interval_id`),
  CONSTRAINT `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`),
  CONSTRAINT `djcelery_periodictask_chk_1` CHECK ((`total_run_count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime(6) NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime(6) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` (`worker_id`),
  KEY `djcelery_taskstate_state_53543be4` (`state`),
  KEY `djcelery_taskstate_name_8af9eded` (`name`),
  KEY `djcelery_taskstate_tstamp_4c3f93a1` (`tstamp`),
  KEY `djcelery_taskstate_hidden_c3905e57` (`hidden`),
  CONSTRAINT `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_last_heartbeat_4539b544` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_groupobjectpermission`
--

DROP TABLE IF EXISTS `guardian_groupobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardian_groupobjectpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_pk` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guardian_groupobjectperm_group_id_permission_id_o_3f189f7c_uniq` (`group_id`,`permission_id`,`object_pk`),
  KEY `guardian_groupobject_permission_id_36572738_fk_auth_perm` (`permission_id`),
  KEY `guardian_gr_content_ae6aec_idx` (`content_type_id`,`object_pk`),
  CONSTRAINT `guardian_groupobject_content_type_id_7ade36b8_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `guardian_groupobject_group_id_4bbbfb62_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `guardian_groupobject_permission_id_36572738_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_groupobjectpermission`
--

LOCK TABLES `guardian_groupobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_userobjectpermission`
--

DROP TABLE IF EXISTS `guardian_userobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardian_userobjectpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_pk` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guardian_userobjectpermi_user_id_permission_id_ob_b0b3d2fc_uniq` (`user_id`,`permission_id`,`object_pk`),
  KEY `guardian_userobjectp_permission_id_71807bfc_fk_auth_perm` (`permission_id`),
  KEY `guardian_us_content_179ed2_idx` (`content_type_id`,`object_pk`),
  CONSTRAINT `guardian_userobjectp_content_type_id_2e892405_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `guardian_userobjectp_permission_id_71807bfc_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `guardian_userobjectpermission_user_id_d5c1e964_fk_用户信息表_index` FOREIGN KEY (`user_id`) REFERENCES `用户信息表` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_userobjectpermission`
--

LOCK TABLES `guardian_userobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_userobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_userobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `上传文件信息表`
--

DROP TABLE IF EXISTS `上传文件信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `上传文件信息表` (
  `上传文件` varchar(100) DEFAULT NULL,
  `项目` varchar(35) NOT NULL,
  `上传者` varchar(35) DEFAULT NULL,
  `上传时间` datetime(6) NOT NULL,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `上传文件信息表`
--

LOCK TABLES `上传文件信息表` WRITE;
/*!40000 ALTER TABLE `上传文件信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `上传文件信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `基本临床信息表`
--

DROP TABLE IF EXISTS `基本临床信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `基本临床信息表` (
  `病理编号` varchar(35) DEFAULT NULL,
  `住院号` varchar(35) DEFAULT NULL,
  `医院编号` varchar(50) DEFAULT NULL,
  `科室` varchar(50) DEFAULT NULL,
  `姓名` varchar(35) DEFAULT NULL,
  `性别` varchar(2) DEFAULT NULL,
  `年龄` int(11) DEFAULT NULL,
  `记录日期` date DEFAULT NULL,
  `肿瘤类型` varchar(50) DEFAULT NULL,
  `分化程度` varchar(15) DEFAULT NULL,
  `肿瘤1直径` double DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `病理编号` (`病理编号`),
  KEY `基本临床信息表_患者编号_5904fad1_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `基本临床信息表_患者编号_5904fad1_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `基本临床信息表`
--

LOCK TABLES `基本临床信息表` WRITE;
/*!40000 ALTER TABLE `基本临床信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `基本临床信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `数据库增删改记录表`
--

DROP TABLE IF EXISTS `数据库增删改记录表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `数据库增删改记录表` (
  `被变更的模型` varchar(35) DEFAULT NULL,
  `操作` varchar(25) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `用户index` int(11) DEFAULT NULL,
  PRIMARY KEY (`index`),
  KEY `数据库增删改记录表_用户index_c1bd8bfe_fk_用户信息表_index` (`用户index`),
  CONSTRAINT `数据库增删改记录表_用户index_c1bd8bfe_fk_用户信息表_index` FOREIGN KEY (`用户index`) REFERENCES `用户信息表` (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `数据库增删改记录表`
--

LOCK TABLES `数据库增删改记录表` WRITE;
/*!40000 ALTER TABLE `数据库增删改记录表` DISABLE KEYS */;
INSERT INTO `数据库增删改记录表` VALUES ('UserInfo','注册','create_time: 2020-07-02 03:32:17.700633+00:00; role: 4',1,'2020-07-02 03:32:17.710355','2020-07-02 03:32:17.710380',NULL),('User','激活成功','无',2,'2020-07-02 03:33:16.481126','2020-07-02 03:33:16.481154',NULL),('UserInfo','修改资料成功','create_time: 2020-07-02 03:16:37.160774+00:00; role: 4',3,'2020-07-02 04:20:50.651683','2020-07-02 04:20:50.651709',NULL),('UserInfo','注册','create_time: 2020-07-03 06:00:29.101514+00:00; role: 4',4,'2020-07-03 06:00:29.117491','2020-07-03 06:00:29.117519',NULL),('User','激活成功','无',5,'2020-07-03 06:01:23.748614','2020-07-03 06:01:23.748651',NULL),('UserInfo','修改资料成功','create_time: 2020-07-03 06:00:29.101514+00:00; role: 4',6,'2020-07-03 09:03:10.917970','2020-07-03 09:03:10.918008',NULL),('UserInfo','修改资料成功','create_time: 2020-07-03 06:00:29.101514+00:00; role: 4',7,'2020-07-03 09:03:14.522276','2020-07-03 09:03:14.522299',NULL),('UserInfo','修改资料成功','create_time: 2020-07-03 06:00:29.101514+00:00; role: 4',8,'2020-07-03 10:02:45.840097','2020-07-03 10:02:45.840122',5),('UserInfo','修改资料成功','create_time: 2020-07-03 06:00:29.101514+00:00; role: 4',9,'2020-07-03 10:02:52.434158','2020-07-03 10:02:52.434185',5);
/*!40000 ALTER TABLE `数据库增删改记录表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `样本信息表`
--

DROP TABLE IF EXISTS `样本信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `样本信息表` (
  `样本编号` varchar(35) DEFAULT NULL,
  `原始样本编号` varchar(50) DEFAULT NULL,
  `冰箱位置` varchar(50) NOT NULL,
  `孔板号` varchar(50) NOT NULL,
  `孔位` varchar(50) NOT NULL,
  `样本类型` varchar(50) NOT NULL,
  `采样日期` date DEFAULT NULL,
  `寄送日期` date DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `样本编号` (`样本编号`),
  KEY `样本信息表_患者编号_86d31585_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `样本信息表_患者编号_86d31585_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `样本信息表`
--

LOCK TABLES `样本信息表` WRITE;
/*!40000 ALTER TABLE `样本信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `样本信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `样本库存信息表`
--

DROP TABLE IF EXISTS `样本库存信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `样本库存信息表` (
  `患者编号` varchar(35) DEFAULT NULL,
  `血浆管数` int(10) unsigned NOT NULL,
  `癌旁组织` int(10) unsigned NOT NULL,
  `癌组织` int(10) unsigned NOT NULL,
  `白细胞` int(10) unsigned NOT NULL,
  `粪便` int(10) unsigned NOT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `患者编号` (`患者编号`),
  CONSTRAINT `样本库存信息表_chk_1` CHECK ((`血浆管数` >= 0)),
  CONSTRAINT `样本库存信息表_chk_2` CHECK ((`癌旁组织` >= 0)),
  CONSTRAINT `样本库存信息表_chk_3` CHECK ((`癌组织` >= 0)),
  CONSTRAINT `样本库存信息表_chk_4` CHECK ((`白细胞` >= 0)),
  CONSTRAINT `样本库存信息表_chk_5` CHECK ((`粪便` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `样本库存信息表`
--

LOCK TABLES `样本库存信息表` WRITE;
/*!40000 ALTER TABLE `样本库存信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `样本库存信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `样本提取表`
--

DROP TABLE IF EXISTS `样本提取表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `样本提取表` (
  `核酸提取编号` varchar(35) NOT NULL,
  `提取日期` date DEFAULT NULL,
  `样本类型` varchar(50) NOT NULL,
  `核酸类型` varchar(50) NOT NULL,
  `样本体积` double DEFAULT NULL,
  `提取方法` varchar(50) DEFAULT NULL,
  `浓度` double DEFAULT NULL,
  `体积` double DEFAULT NULL,
  `冰箱位置` varchar(50) NOT NULL,
  `孔板号` varchar(50) NOT NULL,
  `孔位` varchar(50) NOT NULL,
  `成功建库使用量` double DEFAULT NULL,
  `失败建库使用量` double DEFAULT NULL,
  `科研项目使用量` double DEFAULT NULL,
  `其他使用量` double DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `样本编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `核酸提取编号` (`核酸提取编号`),
  KEY `样本提取表_样本编号_df336c0e_fk_样本信息表_样本编号` (`样本编号`),
  KEY `样本提取表_患者编号_19557bfa_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `样本提取表_患者编号_19557bfa_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `样本提取表_样本编号_df336c0e_fk_样本信息表_样本编号` FOREIGN KEY (`样本编号`) REFERENCES `样本信息表` (`样本编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `样本提取表`
--

LOCK TABLES `样本提取表` WRITE;
/*!40000 ALTER TABLE `样本提取表` DISABLE KEYS */;
/*!40000 ALTER TABLE `样本提取表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `样本核酸使用记录表`
--

DROP TABLE IF EXISTS `样本核酸使用记录表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `样本核酸使用记录表` (
  `使用日期` date DEFAULT NULL,
  `使用量` double DEFAULT NULL,
  `用途` varchar(25) NOT NULL,
  `建库编号` varchar(35) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `核酸提取编号` varchar(35) DEFAULT NULL,
  `样本编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  KEY `样本核酸使用记录表_核酸提取编号_4d003645_fk_样本提取表_核酸提取编号` (`核酸提取编号`),
  KEY `样本核酸使用记录表_样本编号_51a9ba86_fk_样本信息表_样本编号` (`样本编号`),
  KEY `样本核酸使用记录表_患者编号_da4c797a_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `样本核酸使用记录表_患者编号_da4c797a_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `样本核酸使用记录表_样本编号_51a9ba86_fk_样本信息表_样本编号` FOREIGN KEY (`样本编号`) REFERENCES `样本信息表` (`样本编号`),
  CONSTRAINT `样本核酸使用记录表_核酸提取编号_4d003645_fk_样本提取表_核酸提取编号` FOREIGN KEY (`核酸提取编号`) REFERENCES `样本提取表` (`核酸提取编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `样本核酸使用记录表`
--

LOCK TABLES `样本核酸使用记录表` WRITE;
/*!40000 ALTER TABLE `样本核酸使用记录表` DISABLE KEYS */;
/*!40000 ALTER TABLE `样本核酸使用记录表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `样本甲基化检测测序质控表`
--

DROP TABLE IF EXISTS `样本甲基化检测测序质控表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `样本甲基化检测测序质控表` (
  `Sample` varchar(35) DEFAULT NULL,
  `Data_Size-Gb` double DEFAULT NULL,
  `Clean_Rate` double DEFAULT NULL,
  `R1_Q20` double DEFAULT NULL,
  `R2_Q20` double DEFAULT NULL,
  `R1_Q30` double DEFAULT NULL,
  `R2_Q30` double DEFAULT NULL,
  `GC_Content` double DEFAULT NULL,
  `BS_conversion_rate-lambda_DNA` double DEFAULT NULL,
  `BS_conversion_rate-CHH` double DEFAULT NULL,
  `BS_conversion_rate-CHG` double DEFAULT NULL,
  `Uniquely_Paired_Mapping_Rate` double DEFAULT NULL,
  `Mismatch_and_InDel_Rate` double DEFAULT NULL,
  `Mode_Fragment_Length-bp` double DEFAULT NULL,
  `Genome_Duplication_Rate` double DEFAULT NULL,
  `Genome_Depth` double DEFAULT NULL,
  `Genome_Dedupped_Depth` double DEFAULT NULL,
  `Genome_Coverage` double DEFAULT NULL,
  `Genome_4X_CpG_Depth` double DEFAULT NULL,
  `Genome_4X_CpG_Coverage` double DEFAULT NULL,
  `Genome_4X_CpG_methylation_level` double DEFAULT NULL,
  `Panel_4X_CpG_Depth` double DEFAULT NULL,
  `Panel_4X_CpG_Coverage` double DEFAULT NULL,
  `Panel_4X_CpG_methylation_level` double DEFAULT NULL,
  `Panel_Ontarget_Rate-region` double DEFAULT NULL,
  `Panel_Duplication_Rate-region` double DEFAULT NULL,
  `Panel_Depth-site_X` double DEFAULT NULL,
  `Panel_Dedupped_Depth-site_X` double DEFAULT NULL,
  `Panel_Coverage-site_1X` double DEFAULT NULL,
  `Panel_Coverage-site_10X` double DEFAULT NULL,
  `Panel_Coverage-site_20X` double DEFAULT NULL,
  `Panel_Coverage-site_50X` double DEFAULT NULL,
  `Panel_Coverage-site_100X` double DEFAULT NULL,
  `Panel_Uniformity-site_gt0.2mean` double DEFAULT NULL,
  `Strand_balance-F` double DEFAULT NULL,
  `Strand_balance-R` double DEFAULT NULL,
  `GC_bin_depth_ratio` double DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `核酸提取编号` varchar(35) DEFAULT NULL,
  `捕获文库名` varchar(35) DEFAULT NULL,
  `样本编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  `上机文库号` varchar(35) DEFAULT NULL,
  `测序文库名` varchar(35) DEFAULT NULL,
  `建库编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `Sample` (`Sample`),
  KEY `样本甲基化检测测序质控表_上机文库号_a95caecf_fk_测序登记表_上机文库号` (`上机文库号`),
  KEY `样本甲基化检测测序质控表_测序文库名_da313a54_fk_甲基化pooling表_测序文库编号` (`测序文库名`),
  KEY `样本甲基化检测测序质控表_建库编号_4dc472a8_fk_甲基化建库表_建库编号` (`建库编号`),
  KEY `样本甲基化检测测序质控表_核酸提取编号_791d5823_fk_样本提取表_核酸提取编号` (`核酸提取编号`),
  KEY `样本甲基化检测测序质控表_捕获文库名_998dddb7_fk_甲基化捕获文库信息表_捕获文库名` (`捕获文库名`),
  KEY `样本甲基化检测测序质控表_样本编号_6362458c_fk_样本信息表_样本编号` (`样本编号`),
  KEY `样本甲基化检测测序质控表_患者编号_8b52806b_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `样本甲基化检测测序质控表_上机文库号_a95caecf_fk_测序登记表_上机文库号` FOREIGN KEY (`上机文库号`) REFERENCES `测序登记表` (`上机文库号`),
  CONSTRAINT `样本甲基化检测测序质控表_建库编号_4dc472a8_fk_甲基化建库表_建库编号` FOREIGN KEY (`建库编号`) REFERENCES `甲基化建库表` (`建库编号`),
  CONSTRAINT `样本甲基化检测测序质控表_患者编号_8b52806b_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `样本甲基化检测测序质控表_捕获文库名_998dddb7_fk_甲基化捕获文库信息表_捕获文库名` FOREIGN KEY (`捕获文库名`) REFERENCES `甲基化捕获文库信息表` (`捕获文库名`),
  CONSTRAINT `样本甲基化检测测序质控表_样本编号_6362458c_fk_样本信息表_样本编号` FOREIGN KEY (`样本编号`) REFERENCES `样本信息表` (`样本编号`),
  CONSTRAINT `样本甲基化检测测序质控表_核酸提取编号_791d5823_fk_样本提取表_核酸提取编号` FOREIGN KEY (`核酸提取编号`) REFERENCES `样本提取表` (`核酸提取编号`),
  CONSTRAINT `样本甲基化检测测序质控表_测序文库名_da313a54_fk_甲基化pooling表_测序文库编号` FOREIGN KEY (`测序文库名`) REFERENCES `甲基化pooling表` (`测序文库编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `样本甲基化检测测序质控表`
--

LOCK TABLES `样本甲基化检测测序质控表` WRITE;
/*!40000 ALTER TABLE `样本甲基化检测测序质控表` DISABLE KEYS */;
/*!40000 ALTER TABLE `样本甲基化检测测序质控表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `测序登记表`
--

DROP TABLE IF EXISTS `测序登记表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `测序登记表` (
  `上机文库号` varchar(35) DEFAULT NULL,
  `送测日期` date DEFAULT NULL,
  `上机时间` date DEFAULT NULL,
  `下机时间` date DEFAULT NULL,
  `机器号` varchar(100) DEFAULT NULL,
  `芯片号` varchar(100) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `上机文库号` (`上机文库号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `测序登记表`
--

LOCK TABLES `测序登记表` WRITE;
/*!40000 ALTER TABLE `测序登记表` DISABLE KEYS */;
/*!40000 ALTER TABLE `测序登记表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `测序登记表_poolingLB_id`
--

DROP TABLE IF EXISTS `测序登记表_poolingLB_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `测序登记表_poolingLB_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sequencinginfo_id` int(11) NOT NULL,
  `methycaptureinfo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `测序登记表_poolingLB_id_sequencinginfo_id_methyc_5425e8ca_uniq` (`sequencinginfo_id`,`methycaptureinfo_id`),
  KEY `测序登记表_poolingLB_id_methycaptureinfo_id_43b76d05_fk_甲基化捕获文库信息` (`methycaptureinfo_id`),
  CONSTRAINT `测序登记表_poolingLB_id_methycaptureinfo_id_43b76d05_fk_甲基化捕获文库信息` FOREIGN KEY (`methycaptureinfo_id`) REFERENCES `甲基化捕获文库信息表` (`index`),
  CONSTRAINT `测序登记表_poolingLB_id_sequencinginfo_id_9605b664_fk_测序登记表_index` FOREIGN KEY (`sequencinginfo_id`) REFERENCES `测序登记表` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `测序登记表_poolingLB_id`
--

LOCK TABLES `测序登记表_poolingLB_id` WRITE;
/*!40000 ALTER TABLE `测序登记表_poolingLB_id` DISABLE KEYS */;
/*!40000 ALTER TABLE `测序登记表_poolingLB_id` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `用户信息表`
--

DROP TABLE IF EXISTS `用户信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `用户信息表` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `昵称` varchar(35) NOT NULL,
  `邮箱` varchar(254) NOT NULL,
  `头像` varchar(100) NOT NULL,
  `角色` smallint(6) NOT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近登录时间` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `昵称` (`昵称`),
  UNIQUE KEY `邮箱` (`邮箱`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `用户信息表`
--

LOCK TABLES `用户信息表` WRITE;
/*!40000 ALTER TABLE `用户信息表` DISABLE KEYS */;
INSERT INTO `用户信息表` VALUES ('!RwnylEXiHI11Wow0KjVzIdYb5WpzSBwXIdhvw8e2',NULL,0,'AnonymousUser','','',0,1,'2020-07-02 03:14:03.952938','匿名用户','none@none.com','avatar/default.jpg',4,NULL,1,'2020-07-02 03:14:03.953760',NULL),('pbkdf2_sha256$180000$TdrsU3kpsEZP$+jEBStFtbSMTZ9/I9cYbspZWa/nsPaklw1Lcp4D5T8k=','2020-07-02 15:38:47.217661',1,'django','','',1,1,'2020-07-02 03:16:37.013200','root','fcdn007@163.com','avatar/king.jpeg',4,'超级管理员',3,'2020-07-02 03:16:37.160774',NULL),('pbkdf2_sha256$180000$0PkpXSn41F0W$J+h0SxadUa8T/Rh+xcc0FrBvDuAHFTHgvHyDE4wjzV0=','2020-07-02 09:50:45.849596',0,'test','','',0,1,'2020-07-02 03:32:17.467919','测试账号','534087069@qq.com','avatar/bug.jpeg',4,'测试账号',4,'2020-07-02 03:32:17.700633',NULL),('pbkdf2_sha256$180000$5ixzguj0hlAy$MfyGvqwuOjAcXj7W3LzecMPBE8Foy8/8ZVQzERi2O60=','2020-07-06 03:48:49.150416',0,'何广良','','',0,1,'2020-07-03 06:00:28.881529','fcdn007','fcdn007@gmail.com','avatar/飞鸟_1.jpeg',4,'无',5,'2020-07-03 06:00:29.101514',NULL);
/*!40000 ALTER TABLE `用户信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `用户信息表_groups`
--

DROP TABLE IF EXISTS `用户信息表_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `用户信息表_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userinfo_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `用户信息表_groups_userinfo_id_group_id_ea7614b2_uniq` (`userinfo_id`,`group_id`),
  KEY `用户信息表_groups_group_id_bdb0e5dd_fk_auth_group_id` (`group_id`),
  CONSTRAINT `用户信息表_groups_group_id_bdb0e5dd_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `用户信息表_groups_userinfo_id_af9663e1_fk_用户信息表_index` FOREIGN KEY (`userinfo_id`) REFERENCES `用户信息表` (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `用户信息表_groups`
--

LOCK TABLES `用户信息表_groups` WRITE;
/*!40000 ALTER TABLE `用户信息表_groups` DISABLE KEYS */;
INSERT INTO `用户信息表_groups` VALUES (1,4,9),(2,5,9);
/*!40000 ALTER TABLE `用户信息表_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `用户信息表_user_permissions`
--

DROP TABLE IF EXISTS `用户信息表_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `用户信息表_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userinfo_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `用户信息表_user_permissions_userinfo_id_permission_id_6a327aaf_uniq` (`userinfo_id`,`permission_id`),
  KEY `用户信息表_user_permissio_permission_id_34ae7a0e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `用户信息表_user_permissio_permission_id_34ae7a0e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `用户信息表_user_permissions_userinfo_id_358788c4_fk_用户信息表_index` FOREIGN KEY (`userinfo_id`) REFERENCES `用户信息表` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `用户信息表_user_permissions`
--

LOCK TABLES `用户信息表_user_permissions` WRITE;
/*!40000 ALTER TABLE `用户信息表_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `用户信息表_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `甲基化pooling表`
--

DROP TABLE IF EXISTS `甲基化pooling表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `甲基化pooling表` (
  `测序文库编号` varchar(35) DEFAULT NULL,
  `pooling比例` double DEFAULT NULL,
  `取样` double DEFAULT NULL,
  `体积` double DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `核酸提取编号` varchar(35) DEFAULT NULL,
  `捕获文库名` varchar(35) DEFAULT NULL,
  `样本编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  `建库编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `测序文库编号` (`测序文库编号`),
  KEY `甲基化pooling表_核酸提取编号_10d91c4c_fk_样本提取表_核酸提取编号` (`核酸提取编号`),
  KEY `甲基化pooling表_捕获文库名_f23f1770_fk_甲基化捕获文库信息表_捕获文库名` (`捕获文库名`),
  KEY `甲基化pooling表_样本编号_83c32a23_fk_样本信息表_样本编号` (`样本编号`),
  KEY `甲基化pooling表_患者编号_75b01ef4_fk_样本库存信息表_患者编号` (`患者编号`),
  KEY `甲基化pooling表_建库编号_bd7e866d_fk_甲基化建库表_建库编号` (`建库编号`),
  CONSTRAINT `甲基化pooling表_建库编号_bd7e866d_fk_甲基化建库表_建库编号` FOREIGN KEY (`建库编号`) REFERENCES `甲基化建库表` (`建库编号`),
  CONSTRAINT `甲基化pooling表_患者编号_75b01ef4_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `甲基化pooling表_捕获文库名_f23f1770_fk_甲基化捕获文库信息表_捕获文库名` FOREIGN KEY (`捕获文库名`) REFERENCES `甲基化捕获文库信息表` (`捕获文库名`),
  CONSTRAINT `甲基化pooling表_样本编号_83c32a23_fk_样本信息表_样本编号` FOREIGN KEY (`样本编号`) REFERENCES `样本信息表` (`样本编号`),
  CONSTRAINT `甲基化pooling表_核酸提取编号_10d91c4c_fk_样本提取表_核酸提取编号` FOREIGN KEY (`核酸提取编号`) REFERENCES `样本提取表` (`核酸提取编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `甲基化pooling表`
--

LOCK TABLES `甲基化pooling表` WRITE;
/*!40000 ALTER TABLE `甲基化pooling表` DISABLE KEYS */;
/*!40000 ALTER TABLE `甲基化pooling表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `甲基化建库表`
--

DROP TABLE IF EXISTS `甲基化建库表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `甲基化建库表` (
  `建库编号` varchar(35) DEFAULT NULL,
  `管上编号` varchar(35) DEFAULT NULL,
  `是否临床` varchar(25) DEFAULT NULL,
  `样本标签` varchar(25) DEFAULT NULL,
  `文库名` varchar(35) DEFAULT NULL,
  `index列表` varchar(25) DEFAULT NULL,
  `建库日期` date DEFAULT NULL,
  `建库方法` varchar(50) DEFAULT NULL,
  `试剂批次` varchar(50) DEFAULT NULL,
  `起始量` double DEFAULT NULL,
  `PCR循环数` int(11) DEFAULT NULL,
  `文库浓度` double DEFAULT NULL,
  `文库体积` double DEFAULT NULL,
  `操作人` varchar(35) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `核酸提取编号` varchar(35) DEFAULT NULL,
  `样本编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `建库编号` (`建库编号`),
  KEY `甲基化建库表_核酸提取编号_9ebe2070_fk_样本提取表_核酸提取编号` (`核酸提取编号`),
  KEY `甲基化建库表_样本编号_b548e3e8_fk_样本信息表_样本编号` (`样本编号`),
  KEY `甲基化建库表_患者编号_afaf9e28_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `甲基化建库表_患者编号_afaf9e28_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `甲基化建库表_样本编号_b548e3e8_fk_样本信息表_样本编号` FOREIGN KEY (`样本编号`) REFERENCES `样本信息表` (`样本编号`),
  CONSTRAINT `甲基化建库表_核酸提取编号_9ebe2070_fk_样本提取表_核酸提取编号` FOREIGN KEY (`核酸提取编号`) REFERENCES `样本提取表` (`核酸提取编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `甲基化建库表`
--

LOCK TABLES `甲基化建库表` WRITE;
/*!40000 ALTER TABLE `甲基化建库表` DISABLE KEYS */;
/*!40000 ALTER TABLE `甲基化建库表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `甲基化捕获文库信息表`
--

DROP TABLE IF EXISTS `甲基化捕获文库信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `甲基化捕获文库信息表` (
  `捕获文库名` varchar(35) DEFAULT NULL,
  `杂交日期` date DEFAULT NULL,
  `杂交探针` varchar(50) DEFAULT NULL,
  `杂交时间` double DEFAULT NULL,
  `PostPCR循环数` int(11) DEFAULT NULL,
  `PostPCR浓度` double DEFAULT NULL,
  `洗脱体积` double DEFAULT NULL,
  `操作人` varchar(35) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `捕获文库名` (`捕获文库名`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `甲基化捕获文库信息表`
--

LOCK TABLES `甲基化捕获文库信息表` WRITE;
/*!40000 ALTER TABLE `甲基化捕获文库信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `甲基化捕获文库信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `肝癌病理报告信息表`
--

DROP TABLE IF EXISTS `肝癌病理报告信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `肝癌病理报告信息表` (
  `病理报告编号` varchar(35) DEFAULT NULL,
  `检查日期` date DEFAULT NULL,
  `检查阶段` varchar(255) DEFAULT NULL,
  `肿瘤类型` varchar(50) DEFAULT NULL,
  `分化程度` varchar(15) DEFAULT NULL,
  `肿瘤数目` int(10) unsigned NOT NULL,
  `肿瘤1直径` double DEFAULT NULL,
  `肿瘤2直径` double DEFAULT NULL,
  `肿瘤3直径` double DEFAULT NULL,
  `肝包膜侵犯（肝被膜）` varchar(15) DEFAULT NULL,
  `淋巴结转移` varchar(255) DEFAULT NULL,
  `淋巴结转移类型` varchar(15) DEFAULT NULL,
  `肉眼癌栓(脉管侵犯)` varchar(1) DEFAULT NULL,
  `微血管浸润` varchar(1) DEFAULT NULL,
  `MVI类型` varchar(255) DEFAULT NULL,
  `切面距癌距离(切除面)` varchar(255) DEFAULT NULL,
  `G评分` varchar(15) DEFAULT NULL,
  `S评分` varchar(15) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `病理编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `病理报告编号` (`病理报告编号`),
  KEY `肝癌病理报告信息表_病理编号_bcea6d35_fk_基本临床信息表_病理编号` (`病理编号`),
  KEY `肝癌病理报告信息表_患者编号_2ed7b90a_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `肝癌病理报告信息表_患者编号_2ed7b90a_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `肝癌病理报告信息表_病理编号_bcea6d35_fk_基本临床信息表_病理编号` FOREIGN KEY (`病理编号`) REFERENCES `基本临床信息表` (`病理编号`),
  CONSTRAINT `肝癌病理报告信息表_chk_1` CHECK ((`肿瘤数目` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `肝癌病理报告信息表`
--

LOCK TABLES `肝癌病理报告信息表` WRITE;
/*!40000 ALTER TABLE `肝癌病理报告信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `肝癌病理报告信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `肝癌肿瘤标志物检测结果信息表`
--

DROP TABLE IF EXISTS `肝癌肿瘤标志物检测结果信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `肝癌肿瘤标志物检测结果信息表` (
  `检测编号` varchar(35) DEFAULT NULL,
  `检查日期` date DEFAULT NULL,
  `检查阶段` varchar(255) DEFAULT NULL,
  `甲胎蛋白` varchar(255) DEFAULT NULL,
  `甲胎蛋白异质体` varchar(255) DEFAULT NULL,
  `癌胚抗原` varchar(255) DEFAULT NULL,
  `糖类抗原19-9` varchar(255) DEFAULT NULL,
  `黑素瘤抑制蛋白` varchar(255) DEFAULT NULL,
  `细胞角蛋白19片段` varchar(255) DEFAULT NULL,
  `糖类抗原125` varchar(255) DEFAULT NULL,
  `神经元特异性烯醇化酶` varchar(255) DEFAULT NULL,
  `鳞状细胞癌抗原` varchar(255) DEFAULT NULL,
  `胃泌素释放肽前体` varchar(255) DEFAULT NULL,
  `糖类抗原15-3` varchar(255) DEFAULT NULL,
  `前列腺特异性抗原` varchar(255) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `病理编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `检测编号` (`检测编号`),
  KEY `肝癌肿瘤标志物检测结果信息表_病理编号_228592cb_fk_基本临床信息表_病理编号` (`病理编号`),
  KEY `肝癌肿瘤标志物检测结果信息表_患者编号_0abe6a5a_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `肝癌肿瘤标志物检测结果信息表_患者编号_0abe6a5a_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `肝癌肿瘤标志物检测结果信息表_病理编号_228592cb_fk_基本临床信息表_病理编号` FOREIGN KEY (`病理编号`) REFERENCES `基本临床信息表` (`病理编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `肝癌肿瘤标志物检测结果信息表`
--

LOCK TABLES `肝癌肿瘤标志物检测结果信息表` WRITE;
/*!40000 ALTER TABLE `肝癌肿瘤标志物检测结果信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `肝癌肿瘤标志物检测结果信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `肝癌肿瘤生化检测结果信息表`
--

DROP TABLE IF EXISTS `肝癌肿瘤生化检测结果信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `肝癌肿瘤生化检测结果信息表` (
  `检测编号` varchar(35) DEFAULT NULL,
  `检查日期` date DEFAULT NULL,
  `检查阶段` varchar(255) DEFAULT NULL,
  `总胆红素` varchar(255) DEFAULT NULL,
  `丙氨酸氨基转移酶` varchar(255) DEFAULT NULL,
  `γ-谷氨酰转移酶` varchar(255) DEFAULT NULL,
  `白蛋白` varchar(255) DEFAULT NULL,
  `α-L-岩藻糖苷酶` varchar(255) DEFAULT NULL,
  `直接胆红素` varchar(255) DEFAULT NULL,
  `谷丙转氨酶` varchar(255) DEFAULT NULL,
  `谷草转氨酶` varchar(255) DEFAULT NULL,
  `r-谷氨酰转肽酶` varchar(255) DEFAULT NULL,
  `碱性磷酸酶` varchar(255) DEFAULT NULL,
  `总胆汁酸` varchar(255) DEFAULT NULL,
  `前白蛋白` varchar(255) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `病理编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `检测编号` (`检测编号`),
  KEY `肝癌肿瘤生化检测结果信息表_病理编号_ca83c55d_fk_基本临床信息表_病理编号` (`病理编号`),
  KEY `肝癌肿瘤生化检测结果信息表_患者编号_a8dad9ce_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `肝癌肿瘤生化检测结果信息表_患者编号_a8dad9ce_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `肝癌肿瘤生化检测结果信息表_病理编号_ca83c55d_fk_基本临床信息表_病理编号` FOREIGN KEY (`病理编号`) REFERENCES `基本临床信息表` (`病理编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `肝癌肿瘤生化检测结果信息表`
--

LOCK TABLES `肝癌肿瘤生化检测结果信息表` WRITE;
/*!40000 ALTER TABLE `肝癌肿瘤生化检测结果信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `肝癌肿瘤生化检测结果信息表` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `随访信息表`
--

DROP TABLE IF EXISTS `随访信息表`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `随访信息表` (
  `随访记录编号` varchar(35) DEFAULT NULL,
  `生存状态` varchar(2) DEFAULT NULL,
  `死亡日期` date DEFAULT NULL,
  `死因是否与肿瘤相关` varchar(1) DEFAULT NULL,
  `是否复发` varchar(1) DEFAULT NULL,
  `复发日期` date DEFAULT NULL,
  `复发状态` varchar(255) DEFAULT NULL,
  `随访日期` date DEFAULT NULL,
  `随访情况` varchar(255) DEFAULT NULL,
  `备注` longtext,
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `创建时间` datetime(6) NOT NULL,
  `最近修改时间` datetime(6) NOT NULL,
  `病理编号` varchar(35) DEFAULT NULL,
  `患者编号` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`index`),
  UNIQUE KEY `随访记录编号` (`随访记录编号`),
  KEY `随访信息表_病理编号_9849e27e_fk_基本临床信息表_病理编号` (`病理编号`),
  KEY `随访信息表_患者编号_e512c155_fk_样本库存信息表_患者编号` (`患者编号`),
  CONSTRAINT `随访信息表_患者编号_e512c155_fk_样本库存信息表_患者编号` FOREIGN KEY (`患者编号`) REFERENCES `样本库存信息表` (`患者编号`),
  CONSTRAINT `随访信息表_病理编号_9849e27e_fk_基本临床信息表_病理编号` FOREIGN KEY (`病理编号`) REFERENCES `基本临床信息表` (`病理编号`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `随访信息表`
--

LOCK TABLES `随访信息表` WRITE;
/*!40000 ALTER TABLE `随访信息表` DISABLE KEYS */;
/*!40000 ALTER TABLE `随访信息表` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-06 15:04:23
