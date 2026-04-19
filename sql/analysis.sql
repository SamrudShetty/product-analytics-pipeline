-- =========================================
-- PRODUCT ANALYTICS SQL QUERIES
-- =========================================


-- =========================================
-- 1. BASIC EVENT COUNTS
-- =========================================
SELECT
  COUNT(DISTINCT CASE WHEN event_name = 'page_view' THEN user_id END) AS page_views,
  COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS sign_ups,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchases
FROM events;



-- =========================================
-- 2. EVENT DISTRIBUTION
-- =========================================
SELECT 
  event_name,
  COUNT(*) AS total_events
FROM events
GROUP BY event_name
ORDER BY total_events DESC;



-- =========================================
-- 3. TRUE FUNNEL ANALYSIS (USER LEVEL)
-- =========================================
WITH users AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
    MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
    MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
  FROM events
  GROUP BY user_id
)

SELECT
  COUNT(*) AS total_users,
  SUM(viewed) AS page_users,
  SUM(signed_up) AS signup_users,
  SUM(purchased) AS purchase_users,
  SUM(signed_up)::float / SUM(viewed) AS signup_rate,
  SUM(purchased)::float / SUM(signed_up) AS purchase_rate
FROM users;



-- =========================================
-- 4. FUNNEL DROP-OFF ANALYSIS
-- =========================================
WITH users AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
    MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
    MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
  FROM events
  GROUP BY user_id
)

SELECT
  'Page View → Sign Up' AS stage,
  SUM(signed_up)::float / SUM(viewed) AS conversion_rate
FROM users

UNION ALL

SELECT
  'Sign Up → Purchase',
  SUM(purchased)::float / SUM(signed_up)
FROM users;



-- =========================================
-- 5. DAILY USER ACTIVITY
-- =========================================
SELECT
  event_date,
  COUNT(DISTINCT user_id) AS active_users
FROM events
GROUP BY event_date
ORDER BY event_date;



-- =========================================
-- 6. PURCHASE RATE BY DAY
-- =========================================
WITH daily AS (
  SELECT
    event_date,
    COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS signups,
    COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchases
  FROM events
  GROUP BY event_date
)

SELECT
  event_date,
  purchases::float / NULLIF(signups, 0) AS purchase_rate
FROM daily
ORDER BY event_date;


-- =========================================
-- 7. A/B TEST ANALYSIS
-- =========================================

WITH users AS (
  SELECT
    user_id,
    "group",
    MAX(CASE WHEN event_name = 'page_view' THEN 1 ELSE 0 END) AS viewed,
    MAX(CASE WHEN event_name = 'sign_up' THEN 1 ELSE 0 END) AS signed_up,
    MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
  FROM events
  GROUP BY user_id, "group"
)

SELECT
  "group",
  SUM(viewed) AS users,
  SUM(signed_up)::float / SUM(viewed) AS signup_rate,
  SUM(purchased)::float / SUM(signed_up) AS purchase_rate
FROM users
GROUP BY "group";


-- =========================================
-- 8. COHORT ANALYSIS (RETENTION)
-- =========================================

WITH user_first_event AS (
    SELECT
        user_id,
        MIN(event_date::date) AS cohort_date
    FROM events
    GROUP BY user_id
),

user_activity AS (
    SELECT
        e.user_id,
        u.cohort_date,
        e.event_date::date AS event_date,
        (e.event_date::date - u.cohort_date) AS days_since_signup
    FROM events e
    JOIN user_first_event u
        ON e.user_id = u.user_id
),

cohort_size AS (
    SELECT
        cohort_date,
        COUNT(DISTINCT user_id) AS total_users
    FROM user_first_event
    GROUP BY cohort_date
)

SELECT
    ua.cohort_date,
    ua.days_since_signup,
    COUNT(DISTINCT ua.user_id) AS active_users,
    COUNT(DISTINCT ua.user_id)::float / cs.total_users AS retention_rate
FROM user_activity ua
JOIN cohort_size cs
    ON ua.cohort_date = cs.cohort_date
GROUP BY ua.cohort_date, ua.days_since_signup, cs.total_users
ORDER BY ua.cohort_date, ua.days_since_signup;