import camelot
import pandas as pd

from constants import kanumber_page_mapping, filepath

for kanumbers, pages in kanumber_page_mapping.items():
    page_start, page_end = pages
    pages = ",".join([str(i) for i in range(page_start, page_end + 1)])

    tables = camelot.read_pdf(filepath=filepath, pages=pages)

    df = pd.DataFrame()
    for table in tables:
        df = pd.concat([df, table.df])
    df.to_csv(f"page/page{page_start}-{page_end}.csv")

# # Cleanup for routes
# df = df.drop(0, axis=1)
# df = df.drop(7, axis=1)

# columns = {
#     1: "train_number",
#     2: "train_class",
#     3: "train_name",
#     4: "train_route",
#     5: "departure_time",
#     6: "arrival_time",
# }

# df = df.rename(columns=columns)

# # Parse route
# df[["origin_station", "destination_station"]] = df["train_route"].str.split(
#     "-", expand=True
# )
# df = df.drop("train_route", axis=1)
# df = df.drop("index", axis=1)

# df = df.reset_index()

# df.to_csv("routes.csv")

# a = 1
