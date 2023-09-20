def compute_raster_stats(session, raster_table, id, raster_column='raster'):
    """
    Compute statistics on raster: count, sum, mean, stddev, min, max

    Returns:
        dict<min, max, mean, count, sum, stddev>: stats dictionary.
    """
    default_stats = {
        'min': None,
        'max': None,
        'mean': None,
        'count': None,
        'sum': None,
        'stddev': None
    }

    sql = "SELECT (stats).* " \
          "FROM (" \
          "SELECT ST_SummaryStats({raster_column}) as stats " \
          "FROM {raster_table} " \
          "WHERE id={id}) AS foo"\
        .format(
            raster_column=raster_column,
            raster_table=raster_table,
            id=id
        )

    res = session.execute(sql)

    for row in res:
        return dict(row)

    return default_stats
