from abc import ABCMeta, abstractmethod
from enum import Enum
import re

END_NUMBER_REGEX = re.compile("[0-9]+([\,\.][0-9]+)?\s*$")
DECIMALS = 3

class UnitTypes( Enum ):
    DISTANCE = "m"
    AREA="m^2"
    VOLUME="L"
    ENERGY="J"
    FORCE="N"
    TORQUE="N*m"
    VELOCITY="m/s"
    MASS="g"
    TEMPERATURE="C"
    PRESSURE="atm"

class Unit:
    def __init__( self, toSI, unitType ):
        self._unitType = unitType
        self._toSI = toSI
    
    def toSI( self, number ):
        return str(round(number * self._toSI, DECIMALS)) + " " + self._unitType.value
    
    @abstractmethod
    def convert( self, message ): pass


class NormalUnit( Unit ):
    def __init__( self, regex, toSI, unitType ):
        super( NormalUnit, self ).__init__(toSI, unitType);
        self._regex = re.compile( regex + "(?![a-z])")
    
    def convert( self, message ):
        iterator = self._regex.finditer( message["text"] )
        replacements = []
        for find in iterator:
            numberResult = END_NUMBER_REGEX.search( message[ "text" ][ 0 : find.start() ] )
            if numberResult is not None:
                repl = {}
                repl[ "start" ] = numberResult.start()
                repl[ "text"  ] = self.toSI( float( numberResult.group() ) ) 
                repl[ "end" ] = find.end()
                replacements.append(repl)
        if len(replacements)>0:
            message["modified"] = True
            lastPoint = 0
            finalMessage = ""
            for repl in replacements:
                finalMessage += message[ "text" ][ lastPoint: repl[ "start" ] ] + repl[ "text" ]
                lastPoint = repl["end"]
            finalMessage += message[ "text" ][ lastPoint : ]
            message["text"] = finalMessage
        return message

units = []

units.append( NormalUnit("inches|inch|in", 0.0254, UnitTypes.DISTANCE) )
units.append( NormalUnit("foot|feet|ft", 0.3048, UnitTypes.DISTANCE) )
units.append( NormalUnit("miles|mile|mi", 1609.344, UnitTypes.DISTANCE) )

units.append( NormalUnit("pounds|pound|lb", 453.59237, UnitTypes.MASS) )
message = { "modified": False, "text" : "a 3.5 inch 5 feet, 3 miles, 5 pounds dick, 5 million" }
for u in units:
  message = u.convert(message);
  
if message["modified"]:
    print("I think @___ meant to say \"" + message["text"] + "\", please forgive him")
