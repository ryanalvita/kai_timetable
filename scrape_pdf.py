import sys
import camelot
import pandas as pd
from constants import kanumber_page_mapping, filepath

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

# Process each filtered mapping.
for kanumber, pages in filtered_mapping.items():
    page_start, page_end = pages
    pages_str = ",".join(str(i) for i in range(page_start, page_end + 1))

    tables = camelot.read_pdf(filepath=filepath, pages=pages_str)

    df = pd.DataFrame()
    for table in tables:
        df = pd.concat([df, table.df])

    output_filename = f"page/page{page_start}-{page_end}.csv"
    df.to_csv(output_filename, index=False)
    print(f"Saved {output_filename}")
