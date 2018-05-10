-- MySQL dump 10.16  Distrib 10.1.31-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: nct
-- ------------------------------------------------------
-- Server version	10.1.31-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `f_name` varchar(30) NOT NULL,
  `l_name` varchar(30) NOT NULL,
  `created_on` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_role`
--

DROP TABLE IF EXISTS `account_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_role` (
  `u_id` int(11) NOT NULL,
  `r_id` int(11) NOT NULL,
  `grant_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`u_id`,`r_id`),
  KEY `r_id` (`r_id`),
  CONSTRAINT `account_role_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `account` (`id`),
  CONSTRAINT `account_role_ibfk_2` FOREIGN KEY (`r_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appointment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registration` varchar(11) NOT NULL,
  `assigned` int(11) NOT NULL,
  `is_tested` datetime DEFAULT NULL,
  `date` datetime NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `registration` (`registration`),
  KEY `assigned` (`assigned`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`registration`) REFERENCES `vehicle` (`registration`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`assigned`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `attribute`
--

DROP TABLE IF EXISTS `attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `failure`
--

DROP TABLE IF EXISTS `failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `failure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `step` int(11) NOT NULL,
  `name` text NOT NULL,
  `item` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `step` (`step`),
  CONSTRAINT `failure_ibfk_1` FOREIGN KEY (`step`) REFERENCES `step` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `owner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `f_name` varchar(30) NOT NULL,
  `l_name` varchar(30) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `appointment` int(11) NOT NULL,
  `comment` text,
  `step` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_result_appointment` (`appointment`),
  KEY `fk_result_step` (`step`),
  CONSTRAINT `fk_result_appointment` FOREIGN KEY (`appointment`) REFERENCES `appointment` (`id`),
  CONSTRAINT `fk_result_step` FOREIGN KEY (`step`) REFERENCES `step` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `result_failure`
--

