# musicgen/app.py
from flask import Flask, request, jsonify, send_file
from generate_music import generate_music
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt   = data.get("prompt")
    duration = float(data.get("duration", 30))
    bpm      = data.get("bpm")
    tempo    = data.get("tempo")
    name     = data.get("name") or "output"
    username = data.get("username")

    if not prompt or not username:
        return jsonify({"error": "Prompt and username are required"}), 400

    bpm = int(bpm) if bpm else None

    path, gen_id = generate_music(
        prompt=prompt,
        duration=duration,
        bpm=bpm,
        tempo=tempo,
        username=username,
        name=name
    )

    filename = os.path.basename(path)

    return jsonify({
        "status": "success",
        "file": f"/download/{username}/{filename}",
        "id": gen_id
    })

@app.route("/download/<username>/<filename>")
def download(username, filename):
    file_path = f"/shared/generated/{username}/{filename}"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)


