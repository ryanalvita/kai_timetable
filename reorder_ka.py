import pandas as pd
import os

# for loop to parsed/KA folder
for file in os.listdir("parsed/KA"):
    df = pd.read_csv(f"parsed/KA/{file}", index_col=0)

    station_split = df["Stasiun"].str.extract(
        r"(?P<station_name>.*?)\s*\((?P<station_code>.*?)\)"
    )
    df = df.join(station_split)

    # Remove any parentheses from station_name (if any still exist)
    df["station_name"] = df["station_name"].str.replace(r"\s*\(.*?\)", "", regex=True)

    # Split 'Datang Berangkat' into two parts: the first token (arrival_time) and the second (departure_time)
    # If the first token is 'Ls' (or 'NaN') we set it to None
    df["arrival_time"] = df["Datang"].apply(
        lambda x: None if x == "Ls" or x == "NaN" else x
    )
    df["departure_time"] = df["Berangkat"]

    # Rename 'Keterangan' to 'notes'
    df = df.rename(columns={"Keterangan": "notes"})

    # Reorder columns to the desired output
    df = df[["station_name", "station_code", "arrival_time", "departure_time", "notes"]]

    df["station_name"] = df["station_name"].str.upper()
    df["station_code"] = df["station_code"].str.upper()

    df.to_csv(f"parsed/KA_reordered/{file}")

print(df)
