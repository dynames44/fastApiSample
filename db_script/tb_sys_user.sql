
CREATE TABLE `tb_sys_user` (
  `USER_ID` varchar(20) NOT NULL COMMENT '관리자ID',
  `USER_NM` varchar(50) DEFAULT NULL COMMENT '사용자명',
  `USER_PW` varchar(100) DEFAULT NULL COMMENT '비밀번호',
  `USE_YN` char(1) DEFAULT NULL COMMENT '사용여부',
  `EMAIL` varchar(100) DEFAULT NULL COMMENT '이메일주소',
  `REG_DTTM` timestamp NULL DEFAULT current_timestamp() COMMENT '등록일자',
  PRIMARY KEY (`USER_ID`)
) ENGINE=InnoDB COMMENT='사용자';


INSERT INTO py_db.tb_sys_user (USER_ID,USER_NM,USER_PW,USE_YN,EMAIL,REG_DTTM) 
VALUES
	 ('TEST1','사용자1','1234','Y','test1@naver.com','2025-04-24 09:00:44.0'),
	 ('TEST2','사용자2','1234','Ｎ','test2@naver.com','2025-04-24 09:00:44.0'),
	 ('TEST3','사용자3','1234','Y','test3@google.com','2025-04-24 09:00:44.0');`