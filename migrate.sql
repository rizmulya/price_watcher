CREATE TABLE `options` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(64) NOT NULL UNIQUE,
  `value` varchar(128) NOT NULL
);

INSERT INTO `options` (`id`, `name`, `value`) VALUES
(1, 'bnc_price_change_perc_treshold', '10');

CREATE TABLE `bnc_alerts` (
  `symbol` VARCHAR(16) NOT NULL PRIMARY KEY,
  `higher` float DEFAULT NULL,
  `lower` float DEFAULT NULL,
  `watch` tinyint(1) NOT NULL DEFAULT 1
);

CREATE TABLE `bnc_ticker_24` (
  `symbol` VARCHAR(16) NOT NULL PRIMARY KEY,
  `priceChangePercent` float DEFAULT NULL,
  `lastPrice` float DEFAULT NULL,
  `highPrice` float DEFAULT NULL,
  `lowPrice` float DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
);

CREATE TABLE `tele_responses` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `trigger_type` enum('case-sensitive','case-insensitive','regex') NOT NULL DEFAULT 'case-insensitive',
  `trigger_text` varchar(128) NOT NULL,
  `response_type` enum('text','func') NOT NULL DEFAULT 'text',
  `response_text` text,
  `response_func` varchar(32) DEFAULT NULL,
  `receiver` BIGINT DEFAULT NULL,
  INDEX (`trigger_text`),
  INDEX (`receiver`) 
);

INSERT INTO `tele_responses` (`id`, `trigger_type`, `trigger_text`, `response_type`, `response_text`, `response_func`, `receiver`) VALUES
(1,	'case-insensitive',	'hi',	'text',	'Hi there!',	NULL,	NULL),
(2,	'case-insensitive',	'id',	'func',	NULL,	'show_tele_id',	NULL);