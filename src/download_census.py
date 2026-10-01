"""Download INEGI 2020 Census data for phase 2 (demand).

Usage:
    python src/download_census.py

Downloads two things for Nuevo León (state code 19):
1. Census 2020 results by AGEB and city block (population, age groups, households).
2. Marco Geoestadístico 2020: the AGEB boundaries needed to place census data on the map.

Everything lands in data/raw/ (gitignored).
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

CENSUS_URL = (
    "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/"
    "ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip"
)
# Marco Geoestadístico 2020, Nuevo León only. If INEGI moves it, see the fallback message below.
GEO_URL = (
    "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/"
    "productos/geografia/marcogeo/889463807469/19_nuevoleon.zip"
)


def fetch(url: str) -> bytes:
    print(f"Downloading {url} ...")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=600) as resp:
        data = resp.read()
    print(f"  {len(data) / 1e6:.1f} MB")
    return data


def get_census() -> None:
    with zipfile.ZipFile(io.BytesIO(fetch(CENSUS_URL))) as zf:
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv") and "conjunto_de_datos" in n.lower()]
        out = RAW_DIR / "censo2020_ageb_mza_nl.csv"
        out.write_bytes(zf.read(csvs[0]))
        for name in zf.namelist():
            if "diccionario" in name.lower() and name.lower().endswith(".csv"):
                (RAW_DIR / "diccionario_censo2020.csv").write_bytes(zf.read(name))
    print(f"  saved {out}")


def get_geo() -> None:
    # Keep only the urban AGEB layer (19a.*) to save space.
    geo_dir = RAW_DIR / "marco_geo_2020"
    geo_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(fetch(GEO_URL))) as zf:
        wanted = [n for n in zf.namelist() if Path(n).stem.lower() == "19a"]
        if not wanted:  # some releases nest the shapefiles inside another zip
            inner = [n for n in zf.namelist() if n.lower().endswith(".zip")]
            print(f"  19a layer not found directly; archive contains: {zf.namelist()[:15]}")
            if inner:
                with zipfile.ZipFile(io.BytesIO(zf.read(inner[0]))) as z2:
                    for n in z2.namelist():
                        if Path(n).stem.lower() == "19a":
                            (geo_dir / Path(n).name).write_bytes(z2.read(n))
        for n in wanted:
            (geo_dir / Path(n).name).write_bytes(zf.read(n))
    print(f"  saved: {sorted(p.name for p in geo_dir.iterdir())}")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    get_census()
    try:
        get_geo()
    except (HTTPError, URLError) as err:
        print(
            f"\nCould not download the Marco Geoestadístico ({err}).\n"
            "Download 'Marco Geoestadístico 2020 – Nuevo León' manually from\n"
            "https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463807469\n"
            "and unzip the 19a.* files into data/raw/marco_geo_2020/"
        )


if __name__ == "__main__":
    main()
