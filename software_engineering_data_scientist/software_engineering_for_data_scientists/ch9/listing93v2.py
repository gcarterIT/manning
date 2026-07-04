import os
import pandas as pd
import sqlite3
from sklearn.ensemble import GradientBoostingClassifier
from ch4.dataset_class_final import DataSet


# ---------------------------------------------------------
# 1. Resolve absolute paths based on THIS script's location
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

CSV_PATH = os.path.join(DATA_DIR, "customer_churn_data.csv")
DB_PATH = os.path.join(DATA_DIR, "customers.db")

print(f"Using CSV: {CSV_PATH}")
print(f"Using DB:  {DB_PATH}")


# ---------------------------------------------------------
# 2. Safety check: verify DB exists BEFORE connecting
# ---------------------------------------------------------
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(
        f"ERROR: Database file not found at:\n{DB_PATH}\n"
        "Refusing to create a new empty DB. Fix the path."
    )


# ---------------------------------------------------------
# 3. Load data
# ---------------------------------------------------------
customer_data = pd.read_csv(CSV_PATH)

customer_obj = DataSet(
    feature_list=[
        "total_day_minutes",
        "total_day_calls",
        "number_customer_service_calls"
    ],
    file_name=CSV_PATH,
    label_col="churn",
    pos_category="yes"
)


# ---------------------------------------------------------
# 4. Train model
# ---------------------------------------------------------
gbm_model = GradientBoostingClassifier(
    learning_rate=0.1,
    n_estimators=300,
    subsample=0.7,
    min_samples_split=40,
    max_depth=3
)

gbm_model.fit(customer_obj.train_features, customer_obj.train_labels)


# ---------------------------------------------------------
# 5. Build output DataFrame
# ---------------------------------------------------------
output = pd.DataFrame(
    [i for i in range(customer_obj.test_features.shape[0])],
    columns=["customer_id"]
)

output["model_prediction"] = gbm_model.predict_proba(
    customer_obj.test_features
)[:, 1]

output["prediction_date"] = "2023-04-01"


# ---------------------------------------------------------
# 6. Connect to SQLite using the verified absolute path
# ---------------------------------------------------------
sqliteConnection = sqlite3.connect(DB_PATH)
cursor = sqliteConnection.cursor()

# Show exactly which DB we opened
print("\nConnected to DB:", DB_PATH)


# ---------------------------------------------------------
# 7. Safety check: verify table exists BEFORE inserting
# ---------------------------------------------------------
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print("Tables found:", tables)

if "customer_churn_predictions" not in tables:
    raise RuntimeError(
        "ERROR: Table 'customer_churn_predictions' does NOT exist in this DB.\n"
        f"DB path: {DB_PATH}\n"
        "Refusing to insert into the wrong database."
    )


# ---------------------------------------------------------
# 8. Insert predictions
# ---------------------------------------------------------
insert_command = """
    INSERT INTO customer_churn_predictions(
        customer_id,
        model_prediction,
        prediction_date
    )
    VALUES (?, ?, ?)
"""

cursor.executemany(insert_command, output.values)
sqliteConnection.commit()

print("\nInsert complete. Rows inserted:", len(output))
