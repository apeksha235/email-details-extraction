CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAllProducts`()
BEGIN
	SELECT items FROM details where company='Lake';
END
