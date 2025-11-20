import pandas as pd
import yfinance as yf
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.inspection import permutation_importance

# 1. Define GDELT column names (57 columns)
gdelt_cols = [
    "GLOBALEVENTID","SQLDATE","MonthYear","Year","FractionDate",
    "A1_Code","A1_Name","A1_Country","A1_Group",
    "A1_Ethnic","A1_Religion1","A1_Religion2",
    "A1_Type1","A1_Type2","A1_Type3",

    "Actor2Code","Actor2Name","Actor2CountryCode","Actor2KnownGroupCode",
    "Actor2EthnicCode","Actor2Religion1Code","Actor2Religion2Code",
    "Actor2Type1Code","Actor2Type2Code","Actor2Type3Code",

    "IsRootEvent","EventCode","EventBaseCode","EventRootCode",
    "QuadClass","GoldsteinScale","NumMentions","NumSources",
    "NumArticles","AvgTone",

    "EventLocationType","EventGeoFullName","EventGeoCountryCode",
    "EventGeoADM1Code","EventGeoLatitude","EventGeoLongitude",
    "EventGeoFeatureID",

    "ActionGeoType","ActionGeoFullName","ActionGeoCountryCode",
    "ActionGeoADM1Code","ActionGeoLatitude","ActionGeoLongitude",
    "ActionGeoFeatureID",

    "DATEADDED"
]

# 2. Load the first 1 million rows (5 * 200k chunks)
chunks = pd.read_csv(
    "1998.csv",
    sep="\t",
    header=None,
    dtype=str,
    chunksize=200000,
    low_memory=True
)

dfs = []
for i in range(5):
    dfs.append(next(chunks))

big_df = pd.concat(dfs, ignore_index=True)

# Add extra column names if needed
if big_df.shape[1] > len(gdelt_cols):
    gdelt_cols += [f"EXTRA_{i}" for i in range(big_df.shape[1] - len(gdelt_cols))]

big_df.columns = gdelt_cols[:big_df.shape[1]]

# 3. Filter technology-related news
tech_companies = [
    "microsoft","intel","cisco","dell","ibm","hp","oracle",
    "amd","netscape","yahoo","aol","amazon","sun","sun microsystems"
]
regex = "|".join(tech_companies)

big_df["Actor2Name"] = big_df["Actor2Name"].str.lower()

df_tech = big_df[big_df["Actor2Name"].str.contains(regex, na=False)]
print("Number of tech-related news:", len(df_tech))

# 4. Data cleaning & daily aggregation
df_tech["SQLDATE"] = pd.to_datetime(df_tech["SQLDATE"], format="%Y%m%d")
df_tech["AvgTone"] = pd.to_numeric(df_tech["AvgTone"], errors="ignore")
df_tech["GoldsteinScale"] = pd.to_numeric(df_tech["GoldsteinScale"], errors="ignore")
df_tech["NumArticles"] = pd.to_numeric(df_tech["NumArticles"], errors="ignore")

daily_news = df_tech.groupby("SQLDATE").agg(
    tone_mean=("AvgTone", "mean"),
    goldstein_mean=("GoldsteinScale", "mean"),
    media_attention=("NumArticles", "sum")
).reset_index()

daily_news.rename(columns={"SQLDATE": "date"}, inplace=True)

# 5. Download stock prices (1998)
tickers = ["MSFT", "INTC", "AMZN"]
prices = yf.download(tickers, start="1998-01-01", end="1999-01-01")["Close"]

# 6. Compute log-returns & 7-day rolling volatility
returns = np.log(prices).diff()
vol = returns.rolling(7).std()

# 7. Merge everything into a single time-series dataset
merged = (
    prices.join(returns, rsuffix="_ret")
          .join(vol, rsuffix="_vol")
          .merge(daily_news, left_index=True, right_on="date", how="left")
)

merged.set_index("date", inplace=True)

# Debug: show actual columns
print("Columns:", merged.columns.tolist())

# Detect available volatility columns (*_vol)
vol_cols = [c for c in merged.columns if c.endswith("_vol")]
ret_cols = [c for c in merged.columns if c.endswith("_ret")]

if not vol_cols:
    raise ValueError("No volatility columns (*_vol) found. Please check the downloaded stock data.")

target_col = vol_cols[0]  # Use the first available volatility column
print("Selected target variable (volatility):", target_col)

feature_cols = ret_cols + ["tone_mean", "goldstein_mean", "media_attention"]

df_model = merged[[target_col] + feature_cols].dropna()

print("Number of usable training samples:", len(df_model))

# Train-test split (no shuffle due to time-series nature)
X = df_model[feature_cols]
y = df_model[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, shuffle=False
)

# Fit XGBoost model
model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = root_mean_squared_error(y_test, y_pred)
print("XGBoost RMSE:", rmse)

# Permutation feature importance
result = permutation_importance(model, X_test, y_test, n_repeats=20)

print("\nFeature Importances (Permutation Importance):")
for f, imp in zip(feature_cols, result.importances_mean):
    print(f"{f}: {imp}")
