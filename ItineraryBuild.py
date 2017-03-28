import os
import sys
import datetime
from time import *
import copy
import pandas as pd
import numpy as np


cwd = os.getcwd()
sys.path.insert(0,cwd)
airlineDomainPath = os.path.join(cwd,'AirlineDomain')
if(airlineDomainPath not in sys.path):
    sys.path.append(airlineDomainPath)

commonPath = os.path.join(cwd,'Common')
if(commonPath not in sys.path):
    sys.path.append(commonPath)

from Station import *
from OD import *
from Flight import *
#from CommonFunctions import ListFunctions

class ItineraryRule(OD):
    def __init__(self,org,dst):
        OD.__init__(self,org,dst)
        self.circuity = 1
     
        self.mct = 30
        self.onlineConXTime = 30
        self.interlineConXTime = 30

        self.SinOnline = True
        self.SinInterline = False
        self.DoubleOnline = False
        self.DoubleInterline = False
        self.nonopOnline = True
        self.nonopPureOnline_Online = False
        self.nonopPureOnline_Interline = False
        self.nonopInterline = False

def populateFlts(skdLine,arpList,SKD):
    opInd = skdLine[1:2]
    aln = skdLine[2:4]
    fltNum = skdLine[5:9]
    org = getStation(arpList,skdLine[36:39])
    dst = getStation(arpList,skdLine[54:57])
    depTer = skdLine[52:53]
    arrTer = skdLine[70:71]
    depHour = int(skdLine[43:45])
    depMin = int(skdLine[45:47])
    arrHour = int(skdLine[61:63])
    arrMin = int(skdLine[63:65])
    depTZ = datetime.timezone(datetime.timedelta(hours = int(skdLine[47:50])))
    arrTZ = datetime.timezone(datetime.timedelta(hours = int(skdLine[65:68])))
    trfRestr = []
    if not skdLine[149:159].isspace():
        for x in skdLine[149:159]:
            if not x.isspace():
                trfRestr.append(TrafficRestriction[x])
    effDate = datetime.datetime(*strptime(skdLine[14:21], "%d%b%y")[:3])
    disDate = datetime.datetime(*strptime(skdLine[21:28], "%d%b%y")[:3])
    delta = disDate - effDate
    dow = skdLine[28:35]
    for i in range(delta.days+1):
        day = effDate + datetime.timedelta(days = i)
        depDateTime = datetime.datetime(day.year,day.month,day.day,depHour,depMin,tzinfo = depTZ)
        arrDateTime = datetime.datetime(day.year,day.month,day.day,arrHour,arrMin,tzinfo = arrTZ)
        if depHour > arrHour:
            arrDateTime = arrDateTime + datetime.timedelta(days = 1)
        if str(day.weekday()+1) in dow:
            flight = Flight(org,dst,aln,fltNum,i,opInd,depTer,arrTer,depDateTime,arrDateTime,trfRestr)
            SKD.append(flight)

def generateItineraries(org,dst,itinerary,itineraries):
    for flt in org.getOutboundFlts():
        itinerary.addFlights(flt)
        if itinerary.isItinerayValidTillNow():
            if flt.getDst() == dst:
                temp = copy.deepcopy(itinerary)
                itineraries.append(temp)
                itinerary.popLastFlight()
            else:
                generateItineraries(flt.getDst(),dst,itinerary,itineraries)
    if(not itinerary.isEmpty()):
        itinerary.popLastFlight()


def main():
    arpList = []
    SKD = []
    itineraries = []
    
    

    #read SKD
    with open('StandardSKD.ssim') as f:
        for line in f:
            if line[0:1] == '3':
                populateFlts(line,arpList,SKD)
                
    airportInfo = pd.read_csv('airportInfo.csv')
    for arp in arpList:
        arp.setLong_Latitude(airportInfo[airportInfo['ArpCode']== arp.getStationName()].lat.item(),
                             airportInfo[airportInfo['ArpCode']== arp.getStationName()].lon.item())
   

   

    itinerary = Itinerary(SKD[0].getOrg(),SKD[0].getDst())
    generateItineraries(SKD[0].getOrg(),SKD[0].getDst(),itinerary,itineraries)
    print("test generate Itineraries")
    for iti in itineraries:
        iti.printItinerary()
        print("************")
    
    
if __name__ == '__main__':
    main()

