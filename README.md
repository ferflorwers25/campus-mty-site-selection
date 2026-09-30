# What business should open near Tec de Monterrey? A site-selection analysis with INEGI data

> **Portfolio case study.** The client below is a simulated scenario. All data is public and comes from INEGI (Mexico's national statistics institute).
> 🚧 **Status: in progress.** Results will be added as each phase ends.

## Business problem

An entrepreneur wants to open a small business within walking distance of **Tec de Monterrey, Campus Monterrey**, an area with steady demand from students, staff and nearby residents. They have one question:

**Which type of student-oriented business is under-supplied around the campus, and where exactly should it go?**

## Questions this project answers

1. How many businesses of each type (cafés, stationery shops, gyms, laundromats, copy shops, etc.) are within 500 m, 1 km and 2 km of the campus?
2. Compared with the Monterrey metro area and with two other university zones (UANL Ciudad Universitaria, UDEM), which categories are **under- or over-represented** near the Tec? (location quotient)
3. Where are the **gaps**: blocks with high foot traffic potential but few competitors?
4. What is the final recommendation: which business, where, and with what risks?

## Data

| Source | What it contains | Use |
|---|---|---|
| [DENUE – INEGI](https://www.inegi.org.mx/app/mapa/denue/default.aspx) | Every registered business in Mexico: activity (SCIAN), size, coordinates | Supply / competition |
| Censo de Población 2020 – INEGI (by AGEB) *(phase 2)* | Population by urban block group | Demand |

Raw data is not committed. It can be rebuilt with the scripts in `src/`.

## Method

- **Cleaning:** filter to the 9 metro municipalities, remove duplicate IDs, drop invalid coordinates, and map official activity names into business categories. Every step is logged in `data/processed/data_quality_report.txt`.
- **Distance:** haversine distance from every business to each campus.
- **Location quotient (LQ):** a category's share of businesses near the campus divided by its share across the metro. LQ < 1 means under-represented.
- **Benchmark:** the same metrics for UANL and UDEM, to separate "normal near universities" from "specific to the Tec."

## Tech stack

Python (Pandas, NumPy) · PostgreSQL · SQL · Jupyter · Folium (maps) · Tableau Public (dashboard)

## How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src
python download_denue.py      # downloads DENUE for Nuevo León
python build_study_area.py    # cleans data, computes distances and location quotients
```

## Project structure

```
├── src/
│   ├── config.py              # campuses, radii, municipalities, categories
│   ├── download_denue.py      # data download
│   └── build_study_area.py    # cleaning + distances + location quotients
├── sql/schema.sql             # PostgreSQL schema + example queries
├── notebooks/                 # exploration and analysis
├── dashboard/                 # Tableau Public link and screenshots
├── docs/                      # business memo
└── data/                      # raw/ and processed/ (gitignored)
```

## Roadmap

- [x] Project structure, download and cleaning pipeline
- [ ] Phase 1: supply, competition by category and distance ring
- [ ] Phase 2: demand, population by AGEB (Censo 2020)
- [ ] Phase 3: opportunity score per block and interactive map
- [ ] Tableau Public dashboard
- [ ] One-page business memo with the recommendation

## Limitations

- DENUE lists registered establishments; informal businesses are under-counted.
- Campus coordinates are approximate centroids.
- Location quotients show relative supply, not profitability.

## Author

**Fernando Flores**: Data Analyst · Backend · AI Automation · B.S. Innovation & Development Engineering, Tec de Monterrey (BI concentration)
[LinkedIn](https://linkedin.com/in/fffa)
