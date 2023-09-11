import keyboard
import typer
from rich.console import Console
from rich.prompt import Prompt

console = Console(color_system="windows")

# Crea un programa capaz de gestionar una pieza de Tetris.
# - La pantalla de juego tiene 10 filas y 10 columnas representadas por símbolos 🔲
# - La pieza de tetris a manejar será la siguiente (si quieres, puedes elegir otra):
#   🔳
#   🔳🔳🔳
# - La pieza aparecerá por primera vez en la parte superior izquierda de la pantalla de juego.
#   🔳🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔳🔳🔳🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
#   🔲🔲🔲🔲🔲🔲🔲🔲🔲🔲
# - Debes desarrollar una función capaz de desplazar y rotar la pieza en el tablero,
#   recibiendo una acción cada vez que se llame, mostrando cómo se visualiza en la pantalla  de juego.
# - Las acciones que se pueden aplicar a la pieza son: derecha, izquierda, abajo, rotar.
# - Debes tener en cuenta los límites de la pantalla de juego.


class PyTetris:
    """
        Movimiento y verificación de piezas del tetris
    """
    def __init__(self):
        self.screen = [
            ["🔳", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔳", "🔳", "🔳", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"],
            ["🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲", "🔲"]
        ]

    # Imprime la pantalla actualizada con el movimiento introducido
    def print_screen(self):
        console.print("\n[green bold]Pantalla Tetris:[/green bold]\n")
        for row in self.screen:
            console.print(" ".join(map(str, row)))

    # Verifica si es permitido el movimiento de la pieza y lo realiza
    def move_piece(self, screen: list, movement: str, rotation: int) -> (list, int):
        # Tablero en blanco
        new_screen = [['🔲' for _ in range(10)] for _ in range(10)]
        # Variable que almacena el item que se verificará la rotación
        rotation_item = 0
        # Lista que almacena las rotaciones que se pueden realizar
        rotate = [
            [(1, 1), (0, 0), (-2, 0), (-1, -1)],
            [(0, 1), (-1, 0), (0, -1), (1, -2)],
            [(0, 2), (1, 1), (-1, 1), (-2, 0)],
            [(0, 1), (1, 0), (2, -1), (1, -2)]
        ]

        new_rotation = rotation
        # Si la acción es rotar la pieza, se verifica si la rotación es la última permitida o alguna de las anteriores
        if movement == "rotate":
            new_rotation = 0 if rotation == 3 else rotation + 1

        # Recorre el tablero actual para verificar y crear el nuevo tablero por sus nuevas coordenadas
        for row_index, row in enumerate(screen):
            for column_index, item in enumerate(row):
                if item == "🔳":
                    new_row_index = 0
                    new_column_index = 0

                    if movement == "down":
                        new_row_index = row_index + 1
                        new_column_index = column_index
                    elif movement == "right":
                        new_row_index = row_index
                        new_column_index = column_index + 1
                    elif movement == "left":
                        new_row_index = row_index
                        new_column_index = column_index - 1
                    elif movement == "rotate":
                        new_row_index = row_index + rotate[new_rotation][rotation_item][0]
                        new_column_index = column_index + rotate[new_rotation][rotation_item][1]
                        rotation_item += 1

                    if new_row_index > 9 or new_column_index > 9 or new_column_index < 0:
                        console.print("\n[red bold]No se puede realizar el movimiento![/red bold]\n")
                        return screen, rotation
                    else:
                        new_screen[new_row_index][new_column_index] = "🔳"
        self.screen = new_screen
        self.print_screen()
        return new_screen, new_rotation


def main():
    tetris_init = PyTetris()

    # Imprime el tablero inicial
    tetris_init.print_screen()

    # Variables iniciales: screen -> pantalla inicial, rotation -> valor inicial de rotación
    screen = tetris_init.screen
    rotation = 0

    while True:
        event = keyboard.read_event()

        if event.name == "esc":
            break
        elif event.event_type == keyboard.KEY_UP:
            console.print("\r")
            if event.name == "down":
                screen, rotation = tetris_init.move_piece(screen, "down", rotation)
            if event.name == "right":
                screen, rotation = tetris_init.move_piece(screen, "right", rotation)
            if event.name == "left":
                screen, rotation = tetris_init.move_piece(screen, "left", rotation)
            if event.name == "space":
                screen, rotation = tetris_init.move_piece(screen, "rotate", rotation)


if __name__ == '__main__':
    typer.run(main)
