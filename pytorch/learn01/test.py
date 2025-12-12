import os
import torch

# Fix für den Pfad-Fehler unter Arch (bevor ROCm initialisiert wird)
os.environ['LIBDRM_AMDGPU_IDS_PATH'] = '/usr/share/libdrm/amdgpu.ids'

# Optional: Falls es abstürzt, entkommentiere die nächste Zeile für RDNA 3 Fallback
# os.environ['HSA_OVERRIDE_GFX_VERSION'] = '11.0.0'

print(f"PyTorch Version: {torch.__version__}")

if torch.cuda.is_available():
    device = torch.device("cuda")
    # Den echten Namen der Karte abfragen
    print(f"GPU erkannt: {torch.cuda.get_device_name(0)}")
    
    # Test-Berechnung (Matrix-Multiplikation)
    try:
        x = torch.randn(1024, 1024).to(device)
        y = torch.randn(1024, 1024).to(device)
        print("Starte Berechnung auf der GPU...")
        z = torch.matmul(x, y)
        print("Berechnung erfolgreich abgeschlossen!")
        print(f"Ergebnis-Größe: {z.shape}")
    except Exception as e:
        print(f"Fehler bei der Berechnung: {e}")
else:
    print("Keine ROCm/CUDA GPU gefunden.")