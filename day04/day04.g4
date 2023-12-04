grammar day04;
start : card+ EOF;
card: 'Card' id=INT ':' win+=INT+ '|' have+=INT+;

INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
