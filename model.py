import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import sys

df = pd.read_csv("data/samples.csv")

feature_cols = ["entropy", "opcode_freq", "file_size"]
X = df[feature_cols]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


def keyword_baseline(X_test, y_test):
    preds = (X_test["entropy"] > 7.0).astype(int)
    return accuracy_score(y_test, preds)

baseline_acc = keyword_baseline(X_test, y_test)



model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)


preds = model.predict(X_test)

print("=" * 45)
print("RESULTS")
print("=" * 45)
print(f"Model accuracy   : {accuracy_score(y_test, preds):.3f}")
print(f"Baseline accuracy: {baseline_acc:.3f}")
print(f"Improvement      : +{(accuracy_score(y_test, preds) - baseline_acc) * 100:.1f}%")
print()

print("--- Classification Report ---")
print(classification_report(y_test, preds, zero_division=0))

print("--- Feature Importance ---")
for feat, imp in zip(feature_cols, model.feature_importances_):
    print(f"{feat:<15}: {imp:.3f}")


if len(sys.argv) >= 2:
    from extract_features import extract

    filepath = sys.argv[1]
    feats = extract(filepath)

    print()
    print("=" * 45)
    print(f"PREDICTING: {filepath}")
    print("=" * 45)
    print(f"Features: {feats}")

    values = pd.DataFrame([feats])[feature_cols]
    prediction = model.predict(values)[0]
    prob = model.predict_proba(values)[0]

    label = "⚠️  MALICIOUS" if prediction == 1 else "✅ BENIGN"
    print(f"\nResult    : {label}")
    print(f"Confidence: {max(prob) * 100:.2f}%")
