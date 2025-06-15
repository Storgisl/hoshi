# app/server.py
from flask import Flask, request, jsonify, send_file, send_from_directory
from generate_music import generate_music
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/tracks.json')
def tracks_json():
    return send_from_directory('/workspace/generated', 'tracks.json')

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    duration = float(data.get("duration", 30))
    bpm = data.get("bpm", None)
    tempo = data.get("tempo", None)
    name = data.get("name", None)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        bpm = int(bpm) if bpm else None
        path, gen_id = generate_music(prompt, duration, bpm, tempo, name=name)
        return jsonify({
            "status": "success",
            "file": f"/download/{gen_id}",
            "id": gen_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<gen_id>")
@app.route("/download/<gen_id>.wav")
def download(gen_id):
    file_path = f"/workspace/generated/{gen_id}/output.wav.wav"
    print("Checking path:", file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    print("File not found!")
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)


