-- PostgreSQL schema for the site-selection analysis.
-- Load data/processed/metro_businesses.parquet into this table (see notebooks/ for the loader).

CREATE TABLE IF NOT EXISTS businesses (
    id                                  TEXT PRIMARY KEY,   -- DENUE establishment id
    nom_estab                           TEXT,
    codigo_act                          TEXT,               -- SCIAN activity code
    nombre_act                          TEXT,               -- SCIAN activity name
    categoria                           TEXT NOT NULL,      -- student-oriented category (src/config.py)
    per_ocu                             TEXT,               -- employee size band
    municipio                           TEXT,
    ageb                                TEXT,
    latitud                             DOUBLE PRECISION NOT NULL,
    longitud                            DOUBLE PRECISION NOT NULL,
    fecha_alta                          TEXT,
    dist_tec_campus_monterrey_m         NUMERIC,
    dist_uanl_ciudad_universitaria_m    NUMERIC,
    dist_udem_san_pedro_m               NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_businesses_categoria ON businesses (categoria);
CREATE INDEX IF NOT EXISTS idx_businesses_dist_tec ON businesses (dist_tec_campus_monterrey_m);

-- Example: competitors per category in distance rings around Campus Monterrey.
-- SELECT categoria,
--        COUNT(*) FILTER (WHERE dist_tec_campus_monterrey_m <= 500)  AS within_500m,
--        COUNT(*) FILTER (WHERE dist_tec_campus_monterrey_m <= 1000) AS within_1km,
--        COUNT(*) FILTER (WHERE dist_tec_campus_monterrey_m <= 2000) AS within_2km
-- FROM businesses
-- GROUP BY categoria
-- ORDER BY within_1km DESC;
