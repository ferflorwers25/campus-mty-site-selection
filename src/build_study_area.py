"""Clean DENUE for the Monterrey metro area and compute competition around each campus.

Usage:
    python src/build_study_area.py

Inputs:  data/raw/denue_nl.csv
Outputs: data/processed/metro_businesses.parquet
         data/processed/category_by_zone.csv
         data/processed/data_quality_report.txt
"""
from __future__ import annotations

import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

from config import CAMPUSES, CATCHMENT_M, CATEGORIES, EXCLUDE, METRO_MUNICIPALITIES, RINGS_M

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "denue_nl.csv"
OUT_DIR = ROOT / "data" / "processed"

KEEP_COLS = [
    "id", "nom_estab", "codigo_act", "nombre_act", "per_ocu",
    "municipio", "ageb", "latitud", "longitud", "fecha_alta",
]


def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    return "".join(c for c in text if not unicodedata.combining(c)).lower().strip()


def haversine_m(lat1, lon1, lat2, lon2):
    """Great-circle distance in meters (vectorized)."""
    r = 6_371_000
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = p2 - p1
    dlmb = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def read_denue(path: Path) -> pd.DataFrame:
    # INEGI files have historically shipped as latin-1; fall back if that changes.
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc, dtype=str, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path}")


def categorize(nombre_act: pd.Series) -> pd.Series:
    norm = nombre_act.map(strip_accents)
    out = pd.Series("otro", index=nombre_act.index)
    # First match wins, so order in CATEGORIES matters.
    for cat, pattern in reversed(list(CATEGORIES.items())):
        out[norm.str.contains(pattern, regex=True, na=False)] = cat
    out[norm.str.contains(EXCLUDE, regex=True, na=False)] = "otro"
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = read_denue(RAW)
    df.columns = [strip_accents(c) for c in df.columns]
    missing = [c for c in KEEP_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"Expected columns not found: {missing}. Got: {list(df.columns)}")

    report = [f"Raw rows (Nuevo León): {len(df):,}"]
    df = df[KEEP_COLS].copy()

    df["municipio_norm"] = df["municipio"].map(strip_accents)
    df = df[df["municipio_norm"].isin(METRO_MUNICIPALITIES)]
    report.append(f"Rows in Monterrey metro: {len(df):,}")

    before = len(df)
    df = df.drop_duplicates(subset="id")
    report.append(f"Duplicate ids removed: {before - len(df):,}")

    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    bad_geo = df["latitud"].isna() | df["longitud"].isna() | ~df["latitud"].between(24.5, 26.5) | ~df["longitud"].between(-101.5, -99.5)
    report.append(f"Rows dropped for missing/out-of-range coordinates: {bad_geo.sum():,}")
    df = df[~bad_geo]

    df["categoria"] = categorize(df["nombre_act"])

    for name, (lat, lon) in CAMPUSES.items():
        df[f"dist_{name}_m"] = haversine_m(df["latitud"], df["longitud"], lat, lon).round(0)

    df.to_parquet(OUT_DIR / "metro_businesses.parquet", index=False)

    # Counts by category for each campus catchment + the whole metro, then location quotients.
    zones = {"metro": pd.Series(True, index=df.index)}
    for name in CAMPUSES:
        zones[name] = df[f"dist_{name}_m"] <= CATCHMENT_M
    counts = pd.DataFrame({z: df.loc[mask, "categoria"].value_counts() for z, mask in zones.items()}).fillna(0).astype(int)
    shares = counts / counts.sum()
    for name in CAMPUSES:
        counts[f"lq_{name}"] = (shares[name] / shares["metro"]).round(2)
    counts.sort_values(f"lq_{list(CAMPUSES)[0]}").to_csv(OUT_DIR / "category_by_zone.csv", index_label="categoria")

    target = list(CAMPUSES)[0]
    for r in RINGS_M:
        report.append(f"Businesses within {r} m of {target}: {(df[f'dist_{target}_m'] <= r).sum():,}")
    (OUT_DIR / "data_quality_report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
