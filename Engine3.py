#import dbUtilities
import findFormDetails
#import dbUtilities


#a = findFormDetails.findFormDetails("http://www.bizee.in/contacts.php")
a = findFormDetails.findFormDetails("http://www.ishir.com/contactus.htm")

for b in a:
    print b
