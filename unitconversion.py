#Area
units.append( NormalUnit("in(ch(es)?)? ?(\^2|squared)", DISTANCE, 0.00064516) )    #inch squared
units.append( NormalUnit("f(oo|ee)?t ?(\^2|squared)", DISTANCE, 0.092903) )        #foot squared
units.append( NormalUnit("mi(les?)? ?(\^2|squared)", DISTANCE, 2589990) )          #mile squared
units.append( NormalUnit("acres?", AREA, 4046.8564224 ) )                          #acre

#Volume
units.append( NormalUnit( "pints?|pt|p", VOLUME, 0.473176 ) )    #pint
units.append( NormalUnit( "quarts?|qt", VOLUME, 0.946353 ) )    #quart
units.append( NormalUnit( "gal(lons?)?", VOLUME, 3.78541 ) )    #galon

#Energy
units.append( NormalUnit("ft( |\*)?lbf?|foot( |-)pound", ENERGY, 1.355818) )    #foot-pound
units.append( NormalUnit("btu", ENERGY, 1055.06) )                              #btu

#Force
units.append( NormalUnit("pound( |-)?force|lbf", FORCE, 4.448222) )    #pound-force

#Torque
units.append( NormalUnit("Pound(-| )?foot|lbf( |\*)?ft", TORQUE, 1.355818) )    #pound-foot

#Velocity
units.append( NormalUnit("miles? per hour|mph", VELOCITY, 0.44704) )    #miles per hour

#Temperature
units.append( NormalUnit("º?F|(degrees? )?farenheit", TEMPERATURE, 5/9, -32 ) )    #Degrees freedom

#Pressure
units.append( NormalUnit( "pounds?((-| )?force)? per square in(ch)?|lbf\/in\^2|psi", PRESSURE, 0.068046 ) ) #Pounds per square inch

#Mass
units.append( NormalUnit( "ounces?|oz", MASS, 28.349523125 ) )    #ounces
units.append( NormalUnit( "pounds?|lbs?", MASS, 453.59237 ) )     #pounds
units.append( NormalUnit( "stones?|st", MASS, 6350.2293318 ) )    #stones

#Distance units
units.append( NormalUnit("in(ch(es)?)?|\"|''", DISTANCE, 0.0254) )  #inch
units.append( NormalUnit("f(oo|ee)?t|'", DISTANCE, 0.3048) )        #foot
units.append( NormalUnit("mi(les?)?", DISTANCE, 1609.344) )         #mile
units.append( NormalUnit("yd|yards?", DISTANCE, 0.9144) )           #yard
