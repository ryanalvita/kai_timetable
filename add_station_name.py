import pandas as pd

df = pd.read_csv("parsed/station.csv")
df_routes = pd.read_csv("parsed/routes.csv", index_col=0)

# Create a dictionary mapping station codes to station names
station_name_mapping = dict(zip(df["station_code"], df["station_name"]))

# map df_routes["station_code"] to station names
df_routes = df_routes.rename(columns={"origin_station":"origin_station_code","destination_station":"destination_station_code"}) 

df_routes["origin_station_name"] = df_routes["origin_station_code"].map(station_name_mapping)
df_routes["destination_station_name"] = df_routes["destination_station_code"].map(station_name_mapping)

a = 1

df_routes.to_csv("parsed/routes.csv")


