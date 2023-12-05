grammar day05;
start :'seeds:' seed_list maps+ EOF;
seed_list: seeds+=INT+;
maps:
'seed-to-soil' 'map:' seed_to_soil_map+=map+ |
'soil-to-fertilizer' 'map:' soil_to_fertilizer_map+=map+ |
'fertilizer-to-water' 'map:' fertilizer_to_water_map+=map+ |
'water-to-light' 'map:' water_to_light_map+=map+ |
'light-to-temperature' 'map:' light_to_temperature_map+=map+ |
'temperature-to-humidity' 'map:' temperature_to_humidity_map+=map+ |
'humidity-to-location' 'map:' humidity_to_location_map+=map+
;

map: destination=INT source=INT length=INT;

INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
