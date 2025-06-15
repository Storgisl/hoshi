import os
import json

GENERATED_DIR = '/workspace/generated'
OUTPUT_JSON = '/workspace/generated/tracks.json'

def generate_manifest():
    manifest = []
    for folder_name in os.listdir(GENERATED_DIR):
        folder_path = os.path.join(GENERATED_DIR, folder_name)
        if os.path.isdir(folder_path):
            # Check for output.wav.wav inside this folder
            audio_file = os.path.join(folder_path, 'output.wav.wav')
            if os.path.exists(audio_file):
                manifest.append({
                    'id': folder_name,
                    'title': folder_name,
                    'audioPath': f'/static/generated/{folder_name}/output.wav.wav'
                })

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == '__main__':
    generate_manifest()
