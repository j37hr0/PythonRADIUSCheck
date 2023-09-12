CREATE DEFINER=`radiusmain`@`%` PROCEDURE `rts_monitor_replication`()
BEGIN
	SELECT *
	FROM radius.radpostauth
	ORDER BY id DESC
	LIMIT 1;
END$$
DELIMITER ;
