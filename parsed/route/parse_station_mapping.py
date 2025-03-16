import pandas as pd

df = pd.read_csv("station_raw_data.csv")


def is_single_alpha(val):
    val = str(val).strip()  # Convert to string and remove any surrounding whitespace
    return len(val) == 1 and val.isalpha()


mask = ~(
    df.iloc[:, 0].apply(
        is_single_alpha
    )  # Excludes rows where the first column is a single alphabet character (e.g., "D")
    | df.iloc[:, 0]
    .astype(str)
    .str.contains(
        "Nama stasiun"
    )  # Excludes rows containing "Nama stasiun" in the first column
)

# Apply the mask to the DataFrame
df_clean = df[mask].reset_index(drop=True)

a = 1
