import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 520
WINDOW_TITLE = "Starting Template"


# Deve conter um menu inicial para definir o Grid da simulação:
# - Irá definir o espaço de busca, quanto médicos e quantos pacientes.
# Grid deve ser desenho a mão(não usar sprites no cenário).
# Usar sprites apenas para os médicos e pacientes.
# Animações e movimentações devem ser realizados pelo agente.


# Modelo de exemplo do arcade

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON

    def reset(self):
        pass

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    game = GameView()

    window.show_view(game)

    arcade.run()

if __name__ == "__main__":
    main()