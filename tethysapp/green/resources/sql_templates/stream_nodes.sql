SELECT prj_project_files.id AS "projectFileID",
       cif_channel_input_files.id AS "channelInputFileID",
       cif_links.id AS "linkID",
       prj_project_files.srid AS "srid",
       cif_nodes."nodeNumber" AS "nodeNumber",
       cif_nodes.x AS "x",
       cif_nodes.y AS "y",
       cif_nodes.elevation AS "elevation",
       cif_nodes.geometry AS "geometry"
FROM cif_nodes
    FULL JOIN cif_links ON (cif_links.id = cif_nodes."linkID")
    FULL JOIN cif_channel_input_files ON (cif_channel_input_files.id = cif_links."channelInputFileID")
    FULL JOIN prj_project_files ON (prj_project_files."channelInputFileID" = cif_channel_input_files.id)
WHERE prj_project_files.id = %scenarioid%
    AND cif_nodes."nodeNumber" != 1
    AND cif_nodes."nodeNumber" != (
        SELECT MAX(cif_nodes."nodeNumber") from cif_nodes
        WHERE cif_nodes."linkID"=cif_links."linkNumber"
        GROUP BY cif_nodes."linkID")
    AND (
        SELECT COUNT(*) from cif_nodes AS CN
        FULL JOIN cif_links ON (cif_links.id = CN."linkID")
        WHERE cif_links."channelInputFileID" = %scenarioid%
        AND CN.x = cif_nodes.x
        AND CN.y = cif_nodes.y
        GROUP BY CN.x) = 1
ORDER BY cif_nodes."linkID", cif_nodes."nodeNumber"