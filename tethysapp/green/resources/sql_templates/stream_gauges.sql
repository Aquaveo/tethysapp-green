SELECT stream_gauge_values.stream_gauge_id as "id",
       app_users_resources.name as "name",
       app_users_resources.description as "description",
       app_users_resources.location as "geometry",
       app_users_organization_resource_association.organization_id as "organization_id",
       app_users_organizations.name as "organization_name",
       MAX(stream_gauge_values.return_period) AS "max_return_period",
       MIN(stream_gauge_values.return_period) AS "min_return_period",
       AVG(stream_gauge_values.return_period) AS "avg_return_period",
       MIN(stream_gauge_values.timestamp) AS "start_timestamp",
       MAX(stream_gauge_values.timestamp) AS "end_timestamp",
       MAX(stream_gauge_values.level) AS "max_level",
       MIN(stream_gauge_values.level) AS "min_level",
       AVG(stream_gauge_values.level) AS "avg_level",
       MAX(stream_gauge_values.discharge) AS "max_discharge",
       MIN(stream_gauge_values.discharge) AS "min_discharge",
       AVG(stream_gauge_values.discharge) AS "avg_discharge"
FROM stream_gauge_values
    FULL JOIN app_users_resources ON (stream_gauge_values.stream_gauge_id = app_users_resources.id)
	FULL JOIN app_users_organization_resource_association ON (app_users_organization_resource_association.resource_id = app_users_resources."id")
    FULL JOIN app_users_organizations ON (app_users_organizations.id = app_users_organization_resource_association."organization_id")
WHERE app_users_resources.type = 'stream_gauge_resource'
    AND location IS NOT NULL
    AND (%organization_id% = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa' OR app_users_organization_resource_association.organization_id IN (%organization_id%))
    AND stream_gauge_values.timestamp >= CURRENT_TIMESTAMP - (%time_period% || ' hour')::interval
GROUP BY stream_gauge_values.stream_gauge_id,
       app_users_resources.name,
       app_users_resources.description,
       app_users_resources.location,
       app_users_organization_resource_association.organization_id,
       app_users_organizations.name
ORDER BY app_users_resources.name ASC