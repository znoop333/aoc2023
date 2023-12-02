grammar day02;
start : game+ EOF;
game: 'Game' id=INT ':' draw (';' draw)* ;
draw: colors+;
colors: count=INT color=COLOR ;

COLOR: 'red' | 'blue' | 'green';
INT : [0-9]+ ;
WS : [, \t\r\n]+ -> skip ;
