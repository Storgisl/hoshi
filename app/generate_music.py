# app/generate_music.py
import os
import uuid
from audiocraft.models.musicgen import MusicGen
from audiocraft.data.audio import audio_write


def generate_music(prompt: str, duration: float, bpm: int = None, tempo: str = None,
                   model_size: str = "facebook/musicgen-medium",
                   base_output_dir: str = "generated",
                   name: str = None) -> str:
    
    if tempo:
        prompt = f"{prompt}, {tempo} tempo"

    if bpm:
        prompt = f"{prompt}, {bpm} bpm"

    gen_id = name if name else str(uuid.uuid4())
    output_dir = os.path.join(base_output_dir, gen_id)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "output.wav")

    print(f"Loading model: {model_size}")
    model = MusicGen.get_pretrained(model_size)
    model.set_generation_params(duration=duration, use_sampling=True, top_k=250)

    print("Generating audio...")
    wav = model.generate([prompt], progress=True)

    print(f"Saving to: {output_path}")
    audio_write(output_path, wav[0].cpu(), model.sample_rate, strategy="loudness", format="wav")

    return output_path, gen_id

if __name__ == "__main__":
    import sys
    if "--dry-run" in sys.argv:
        print("Dry run: Loading model to test setup.")
        MusicGen.get_pretrained("facebook/musicgen-medium")
        exit(0)

    prompt = "a calm piano melody with soft strings"
    duration = 30
    path, gen_id = generate_music(prompt, duration)
    print(f"Generated: {path}")

