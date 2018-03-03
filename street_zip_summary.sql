--SQL used by postGIS to spatially join OpenStreeMap roads to Esri ZIP Code polygons
--jhickok 2018-02-01

SELECT 
osm_roads_ca.stname AS st_name,
zip.PO_NAME AS community,
zip.ZIP_CODE AS zip,
COUNT(osm_roads_ca.stname) as st_count
FROM (SELECT PO_NAME, ZIP_CODE, wkb_geometry FROM usa_zip_poly where STATE = 'CA') AS zip
join osm_roads_ca
ON ST_intersects(zip.wkb_geometry, osm_roads_ca.wkb_geometry)
GROUP BY osm_roads_ca.stname, zip.ZIP_CODE, zip.PO_NAME
ORDER BY osm_roads_ca.stname
;
