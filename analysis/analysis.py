import pandas as pd

df = pd.read_csv("data/events.csv")

print("Raw Data Sample:")
print(df.head())

# Funnel counts
page_views = df[df["event_name"] == "page_view"]["user_id"].nunique()
sign_ups = df[df["event_name"] == "sign_up"]["user_id"].nunique()
purchases = df[df["event_name"] == "purchase"]["user_id"].nunique()

print("\nFunnel:")
print("Page Views:", page_views)
print("Sign Ups:", sign_ups)
print("Purchases:", purchases)

# Conversion rates
signup_rate = sign_ups / page_views
purchase_rate = purchases / sign_ups

print("\nConversion Rates:")
print("Signup Rate:", signup_rate)
print("Purchase Rate:", purchase_rate)