DROP TABLE IF EXISTS `result_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `result_failure` (
  `appointment` int(11) NOT NULL,
  `failure` int(11) NOT NULL,
  PRIMARY KEY (`appointment`,`failure`),
  KEY `result_failure_fk` (`failure`),
  CONSTRAINT `result_failure_appointment_fk` FOREIGN KEY (`appointment`) REFERENCES `appointment` (`id`),
  CONSTRAINT `result_failure_fk` FOREIGN KEY (`failure`) REFERENCES `failure` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `step`
--

DROP TABLE IF EXISTS `step`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `step` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle` (
  `registration` varchar(11) NOT NULL,
  `vin` varchar(30) NOT NULL,
  `owner` int(11) NOT NULL,
  `make` varchar(30) NOT NULL,
  `model` varchar(30) NOT NULL,
  `year` int(4) NOT NULL,
  `colour` varchar(20) NOT NULL,
  PRIMARY KEY (`registration`),
  UNIQUE KEY `vin` (`vin`),
  KEY `owner` (`owner`),
  CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `owner` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehicle_attribute`
--

DROP TABLE IF EXISTS `vehicle_attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_attribute` (
  `registration` varchar(11) NOT NULL,
  `a_id` int(11) NOT NULL,
  `value` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`registration`,`a_id`),
  KEY `a_id` (`a_id`),
  CONSTRAINT `vehicle_attribute_ibfk_1` FOREIGN KEY (`registration`) REFERENCES `vehicle` (`registration`),
  CONSTRAINT `vehicle_attribute_ibfk_2` FOREIGN KEY (`a_id`) REFERENCES `attribute` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-10  6:58:41

INSERT INTO `account` (`username`, `password`, `f_name`, `l_name`)
  VALUES ('admin', '$pbkdf2-sha256$29000$HcPYGyMkZExJSWmNEeIcYw$6KpAgTPyVFKy0pLtvDfbw0lbEO6B2nN00e/asVivrfY', 'admin', 'istrator');

INSERT INTO `role` (`id`, `name`) VALUES (1,'Administrator'),(2,'Mechanic');

INSERT INTO `account_role` (`u_id`, `r_id`) VALUES (1, 1);
INSERT INTO `step` VALUES (1,'Registration Plates','1. Check the registration plates for security, location, format, legibility, visibility and correct colour.','Owners of vehicles first registered prior to 31 December 1990, have the option of converting their\nregistration plates to the new format.\n1. Vehicles first registered on or after 1 January 1991\nFor vehicles registered on or after 1 January 1991, letters and numbers must be black set against a white\nbackground of reflex reflective material. The flag of the European Communities, the Nationality Symbol,\nIRL, and the Irish language name of the City/County of registration to be shown. No other marks may\nappear on the plate. Any additional tabs, etc. outside the dimensions shown for the registration plate\nare not considered part of the plate.\n2. Vehicles first registered on or after 1 January 1987\nFor vehicles registered on or after 1 January 1987, letters and numbers must be black set against a white\nbackground of reflex reflective material and minimum dimensions should be as shown in the sketches on\npage 9.\n3. Vehicles first registered prior to 1 January 1987\n(a) Reflex Reflecting Registration Plates\nFront registration plates should have black numbers and letters on a white background. Rear registration\nplates should have black numbers and letters on a red or white background.\n(b) Non-Reflex Reflecting Registration Plates\nFront and rear registration plates should have white, silver or light grey numbers and letters on a\nblack background.\n(c) Back Lit Registration Numbers and Letters\nWhere registration numbers and letters are back lit the letters and figures must, when illuminated\nduring lighting-up hours appear white in the front identification mark and either white or red in the rear\nidentification mark. At all other times they should appear white on a black background.\n(d) Dimensions for letters and numbers should be as shown in the sketch on page 9.\n4. Where the indented space provided for the number plate is not sufficient to accommodate a standard size\nnumber plate, the registration plate and registration letters and numbers may be reduced in size relative\nto the space provided for the number plate.'),(2,'Exhaust Smoke (Diesel)','Vehicles first registered on or after 1st January 1980\n1. Check visually that the emission control system is complete and properly connected and that there are no leaks in the\nexhaust system.\n2. With the engine at normal operating temperature, raise the engine speed slowly to 2,500 rpm or half the engine manufacturer’s\nrecommended governed speed whichever is less and hold for 20 seconds in order to purge the exhaust system. If the engine\nemits any unusual noises the test should be abandoned. Slowly raise the engine speed to its maximum rpm and note if the\ngovernor operates within the vehicle manufacturer’s recommended rpm setting. If not the test should be discontinued.\nDo not hold the engine at maximum rpm for any length of time.\n3. Connect the diesel smoke meter to the vehicle following the smoke meter manufacturer’s instructions. Depress the accelerator\npedal firmly from the idling position to the maximum fuel delivery position following the prompts of the smoke meter. The\nsmoke meter is programmed to ignore the first reading. The operation is repeated and if the reading on this occasion is less\nthan 60% of the acceptable limit the test is ended. If the reading is not less than 60% of the acceptable limit, the operation is\nrepeated. If the average of this and the previous reading is within the acceptable limit the test is ended. If the average readings\nare not within the limits the operation is repeated up to a maximum of three more times taking the average of the last two\nreadings after which the test is ended.\nVehicles first registered before 1st January 1980\n4. For these vehicles, the exhaust emission should be assessed while driving the vehicle in the test area or test lane. Under no\ncircumstances should the engine rpm be taken above that required to drive the vehicle through the various tests.','(Vehicles first registered on or after 1st January 1980)\n1. All diesel engine tests must be performed according to EU Directives. Where an automatic transmission is\nfitted, the manufacturer’s guidelines should be consulted.\n2. No smoke test should be carried out without having done the pre test check detailed on page 10.\n3. It is absolutely essential that the engine is at normal operating temperature before carrying out a smoke\ntest. Testers should ensure that engines are not warmed up by being left idling or at half throttle. They\nshould be warmed up by normal driving.\n4. Engines left idling for any length of time will show a high smoke opacity reading.\n5. When carrying out this test the throttle must not be “blipped”.\n6. Exhaust emissions tests should not be performed on a vehicle where the oil level is well over the dipstick\n“Full” mark.\n7. Where the oil level is below the minimum level, the exhaust emission test should not be performed if it is\nnecessary to purge the engine.\n8. Where a diesel engine is at the correct operating temperature and has been correctly purged and the first\nthree readings are at or above 9.99, the exhaust emissions test may be aborted.\n9. Where a vehicle is producing black smoke to such an extent that the smoke meter might be damaged,\nthe vehicle should be failed without carrying out the normal smoke test (see Test for vehicles first\nregistered prior to 1980.)\n10. Where a vehicle’s engine speed is limited when the vehicle is stationary, the smoke test may be carried\nout at the restricted rpm.'),(3,'Exhaust CO/HC/Lambda','1. Check visually in the case of 4 stroke spark ignition engines (petrol or gas) that the emission control system is complete and\nproperly connected and that there are no leaks in the exhaust system.\nPre Jan 1994 Registrations\n2. With the engine at normal operating temperature connect the CO/HC meter as per manufacturer’s instructions. Raise the\nengine speed to approximately 2,500 rpm and hold for 20 seconds. Allow the engine to return to idle and the emissions\nreadings to stabilise. Note the carbon monoxide and hydrocarbon content of the exhaust gases at normal idle speed.\nPost Jan 1994 Registrations\n3. For vehicles first registered on or after the 1st January 1994 raise the engine speed to 2,500 rpm or to a speed specified by the\nvehicle manufacturer and hold for a minimum of 30 seconds. Check the HC, CO and Lambda values. If the exhaust emissions\nare not within the specified limits with the vehicle engine at normal operating temperature raise the engine speed to 2,500\nrpm or to a speed specified by the vehicle manufacturer and hold for 3 minutes and note HC, CO and Lambda values. Allow the\nvehicle engine to return to normal idle speed and the exhaust reading to stabilise and note the CO reading.','1. When checking exhaust emissions, the vehicle must be conditioned in accordance with the vehicle\nmanufacturer’s recommendations.\n2. Hybrid vehicles should be viewed as an electric vehicle and will not require an exhaust emissions test.\n3. For the following Rover vehicles: a) Mini 1300 carburettor and open loop three-way catalyst, b) Metro\nRover 100 1100 carburettor and open loop three-way catalyst, first registered on or before 31 December\n1994, the exhaust emission limit for CO is 3.5% and for HC is 1200 ppm. Where a vehicle meets the CO\nlimit but fails the HC limit, the inspector must perform a further HC test at 2000 rpm. If the vehicle meets\nthe HC limit at 2000 rpm, it is considered to have met the requirements.\n4. For Suzuki Cultas, the maximum allowable CO value is 4.5% and the maximum allowable HC value\nis 1200 ppm.\n5. Where it can be established that the vehicle manufacturer’s recommendations on exhaust emissions are\nhigher than those listed in the reasons for failure then the manufacturer’s figure should be the criteria\nused when deciding whether or not the vehicle passes.\n6. For vehicles tested operating on L.P.G. the hydrocarbon reading must be divided by the propane/hexane\nequivalent factor (PEF) which is marked on the hydrocarbon test equipment.\n7. Where vehicles are fitted with twin exhaust systems the higher of the two should be taken.\n8. A HC test is not required on vehicles operating on CNG.\n9. This test should not be carried out where:\n(a) the oil warning light remains on with the engine running.\n(b) the oil level is below the manufacturer’s minimum level.\n(c) the oil level is above the manufacturer’s maximum level.\n10 This test does not apply to two-stroke or rotary piston (Wankel) engines.');
INSERT INTO `failure` VALUES (1,1,'One or both plates missing, insecure or not clearly visible.','Registration Number Plate'),(2,1,'Numbers or letters missing or illegible or incorrect size.','Registration Number Plate'),(3,1,'Numbers, letter or background of incorrect colour.','Registration Number Plate'),(4,1,'Marks, other than those prescribed, on the plate within the boundary shown in the diagram.','Registration Number Plate'),(5,2,'Engine oil level too high or too low, coolant level too low','Preliminary Check'),(6,2,'Obvious Engine defects','Preliminary Check'),(7,2,'Where the average smoke meter reading is not inaccordance with the manufacturer’s standard for exhaustsmoke emissions or is higher than 2.5m-1 in the case ofnaturally aspirated diesel engines and 3.0m-1 in the caseof turbocharged or supercharged diesel engines.','Exhaust Smoke (Vehicles first registered on or after 1st January 1980 up to 1st July 2008)'),(8,2,'Where the maximum attainable engine speed is less than or equal to 90% of the maximum speed specified by the manufacturer.','Exhaust Smoke (Vehicles registered after 1st July 2008)'),(9,2,'Where the average smoke meter reading is not in accordance with the manufacturer’s standard for exhaust smoke emissions or is higher than 1.5m.','Exhaust Smoke (Vehicles registered after 1st July 2008)'),(10,2,'The exhaust emission is coloured black haze or darker.','Exhaust Smoke (Vehicles registered after 1st January 1980)'),(11,2,'Emission control system leaking, incomplete or incorrectly assembled.','Emission Control System'),(12,2,'Engine idle speed incorrect (e.g. ± 100 rpm of manufacturer’s stated speed).','Idle Speed'),(13,3,'Leaking','Engine Exhaust System'),(14,3,'Emission control system leaking, incomplete, incorrectly assembled or obviously unsafely repaired or modified','Emission Control System'),(15,3,'Obviously outside vehicle manufacturer’s recommendations (± 100 rpm or ±10% of manufacturer’s stated speed whichever is greater)','Idle Speed'),(16,3,'Carbon monoxide emission is is not in accordance with the vehicle manufacturer’s standard or for vehicles first registered before 1st of October 1986, the carbon monoxide content is more than 4.5% at idling speed.','Carbon Monoxide Emission'),(17,3,'For vehicles first registered on or after 1st of October 1986, up to 31st December 1993, the carbon monoxide content at idling speed is more than 3.5%.','Carbon Monoxide Emission'),(18,3,'For vehicles first registered on or after 1st of January 1994, the carbon monoxide content at idling speed is more than 0.5%.','Carbon Monoxide Emission'),(19,3,'For vehicles first registered on or after 1st of January 1994, the carbon monoxide content at 2,500 rpm or at a speed specified by the vehicle manufacturer is more than 0.3%.','Carbon Monoxide Emission'),(20,3,'For vehicles first registered on or after 1st of July 2002 the carbon monoxide at idling speed is more than 0.3%.','Carbon Monoxide Emission'),(21,3,'For vehicles first registered on or after 1st of July 2002 the carbon monoxide content is more than 0.2% by volume at either an engine speed of 2500 rpm or at a speed specified by the vehicle manufacturer.','Carbon Monoxide Emission'),(22,3,'Hydrocarbon emission is is not in accordance with the vehicle manufacturer’s standard or for vehicles firstr egistered before 1st October, 1986, the hydrocarbon content at idling speed is more than 1,000 ppm.','Hydrocarbon (H.C.)'),(23,3,'For vehicles first registered on or after 1st of October 1986, up to 31st December 1993, the hydrocarbon content at idling speed is more than 750 ppm.','Hydrocarbon (H.C.)'),(24,3,'For vehicles first registered on or after 1st of January 1994, the hydrocarbon content at 2,500 rpm or at a speed specified by the vehicle manufacturer is more than 200 ppm.','Hydrocarbon (H.C.)'),(25,3,'For vehicles first registered on or after 1st of January 1994, the lambda value at 2,500 rpm or at the speed specified by the vehicle manufacturer is not 1 ± .03 or within the vehicle manufacturer’s recommendation.','Lambda'),(26,3,'Excessive exhaust smoke likely to affect other road users.','Exhaust Emissions');
