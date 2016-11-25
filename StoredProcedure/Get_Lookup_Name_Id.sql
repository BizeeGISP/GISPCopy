DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Get_Lookup_Name_Id`(IN NameValue varchar(100), Out Name_Id int, Out Element_lookup_Id int)
BEGIN

	Select id, ifnull(element_id,0) into Name_Id, Element_lookup_Id from lookup_name where name = NameValue;

	IF ( Name_Id Is Null ) then   
	   
		Insert into lookup_name ( name ) values ( NameValue );
		Select id, ifnull(element_id,0) into Name_Id, Element_lookup_Id from lookup_name where name = NameValue;
	
	END IF;
END$$
DELIMITER ;
