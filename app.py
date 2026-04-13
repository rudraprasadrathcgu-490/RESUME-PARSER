from flask import Flask, render_template, request
from parser import extract_text, extract_email, extract_phone, extract_skills, extract_name
import os

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")

        # File validation
        if not file or file.filename == "":
            return "Error: No file uploaded."

        try:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Extract text safely
            text = extract_text(filepath)

            if not text:
                return "Error: Could not read resume. Please upload a valid text-based PDF."

            # Extract skills
            skills = extract_skills(text)

            # Resume Score
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

        except Exception as e:
            print("ERROR:", e)
            return "Internal Server Error: Something went wrong."

    return render_template("index.html")


# Render deployment config
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
