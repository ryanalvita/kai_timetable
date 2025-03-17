import pandas as pd 

# import station data with cities and geographical coordinates
url = "https://portaldata.kemenhub.go.id/api/sigita/dp_stasiun_ka?&format=json"
df = pd.read_json(url)

# drop duplicate on "kodkod" column
df = df.drop_duplicates(subset="kodkod")

# extract the station code, station name, city, latitude, and longitude
df = df[["kodkod", "kabkot", "lat", "lon", "srs_id"]]
df.rename(columns={
    "kodkod":"station_code",
    "kabkot":"city",
    "lat":"latitude",
    "lon":"longitude"
},  inplace=True)

# format the column "station_code" into string
df["station_code"] = df['station_code'].astype(str) 

# remove rows with "-" in the "station_code" column
df = df[df["station_code"] != "-"]

# import the station data
df_station = pd.read_csv("parsed/station.csv")
df_station["station_code"] = df_station['station_code'].astype(str) 

# merge the station DataFrame with the city, latitude, and longitude
df_station = pd.merge(df_station,df, on="station_code").reset_index(drop=True)

# save the DataFrame to a CSV file
df_station.to_csv("parsed/station.csv")

