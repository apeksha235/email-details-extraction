USE  'proj_db'
DELIMITER $$
CREATE TRIGGER finallly
AFTER INSERT ON details 
for each row 
begin 
insert into test values('record inserted');
end$$


