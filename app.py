# app.py
from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "sujin1325!"

# Gemini 설정
genai.configure(api_key="AIzaSyDMqA1eo9ep7RMdSbCxtnVWm6Q9I9D-hzU")  # <-- 여기에 너의 실제 API 키를 넣어야 해!
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def get_response(user_input, mode):
    if mode == "confirm":
        prompt = "너는 사용자의 의견에 동의하며, 그 의견을 강화하는 정보만 제공하는 AI야. 간결하게 대답해.\n"
    else:
        prompt = "너는 사용자의 의견과 다른 관점도 공정하게 제시하는 AI야. 간결하게 대답해.\n"
    prompt += f"User: {user_input}\nAI:"
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    if "mode" not in session:
        return redirect(url_for("select_mode"))
    
    answer = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        mode = session["mode"]
        answer = get_response(user_input, mode)

    return render_template("index.html", answer=answer)

@app.route("/select", methods=["GET", "POST"])
def select_mode():
    if request.method == "POST":
        selected = request.form["mode"]
        session["mode"] = selected
        return redirect(url_for("index"))
    return """
    <form method="post">
        <h2>모드를 선택하세요:</h2>
        <button name="mode" value="confirm">확증편향</button>
        <button name="mode" value="diverse">다양성</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

