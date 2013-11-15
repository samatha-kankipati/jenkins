Raw = load '/user/lavaqe/cfsmall' using PigStorage(' ') as (mmm:chararray,
dd:int,
time:bytearray,
ip1:chararray,
foo1:chararray,
ip2:chararray,
ip3:chararray,
longdate:chararray,
httpop:chararray,
uri:chararray,
httpver:chararray,
httpcode:int,
hyphen1:bytearray,
foo2:bytearray,
foo3:bytearray,
hyphen2:bytearray,
hyphen3:bytearray,
hyphen4:bytearray,
foo:bytearray,
hyphen5:bytearray,
latency:double
);

Projected = foreach Raw generate httpop;
Grouped = foreach (group Projected by httpop) generate $0,COUNT($1) parallel 3;

Final = filter Grouped by
($0 == 'DELETE') or
($0 == 'GET') or
($0 == 'HEAD') or
($0 == 'POST') or
($0 == 'PUT');


store Final into 'result8' using PigStorage(',');