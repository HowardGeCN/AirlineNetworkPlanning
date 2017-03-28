
class Station:
    
    def __init__(self,name):
        self._stationName = name
        self._outboundFlts = []
    def getStationName(self):
        return self._stationName
    def addOutboundFlt(self,flt):
        self._outboundFlts.append(flt)
    def getOutboundFlts(self):
        return self._outboundFlts
    def setLong_Latitude(self,lat,lon):
        self._lat = lat
        self._lon = lon
    def getLat(self):
        return self._lat
    def getLon(self):
        return self._lon
    def printOutboundFlts(self):
        for flt in self.__outboundFlts:
            flt.printFlt()

def getStation(arpList,name):
    isFound = False
    for arp in arpList:
        if arp.getStationName() == name:
            isFound = True
            return arp
    if not isFound:
        arp =Station(name)
        arpList.append(arp)
        return arp
                

