from pathlib import Path

import joblib
import numpy as np

base_dir = Path(__file__).resolve().parent
artifacts_dir = base_dir / "models"
artifacts_dir.mkdir(exist_ok=True)

product_count = 20
user_count = 4
matrix = np.zeros((user_count, product_count), dtype=float)
for user_index in range(user_count):
    for product_index in range(product_count):
        if (user_index + 1) % 2 == 0 and product_index % 3 == 0:
            matrix[user_index, product_index] = 1.0
        elif user_index == product_index % user_count:
            matrix[user_index, product_index] = 0.7

similarity = np.eye(product_count, dtype=float)
for idx in range(product_count):
    for jdx in range(product_count):
        if idx != jdx:
            similarity[idx, jdx] = 0.5 if (idx + jdx) % 3 == 0 else 0.1

joblib.dump({"kind": "demo-model"}, artifacts_dir / "model.pkl")
joblib.dump({"kind": "demo-vectorizer"}, artifacts_dir / "vectorizer.pkl")
np.save(artifacts_dir / "user_item_matrix.npy", matrix)
np.save(artifacts_dir / "product_similarity.npy", similarity)

print(f"Demo model artifacts written to {artifacts_dir}")
print("Use them in local development or run the backend after exporting.")
