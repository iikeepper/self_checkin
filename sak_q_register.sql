CREATE TABLE `sak_q_register` (
  `auto_id` int(10) NOT NULL AUTO_INCREMENT,
  `pid` varchar(13) DEFAULT NULL,
  `ptname` varchar(200) DEFAULT NULL,
  `birthDate` varchar(20) DEFAULT NULL,
  `sex` varchar(20) DEFAULT NULL,
  `correlationId` varchar(200) DEFAULT NULL,
  `startDateTime` varchar(100) DEFAULT NULL,
  `mainInscl` varchar(150) DEFAULT NULL,
  `subInscl` varchar(150) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `hn` varchar(9) DEFAULT NULL,
  `tel` varchar(10) DEFAULT NULL,
  `service_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`auto_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7836 DEFAULT CHARSET=tis620;

