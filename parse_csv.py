import pandas as pd
import re
import sys

from constants import kanumber_page_mapping


def clean_initial_dataframe(raw_df):
    """
    Drop the extra first (dummy) column if present and remove header rows.
    Header rows are identified as those where the value in the second column is "No.".
    Then, assign proper column names.
    """
    # If the first column is dummy (for example, named "Unnamed: 0" or all missing), drop it.
    first_col = raw_df.columns[0]
    if raw_df[first_col].isnull().all() or str(first_col).lower().startswith("unnamed"):
        df = raw_df.drop(columns=first_col)
    else:
        df = raw_df.copy()

    # After dropping the dummy column, we expect 5 columns.
    # The header row in the CSV is: "No.,Stasiun dan Perhentian,Datang,Berangkat,Keterangan"
    # Set the column names explicitly.
    df.columns = ["No.", "Stasiun", "Datang", "Berangkat", "Keterangan"]

    # Remove rows that are header rows (where the "No." column equals "No.").
    df = df[df["No."].astype(str).str.strip().str.lower() != "no."]

    return df


def split_no_value(no_val, stasiun_val):
    """
    If the 'No.' cell contains extra text (e.g. "1 some extra info"), split it.
    Return the number part and (if the station cell is blank) use the extra text as station name.
    """
    if pd.isna(no_val):
        return no_val, stasiun_val
    s = str(no_val).strip()
    m = re.match(r"^(\d+)\s+(.*)$", s)
    if m:
        number = m.group(1)
        extra_text = m.group(2).strip()
        if pd.isna(stasiun_val) or str(stasiun_val).strip() == "":
            stasiun_val = extra_text
        return number, stasiun_val
    return s, stasiun_val


def clean_no_and_stasiun(df):
    """
    For each row in the DataFrame (which has columns: No., Stasiun, Datang, Berangkat, Keterangan):
      - If "No." is empty, then try to extract the number and the actual station name from the beginning of "Stasiun".
      - If "No." is non-empty but contains extra text (e.g. "10 extra info"), then extract just the number.
    Returns the cleaned DataFrame.
    """

    def clean_row(row):
        no_val = row["No."]
        stasiun_val = row["Stasiun"]

        # If "No." is missing or empty, try to extract from "Stasiun"
        if pd.isna(no_val) or str(no_val).strip() == "":
            if pd.notna(stasiun_val):
                s = str(stasiun_val).strip()
                m = re.match(r"^(\d+)\s+(.*)$", s)
                if m:
                    row["No."] = m.group(1)
                    row["Stasiun"] = m.group(2)
                    return row

        # If "No." is non-empty, check if it contains extra text
        else:
            s = str(no_val).strip()
            m = re.match(r"^(\d+)\s+(.*)$", s)
            if m:
                row["No."] = m.group(1)
                # Only update "Stasiun" if it's empty
                if pd.isna(stasiun_val) or str(stasiun_val).strip() == "":
                    row["Stasiun"] = m.group(2)
                return row

        return row

    return df.apply(clean_row, axis=1)


def split_into_blocks(df):
    """
    Split the cleaned DataFrame into blocks.
    Each new block is created when the (cleaned) "No." column value has its first token equal to "1".
    (That is, the station number resets to 1.)
    """
    blocks = []
    current_block_rows = []

    # Iterate over rows in order.
    for idx, row in df.iterrows():
        # Get the cleaned "No." value as a string and extract its first token.
        no_str = str(row["No."]).strip()
        first_token = no_str.split()[0] if no_str else ""
        # If we find a row where the first token is "1", this signals the start of a new block.
        if first_token == "1":
            if current_block_rows:
                blocks.append(pd.DataFrame(current_block_rows, columns=df.columns))
                current_block_rows = []
        # Append the current row (as a Series) to the current block.
        current_block_rows.append(row)
    # Append the last block, if any.
    if current_block_rows:
        blocks.append(pd.DataFrame(current_block_rows, columns=df.columns))
    return blocks

# Parse command-line arguments.
# Expected usage: python scrape_pdf.py <start_index> <end_index>
if len(sys.argv) >= 3:
    start_index = int(sys.argv[1])
    end_index = int(sys.argv[2])
else:
    # If not provided, process all entries.
    start_index = 0
    end_index = len(kanumber_page_mapping) - 1

# Filter the mapping based on the provided indices.
mapping_keys = list(kanumber_page_mapping.keys())
filtered_keys = mapping_keys[start_index : end_index + 1]

# Build a filtered mapping dictionary
filtered_mapping = {key: kanumber_page_mapping[key] for key in filtered_keys}

for kanumbers, pages in filtered_mapping.items():
    page_start, page_end = pages
    pages = ",".join([str(i) for i in range(page_start, page_end + 1)])

    df = pd.read_csv(f"parsed/page/page{page_start}-{page_end}.csv")
    df = clean_initial_dataframe(df)
    df = clean_no_and_stasiun(df)
    df_blocks = split_into_blocks(df)

    # Validate blocks with kanumbers
    assert len(kanumbers) == len(
        df_blocks
    ), f"Expected {len(kanumbers)} blocks, got {len(df_blocks)}"

    # Save each block to a separate CSV file
    for kanumber, block in zip(kanumbers, df_blocks):
        block.to_csv(f"parsed/KA/KA{kanumber}.csv", index=False)