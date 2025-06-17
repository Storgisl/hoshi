import os
import uuid
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

def generate_music(
    prompt: str,
    duration: float,
    *,
    username: str,
    name: str | None = None,
    bpm: int | None = None,
    tempo: str | None = None,
    model_size: str = "facebook/musicgen-medium",
    base_output_dir: str = "/shared/generated",
    output_path: str | None = None
):
    # -------- build prompt ------------------------------------------------
    if tempo:
        prompt = f"{prompt}, {tempo} tempo"
    if bpm:
        prompt = f"{prompt}, {bpm} bpm"

    # -------- decide where to save ----------------------------------------
    song_name = (name or "output").replace(" ", "_")
    gen_id = name or str(uuid.uuid4())
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    else:
        output_dir = os.path.join(base_output_dir, username)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{song_name}.wav")

    # -------- generate ----------------------------------------------------
    print(f"Loading model: {model_size}")
    model = MusicGen.get_pretrained(model_size)
    model.set_generation_params(duration=duration, use_sampling=True, top_k=250)

    print("Generating audio…")
    wav = model.generate([prompt], progress=True)

    print(f"Saving to: {output_path}")
    audio_write(output_path, wav[0].cpu(), model.sample_rate,
                strategy="loudness", format="wav")

    return output_path, gen_id


if __name__ == "__main__":
    import sys
    if "--dry-run" in sys.argv:
        print("Dry run: Loading model to test setup.")
        MusicGen.get_pretrained("facebook/musicgen-medium")
        exit(0)

    prompt = "a calm piano melody with soft strings"
    duration = 30
    path, gen_id = generate_music(prompt, duration, username="testuser")
    print(f"Generated: {path}")

