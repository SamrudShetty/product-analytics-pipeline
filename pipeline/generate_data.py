import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# -------------------------
# CONFIG
# -------------------------
NUM_USERS = 10000

users = list(range(1, NUM_USERS + 1))
events = []

channels = [
    "google_ads",
    "facebook_ads",
    "organic",
    "email",
    "referral"
]

# -------------------------
# GENERATE DATA
# -------------------------
for user in users:

    # Assign A/B group
    group = random.choice(["A", "B"])

    # Assign marketing channel
    channel = random.choice(channels)

    # Base journey date
    base_date = fake.date_this_year()

    # -------------------------
    # PAGE VIEW
    # -------------------------
    page_date = base_date
    events.append([
        page_date,
        "page_view",
        user,
        group,
        channel
    ])

    # -------------------------
    # BASE PROBABILITIES (A/B)
    # -------------------------
    if group == "A":
        signup_prob = 0.6
        purchase_prob = 0.3
    else:
        signup_prob = 0.7
        purchase_prob = 0.4

    # -------------------------
    # CHANNEL MODIFIERS (KEY UPGRADE)
    # -------------------------
    if channel == "google_ads":
        signup_prob += 0.05
        purchase_prob += 0.05

    elif channel == "facebook_ads":
        signup_prob -= 0.05
        purchase_prob -= 0.05

    elif channel == "email":
        signup_prob += 0.03
        purchase_prob += 0.02

    elif channel == "referral":
        signup_prob += 0.07
        purchase_prob += 0.06

    elif channel == "organic":
        signup_prob += 0.02
        purchase_prob += 0.01

    # Ensure probabilities stay valid
    signup_prob = min(max(signup_prob, 0), 1)
    purchase_prob = min(max(purchase_prob, 0), 1)

    # -------------------------
    # SIGN UP
    # -------------------------
    if random.random() < signup_prob:
        signup_date = page_date + timedelta(days=random.randint(0, 5))

        events.append([
            signup_date,
            "sign_up",
            user,
            group,
            channel
        ])

        # -------------------------
        # PURCHASE
        # -------------------------
        if random.random() < purchase_prob:
            purchase_date = signup_date + timedelta(days=random.randint(0, 5))

            events.append([
                purchase_date,
                "purchase",
                user,
                group,
                channel
            ])

# -------------------------
# CREATE DATAFRAME
# -------------------------
df = pd.DataFrame(events, columns=[
    "event_date",
    "event_name",
    "user_id",
    "group",
    "channel"
])

# -------------------------
# SAVE FILE
# -------------------------
df.to_csv("data/events.csv", index=False)

print("✅ Data generated with A/B testing + channel attribution + realistic conversion differences!")