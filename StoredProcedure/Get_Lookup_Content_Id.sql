DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Get_Lookup_Content_Id`(IN NameValue varchar(100), Out Name_Id int, Out Element_lookup_Id int)
BEGIN

	Select id, ifnull(element_id,0) into Name_Id, Element_lookup_Id from lookup_content where name = NameValue;

	IF ( Name_Id Is Null ) then   
	   
		Insert into lookup_content ( name ) values ( NameValue );
		Select id, ifnull(element_id,0) into Name_Id, Element_lookup_Id from lookup_content where name = NameValue;
	
	END IF;
END$$
DELIMITER ;
