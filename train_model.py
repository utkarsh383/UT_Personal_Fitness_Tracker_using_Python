import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("fitness_dataset.csv")

label_encoders = {}
for col in ['Gender', 'Activity_Level', 'Exercise_Type']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df[['Age', 'Weight', 'Height', 'Activity_Level']]
y = df['Exercise_Type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("fitness_model.pkl", "wb") as f:
    pickle.dump((model, scaler, label_encoders), f)

print("Model trained and saved successfully!")
