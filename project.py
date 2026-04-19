import pickle

import pandas as pd
# dataset loading
df = pd.read_csv(r"C:\Users\HP\AppData\Local\Temp\3f423988-7e60-4b1b-a65b-1e53f9225f23_Converted files.zip.f23\archive.csv")
print(df.head())
print(df.info())

# data cleaning

# missing value check
print(df.isnull().sum())
#missing value fill
df = df.fillna(df.mean())

df = pd.get_dummies(df)

# making model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

#spliting data
x = df.drop('stress_level', axis=1)
y = df['stress_level']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#model train
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

#save model
pickle.dump(model, open('model.pkl', 'wb'))

print("Model saved successfully.")