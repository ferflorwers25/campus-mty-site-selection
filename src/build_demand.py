"""Phase 2: add demand (2020 Census) to the supply analysis and score candidate locations.

Usage:
    python src/build_demand.py

Inputs:  data/raw/censo2020_ageb_mza_nl.csv, data/raw/marco_geo_2020/19a.shp,
         data/processed/metro_businesses.parquet (from build_study_area.py)
Outputs: data/processed/ageb_demand.geojson   urban AGEBs near the campus with population
         data/processed/grid_scores.csv        250 m grid with demand, supply and opportunity score
"""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

from config import CAMPUSES, TARGET_CAMPUS

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

GRID_STEP_M = 250       # cell size
GRID_RADIUS_M = 1500    # study area around the campus
WALK_RADIUS_M = 500     # catchment for demand and competition (~6 minutes on foot)
TARGET_CATEGORIES = ["papeleria", "fotocopiado_impresion"]
POP_COLS = ["POBTOT", "P_18A24", "P_15A17", "TVIVPARHAB"]


def load_census_ageb() -> pd.DataFrame:
    c = pd.read_csv(RAW / "censo2020_ageb_mza_nl.csv", dtype=str, encoding="utf-8-sig")
    # AGEB totals are the rows with block code 000 and a real AGEB code.
    c = c[(c["MZA"] == "000") & (c["AGEB"] != "0000")].copy()
    c["CVEGEO"] = c["ENTIDAD"] + c["MUN"] + c["LOC"] + c["AGEB"]
    for col in POP_COLS:
        # INEGI masks small counts with '*' and missing values with 'N/D'; treat both as unknown.
        c[col] = pd.to_numeric(c[col], errors="coerce")
    return c[["CVEGEO", "NOM_MUN"] + POP_COLS]


def campus_point(crs):
    lat0, lon0 = CAMPUSES[TARGET_CAMPUS]
    return gpd.GeoSeries(gpd.points_from_xy([lon0], [lat0]), crs=4326).to_crs(crs).iloc[0]


def build_grid(crs) -> gpd.GeoDataFrame:
    center = campus_point(crs)
    offsets = np.arange(-GRID_RADIUS_M, GRID_RADIUS_M + 1, GRID_STEP_M)
    pts = [(center.x + dx, center.y + dy) for dx in offsets for dy in offsets
           if np.hypot(dx, dy) <= GRID_RADIUS_M]
    grid = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*zip(*pts)), crs=crs)
    grid["cell_id"] = range(len(grid))
    return grid


def main() -> None:
    agebs = gpd.read_file(RAW / "marco_geo_2020" / "19a.shp")  # projected CRS in meters (INEGI LCC)
    crs = agebs.crs
    census = load_census_ageb()
    agebs = agebs.merge(census, on="CVEGEO", how="left")
    agebs["ageb_area"] = agebs.geometry.area

    grid = build_grid(crs)
    center = campus_point(crs)
    buffers = grid.copy()
    buffers["geometry"] = grid.buffer(WALK_RADIUS_M)

    # Areal interpolation: each AGEB contributes in proportion to the share of its area inside the buffer.
    inter = gpd.overlay(buffers[["cell_id", "geometry"]], agebs[["CVEGEO", "ageb_area", *POP_COLS, "geometry"]],
                        how="intersection", keep_geom_type=True)
    w = inter.geometry.area / inter["ageb_area"]
    demand = pd.DataFrame({"cell_id": inter["cell_id"]})
    for col in POP_COLS:
        demand[col] = inter[col] * w
    demand = demand.groupby("cell_id").sum(min_count=1).round(0)

    biz = pd.read_parquet(OUT / "metro_businesses.parquet")
    biz = gpd.GeoDataFrame(biz, geometry=gpd.points_from_xy(biz.longitud, biz.latitud), crs=4326).to_crs(crs)
    biz = biz[biz.distance(center) <= GRID_RADIUS_M + WALK_RADIUS_M + 500]
    targets = biz[biz.categoria.isin(TARGET_CATEGORIES)]

    grid["competitors_500m"] = [int((targets.distance(p) <= WALK_RADIUS_M).sum()) for p in grid.geometry]
    grid["nearest_competitor_m"] = [float(targets.distance(p).min()) for p in grid.geometry]
    grid["businesses_250m"] = [int((biz.distance(p) <= 250).sum()) for p in grid.geometry]
    grid = grid.merge(demand, left_on="cell_id", right_index=True, how="left")

    # Opportunity score: young adults (18-24) within a 5-6 minute walk per existing stationery/copy shop.
    grid["youth_per_competitor"] = (grid["P_18A24"] / (grid["competitors_500m"] + 1)).round(0)
    grid["score_pct"] = grid["youth_per_competitor"].rank(pct=True).round(3)

    ll = grid.to_crs(4326)
    grid["lat"], grid["lon"] = ll.geometry.y.round(6), ll.geometry.x.round(6)
    grid["dist_campus_m"] = grid.distance(center).round(0)
    grid.drop(columns="geometry").to_csv(OUT / "grid_scores.csv", index=False)

    near = agebs[agebs.intersects(buffers.union_all())].to_crs(4326)
    near["share_18_24"] = (near["P_18A24"] / near["POBTOT"]).round(3)
    near.drop(columns="ageb_area").to_file(OUT / "ageb_demand.geojson", driver="GeoJSON")

    matched = agebs["POBTOT"].notna().mean()
    print(f"Urban AGEBs: {len(agebs):,} · matched to census: {matched:.1%}")
    print(f"AGEBs near campus: {len(near)} · grid cells: {len(grid)}")
    print(grid.sort_values("youth_per_competitor", ascending=False)
              .head(10)[["cell_id", "lat", "lon", "dist_campus_m", "POBTOT", "P_18A24",
                         "competitors_500m", "nearest_competitor_m", "businesses_250m", "youth_per_competitor"]]
              .to_string(index=False))


if __name__ == "__main__":
    main()
