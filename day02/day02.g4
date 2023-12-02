grammar day02;
start_ : frame+ EOF;
frame: id=INT  time_start=time_stamp_ms '-->' time_end=time_stamp_ms home  airframe  camera  orientation;
time_stamp_ms: hh=INT ':' mm=INT ':' ss=INT ',' ms=INT;

home: 'HOME(' lat_lon ')' datetimestamp;
datetimestamp: yyyy=INT '-' mmmm=INT '-' dddd=INT  hh=INT ':' mm=INT ':' ss=INT;
lat_lon: lon_dir=('E'|'W') ':' lon_gps=FLOAT ',' lat_dir=('N'|'S') ':' lat_gps=FLOAT;
airframe: 'GPS(' lat_lon ',' alt_gps=FLOAT 'm)';

camera: 'ISO:' iso=INT 'SHUTTER:' shutter=INT  'EV:' exposure=FLOAT 'F-NUM:' f_num=FLOAT;

orientation: 'F.PRY' '(' frame_pry=pry '),' 'G.PRY' '(' gimbal_pry=pry ')';
pry: pitch=FLOAT '°,' roll=FLOAT '°,' yaw=FLOAT '°';

INT : [0-9]+ ;
FLOAT: '-'? [0-9]+ '.' [0-9]+;

WS : [ \t\r\n]+ -> skip ;
