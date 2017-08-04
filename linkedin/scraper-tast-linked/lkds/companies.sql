-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 19, 2017 at 11:07 AM
-- Server version: 5.7.11-0ubuntu6
-- PHP Version: 7.0.4-7ubuntu2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `linkdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `companies`
--

CREATE TABLE `companies` (
  `slug` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `name` varchar(1500) CHARACTER SET utf8 NOT NULL,
  `logo` varchar(1000) COLLATE utf8_bin DEFAULT NULL,
  `betaId` int(9) DEFAULT NULL,
  `website` varchar(1500) CHARACTER SET utf8 DEFAULT NULL,
  `host` varchar(750) CHARACTER SET utf8 DEFAULT NULL,
  `description` text CHARACTER SET utf8,
  `type` varchar(250) CHARACTER SET utf8 DEFAULT NULL,
  `address` varchar(1000) CHARACTER SET utf8 DEFAULT NULL,
  `region` varchar(350) CHARACTER SET utf8 DEFAULT NULL,
  `postalCode` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `country` varchar(25) CHARACTER SET utf8 DEFAULT NULL,
  `industry` varchar(150) CHARACTER SET utf8 DEFAULT NULL,
  `companySize` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `founded` int(4) DEFAULT NULL,
  `specialties` text CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
