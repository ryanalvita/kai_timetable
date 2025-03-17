import pandas as pd

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# df = pd.read_csv("parsed/route.csv", index_col=0)
# train_names = df.train_name.unique()
# table_name = "train"
# for train_name in train_names:
#     db_record = (
#         supabase.table(table_name=table_name)
#         .select("name")
#         .eq("name", train_name)
#         .execute()
#     )

#     if db_record.data:
#         continue
#     json = {"name": train_name}
#     response = supabase.table(table_name=table_name).upsert(json=json).execute()

# class_names = df.class_name.unique()
# table_name = "class"
# for class_name in class_names:
#     db_record = (
#         supabase.table(table_name=table_name)
#         .select("name")
#         .eq("name", class_name)
#         .execute()
#     )

#     if db_record.data:
#         continue
#     json = {"name": class_name}
#     response = supabase.table(table_name=table_name).upsert(json=json).execute()

# for ix, row in df.iterrows():
#     train_name = row["train_name"]
#     class_name = row["class_name"]
#     train_id = (
#         supabase.table(table_name="train").select("id").eq("name", train_name).execute()
#     ).data[0]["id"]

#     if "ARGO" in class_name or "EKSEKUTIF" in class_name:
#         class_name = "EKSEKUTIF"
#         class_id = (
#             supabase.table(table_name="class")
#             .select("id")
#             .eq("name", class_name)
#             .execute()
#         ).data[0]["id"]
#         json = {
#             "train_id": train_id,
#             "class_id": class_id,
#         }
#         response = supabase.table(table_name="train_class").upsert(json=json).execute()

#     if "BISNIS" in class_name:
#         class_name = "BISNIS"
#         class_id = (
#             supabase.table(table_name="class")
#             .select("id")
#             .eq("name", class_name)
#             .execute()
#         ).data[0]["id"]
#         json = {
#             "train_id": train_id,
#             "class_id": class_id,
#         }
#         response = supabase.table(table_name="train_class").upsert(json=json).execute()

#     if "EKONOMI" in class_name:
#         class_name = "EKONOMI"
#         class_id = (
#             supabase.table(table_name="class")
#             .select("id")
#             .eq("name", class_name)
#             .execute()
#         ).data[0]["id"]
#         json = {
#             "train_id": train_id,
#             "class_id": class_id,
#         }
#         response = supabase.table(table_name="train_class").upsert(json=json).execute()

# # for loop to parsed/KA folder
# for file in os.listdir("parsed/KA_reordered")[:104]:
#     df = pd.read_csv(f"parsed/KA_reordered/{file}", index_col=0)
#     train_station_names, train_station_codes = (
#         df.station_name.unique(),
#         df.station_code.unique(),
#     )
#     for train_station_name, train_station_code in zip(
#         train_station_names, train_station_codes
#     ):
#         json = {
#             "name": train_station_name,
#             "code": train_station_code,
#         }
#         response = (
#             supabase.table(table_name="station")
#             .upsert(json=json, ignore_duplicates=True, on_conflict="code")
#             .execute()
#         )

## Add route
# route = pd.read_csv("parsed/route.csv", index_col=0)

# for ix, row in route.iterrows():
#     train_name = row["train_name"]
#     train_id = (
#         supabase.table(table_name="train").select("id").eq("name", train_name).execute()
#     ).data[0]["id"]

#     origin_station_id = (
#         supabase.table(table_name="station")
#         .select("id")
#         .eq("code", row["origin_station_code"])
#         .execute()
#     ).data[0]["id"]
#     destination_station_id = (
#         supabase.table(table_name="station")
#         .select("id")
#         .eq("code", row["destination_station_code"])
#         .execute()
#     ).data[0]["id"]
#     json = {
#         "ka_number": row["ka_number"],
#         "train_id": train_id,
#         "origin_station_id": origin_station_id,
#         "destination_station_id": destination_station_id,
#         "departure_time": row["departure_time"],
#         "arrival_time": row["arrival_time"],
#     }
#     response = supabase.table(table_name="route").upsert(json=json).execute()


## Add stop
# route = pd.read_csv("parsed/route.csv", index_col=0)
# for file in os.listdir("parsed/KA_reordered"):
#     df = pd.read_csv(f"parsed/KA_reordered/{file}", index_col=0)
#     ka_number = file.lstrip("KA").rstrip(".csv")
#     for ix, row in df.iterrows():
#         station_name = row["station_name"]
#         station_code = row["station_code"]
#         route_id = (
#             supabase.table(table_name="route")
#             .select("id")
#             .eq("ka_number", ka_number)
#             .execute()
#         ).data[0]["id"]
#         station_id = (
#             supabase.table(table_name="station")
#             .select("id")
#             .eq("code", station_code)
#             .execute()
#         ).data[0]["id"]
#         json = {
#             "route_id": route_id,
#             "station_id": station_id,
#             "arrival_time": row["arrival_time"],
#             "departure_time": row["departure_time"],
#             "order": ix - 1,
#         }
#         response = supabase.table(table_name="stop").upsert(json=json).execute()

# city = pd.read_csv("parsed/city.csv", index_col=0)
# for ix, row in city.iterrows():
#     json = {
#         "name": row["name"],
#     }
#     response = (
#         supabase.table(table_name="city")
#         .upsert(json=json, ignore_duplicates=True)
#         .execute()
#     )

# station = pd.read_csv("parsed/station.csv", index_col=0)
# station_supabase = supabase.table(table_name="station").select("*").execute()

# for ix, row in station.iterrows():
#     json = {
#         "name": row["name"],
#     }
#     response = (
#         supabase.table(table_name="city")
#         .upsert(json=json, ignore_duplicates=True)
#         .execute()
#     )

# a = 1
