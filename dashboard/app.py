import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LearnTastic Clone")

# ✅ Proper GA4 injection
components.html(
    """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-6X4XPZWZHG"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-6X4XPZWZHG');
    </script>
    """,
    height=0,
)

st.title("LearnTastic Clone")

st.write("Welcome to your learning platform")

st.subheader("Explore Courses")

if st.button("Sign Up"):
    st.write("User Signed Up!")

if st.button("View Course"):
    st.write("Viewing Course")

if st.button("Buy Course"):
    st.write("Purchase Successful!")