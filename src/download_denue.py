"""Download the INEGI DENUE bulk file for Nuevo León (state code 19).

Usage:
    python src/download_denue.py

Writes the raw CSV to data/raw/denue_nl.csv. Raw data is not committed to git.
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = RAW_DIR / "denue_nl.csv"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {URL} ...")
    req = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=300) as resp:
        payload = resp.read()
    print(f"Downloaded {len(payload) / 1e6:.1f} MB")

    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        csvs = [n for n in zf.namelist() if n.lower().endswith(".csv") and "denue_inegi" in n.lower()]
        if not csvs:
            sys.exit(f"No DENUE CSV found in zip. Contents: {zf.namelist()}")
        # The zip also ships a data dictionary; keep it for documentation.
        for name in zf.namelist():
            if "diccionario" in name.lower() and name.lower().endswith(".csv"):
                (RAW_DIR / "diccionario_denue.csv").write_bytes(zf.read(name))
        OUT.write_bytes(zf.read(csvs[0]))
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
