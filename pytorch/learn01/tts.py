import torch
import os
import torchaudio


# Wir überschreiben die Standard-Ladefunktion
_original_load = torch.load

def strict_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)

torch.load = strict_load

# --- FIX 3: Torchaudio Backend (Das löst deinen aktuellen Fehler) ---
# Wir zwingen torchaudio, 'soundfile' zu nutzen, statt nach 'torchcodec' zu suchen.
if hasattr(torchaudio, 'set_audio_backend'):
    torchaudio.set_audio_backend("soundfile")

# Zusätzlich patchen wir die load-Funktion, falls die Version zu neu ist:
_original_audio_load = torchaudio.load
def safe_audio_load(*args, **kwargs):
    # Erzwinge den soundfile Backend, wenn keiner angegeben ist
    if 'backend' not in kwargs:
        kwargs['backend'] = 'soundfile'
    return _original_audio_load(*args, **kwargs)
torchaudio.load = safe_audio_load
# -------------------------------------------------------------------


from TTS.api import TTS


# Prüfen ob ROCm da ist
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Lade TTS auf: {device}")

# Modell laden (XTTS v2 ist multilingual und sehr gut)
# Beim ersten Start wird das Modell heruntergeladen (ca. 2-3 GB)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Text in Audio umwandeln
text="Hallo! Ich bin eine künstliche Intelligenz, die auf deiner AMD Grafikkarte läuft."
speaker_wav="ref/me-reference.flac" # Pfad zu einer kurzen Aufnahme (z.B. deine eigene Stimme)

if os.path.exists(speaker_wav):
    print("Generiere Audio...")
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="de",
        file_path="output.wav"
    )
    print("Erfolg! Datei 'output.wav' wurde erstellt.")
else:
    print(f"FEHLER: Die Datei '{ref_audio}' existiert nicht. Bitte nimm erst eine kurze WAV-Datei auf.")
