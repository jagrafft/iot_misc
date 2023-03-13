print("Imports...")
import pyarrow as pa
import pyarrow.parquet as pq
import redis

r = redis.Redis()
r.select(7)

print("Redis Streams...")
streams = [x.decode() for x in r.scan()[1]]

for stream in streams:
    print(f"Transform XStream '{stream}'...")
    print("1. Decode rows...")
    rows = {x[0].decode():{k.decode():v.decode() for (k,v) in x[1].items()} for x in r.xrange(f"{stream}")}

    d = {"timestamp": [], "CO2": [], "C": [], "RH": []}
    
    print("2. Reshape rows to columns...")
    for row in rows.items():
        for k in row[1].keys():
            d[k].append(row[1][k])

    print("3. Format data for Arrow Table...")
    d["timestamp"] = pa.array(d["timestamp"], pa.string())

    for k in d.keys():
        if k != "timestamp":
            d[k] = pa.array([float(v) for v in d[k]], type=pa.float64())

    print(f"4. Write '{stream}.parquet'...")
    pq.write_table(pa.table(d), f"{stream}.parquet")

    print("DONE\n")
print("FINISHED")
