print("Imports...")
import base64
import cv2
import pyarrow as pa
import pyarrow.parquet as pq
import redis

r = redis.Redis()
r.select(7)

print("Redis Streams...")
streams = [x.decode() for x in r.scan()[1]]

print("Check for envar 'BASE_IMAGES_PATH'...")

serialize_images = False

# from pathlib import Path
# base_image_path = Path("")
# serialize_images = True

if serialize_images:
    print(f"serialize_images = {serialize_images}")
    print(f"Serailizing images at base path '{base_image_path}'...")
else:
    print(f"serialize_images = {serialize_images}")
    print("Skipping serialization of images...")


for stream in streams:
    print()
    print(f"Transform XStream '{stream}'...")
    print("\t1. Decode rows...")
    rows = {
        x[0].decode(): {k.decode(): v.decode() for (k, v) in x[1].items()}
        for x in r.xrange(f"{stream}")
    }

    d = {"timestamp": [], "CO2": [], "C": [], "RH": []}

    if serialize_images:
        d["jpeg"] = []

    print("\t2. Reshape rows to columns...")
    for row in rows.items():
        if serialize_images:
            img_path = Path(
                base_image_path
                / f"{stream[:6]}fswebcam_{stream[6:len(stream)]}"
                / "images"
                / f"{row[1]['timestamp'].replace(':', '')}.jpeg"
            )

            if img_path.exists():
                print(f"Converting {img_path} to bytestring...")
                img = cv2.imread(f"{img_path}")
                b64_str = base64.b64encode(img[1]).decode("UTF-8")
                d["jpeg"].append(b64_str)
            else:
                print(f"{img_path} not found, skipping...")
                d["jpeg"].append(None)

        for k in row[1].keys():
            d[k].append(row[1][k])

    print("\t3. Format data for Arrow Table...")
    d["timestamp"] = pa.array(d["timestamp"], pa.string())
    d["CO2"] = pa.array([float(v) for v in d["CO2"]], type=pa.float64())
    d["C"] = pa.array([float(v) for v in d["C"]], type=pa.float64())
    d["RH"] = pa.array([float(v) for v in d["RH"]], type=pa.float64())

    if serialize_images:
        d["jpeg"] = pa.array(d["jpeg"], type=pa.string())

    print(f"\t4. Write '{stream}.parquet'...")
    if serialize_images:
        parquet_file_name = f"{stream}_img.parquet"
    else:
        parquet_file_name = f"{stream}.parquet"

    pq.write_table(pa.table(d), parquet_file_name)

    print("DONE")

print("FINISHED")
