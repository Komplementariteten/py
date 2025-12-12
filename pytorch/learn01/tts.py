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

print(TTS().list_models())

# Prüfen ob ROCm da ist
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Lade TTS auf: {device}")

# Modell laden (XTTS v2 ist multilingual und sehr gut)
# Beim ersten Start wird das Modell heruntergeladen (ca. 2-3 GB)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Text in Audio umwandeln
text="""Ihr wurdet auserwählt mir [[Inquisitorin Lira Mardox]] und der heiligen Inquisition zu Terra vertreten durch mich zu Dienen. Es gibt keine höhere Pflicht, denn ich diene dem Imperator und seinem Regenten direkt. 
Euer Leben, voller Angst vor dem Tod, Angst vor Hunger oder euren Herren ist vorbei. Von nun an gibt es nur noch eure Pflicht. Denn selbst der Tod befreit euch nicht vor eurer Pflicht dem Thron gegenüber.
Ihr werdet meine Augen und Hände sein, werdet dort hin gehen wo ich es nicht kann. Freudig werdet ihr eure Seelen der Verdammnis übergeben wenn das eure Pflicht verlangt. Euer einziger Trost ist, dass ihr die Wächter im Schatten seit, die die Menschheit insgesamt vor der Verdammnis schützen. 
Denn die Feinde der Menschheit lauern in jeder Gestalt, kein Rang, kein Privileg soll sie vor der Gerechtigkeit des Imperators schützen. Unsere Wachsamkeit soll von keiner Amts-Insignie geblendet werden, doch bedenkt, auch wenn meine Autorität absolut ist, so ist es meine Macht nicht. Und so sind Vorsicht und Heimlichkeit das mächtigste Schwert in unserem Arsenal. 
Unsere Pflicht ist es die Feinde des Regenten und des Imperators zu identifizieren und ihre Pläne zu nichte zu machen. Und der Regent hat viele Feinde, manche offen andere im Geheimen. Seit immer auf der Hut, denn jeder Kardinal, jeder General oder Herr kann Geheim einem anderen Herren dienen. Selbst in den Reihen des Imdomitus Kreuzzuges gibt es Verräter. 
Wir sind die geheime Klinge des Regenten, unsere Pflicht ist es diese Geschwüre heraus zu schneiden und zu vernichten.
Von nun an, seit Ihr meine Augen und Ohren, meine Hände und mein Zorn. Und nur mir steht Ihre Rede und Antwort. Doch seit nicht Sorglos, gehen den Falschen aufzubegehren lässt euch in eurer Pflicht versagen und dies ist ein Verbrechen gegen den Imperator selbst.
Seid gewahr, die die sich Priester des Imperators nennen und seine Göttlichkeit preisen sind besten falls nützliche Narren. All zu leicht lässt sich ihr Glaube vom Erzfeind oder den Xenos nutzen um Sie gegen ihre Brüder und den Imperator aufzubringen. Lasst keinen Glauben, mag er auch noch so gut gemeint sein, eurer Pflicht im Wege stehen. Die Lage ist ernst! Jahrhunderte der Korruption und Inkompetenz haben es dem Erz-Verraeter Abaddon erlaubt das Imperium an den Rand der Vernichtung zu bringen. Es waren nicht die Hohen Senatoren von Terra, nicht die Kardinäle der Ekklesiarchie, die Handelsherren der Hohen Häuser, die sich Abaddon in den Weg stellten, die Terra gegen den Kreuzzug der Schlächter verteidigten, die die grösste Flotte seit den Tagen des Imperators selbst aussenden um mit ihr und dem Licht der Wahrheit die große Nacht zurückschlagen. 
Es war Guillaume und die Adeptus Astartes, es waren die Agenten des Trons wie wir, die Custodes und Schwestern der Stille. Es waren die tapferen Soldaten von Cardia unter Großkastellan Creed und die Imperiale Flotte unter Admiral Quarren. Es ist der Imdomitus Kreuzzug!
Wir werden mit Schlachtgruppe Fortis in den Macharian Sektor aufbrechen und zwei Hauptmissionen verfolgen. Wir werden die Schlachtgruppe vor Sabotage schuetzen und nach kraeften Unterstuetzen waehrend wir fuer Lord Inquisitorin Greyfax einen Bericht ueber die Inquisition des Macharian Sektors und die Ereignisse nach der Langen Nacht erstellen. 

Eigentlich ist das schon alles was ihr zu eurer Mission wissen muesst und manche Inquisitoren wuerden es dabei belassen. Doch ich verlange von euch Vertrauen das nur gedeihen kann wenn Vertrauen gegeben wird, deswegen will ich eurer erstes Briefing mit einigen Informationen beginnen, die nur fuer eure Ohren bestimmt sind. Uns haben Informationen von Inquisitor Lord Hieronymo Drak erreicht und sobald die Kampfgruppe den Sektor erreicht wird Gruppenmeister [[Valdur Slain]] die Welt Belnshudha vernichten. Gleichzeitig haben wir die Nachricht an Schiffe der Navis Imperiales Macharian weitergeleitet. Aktuell bereite ich einen Bericht ueber den Sektor vor. Sollange widmet euch euren Aufgaben und meldet euch zum Mentalen Training bei [[Interogator Vassa Leondir]] und fuer das Koeperliche Training bei [[Captian Me'an Alzius]]. [[Constable Wallfeld]] wird euch in der Wichtigsten Faehigkeit unterrichten, dem Studium und Recherche Imperialer Akten.
"""
speaker_wav="ref/me-reference.flac" # Pfad zu einer kurzen Aufnahme (z.B. deine eigene Stimme)

if os.path.exists(speaker_wav):
    print("Generiere Audio...")
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="de",
        file_path="xtts_v2.wav"
    )
    print("Erfolg! Datei 'output.wav' wurde erstellt.")
else:
    print(f"FEHLER: Die Datei '{ref_audio}' existiert nicht. Bitte nimm erst eine kurze WAV-Datei auf.")
