import pandas as pd
import matplotlib.pyplot as plt

# =========================
# READ CSV
# =========================
df = pd.read_csv("test_summary.csv")

num_products = df["num_products"]
create_mean = df["create_mean_ms"]
read_mean = df["read_mean_ms"]
getall_mean = df["getall_mean_ms"]
batch_total = df["batch_total_ms"]

# =========================
# 1. Create vs Read
# =========================
plt.figure(figsize=(8,5))
plt.plot(num_products, create_mean, marker='o', label="Create (single)")
plt.plot(num_products, read_mean, marker='s', label="Read (single)")
plt.ylabel("Time (ms)")
plt.xlabel("Number of products")
plt.title("Create vs Read Performance")
plt.grid(True, ls="--")
plt.legend()
plt.tight_layout()
plt.savefig("create_vs_read.png")
plt.close()

# =========================
# 2. GetAll vs Batch
# =========================
plt.figure(figsize=(8,5))
plt.plot(num_products, getall_mean, marker='^', label="GetAll")
plt.plot(num_products, batch_total, marker='o', label="Batch Create")
plt.ylabel("Time (ms)")
plt.xlabel("Number of products")
plt.title("GetAll vs Batch Create Performance")
plt.grid(True, ls="--")
plt.legend()
plt.tight_layout()
plt.savefig("getall_vs_batch.png")
plt.close()

print("Graphs saved as PNG files:")
print("- create_vs_read.png")
print("- getall_vs_batch.png")
