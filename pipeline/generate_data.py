import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

users = list(range(1, 10001))
events = []

for user in users:
    # Assign A/B group
    group = random.choice(["A", "B"])

    # Base date (start of journey)
    base_date = fake.date_this_year()

    # Page View
    page_date = base_date
    events.append([page_date, "page_view", user, group])

    # Behavior probabilities
    if group == "A":
        signup_prob = 0.6
        purchase_prob = 0.3
    else:
        signup_prob = 0.7
        purchase_prob = 0.4

    # Sign Up (after page view)
    if random.random() < signup_prob:
        signup_date = page_date + timedelta(days=random.randint(0, 5))
        events.append([signup_date, "sign_up", user, group])

        # Purchase (after signup)
        if random.random() < purchase_prob:
            purchase_date = signup_date + timedelta(days=random.randint(0, 5))
            events.append([purchase_date, "purchase", user, group])

df = pd.DataFrame(events, columns=["event_date", "event_name", "user_id", "group"])

df.to_csv("data/events.csv", index=False)

print("✅ Realistic A/B test data generated!")