CREATE DATABASE wmscoin default CHARACTER SET UTF8;
use wmscoin;
CREATE TABLE usertbl(
    userid VARCHAR(45) PRIMARY KEY NOT NULL,
    userpw VARCHAR(45) NOT NULL,
    countcoin VARCHAR(45)
) ENGINE=INNODB;

INSERT INTO usertbl
(userid, userpw)
VALUES('admin', '1234');

select * from usertbl;