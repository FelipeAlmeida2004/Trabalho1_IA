"""Tela de configuração da simulação."""

from __future__ import annotations

import sys
from pathlib import Path

import arcade

try:
    from integrate_pl import gerar_e_adicionar
    from .scenario import queue_limit
    from .simulation_view import SimulationView
except ImportError:  # executado como script, fora do pacote
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from integrate_pl import gerar_e_adicionar
    from scenario import queue_limit
    from simulation_view import SimulationView

WINDOW_WIDTH = 930
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Simulador Hospitalar"

BACKGROUND_COLOR = arcade.color.DARK_MIDNIGHT_BLUE

PANEL_COLOR = arcade.color.DARK_SLATE_BLUE
TEXT_COLOR = arcade.color.WHITE
SECONDARY_TEXT_COLOR = arcade.color.LIGHT_GRAY

ERROR_TEXT_COLOR = arcade.color.LIGHT_SALMON

START_BUTTON_COLOR = arcade.color.DARK_GREEN
DECREASE_BUTTON_COLOR = arcade.color.DARK_RED
INCREASE_BUTTON_COLOR = arcade.color.DARK_BLUE


class MainView(arcade.View):
    """Permite configurar os parâmetros antes de iniciar a simulação."""

    PARAMETER_ROWS = (
        ("Quantidade de médicos", "num_doctors", 1, 10, 430),
        ("Quantidade de pacientes", "num_patients", 1, 30, 340),
    )
    LIMIT_ROW_Y = 250

    def __init__(self) -> None:
        super().__init__()
        self.num_doctors = 2
        self.num_patients = 8
        self.error_message = ""
        self.background_color = BACKGROUND_COLOR

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_text(
            "SIMULADOR HOSPITALAR",
            WINDOW_WIDTH / 2,
            610,
            TEXT_COLOR,
            28,
            anchor_x="center",
        )
        arcade.draw_text(
            "Configure o ambiente antes de iniciar",
            WINDOW_WIDTH / 2,
            570,
            SECONDARY_TEXT_COLOR,
            15,
            anchor_x="center",
        )

        for label, attribute, _, _, y in self.PARAMETER_ROWS:
            self._draw_parameter(label, getattr(self, attribute), y)

        self._draw_parameter(
            "Limite por médico (calculado)",
            queue_limit(self.num_patients, self.num_doctors),
            self.LIMIT_ROW_Y,
            editable=False,
        )

        arcade.draw_rect_filled(
            arcade.XYWH(WINDOW_WIDTH / 2, 125, 300, 60),
            START_BUTTON_COLOR,
        )
        arcade.draw_text(
            "INICIAR SIMULACAO",
            WINDOW_WIDTH / 2,
            116,
            TEXT_COLOR,
            16,
            anchor_x="center",
        )
        if self.error_message:
            arcade.draw_text(
                self.error_message,
                WINDOW_WIDTH / 2,
                80,
                ERROR_TEXT_COLOR,
                13,
                anchor_x="center",
            )
        arcade.draw_text(
            "Use os botoes - e + para alterar os valores",
            WINDOW_WIDTH / 2,
            45,
            SECONDARY_TEXT_COLOR,
            12,
            anchor_x="center",
        )

    def _draw_parameter(
        self,
        label: str,
        value: int,
        y: int,
        editable: bool = True,
    ) -> None:
        arcade.draw_rect_filled(
            arcade.XYWH(WINDOW_WIDTH / 2, y + 10, 650, 58),
            PANEL_COLOR,
        )
        arcade.draw_text(label, 145, y, TEXT_COLOR, 18)
        arcade.draw_text(
            str(value),
            WINDOW_WIDTH / 2,
            y,
            TEXT_COLOR,
            20,
            anchor_x="center",
        )
        if editable:
            self._draw_button("-", 590, y + 10, DECREASE_BUTTON_COLOR)
            self._draw_button("+", 670, y + 10, INCREASE_BUTTON_COLOR)

    @staticmethod
    def _draw_button(label: str, center_x: int, center_y: int, color: arcade.Color) -> None:
        arcade.draw_rect_filled(arcade.XYWH(center_x, center_y, 40, 40), color)
        arcade.draw_text(
            label,
            center_x,
            center_y - 11,
            TEXT_COLOR,
            22,
            anchor_x="center",
        )

    def on_mouse_press(
        self,
        x: float,
        y: float,
        button: int,
        _modifiers: int,
    ) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        for _, attribute, minimum, maximum, row_y in self.PARAMETER_ROWS:
            if row_y - 10 <= y <= row_y + 50:
                if 570 <= x <= 610:
                    self._change_parameter(attribute, -1, minimum, maximum)
                elif 650 <= x <= 690:
                    self._change_parameter(attribute, 1, minimum, maximum)
                return

        if 300 <= x <= 600 and 95 <= y <= 155:
            self._start_simulation()

    def _start_simulation(self) -> None:
        """Gera os fatos com os valores da tela e abre o cenário."""
        try:
            gerar_e_adicionar(self.num_doctors, self.num_patients)
        except Exception as error:
            self.error_message = f"Erro ao gerar os fatos: {error}"
            return

        self.error_message = ""
        self.window.show_view(
            SimulationView(
                num_doctors=self.num_doctors,
                num_patients=self.num_patients,
                previous_view=self,
            )
        )

    def _change_parameter(
        self,
        attribute: str,
        amount: int,
        minimum: int,
        maximum: int,
    ) -> None:
        value = getattr(self, attribute)
        setattr(self, attribute, max(minimum, min(maximum, value + amount)))


def main() -> None:
    """Cria a janela principal e inicia o loop do Arcade."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.show_view(MainView())
    arcade.run()


if __name__ == "__main__":
    main()
