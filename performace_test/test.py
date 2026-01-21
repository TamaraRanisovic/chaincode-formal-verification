import requests
import time
import statistics
import json
import csv
import os


INVOKE_URL = "http://localhost:3000/invoke"
QUERY_URL = "http://localhost:3000/query"
CHANNEL_ID = "mychannel"
CHAINCODE_ID = "basic"

N = 10000  # broj proizvoda
REQUEST_TIMEOUT = 60
CSV_FILE = "test_summary.csv"


def create_product(product_id, product_name):
    payload = [
        ("channelid", CHANNEL_ID),
        ("chaincodeid", CHAINCODE_ID),
        ("function", "CreateProduct"),
        ("args", product_id),
        ("args", product_name),
        ("args", "250.99"),
        ("args", "100"),
        ("args", "seller123"),
    ]
    requests.post(INVOKE_URL, data=payload, timeout=REQUEST_TIMEOUT)


def read_product(product_id):
    url = (
        f"{QUERY_URL}"
        f"?channelid={CHANNEL_ID}"
        f"&chaincodeid={CHAINCODE_ID}"
        f"&function=ReadProduct"
        f"&args={product_id}"
    )
    requests.get(url, timeout=REQUEST_TIMEOUT)


def get_all_products():
    url = (
        f"{QUERY_URL}"
        f"?channelid={CHANNEL_ID}"
        f"&chaincodeid={CHAINCODE_ID}"
        f"&function=GetAllProducts"
    )
    requests.get(url, timeout=REQUEST_TIMEOUT)


def delete_product(product_id):
    payload = [
        ("channelid", CHANNEL_ID),
        ("chaincodeid", CHAINCODE_ID),
        ("function", "DeleteProduct"),
        ("args", product_id),
    ]
    requests.post(INVOKE_URL, data=payload, timeout=REQUEST_TIMEOUT)


def create_products_batch(n):
    products = []
    for i in range(1, n + 1):
        products.append([
            f"product{i}",
            f"Smart phone {i}",
            "250.99",
            "100",
            "seller123"
        ])

    payload = [
        ("channelid", CHANNEL_ID),
        ("chaincodeid", CHAINCODE_ID),
        ("function", "CreateProductsBatch"),
        ("args", json.dumps(products))
    ]

    start = time.time()
    requests.post(INVOKE_URL, data=payload, timeout=REQUEST_TIMEOUT)
    return (time.time() - start) * 1000  # total batch time



create_times = []
for i in range(1, N + 1):
    start = time.time()
    create_product(f"product{i}", f"Product {i}")
    create_times.append((time.time() - start) * 1000)

create_mean = statistics.mean(create_times)

read_times = []
for i in range(1, N + 1):
    start = time.time()
    read_product(f"product{i}")
    read_times.append((time.time() - start) * 1000)

read_mean = statistics.mean(read_times)

getall_times = []
for _ in range(3):
    get_all_products()

for _ in range(N):
    start = time.time()
    get_all_products()
    getall_times.append((time.time() - start) * 1000)

getall_mean = statistics.mean(getall_times)

for i in range(1, N + 1):
    delete_product(f"product{i}")

batch_total_time = create_products_batch(N)


file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, mode="a", newline="") as csvfile:
    writer = csv.writer(csvfile)

    if not file_exists:
        writer.writerow([
            "num_products",
            "create_mean_ms",
            "read_mean_ms",
            "getall_mean_ms",
            "batch_total_ms"
        ])

    writer.writerow([
        N,
        f"{create_mean:.2f}",
        f"{read_mean:.2f}",
        f"{getall_mean:.2f}",
        f"{batch_total_time:.2f}"
    ])


print("\n=== SUMMARY ===")
print(f"Products: {N}")
print(f"Create mean:   {create_mean:.2f} ms")
print(f"Read mean:     {read_mean:.2f} ms")
print(f"GetAll mean:   {getall_mean:.2f} ms")
print(f"Batch total:   {batch_total_time:.2f} ms")
print(f"\nResults saved to {CSV_FILE}")