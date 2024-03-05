import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer  # Make sure this import is included


# Assuming df is your DataFrame after loading the CSV
df = pd.read_csv('./../../box/CSE 531 Project/cleaned_data_with_chart_events.csv')

# Preprocess and feature engineering steps here

# Define feature matrix X and target y


# Convert 'INTIME' and 'OUTTIME' to datetime
df['INTIME'] = pd.to_datetime(df['INTIME'])
df['OUTTIME'] = pd.to_datetime(df['OUTTIME'])


# Create new features, e.g., stay duration in hours (or any other relevant feature)
df['STAY_DURATION'] = (df['OUTTIME'] - df['INTIME']).dt.total_seconds() / 3600

X = df.drop('ICU_STAY_LENGTH', axis=1)
y = df['ICU_STAY_LENGTH']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Now, let's define our preprocessing for categorical and numerical columns
categorical_cols = ['FIRST_CAREUNIT', 'LAST_CAREUNIT', 'GENDER', 'ITEMID']
numerical_cols = ['VALUENUM', 'STAY_DURATION']  # Add more numerical columns as needed

# For numerical features: impute missing values and scale
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# For categorical features: impute missing values and one-hot encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combine transformers into a ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('model', RandomForestRegressor(random_state=42))])

# Train the model
model_pipeline.fit(X_train, y_train)

# Predict and evaluate
y_pred = model_pipeline.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'MSE: {mse}')