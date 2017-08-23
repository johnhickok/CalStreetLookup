SELECT 
roads.name AS st_name,
zip_codes.name AS community,
zip_codes.zip_code AS zip,
COUNT(roads.name) as st_count
FROM zip_codes
join roads
ON ST_intersects(zip_codes.geom, roads.geom)
GROUP BY roads.name, zip_codes.zip_code, zip_codes.name
ORDER BY roads.name
;