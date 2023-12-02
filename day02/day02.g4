grammar day02;
start : game+ EOF;
game: 'Game' id=INT ':' colors (';' colors)* ;
colors: color_spec (',' color_spec)*;
color_spec: count=INT color=COLOR ;

COLOR: 'red' | 'blue' | 'green';
INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
