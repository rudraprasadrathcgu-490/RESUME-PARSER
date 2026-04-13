from flask import Flask, render_template, request
from parser import extract_text, extract_email, extract_phone, extract_skills, extract_name
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename != "":
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            text = extract_text(filepath)

            skills = extract_skills(text)

  
            score = len(skills) * 10
            if score > 100:
                score = 100

            data = {
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text),
                "skills": skills,
                "score": score
            }

            return render_template("result.html", data=data)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
