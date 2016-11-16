import mechanize
from pyquery import PyQuery as pq

def findFormDetails(url_contact):
    """
    br = mechanize.Browser()
    br.open(url_contact)
    for g in br.forms():
        return g
    """


    #url='http://www.ishir.com/outsourcing-services.htm//contactus.htm'
    url='http://www.bizee.in/contacts.php'
    d = pq(url=url_contact)

    forms = d('form')
    x = ()
    l = list(x)
    links=d('a')
    for link in links:
        btn = pq(link).attr('id')
        if btn is not None:
            #print "in btn"
            y=l.append(str(btn))
            #print y
    inputs = d('input')
    for inp in inputs:
        #print "second"
        i = pq(inp).attr('name')
        #print i
        y=l.append(i)

    for inp in inputs:
        i = pq(inp).attr('type')
        #if i == 'submit':
        y = l.append(i)
    y=tuple(l)
    #print y
    #x = btn + i
    return y

