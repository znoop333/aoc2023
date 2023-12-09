grammar day08;
start : lr+=LR+ '\n' nodes+=node+ EOF;
node: base=ID '=' '(' left=ID ',' right=ID ')' '\n';


LR : 'L' | 'R';
ID: [A-Z][A-Z][A-Z];
INT : [0-9]+ ;
WS : [ \t]+ -> skip ;
