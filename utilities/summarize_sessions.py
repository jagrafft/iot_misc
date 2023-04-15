import pyarrow as pa
import pyarrow.parquet as pq

from datetime import datetime
from pathlib import Path

colnames = ["session", "value", "minimum", "maximum", "range"]
date_format = "%Y-%m-%dT%H:%M:%S"
pq_files = list(Path(Path.home() / "data/leaven/parquet_datasets").glob("*.parquet"))
value_names = ["timestamp", "CO2", "C", "RH"]

data = {k: [] for k in colnames}

for p in pq_files:
    pf = pq.ParquetFile(p)
    session_name = p.name.split(".")[0]
    session_name = session_name[6 : len(session_name)]

    for (col, idx) in zip(value_names, range(pf.metadata.num_columns)):
        summary = pf.metadata.row_group(0).column(idx).statistics

        if col == "timestamp":
            min_val = datetime.strptime(summary.min, date_format).timestamp()
            max_val = datetime.strptime(summary.max, date_format).timestamp()
            summary_range = max_val - min_val
        else:
            min_val = summary.min
            max_val = summary.max
            summary_range = max_val - min_val

        data["session"].append(session_name)
        data["minimum"].append(min_val)
        data["maximum"].append(max_val)
        data["value"].append(col)
        data["range"].append(summary_range)

pq.write_table(
    pa.Table.from_pydict(data),
    Path(Path.home() / "data/leaven/session_summaries.parquet"),
)
