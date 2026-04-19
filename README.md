# 📊 Product Analytics Pipeline

## 🚀 Overview
This project simulates a real-world product analytics system for a SaaS learning platform. It tracks user behavior, analyzes conversion funnels, performs A/B testing, and evaluates user retention.

---

## 🧱 Architecture
Frontend → Event Tracking → Data Storage (PostgreSQL) → SQL Analysis → Dashboard (Streamlit)

---

## ⚙️ Tech Stack
- Python
- PostgreSQL
- SQL
- Streamlit

---

## 📈 Key Features

### 1. Funnel Analysis
- Tracks user journey from page view → signup → purchase
- Identifies conversion drop-offs

### 2. A/B Testing
- Compares two user variants (A vs B)
- Measures impact on conversion rates
- Variant B improved conversion by ~10%

### 3. Cohort Analysis
- Groups users by first activity date
- Tracks retention over time

---

## 📊 Key Insights

- ~60% of users sign up after visiting  
- ~30% convert into paying customers  
- ~70% drop-off occurs after signup  
- A/B testing showed ~10% improvement in conversions  

---

## 💡 Business Impact

- Identified key drop-off stage in user journey  
- Demonstrated how A/B testing can improve revenue  
- Showed retention patterns using cohort analysis  
- Enabled data-driven decision-making  

---

## 📌 Conclusion
This project demonstrates how product analytics can be used to optimize user conversion, improve retention, and drive business growth.

---

## ▶️ How to Run

```bash
python pipeline/generate_data.py
python pipeline/load_data.py
python -m streamlit run dashboard/analytics_dashboard.py