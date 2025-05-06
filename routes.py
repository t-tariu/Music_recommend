import os
from flask import Blueprint, render_template, request, url_for
from .config import run_music_recommendation
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files["image"]
        prompt = request.form["prompt"]
        filename = secure_filename(image.filename)

        upload_folder = os.path.join("static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)
        image.save(filepath)

        result, color = run_music_recommendation(filepath, prompt)
        image_url = url_for("static", filename=f"uploads/{filename}")

        return render_template("index.html", result=result, color=color, image_url=image_url)

    return render_template("index.html", result=None, color=None, image_url=None)
