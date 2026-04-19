from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LearnTastic Clone</title>

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-6X4XPZWZHG"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-6X4XPZWZHG');
    </script>

</head>
<body>
    <h1>LearnTastic Clone</h1>

    <button onclick="pageView()">Page View</button>
    <button onclick="signup()">Sign Up</button>
    <button onclick="buyCourse()">Buy Course</button>

    <script>
        function pageView() {
            gtag('event', 'page_view');
            alert("Page Viewed!");
        }

        function signup() {
            gtag('event', 'sign_up');
            alert("Signed Up!");
        }

        function buyCourse() {
            gtag('event', 'purchase', {value: 100});
            alert("Purchased!");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(port=5000)