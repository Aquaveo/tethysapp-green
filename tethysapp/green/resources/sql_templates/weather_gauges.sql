SELECT weather_gauge_values.weather_gauge_id as "id",
       app_users_resources.name as "name",
       app_users_resources.description as "description",
       app_users_resources.location as "geometry",
       app_users_organization_resource_association.organization_id as "organization_id",
       app_users_organizations.name as "organization_name",
       MAX(CAST(weather_gauge_values.return_period as double precision)) AS "max_return_period",
       MIN(CAST(weather_gauge_values.return_period as double precision)) AS "min_return_period",
       AVG(CAST(weather_gauge_values.return_period as double precision)) AS "avg_return_period",
       MAX(weather_gauge_values.timestamp) AS "end_timestamp",
       MIN(weather_gauge_values.timestamp) AS "start_timestamp",
       MAX(weather_gauge_values.temperature) AS "max_temperature",
       MIN(weather_gauge_values.temperature) AS "min_temperature",
       AVG(weather_gauge_values.temperature) AS "avg_temperature",
       AVG(weather_gauge_values.dew_point) AS "avg_dew_point",
       MAX(weather_gauge_values.precip_accum) AS "max_precip_accum",
       MAX(weather_gauge_values.precip_rate) AS "max_precip_rate",
       MIN(weather_gauge_values.precip_rate) AS "min_precip_rate",
       AVG(weather_gauge_values.precip_rate) AS "avg_precip_rate",
       AVG(weather_gauge_values.humidity) AS "avg_humidity",
       MODE() WITHIN GROUP (ORDER BY weather_gauge_values.wind) as "wind",
       AVG(weather_gauge_values.speed) AS "avg_speed",
       AVG(weather_gauge_values.gust) AS "avg_gust",
       AVG(weather_gauge_values.pressure) AS "avg_pressure",
       AVG(weather_gauge_values.uv) AS "avg_uv",
       AVG(weather_gauge_values.solar) AS "avg_solar"
FROM weather_gauge_values
    FULL JOIN app_users_resources ON (weather_gauge_values.weather_gauge_id = app_users_resources.id)
    FULL JOIN app_users_organization_resource_association ON (app_users_organization_resource_association.resource_id = app_users_resources."id")
    FULL JOIN app_users_organizations ON (app_users_organizations.id = app_users_organization_resource_association."organization_id")
WHERE app_users_resources.type = 'weather_gauge_resource'
    AND location IS NOT NULL
    AND (%organization_id% = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' OR app_users_organization_resource_association.organization_id IN (%organization_id%))
    AND weather_gauge_values.timestamp >= CURRENT_TIMESTAMP - (%time_period% || ' hour')::interval
GROUP BY weather_gauge_values.weather_gauge_id,
       app_users_resources.name,
       app_users_resources.description,
       app_users_resources.location,
       app_users_organization_resource_association.organization_id,
       app_users_organizations.name
ORDER BY app_users_resources.name ASC