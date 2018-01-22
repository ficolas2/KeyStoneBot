# Created by Nicolas de Pineda Gutiérrez (Horned horn) 21/01/2018

from abc import ABCMeta, abstractmethod
from enum import Enum
import re

END_NUMBER_REGEX = re.compile("[0-9]+([\,\.][0-9]+)?\s*$")
DECIMALS = 3

class UnitType:

    def __init__( self ):
        self._multiples = {}
    
    def addMultiple( self, unit, multiple ):
        self._multiples[ multiple ] = unit;
        return self
        
    def getStringFromMultiple(self, value, multiple):
        return str(round(value / multiple, DECIMALS)) + self._multiples[multiple]
    
    def getString( self, value ):
        sortedMultiples = sorted(self._multiples, reverse=True)
        for multiple in sortedMultiples:
            if value > multiple:
                return self.getStringFromMultiple(value, multiple)
        return self.getStringFromMultiple( value, sortedMultiples[-1] )

DISTANCE = UnitType().addMultiple("m", 1).addMultiple( "km", 10**3 ).addMultiple( "cm", 10**-2).addMultiple( "mm", 10**-3).addMultiple( "µm", 10**-6).addMultiple( "nm", 10**-9)
AREA = UnitType().addMultiple( "m^2", 1 ).addMultiple( "km^2", 10**6 ).addMultiple( "cm^2", 10**-4).addMultiple( "mm^2", 10**-6)
VOLUME = UnitType().addMultiple( "L", 1 ).addMultiple( "mL", 10**-3 )
ENERGY = UnitType().addMultiple( "J", 1 ).addMultiple( "TJ", 10**12 ).addMultiple( "GJ", 10**9 ).addMultiple( "MJ", 10**6 ).addMultiple( "kJ", 10**3 ).addMultiple( "mJ", 10**-3 ).addMultiple( "µJ", 10**-6 ).addMultiple( "nJ", 10**-9 )
FORCE = UnitType().addMultiple( "N", 1 ).addMultiple( "kN", 10**3 ).addMultiple( "MN", 10**6 )
TORQUE = UnitType().addMultiple( "N*m", 1 )
VELOCITY = UnitType().addMultiple("m/s", 1).addMultiple( "km/s", 10**3 ).addMultiple( "cm/s", 10**-2).addMultiple( "mm/s", 10**-3)
MASS = UnitType().addMultiple( "g", 1 ).addMultiple( "kg", 10**3 ).addMultiple( "t", 10**6 ).addMultiple( "mg", 10**-3 ).addMultiple( "µg", 10**-6 )
TEMPERATURE = UnitType().addMultiple( "C", 1 )
PRESSURE = UnitType().addMultiple( "atm", 1 )

class Unit:
    def __init__( self, unitType, toSIMultiplication, toSIAddition ):
        self._unitType = unitType
        self._toSIMultiplication = toSIMultiplication
        self._toSIAddition = toSIAddition
    
    def toMetric( self, value ):
        return self._unitType.getString( ( value + self._toSIAddition ) * self._toSIMultiplication)
    
    @abstractmethod
    def convert( self, message ): pass

#NormalUnit class, that follow number + unit name.
class NormalUnit( Unit ):
    def __init__( self, regex, unitType, toSIMultiplication, toSIAddition = 0 ):
        super( NormalUnit, self ).__init__(unitType, toSIMultiplication, toSIAddition)
        self._regex = re.compile( regex + "(?![a-z])")
    
    def convert( self, message ):
        originalText = message.getText()
        iterator = self._regex.finditer( originalText )
        replacements = []
        for find in iterator:
            numberResult = END_NUMBER_REGEX.search( originalText[ 0 : find.start() ] )
            if numberResult is not None:
                repl = {}
                repl[ "start" ] = numberResult.start()
                repl[ "text"  ] = self.toMetric( float( numberResult.group() ) ) 
                repl[ "end" ] = find.end()
                replacements.append(repl)
        if len(replacements)>0:
            lastPoint = 0
            finalMessage = ""
            for repl in replacements:
                finalMessage += originalText[ lastPoint: repl[ "start" ] ] + repl[ "text" ]
                lastPoint = repl["end"]
            finalMessage += originalText[ lastPoint : ]
            message.setText(finalMessage)

# Class containing a string, for the modificable message, and a boolean
# to indicate if the message has been modified
class ModificableMessage:
    
    def __init__(self, text):
        self._text = text
        self._modified = False
        
    def getText(self):
        return self._text
    
    def setText(self, text):
        self._text = text
        self._modified = True
        
    def isModified(self):
        return self._modified
        
units = []

#Distance units
units.append( NormalUnit("inches|inch|in|\"|''", DISTANCE, 0.0254) )
units.append( NormalUnit("foot|feet|ft|'", DISTANCE, 0.3048) )
units.append( NormalUnit("miles|mile|mi", DISTANCE, 1609.344) )

#Area
# TODO in/ft/mi ^ 2
units.append( NormalUnit("acre|acres", AREA, 4046.8564224 ) )
#Volume
units.append( NormalUnit( "pints|pint|pt|p", VOLUME, 0.473176 ) )
units.append( NormalUnit( "quarts|quart|qt", VOLUME, 0.946353 ) )
units.append( NormalUnit( "gallons|gallon|gal", VOLUME, 3.78541 ) )

#Energy
# TODO

#Force
# TODO

#Torque
# TODO

#Velocity
# TODO

#Mass
units.append( NormalUnit( "ounces|ounce|oz", MASS, 28.349523125 ) )
units.append( NormalUnit( "pounds|pound|lbs|lb", MASS, 453.59237 ) )

#Temperature
units.append( NormalUnit("F|ºF", TEMPERATURE, 5/9, -32 ) )
#Pressure
units.append( NormalUnit( "pounds per square inch|lbf/in^2|psi", PRESSURE, 0.068046 ) )
 
#Processes a string, converting freedom units to science units.
def process(message):    
    modificableMessage = ModificableMessage(message)
    for u in units:
        u.convert(modificableMessage)
    if modificableMessage.isModified():
        return modificableMessage.getText()
