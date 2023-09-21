SELECT north, south, east, west, rows, columns,
       ST_Polygon(raster) AS geometry,
       {% if units == 'metric' %}
       ST_Area(ST_Polygon(raster))/POWER(1000,2) as area
       {% else %}
       ST_Area(ST_Polygon(raster))/POWER(5280,2) as area
       {% endif %}
FROM raster_maps
WHERE "projectFileID" = %scenarioid% AND "fileExtension" = '{{ boundary_raster }}'