import geograpy


def ContactUsPage(soup):
    strings = soup.strings
    data = ""
    dat = ""

    for string in strings:
        if not string == '\n' and string != "":
            # print string
            dat += string
            print( "Data:", dat)
            if dat != "":
                places = geograpy.get_place_context(text=dat)
                country = places.country_cities
                if len(country) > 0:
                    if not country in data:
                        data.append(country)
    print ("Result: ", data)
    return data

