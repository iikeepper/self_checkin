CREATE TABLE `sak_claim_log` (
  `auto_id` int(10) NOT NULL AUTO_INCREMENT,
  `pid` varchar(13) DEFAULT NULL,
  `claimType` varchar(20) DEFAULT NULL,
  `correlationId` varchar(150) DEFAULT NULL,
  `createdDate` varchar(50) DEFAULT NULL,
  `claimCode` varchar(20) DEFAULT NULL,
  `service_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`auto_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4100 DEFAULT CHARSET=tis620;
