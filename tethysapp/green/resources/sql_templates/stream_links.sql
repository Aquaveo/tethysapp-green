SELECT prj_project_files.id AS "projectFileID",
       cif_channel_input_files.id AS "channelInputFileID",
       prj_project_files.srid AS "srid",
       cif_links."linkNumber" AS "linkNumber",
       cif_links.type AS "type",
       cif_links."numElements" AS "numElements",
       cif_links.dx AS "dx",
       cif_links.erode AS "erode",
       cif_links.subsurface AS "subsurface",
       cif_links."downstreamLinkID" AS "downstreamLinkID",
       cif_links."numUpstreamLinks" AS "numUpstreamLinks",
       cif_links.geometry AS "geometry"
FROM cif_links
    FULL JOIN cif_channel_input_files ON (cif_channel_input_files.id = cif_links."channelInputFileID")
    FULL JOIN prj_project_files ON (prj_project_files."channelInputFileID" = cif_channel_input_files.id)
WHERE prj_project_files.id = %scenarioid%
ORDER BY cif_links."linkNumber"