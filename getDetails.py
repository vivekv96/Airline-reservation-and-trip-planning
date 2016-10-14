import requests
import json

class goibiboAPI(object):
    BASE = "http://developer.goibibo.com/api/"

    def __init__(self, app_id, app_key):
        self.auth = {"app_id" : app_id,
                    "app_key" : app_key}

    def FlightSearch(self, source, destination,
                    dateofdeparture, dateofarrival=None,
                    seatingclass="E", adults=1, children=0, infants=0):
        
        if dateofarrival:
            dateda = "&dateofdeparture=%d\
                    &dateofarrival%d" % (dateofdeparture, dateofarrival)
        else:
            dateda = "&dateofdeparture=%d" % dateofdeparture

        return (requests.get(self.BASE + "search/" + 
                "?app_id=%s" % app_id + "&app_key=%s" % app_key + "&format=json" +
                "&source=%s" % source + "&destination=%s" % destination +
                dateda +
                "&seatingclass=%s" % seatingclass +
                "&adults=%d" % adults +
                "&children=%d" % children + "&infants=%d" % infants
                + "&counter=100"))

    def MinimumFare(self, source, destination, sdate, edate=None,
                    vertical="flight", mode=None, tclass=None):
        if edate:
            dateda = "&sdatte=%d&edate%d" % (sdate, edate)
        else:
            dateda = "&sdate=%d" % sdate
        strclass = "&vertical=%s" % vertical
        if mode:
            strclass = strclass + "&mode=" % mode
        if tclass:
            strclass = strclass + "&class=" % tclass

        return (requests.get(self.BASE + "stats/minfare/" + "?format=json" +
                "&source=%s" % source + "&destination=%s" % destination +
                strclass + dateda, params=self.auth).json())

    def BusSearch(self, source, destination,
                    dateofdeparture, dateofarrival=None):
        if dateofarrival:
            dateda = "&dateofdeparture=%d\
                    &dateofarrival%d" % (dateofdeparture, dateofarrival)
        else:
            dateda = "&dateofdeparture=%d" % dateofdeparture

        return (requests.get(self.BASE + "bus/search/" + "?format=json" +
                "&source=%s" % source + "&destination=%s" % destination +
                dateda, params=self.auth).json())

    def BusSeatMap(self, skey):
        return (requests.get(self.BASE + "bus/seatmap/" + "?format=json" +
                "&skey=%s" % skey,
                params=self.auth).json())

    def SearchHotelsByCity(self, city_id):
        return (requests.get(self.BASE + "voyager/" +
                "?method=hotels.get_hotels_data_by_city" +
                "&city_id=%d" % city_id, params=self.auth).json())

    def GetHotelData(self, id_list):
        id_list = str(id_list)\
                    .replace(" ", "")\
                    .replace("L", "")\
                    .replace(",", "%2C+")\
                    .replace("[", "%5B")\
                    .replace("]", "%5D")

        return (requests.get(self.BASE + "voyager/" +
                "?method=hotels.get_hotels_data" +
                "&id_list=%s" % id_list +
                "&id_type=_id", params=self.auth).json())

    def GetHotelPriceByCity(self, city_id, check_in, check_out):
        return (requests.get(self.BASE + "cyclone/" +
                "?city_id=%d" % city_id +
                "&check_in=%d" % check_in +
                "&check_out=%d" % check_out, params=self.auth).json())

# app_key = "Enter app_key"
# app_id = "Enter app_id"
# enter your app_key and app_id above 
GO = goibiboAPI(app_id, app_key)


FlightDetails = GO.FlightSearch("BLR", "DEL", 20161020)

with open('flights.txt', 'w') as outfile:
    outfile.writelines(FlightDetails.iter_lines())

uglyJSON = open("flights.txt", "r").read()
newDictionary = json.loads(str(uglyJSON))
prettyJSON = json.dumps(newDictionary, indent=4, sort_keys=True)

with open('flights.txt', 'w') as outfile:
    outfile.write(prettyJSON)

# print GO.MinimumFare("BLR", "HYD", 20161028)
# print GO.BusSearch("bangalore", "hyderabad", 20161028)
# print GO.BusSeatMap("vJ52KC0ymd0635qTD9bDDy9GHBkGl5FJMJje0aFX\
#                     _GQTyev_4N9Y62TTfrmS-Re3dCHl0-UxLq4AsoQ%3D")
# print GO.SearchHotelsByCity(6771549831164675055)
# print GO.GetHotelData([1017089108070373346, 6085103403340214927])
# print GO.GetHotelPriceByCity(6771549831164675055, 20161101, 20161102)