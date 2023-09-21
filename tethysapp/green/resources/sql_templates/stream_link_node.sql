SELECT lnd_link_node_dataset_files."projectFileID" AS "projectFileID",
       lnd_link_node_dataset_files."channelInputFileID" AS "channelInputFileID",
       lnd_link_node_dataset_files."name" AS "lndName",
       lnd_link_node_dataset_files."fileExtension" AS "lndExtension",
       cif_nodes."linkID" AS "linkID",
       cif_nodes."nodeNumber" AS "nodeNumber",
       cif_nodes.x AS "x",
       cif_nodes.y AS "y",
       cif_nodes.elevation AS "elevation",
       lnd_node_datasets.status AS status,
       CASE
            WHEN '%timesummary%' = 'Min' THEN
                ROUND(MIN(lnd_node_datasets."value")::numeric, 6)
            WHEN '%timesummary%' = 'Max' THEN
                ROUND(MAX(lnd_node_datasets."value")::numeric, 6)
            ELSE
                ROUND(AVG(lnd_node_datasets."value")::numeric, 6)
        END AS "value",
       cif_nodes.geometry AS "geometry"
FROM lnd_node_datasets
    FULL JOIN cif_nodes ON (cif_nodes.id = lnd_node_datasets."streamNodeID")
    FULL JOIN lnd_link_node_dataset_files ON (lnd_link_node_dataset_files.id = lnd_node_datasets."linkNodeDatasetFileID")
WHERE lnd_link_node_dataset_files."projectFileID" = %scenarioid%
  AND lnd_link_node_dataset_files."fileExtension" = '{{ variable }}'
GROUP BY cif_nodes."nodeNumber", lnd_link_node_dataset_files."projectFileID",
         lnd_link_node_dataset_files."channelInputFileID", lnd_link_node_dataset_files."name",
         lnd_link_node_dataset_files."fileExtension", cif_nodes."linkID", cif_nodes.x, cif_nodes.y,
         cif_nodes.elevation, lnd_node_datasets.status, cif_nodes.geometry
ORDER BY cif_nodes."linkID", cif_nodes."nodeNumber"
