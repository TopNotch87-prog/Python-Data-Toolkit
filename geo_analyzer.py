import pandas as pd
import spacy
import folium
from collections import Counter

nlp = spacy.load("en_core_web_sm")

KENYAN_TOWNS = {
    "Nairobi": (-1.286389, 36.817223),
    "Mombasa": (-4.043477, 39.668206),
    "Kisumu": (-0.091702, 34.768000),
    "Nakuru": (-0.303099, 36.080025),
    "Eldoret": (0.514277, 35.269779),
    "Thika": (-1.033260, 37.069330),
    "Machakos": (-1.517683, 37.263414),
    "Nyeri": (-0.416667, 36.950000),
    "Meru": (0.050000, 37.650000),
    "Kitale": (1.016667, 35.000000),
    "Malindi": (-3.219186, 40.116890)
}


def extract_locations(df):

    text = " ".join(
        df.fillna("")
          .astype(str)
          .values.flatten()
    )

    doc = nlp(text)

    locations = []

    for ent in doc.ents:

        if ent.label_ in ["GPE", "LOC"]:
            locations.append(ent.text.strip())

    return Counter(locations)


def kenya_only(location_counts):

    verified = {}

    for location, count in location_counts.items():

        for town in KENYAN_TOWNS:

            if location.lower() == town.lower():

                verified[town] = count

    return verified


def export_excel(results,
                 filename="location_report.xlsx"):

    df = pd.DataFrame(
        results.items(),
        columns=["Location", "Count"]
    )

    df = df.sort_values(
        "Count",
        ascending=False
    )

    df.to_excel(
        filename,
        index=False
    )

    print(
        f"Saved Excel report: {filename}"
    )


def create_map(results,
               filename="kenya_map.html"):

    kenya_map = folium.Map(
        location=[-0.0236, 37.9062],
        zoom_start=6
    )

    for town, count in results.items():

        if town in KENYAN_TOWNS:

            lat, lon = KENYAN_TOWNS[town]

            folium.CircleMarker(
                location=[lat, lon],
                radius=max(5, min(count, 50)),
                popup=f"{town}: {count}",
                fill=True
            ).add_to(kenya_map)

    kenya_map.save(filename)

    print(
        f"Saved map: {filename}"
    )


def run_geo_analysis(df):

    locations = extract_locations(df)

    kenya_locations = kenya_only(
        locations
    )

    print("\nTOP LOCATIONS\n")

    for loc, count in sorted(
        kenya_locations.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(
            f"{loc:<20} {count}"
        )

    export_excel(kenya_locations)

    create_map(kenya_locations)

    return kenya_locations
