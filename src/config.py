"""Project settings. Coordinates are approximate campus centroids: verify on a map before publishing."""

# name -> (lat, lon)
CAMPUSES = {
    "tec_campus_monterrey": (25.6514, -100.2895),  # Av. Eugenio Garza Sada 2501 Sur
    "uanl_ciudad_universitaria": (25.7260, -100.3120),  # San Nicolás de los Garza
    "udem_san_pedro": (25.6610, -100.4200),  # San Pedro Garza García
}
TARGET_CAMPUS = "tec_campus_monterrey"

# Distance rings in meters for the catchment analysis.
RINGS_M = [500, 1000, 2000]
CATCHMENT_M = 1000  # main radius used for location quotients

# Monterrey metro municipalities used as the baseline (accent-insensitive match).
METRO_MUNICIPALITIES = [
    "monterrey",
    "san pedro garza garcia",
    "san nicolas de los garza",
    "guadalupe",
    "apodaca",
    "santa catarina",
    "general escobedo",
    "juarez",
    "garcia",
]

# Student-oriented business categories, matched on DENUE's official activity name (nombre_act).
# Regexes run against lowercase, accent-stripped text. Check matches against the data dictionary.
CATEGORIES = {
    # Order matters: first match wins ("Farmacias con minisúper" must land in farmacia).
    "farmacia": r"farmacia",
    "cafeteria": r"cafeteria",
    "restaurante": r"restaurante",
    "bar": r"\bbares?\b|cantina|centros nocturnos",
    "minisuper_conveniencia": r"minisuper|tiendas de conveniencia",
    "abarrotes": r"abarrotes",
    "papeleria": r"papeleria",
    "fotocopiado_impresion": r"fotocopiado|impresion de formas continuas|revelado e impresion",
    "gimnasio": r"acondicionamiento fisico",
    "lavanderia": r"lavanderia",
    "belleza_barberia": r"salones y clinicas de belleza|peluqueria|barberia",
}

# Activities excluded from every category (wholesale, manufacturing, publishing, public sector):
# they are not walk-in competitors for a small student-oriented business.
EXCLUDE = r"al por mayor|fabricacion|edicion de|industrias conexas|sector publico"
