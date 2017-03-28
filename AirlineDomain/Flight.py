from enum import Enum
from geopy.distance import great_circle

class TrafficRestriction(Enum):
    A = 1  # No boarding this city (flight item is not displayed and cannot be sold)
    B = 2  # Not valid for connections
    C = 3  # Not valid for international connections
    D = 4  # Valid for international online connections only, except if D, E, or G restrictions apply into and out of all online connect points
    E = 5  # Valid for online connections only, except if D, E, or G restrictions apply into and out of all online connect points
    F = 6  # Not valid for interline connections
    G = 7  # Valid for Online Connections Only; except if D, E, or G restrictions apply into and out of all online connect points (Note: Proper application of this rule is complicated).
    H = 8  # Not valid for connections and the direct service is not displayed (flight can be sold)
    I = 9  # No boarding/deplaning this city (flight item is not displayed and cannot be sold)
    K = 10 # Valid for connections only
    M = 11 # Valid for international online stopovers only
    N = 12 # Valid for international connections only
    O = 13 # Valid for international online connections only
    Q = 14 # Valid for international online stopover and connections only
    T = 15 # Valid for online stopovers only
    V = 16 # Valid for stopover and connections only
    W = 17 # Valid for international stopover and connections only
    X = 18 # Valid for online stopover and connections only
    Y = 19 # Valid for online connections only
    Z = 20 # Multiple traffic restrictions apply


class OD:
    def __init__(self,org,dst,demand = 0):
        self._org = org
        self._dst = dst
        self._demand = demand
    def getOrg(self):
        return self._org
    def getDst(self):
        return self._dst
class Flight(OD):
    def __init__(self,org,dst,aln,fltnum,dow,opInd,depTer,arrTer,
                 depDateTime,arrDateTime,trafficRestriction):
        OD.__init__(self,org,dst)
        self._airline = aln
        self._fltnum = fltnum
        self._dow = dow
        self._opInd = opInd
        self._depTer = depTer
        self._arrTer = arrTer
        self._depDateTime = depDateTime
        self._arrDateTime = arrDateTime
        self._trafficRestriction = trafficRestriction
        self._org.addOutboundFlt(self)
    def isHost(self):
        if self._airline in ['MU','FM']:
            return True
        else:
            return False
    def getDepTime(self):
        return self._depDateTime
    def getArrTime(self):
        return self._arrDateTime
    def getMiles(self):
        dep = (self._org.getLat(),self._org.getLon())
        arr = (self._dst.getLat(),self._dst.getLon())
        return  great_circle(dep,arr).miles
    def getElapInMins(self):
        return (self._arrDateTime - self._depDateTime).seconds/60
    
    def printFlt(self):
        print(self._airline,self._fltnum,
              self._org.getStationName(),self._depTer,self._depDateTime,
              self._dst.getStationName(),self._arrTer,self._arrDateTime,
              self.getMiles(),self.getElapInMins())
    
    
class Itinerary(OD):
    def __init__(self,org,dst):
        OD.__init__(self,org,dst)
        self._flights = []
    def addFlights(self,flight):
        self._flights.append(flight)
    def popLastFlight(self):
        self._flights.pop()
    def isEmpty(self):
        if len(self._flights) ==0:
            return True
        else:
            return False
    def isItinerayValidTillNow(self):
        if len(self._flights) > 3: #maximum double connection
            return False
        else:
            return True
    def getCircuity(self):
        distance = 0
        for flt in self._flights:
            distance = distance + flt.getMiles()
        dep = (self._org.getLat(),self._org.getLon())
        arr = (self._dst.getLat(),self._dst.getLon())
        return  distance/great_circle(dep,arr).miles
    def getElapInMins(self):
        diff = (self._flights[len(self._flights)-1].getArrTime() -
                      self._flights[0].getDepTime())
        return (diff.days*86400 + diff.seconds)/60
    
    def printItinerary(self):
        #print(self._org.getStationName(),self._dst.getStationName())
        print(self.getCircuity(),self.getElapInMins())
        for flight in self._flights:
            flight.printFlt()
    
        
