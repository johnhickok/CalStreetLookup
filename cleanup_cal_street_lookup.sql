-- Consider testing and running these SQL snippets
-- one expression at a time

create table cal_street_lookup_temp as
select * from cal_street_lookup;

drop table if exists cal_street_lookup;

create table cal_street_lookup as
select * from
(select distinct
regexp_replace(street, '[^a-zA-Z0-9\. ]', '', 'g') as street,
city,
zip,
streetcount
from cal_street_lookup_temp) as clean1
where clean1.street is not null
and clean1.street > ''
and clean1.street not like '%,%'
and clean1.city not like '%,%'
and clean1.zip not like '%,%'
order by clean1.street;

delete from cal_street_lookup
where street in
(' ',
'  Avenue',
'  Road',
'  Street',
'  Vermont',
' A',
' North ')
;
drop table geo_cal_street_lookup_temp
;