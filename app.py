from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "sujin1325!"

api_key = os.environ.get("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def get_response(user_input, mode):
    if mode == "confirm":
        prompt = "너는 사용자의 의견에 동의하기만하며, 그 의견에 관한 상세한 근거를 제공하는 AI야. 가끔가다가는 사용자의 의견에 동의하기 위해 거짓말도 하는 AI야. 간결하게 대답해.\n"
    else:
        prompt = "너는 사용자의 의견과 다른 관점도 공정하게 제시하는 AI야. 간결하게 대답해.\n"
    prompt += f"User: {user_input}\nAI:"
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/")
def root():
    # 첫 접속 시 바로 모드 선택 페이지로 이동
    return redirect(url_for("select_mode"))

@app.route("/select", methods=["GET", "POST"])
def select_mode():
    if request.method == "POST":
        selected = request.form["mode"]
        session["mode"] = selected
        return redirect(url_for("chat"))
    return render_template("select.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "mode" not in session:
        # 세션에 모드 없으면 다시 선택 페이지로
        return redirect(url_for("select_mode"))

    answer = ""
    user_input = ""
    mode = session["mode"]

    if request.method == "POST":
        user_input = request.form["user_input"]
        answer = get_response(user_input, mode)

    return render_template("index.html", answer=answer, user_input=user_input, selected_mode=mode)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
