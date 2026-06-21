"""
Módulo engine.py - Motor de la novela interactiva.
Gestiona la carga de la historia, el estado del jugador y el flujo de la partida.
"""

import json
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# Inicializar consola Rich para darle estética
console = Console()

class StoryEngine:
    """
    Motor principal de la novela interactiva.
    Carga un archivo JSON con la estructura de la historia y maneja la navegación.
    """

    def __init__(self, filepath: str):
        """
        Inicializa el motor cargando la historia desde un archivo JSON.

        Args:
            filepath (str): Ruta al archivo JSON con la historia.
        """
        self.filepath = filepath
        self.historia = self._cargar_historia()
        self.estado = {
            "PROVISIONES": False,
            "CONFIANZA_SOFIA": 0,
            "CARLOS_VIVE": False,
            "SOFIA_VIVE": False,
            "RUIDO": False
        }
        self.nodo_actual = self.historia.get("inicio")

    def _cargar_historia(self) -> dict:
        """
        Carga el archivo JSON de la historia.

        Returns:
            dict: Diccionario con la estructura de la historia.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el archivo tiene formato inválido.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            console.print("[red]ERROR: No se encontró el archivo de historia.[/red]")
            raise
        except json.JSONDecodeError:
            console.print("[red]ERROR: El archivo JSON tiene errores de sintaxis.[/red]")
            raise

    def _ejecutar_accion(self, accion: str):
        """
        Ejecuta una acción que modifica el estado del jugador.
        Ejemplo de acción: "PROVISIONES = true"

        Args:
            accion (str): La acción a ejecutar.
        """
        if accion:
            try:
                # Separar clave y valor (ej: "PROVISIONES = true")
                clave, valor = accion.split("=")
                clave = clave.strip()
                valor = valor.strip()
                # Convertir valor booleano o entero
                if valor.lower() == "true":
                    self.estado[clave] = True
                elif valor.lower() == "false":
                    self.estado[clave] = False
                elif valor.isdigit():
                    self.estado[clave] = int(valor)
                else:
                    self.estado[clave] = valor
            except (ValueError, KeyError):
                console.print(f"[yellow]Advertencia: No se pudo ejecutar la acción '{accion}'[/yellow]")

    def mostrar_nodo(self):
        """
        Muestra el nodo actual por pantalla con estilo Rich.
        Detecta si el nodo es un final y termina el juego.
        """
        nodo_data = self.historia["nodos"].get(self.nodo_actual)
        if not nodo_data:
            console.print("[red]ERROR: Nodo no encontrado.[/red]")
            return

        # Limpiar pantalla para dar sensación de "escena"
        os.system("cls" if os.name == "nt" else "clear")

        # Mostrar texto en panel con color según tipo
        if nodo_data.get("final", False):
            panel = Panel(
                Text(nodo_data["texto"], style="bold red"),
                title="[bold]☠️ FINAL DEL CAPÍTULO[/bold]",
                border_style="red"
            )
        else:
            panel = Panel(
                Text(nodo_data["texto"], style="white"),
                title=f"[bold cyan]📍 {nodo_data['id']}[/bold cyan]",
                border_style="blue"
            )
        console.print(panel)

        # Si es final, salir
        if nodo_data.get("final", False):
            console.print("\n[bold yellow]Presiona Enter para salir...[/bold yellow]")
            input()
            return

        # Mostrar opciones numeradas
        opciones = nodo_data.get("opciones", [])
        if not opciones:
            console.print("[red]Error: Nodo sin opciones.[/red]")
            return

        console.print("\n[bold green]❓ ¿Qué hacés?[/bold green]")
        for idx, opcion in enumerate(opciones, 1):
            console.print(f"  [bold yellow]{idx}.[/bold yellow] {opcion['texto']}")

        # Manejar entrada del usuario
        while True:
            try:
                eleccion = input("\n[bold]> [/bold]")
                if not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > len(opciones):
                    console.print("[red]Opción inválida. Elegí un número de la lista.[/red]")
                    continue

                opcion_seleccionada = opciones[int(eleccion) - 1]
                # Ejecutar acción (oculta)
                if opcion_seleccionada.get("accion"):
                    self._ejecutar_accion(opcion_seleccionada["accion"])

                # Ir al siguiente nodo
                self.nodo_actual = opcion_seleccionada["destino"]
                break

            except KeyboardInterrupt:
                console.print("\n[red]Juego interrumpido por el usuario.[/red]")
                exit()

    def jugar(self):
        """
        Bucle principal del juego. Muestra nodos hasta llegar a un final.
        """
        console.print("[bold magenta]🧟 BIENVENIDO A 'ÚLTIMO LATIDO' - BUENOS AIRES[/bold magenta]")
        console.print("[italic]La ciudad está muerta. Vos decidís quién vive.[/italic]\n")
        input("Presiona Enter para comenzar...")

        while True:
            nodo_data = self.historia["nodos"].get(self.nodo_actual)
            if not nodo_data:
                break
            self.mostrar_nodo()
            if nodo_data.get("final", False):
                break
