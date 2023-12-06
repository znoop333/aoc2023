grammar day05;
start :'seeds:' seed_list maps+ EOF;
seed_list: seeds+=INT+;
maps: source=MAP_NAME '-to-' destination=MAP_NAME 'map:' entries+=map+;

MAP_NAME: 'seed'
| 'soil'
| 'fertilizer'
| 'water'
| 'light'
| 'temperature'
| 'humidity'
| 'location' ;

map: destination=INT source=INT length=INT;

INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
