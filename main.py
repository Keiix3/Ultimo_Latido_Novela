import sys
import os

sys.path.append(os.path.join(os.path.dirname, "src"))

from engine import StoryEngine

def main():
    """
    Función principal.
    """
    # Ruta al archivo JSON
    ruta_historia = os.path.join("data", "historia.json")

    # Iniciar el motor
    juego = StoryEngine(ruta_historia)
    juego.jugar()

if __name__ == "__main__":
    main()
