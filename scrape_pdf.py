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
    start_index = None
    end_index = None

# Filter the mapping based on the provided indices.
if start_index is not None and end_index is not None:
    filtered_mapping = {}
    for k, pages in kanumber_page_mapping.items():
        try:
            key_int = int(k)
        except ValueError:
            continue  # Skip keys that can't be converted to an integer.
        if start_index <= key_int <= end_index:
            filtered_mapping[k] = pages
else:
    filtered_mapping = kanumber_page_mapping

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
