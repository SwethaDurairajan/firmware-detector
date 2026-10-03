import os
import math
import csv
from collections import Counter

def entropy(data):
    if not data:
        return 0
    counts = Counter(data)
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())

def extract(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return {
        "entropy": round(entropy(data), 3),
        "string_count": data.count(b"\x00"),
        "opcode_freq": len(set(data)) % 256,
        "file_size": len(data)
    }

def build_dataset():
    rows = []
    for label, folder in [(0, "firmware/benign"), (1, "firmware/malicious")]:
        if not os.path.exists(folder):
            print(f"Skipping: {folder}")
            continue
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                try:
                    feats = extract(filepath)
                    feats["label"] = label
                    rows.append(feats)
                    print(f"Processed: {filepath} -> label={label}")
                except Exception as e:
                    print(f"Error: {filepath} -> {e}")
    
    with open("data/samples.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["entropy", "string_count", "opcode_freq", "file_size", "label"]
        )
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n{'='*40}")
    print(f"Total samples : {len(rows)}")
    print(f"Benign (0)    : {sum(1 for r in rows if r['label'] == 0)}")
    print(f"Malicious (1) : {sum(1 for r in rows if r['label'] == 1)}")
    print(f"{'='*40}")

if __name__ == "__main__":
    build_dataset()
