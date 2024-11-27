CREATE VIEW IF NOT EXISTS vw_assets
AS
  SELECT
    a.asset_id,
    cat.category_id,
    cat.class_id,
    cat.class_name,
    cat.category_name,
    a.asset_name,
    a.asset_ticker
  FROM assets a
    INNER JOIN vw_categories cat USING (category_id);


CREATE VIEW IF NOT EXISTS vw_assets_state
AS
  WITH
    prepared AS (
      SELECT
        asset_id,
        amount,
        LAST_VALUE(amount) OVER (
          PARTITION BY asset_id
          ORDER BY value_datetime
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last,
        LAG(amount, 1, 0) OVER (
          PARTITION BY asset_id
          ORDER BY value_datetime
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS lag,
        FIRST_VALUE(amount) OVER (
          PARTITION BY asset_id
          ORDER BY value_datetime
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first
      FROM assets_values
    ),
    av AS (
      SELECT
        asset_id,
        last,
        lag,
        first,
        COALESCE(ROUND(CAST(last - lag as REAL) / lag, 3), 1) as last_lag_percent,
        COALESCE(ROUND(CAST(last - first as REAL) / first, 3), 1) as last_first_percent,
        COALESCE(ROUND(CAST(lag - first as REAL) / first, 3), 1) as lag_first_percent
      FROM prepared
      WHERE last = amount
    ),
    currency AS (
      SELECT
        IIF(config_value ->> '$.position' == 'before', (config_value ->> '$.symbol') || ' ', '') as before,
        IIF(config_value ->> '$.position' == 'after', ' ' || (config_value ->> '$.symbol'), '') as after,
        1 as flag
      FROM config
      WHERE config_name = 'currency'
      UNION ALL
      SELECT
        '' as before,
        '' as after,
        0 as flag
    )

  SELECT
    a.*,
    av.last,
    av.lag,
    av.first,
    av.last_lag_percent,
    av.last_first_percent,
    av.lag_first_percent,
    FORMAT('%s%,d%s', c.before, av.last / 100, c.after) as out_last,
    FORMAT('%s%,d%s', c.before, av.lag / 100, c.after) as out_lag,
    FORMAT('%s%,d%s', c.before, av.first / 100, c.after) as out_first,
    FORMAT(
      '%s%.1f%%',
      IIF(av.last_lag_percent > 0, '+', IIF(av.last_lag_percent < 0, char(8722), '')),
      ABS(av.last_lag_percent * 100)
    ) as out_last_lag_percent,
    FORMAT(
      '%s%.1f%%',
      IIF(av.last_first_percent > 0, '+', IIF(av.last_first_percent < 0, char(8722), '')),
      ABS(av.last_first_percent * 100)
    ) as out_last_first_percent,
    FORMAT(
      '%s%.1f%%',
      IIF(av.lag_first_percent > 0, '+', IIF(av.lag_first_percent < 0, char(8722), '')),
      ABS(av.lag_first_percent * 100)
    ) as out_lag_first_percent
  FROM av
    INNER JOIN vw_assets a USING (asset_id)
    CROSS JOIN (select before, after from currency order by flag desc limit 1) c;


CREATE VIEW IF NOT EXISTS vw_assets_values
AS
  WITH
    currency AS (
      SELECT
        IIF(config_value ->> '$.position' == 'before', (config_value ->> '$.symbol') || ' ', '') as before,
        IIF(config_value ->> '$.position' == 'after', ' ' || (config_value ->> '$.symbol'), '') as after,
        1 as flag
      FROM config
      WHERE config_name = 'currency'
      UNION ALL
      SELECT
        '' as before,
        '' as after,
        0 as flag
    )

  SELECT
    av.value_id,
    a.*,
    av.value_datetime as asset_value_datetime,
    av.amount,
    FORMAT('%s%,d%s', c.before, av.amount / 100, c.after) as out_amount
  FROM assets_values av
    INNER JOIN vw_assets a USING (asset_id)
    CROSS JOIN (select before, after from currency order by flag desc limit 1) c;


CREATE VIEW IF NOT EXISTS vw_categories
AS
  SELECT
    cat.category_id,
    c.class_id,
    c.class_name,
    cat.category_name
  FROM classes c
    INNER JOIN categories cat USING (class_id);


CREATE VIEW IF NOT EXISTS vw_structure_categories
AS
  SELECT
    sc.structure_id,
    c.*,
    sc.percentile,
    FORMAT('%.1f%%', sc.percentile / 10) as out_percentile

  FROM structure_categories sc
    INNER JOIN vw_categories c USING (category_id);


CREATE VIEW IF NOT EXISTS vw_portfolio
AS
  WITH
    prepared AS (
      SELECT
        structure_id,
        category_id,
        category_name,
        SUM(last) as amount,
        percentile
      FROM vw_assets_state
        INNER JOIN structure_categories USING (category_id)
      GROUP BY
        structure_id,
        category_id,
        category_name
    ),
    total AS (
      SELECT
        structure_id,
        category_id,
        SUM(amount) OVER (
          PARTITION BY structure_id
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as total
      FROM prepared
    ),
    currency AS (
      SELECT
        IIF(config_value ->> '$.position' == 'before', (config_value ->> '$.symbol') || ' ', '') as before,
        IIF(config_value ->> '$.position' == 'after', ' ' || (config_value ->> '$.symbol'), '') as after,
        1 as flag
      FROM config
      WHERE config_name = 'currency'
      UNION ALL
      SELECT
        '' as before,
        '' as after,
        0 as flag
    )

  SELECT
    structure_id,
    category_id,
    category_name,
    percentile as structure_percentile,
    FORMAT('%.1f%%', percentile / 10) as out_structure_percentile,
    amount,
    FORMAT('%s%,d%s', c.before, amount / 100, c.after) as out_amount, -- .%02d amount % 100
    total,
    FORMAT('%s%,d%s', c.before, total / 100, c.after) as out_total,
    CAST(ROUND(CAST(amount AS REAL) / total, 3) * 1000 AS INTEGER) as current_percentile,
    FORMAT('%.1f%%', ROUND(CAST(amount AS REAL) / total, 3) * 100) as out_current_percentile
  FROM prepared
    INNER JOIN total USING (structure_id, category_id)
    CROSS JOIN (select before, after from currency order by flag desc limit 1) c;
