-- MySQL dump 10.16  Distrib 10.1.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 192.168.178.90    Database: mc_scheduler
-- ------------------------------------------------------
-- Server version	10.1.37-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `division`
--

DROP TABLE IF EXISTS `division`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `division` (
  `division_id` int(16) NOT NULL AUTO_INCREMENT,
  `division_name` varchar(128) CHARACTER SET utf8 NOT NULL,
  `division_acronym` varchar(8) CHARACTER SET utf8 NOT NULL,
  `division_color` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `division_optimized` int(8) NOT NULL,
  PRIMARY KEY (`division_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `game_id` int(16) NOT NULL AUTO_INCREMENT,
  `matchup_id` int(16) NOT NULL,
  `slot_id` int(16) NOT NULL,
  `game_state` int(1) NOT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `slot_id_2` (`slot_id`),
  UNIQUE KEY `matchslot` (`matchup_id`,`slot_id`),
  KEY `matchup_id` (`matchup_id`),
  KEY `slot_id` (`slot_id`),
  CONSTRAINT `game_ibfk_1` FOREIGN KEY (`slot_id`) REFERENCES `slot` (`slot_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_ibfk_2` FOREIGN KEY (`matchup_id`) REFERENCES `matchup` (`matchup_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gamestate`
--

DROP TABLE IF EXISTS `gamestate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gamestate` (
  `gamestate_id` int(16) NOT NULL,
  `gamestate_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `gamestate_color` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`gamestate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gamestate`
--

LOCK TABLES `gamestate` WRITE;
/*!40000 ALTER TABLE `gamestate` DISABLE KEYS */;
INSERT INTO `gamestate` VALUES
(0,'toDo','#ff0000'),
(1,'Done','#00ff00'),
(2,'Doing','#0000ff');
/*!40000 ALTER TABLE `gamestate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `location_id` int(16) NOT NULL AUTO_INCREMENT,
  `location_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `location_description` text COLLATE utf8_unicode_ci NOT NULL,
  `location_color` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  `location_latitude` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `location_longitude` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `location_gym` tinyint(1) NOT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `matchup`
--

DROP TABLE IF EXISTS `matchup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `matchup` (
  `matchup_id` int(16) NOT NULL AUTO_INCREMENT,
  `matchup_team1_id` int(8) NOT NULL,
  `matchup_team2_id` int(8) NOT NULL,
  `matchup_team1_score` int(8) NOT NULL,
  `matchup_team2_score` int(8) NOT NULL,
  `matchup_team1_timeouts` int(8) NOT NULL,
  `matchup_team2_timeouts` int(8) NOT NULL,
  PRIMARY KEY (`matchup_id`),
  KEY `matchup_team1_id` (`matchup_team1_id`),
  KEY `matchup_team2_id` (`matchup_team2_id`),
  CONSTRAINT `matchup_ibfk_1` FOREIGN KEY (`matchup_team1_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `matchup_ibfk_2` FOREIGN KEY (`matchup_team2_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking`
--

DROP TABLE IF EXISTS `ranking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking` (
  `ranking_id` int(16) NOT NULL AUTO_INCREMENT,
  `team_id` int(16) NOT NULL,
  `ranking_rank` int(8) NOT NULL,
  `round_id` int(16) NOT NULL,
  `division_id` int(16) NOT NULL,
  PRIMARY KEY (`ranking_id`),
  UNIQUE KEY `rank_id` (`team_id`,`round_id`,`division_id`),
  KEY `team_id` (`team_id`),
  KEY `round_id` (`round_id`),
  KEY `division_id` (`division_id`),
  CONSTRAINT `ranking_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ranking_ibfk_2` FOREIGN KEY (`round_id`) REFERENCES `round` (`round_id`),
  CONSTRAINT `ranking_ibfk_3` FOREIGN KEY (`division_id`) REFERENCES `division` (`division_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `round`
--

DROP TABLE IF EXISTS `round`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `round` (
  `round_id` int(16) NOT NULL AUTO_INCREMENT,
  `division_id` int(16) NOT NULL,
  `round_number` int(16) NOT NULL,
  `round_color` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  `round_group` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `round_grouporder` int(8) NOT NULL,
  `round_state` int(11) NOT NULL,
  `round_fixnextgametime` int(16) NOT NULL,
  `round_swissdrawGames` tinyint(1) NOT NULL,
  `round_swissdrawRanking` tinyint(1) NOT NULL,
  `round_swissdrawMatchup` tinyint(1) NOT NULL,
  PRIMARY KEY (`round_id`),
  KEY `division_id` (`division_id`),
  CONSTRAINT `round_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `division` (`division_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `scoreboardtext`
--

DROP TABLE IF EXISTS `scoreboardtext`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scoreboardtext` (
  `scoreboardtext_id` int(16) NOT NULL AUTO_INCREMENT,
  `location_id` int(8) NOT NULL,
  `scoreboardtext_text` text CHARACTER SET utf8 NOT NULL,
  `scoreboardtext_start` int(16) NOT NULL,
  `scoreboardtext_end` int(16) NOT NULL,
  `scoreboardtext_color` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`scoreboardtext_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `scoreboardtext_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `slot`
--

DROP TABLE IF EXISTS `slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `slot` (
  `slot_id` int(16) NOT NULL AUTO_INCREMENT,
  `location_id` int(16) NOT NULL,
  `slot_start` int(16) NOT NULL,
  `slot_end` int(16) NOT NULL,
  `round_id` int(16) NOT NULL,
  `slot_name` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `slot_description` text COLLATE utf8_unicode_ci,
  `slot_alternateText` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`slot_id`),
  KEY `location_id` (`location_id`),
  KEY `slot_start` (`slot_start`,`location_id`) USING BTREE,
  KEY `round_id` (`round_id`),
  CONSTRAINT `slot_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `slot_ibfk_3` FOREIGN KEY (`round_id`) REFERENCES `round` (`round_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `team_id` int(8) NOT NULL AUTO_INCREMENT,
  `division_id` int(16) NOT NULL,
  `team_name` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `team_acronym` varchar(8) COLLATE utf8_unicode_ci NOT NULL,
  `team_seed` int(8) NOT NULL,
  `team_city` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `team_color` varchar(7) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`team_id`),
  KEY `division_id` (`division_id`),
  CONSTRAINT `team_ibfk_1` FOREIGN KEY (`division_id`) REFERENCES `division` (`division_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `user_password` varchar(1024) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,'admin','$2y$12$RYShfse/i8PI7pvXskhQT.NQppmVAP.pmR8X33O1pl6ghv8AbRPIe'),
(2,'temp','$2y$12$x5Yr69iIlHVR1cCUYgOYoudQxWDTaT9.3B77kZgVIy5ODyE5lVMa.');
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