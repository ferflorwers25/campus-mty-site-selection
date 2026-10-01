# Tableau Public dashboard

Link: *coming soon*

## Data files (`tableau_data/`)

| File | One row per | Key fields |
|---|---|---|
| `opportunity_grid.csv` | 250 m grid cell within 1.5 km of campus | `lat`, `lon`, `rank`, `youth_per_competitor` (score), `residents_18_24_500m`, `competitors_500m`, `nearest_competitor_m`, `dist_campus_m`, `direction` |
| `businesses_near_campus.csv` | DENUE business within 2.2 km of campus | `name`, `activity`, `category`, `employees`, `lat`, `lon`, `dist_campus_m`, `distance_ring` |
| `location_quotients.csv` | category × campus | `businesses_1km`, `metro_businesses`, `location_quotient` |
| `ageb_demand.geojson` | urban AGEB near campus (polygon) | `residents`, `residents_18_24`, `share_18_24` |

The files are regenerated from `data/processed/` and contain public INEGI data (DENUE 2026, Census 2020).
