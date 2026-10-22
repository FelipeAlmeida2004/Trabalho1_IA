"""Tela do cenário da simulação."""

from __future__ import annotations

from collections import deque
from queue import Empty, SimpleQueue
from threading import Thread
from textwrap import wrap
import traceback
from typing import TYPE_CHECKING

import arcade

try:
    from .prolog_bridge import initialize_prolog, solve_scenario
    from .scenario import GROUP_INITIALS, Doctor, Patient, build_scenario
except ImportError:  # executado como script, fora do pacote
    from prolog_bridge import initialize_prolog, solve_scenario
    from scenario import GROUP_INITIALS, Doctor, Patient, build_scenario

if TYPE_CHECKING:
    from .main_view import MainView

WINDOW_WIDTH = 930
WINDOW_HEIGHT = 700

BACKGROUND_COLOR = arcade.color.DARK_MIDNIGHT_BLUE

GRID_COLOR = arcade.color.DARK_SLATE_GRAY
GRID_LINE_COLOR = arcade.color.LIGHT_GRAY
PANEL_COLOR = arcade.color.DARK_SLATE_BLUE
DOCTOR_COLOR = arcade.color.DARK_CYAN
GENERALIST_COLOR = arcade.color.TEAL

RISK_COLORS = {
    "baixa": arcade.color.MEDIUM_SEA_GREEN,
    "media": arcade.color.GOLD,
    "alta": arcade.color.TOMATO,
}

TEXT_COLOR = arcade.color.WHITE
SECONDARY_TEXT_COLOR = arcade.color.LIGHT_GRAY
TOKEN_TEXT_COLOR = arcade.color.BLACK

BACK_BUTTON_COLOR = arcade.color.DARK_RED
BACK_BUTTON_CENTER_X = 830
BACK_BUTTON_CENTER_Y = 165
BACK_BUTTON_WIDTH = 150
BACK_BUTTON_HEIGHT = 52

SOLVE_BUTTON_CENTER_Y = 225
SOLVE_BUTTON_COLOR = arcade.color.DARK_GREEN
ANIMATION_INTERVAL = 0.4

Hotspot = tuple[float, float, float, float, list[str]]


class SimulationView(arcade.View):
    """Exibe a fila de espera, a lista de cada médico e os parâmetros."""

    GRID_ORIGIN_X = 175
    GRID_ORIGIN_Y = 65
    GRID_MAX_SIZE = 560

    QUEUE_COLUMNS = 4
    QUEUE_TOKEN_SIZE = 34
    QUEUE_TOKEN_PITCH = 40
    QUEUE_ORIGIN_X = 27
    QUEUE_ORIGIN_Y = 565

    MIN_TEXT_SIZE = 26

    def __init__(
        self,
        num_doctors: int,
        num_patients: int,
        previous_view: MainView | None = None,
    ) -> None:
        super().__init__()
        self.num_doctors = num_doctors
        self.num_patients = num_patients
        self.previous_view = previous_view
        self.background_color = BACKGROUND_COLOR

        self.scenario = build_scenario(num_doctors, num_patients)
        self._mouse_x = -1.0
        self._mouse_y = -1.0
        self._hotspots: list[Hotspot] = []
        self._text_cache: dict[tuple, arcade.Text] = {}
        self._results: SimpleQueue = SimpleQueue()
        self._searching = False
        self._frames: deque = deque()
        self._animation_elapsed = 0.0
        self._status = "Cenario viavel. Clique em RESOLVER."
        self._statistics: tuple[int, int] | None = None
        self._patients = {
            patient.patient_id: patient for patient in self.scenario.waiting
        }

    def _draw_text(
        self,
        text: str,
        x: float,
        y: float,
        color: arcade.Color,
        font_size: int,
        anchor_x: str = "left",
        anchor_y: str = "baseline",
    ) -> None:
        """Como arcade.draw_text, reaproveitando o objeto Text (bem mais rápido)."""
        if not text:
            return
        key = (text, color, font_size, anchor_x, anchor_y)
        label = self._text_cache.get(key)
        if label is None:
            label = arcade.Text(
                text,
                x,
                y,
                color,
                font_size,
                anchor_x=anchor_x,
                anchor_y=anchor_y,
            )
            self._text_cache[key] = label
        label.x = x
        label.y = y
        label.draw()

    def on_draw(self) -> None:
        self.clear()
        self._hotspots = []

        arcade.draw_text(
            "CENARIO DE SIMULACAO",
            WINDOW_WIDTH / 2,
            640,
            TEXT_COLOR,
            28,
            anchor_x="center",
        )
        self._draw_waiting_queue()
        self._draw_grid()
        self._draw_legend()
        self._draw_summary()
        self._draw_tooltip()

    def _draw_waiting_queue(self) -> None:
        self._draw_text(
            "FILA DE ESPERA",
            87,
            598,
            TEXT_COLOR,
            14,
            anchor_x="center",
        )

        for index, patient in enumerate(self.scenario.waiting):
            row, column = divmod(index, self.QUEUE_COLUMNS)
            self._draw_patient(
                patient,
                self.QUEUE_ORIGIN_X + column * self.QUEUE_TOKEN_PITCH,
                self.QUEUE_ORIGIN_Y - row * self.QUEUE_TOKEN_PITCH,
                self.QUEUE_TOKEN_SIZE,
            )

    def _draw_grid(self) -> None:
        """Uma linha por médico: a célula do médico e uma célula por vaga."""
        limit = self.scenario.queue_limit
        columns = limit + 1
        rows = len(self.scenario.doctors)
        cell_size = min(self.GRID_MAX_SIZE / columns, self.GRID_MAX_SIZE / rows)

        left = self.GRID_ORIGIN_X
        top = self.GRID_ORIGIN_Y + self.GRID_MAX_SIZE

        for row, doctor in enumerate(self.scenario.doctors):
            center_y = top - (row + 0.5) * cell_size
            self._draw_doctor(doctor, left + 0.5 * cell_size, center_y, cell_size)

            for slot in range(limit):
                center_x = left + (slot + 1.5) * cell_size
                arcade.draw_rect_filled(
                    arcade.XYWH(center_x, center_y, cell_size - 2, cell_size - 2),
                    GRID_COLOR,
                )
                if slot < len(doctor.queue):
                    self._draw_patient(
                        doctor.queue[slot],
                        center_x,
                        center_y,
                        cell_size - 8,
                    )
                elif cell_size >= 40:
                    self._draw_text(
                        str(slot + 1),
                        center_x,
                        center_y,
                        SECONDARY_TEXT_COLOR,
                        10,
                        anchor_x="center",
                        anchor_y="center",
                    )

        arcade.draw_rect_outline(
            arcade.XYWH(
                left + columns * cell_size / 2,
                top - rows * cell_size / 2,
                columns * cell_size,
                rows * cell_size,
            ),
            GRID_LINE_COLOR,
            2,
        )

    def _draw_doctor(
        self,
        doctor: Doctor,
        center_x: float,
        center_y: float,
        cell_size: float,
    ) -> None:
        color = GENERALIST_COLOR if doctor.is_generalist else DOCTOR_COLOR
        arcade.draw_rect_filled(
            arcade.XYWH(center_x, center_y, cell_size - 2, cell_size - 2),
            color,
        )
        self._draw_text(
            doctor.doctor_id.upper(),
            center_x,
            center_y + (6 if cell_size >= 50 else 0),
            TEXT_COLOR,
            max(10, int(cell_size * 0.26)),
            anchor_x="center",
            anchor_y="center",
        )
        if cell_size >= 50:
            tag = "geral" if doctor.is_generalist else doctor.specialties[0][:8]
            self._draw_text(
                tag,
                center_x,
                center_y - 14,
                TEXT_COLOR,
                9,
                anchor_x="center",
                anchor_y="center",
            )

        self._add_hotspot(
            center_x,
            center_y,
            cell_size,
            [
                f"Medico {doctor.doctor_id.upper()}",
                "Especialidades: " + ", ".join(doctor.specialties),
                f"Pacientes: {len(doctor.queue)}/{self.scenario.queue_limit}",
            ],
        )

    def _draw_patient(
        self,
        patient: Patient,
        center_x: float,
        center_y: float,
        size: float,
    ) -> None:
        arcade.draw_rect_filled(
            arcade.XYWH(center_x, center_y, size, size),
            RISK_COLORS[patient.risk],
        )
        arcade.draw_rect_outline(
            arcade.XYWH(center_x, center_y, size, size),
            TEXT_COLOR,
            1,
        )
        if size >= self.MIN_TEXT_SIZE:
            font_size = max(8, int(size * 0.28))
            self._draw_text(
                patient.patient_id,
                center_x,
                center_y + size * 0.12,
                TOKEN_TEXT_COLOR,
                font_size,
                anchor_x="center",
                anchor_y="center",
            )
            self._draw_text(
                patient.group_initials,
                center_x,
                center_y - size * 0.22,
                TOKEN_TEXT_COLOR,
                max(7, font_size - 1),
                anchor_x="center",
                anchor_y="center",
            )

        self._add_hotspot(
            center_x,
            center_y,
            size,
            [
                f"Paciente {patient.patient_id}",
                f"Risco: {patient.risk}",
                "Grupos: " + ", ".join(patient.groups),
                f"Prioridade: {patient.priority}",
            ],
        )

    def _add_hotspot(
        self,
        center_x: float,
        center_y: float,
        size: float,
        lines: list[str],
    ) -> None:
        half = size / 2
        self._hotspots.append(
            (center_x - half, center_y - half, center_x + half, center_y + half, lines)
        )

    def _draw_legend(self) -> None:
        self._draw_text("RISCO", 12, 195, TEXT_COLOR, 12)
        for index, risk in enumerate(RISK_COLORS):
            y = 175 - index * 20
            arcade.draw_rect_filled(arcade.XYWH(20, y + 5, 14, 14), RISK_COLORS[risk])
            self._draw_text(risk, 34, y, SECONDARY_TEXT_COLOR, 11)

        self._draw_text("GRUPOS", 12, 105, TEXT_COLOR, 12)
        groups = [
            f"{initials} {group}"
            for group, initials in GROUP_INITIALS.items()
            if initials
        ]
        for index, text in enumerate(groups):
            column, row = index % 2, index // 2
            self._draw_text(
                text,
                12 + column * 80,
                85 - row * 18,
                SECONDARY_TEXT_COLOR,
                10,
            )

    def _draw_summary(self) -> None:
        panel_x = BACK_BUTTON_CENTER_X
        assigned = sum(len(doctor.queue) for doctor in self.scenario.doctors)

        arcade.draw_text("PARAMETROS", panel_x, 450, TEXT_COLOR, 20, anchor_x="center")
        summary = (
            (410, f"Medicos: {self.num_doctors}"),
            (370, f"Pacientes: {self.num_patients}"),
            (330, f"Limite por medico: {self.scenario.queue_limit}"),
            (290, f"Na espera: {len(self.scenario.waiting)}"),
            (265, f"Atribuidos: {assigned}"),
        )
        for y, text in summary:
            arcade.draw_text(
                text,
                panel_x,
                y,
                SECONDARY_TEXT_COLOR,
                12 if y == 330 else 14,
                anchor_x="center",
            )
        can_solve = self._can_solve()
        arcade.draw_rect_filled(
            arcade.XYWH(
                panel_x, SOLVE_BUTTON_CENTER_Y,
                BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT,
            ),
            SOLVE_BUTTON_COLOR if can_solve else GRID_COLOR,
        )
        self._draw_text(
            "BUSCANDO..." if self._searching else "RESOLVER",
            panel_x, SOLVE_BUTTON_CENTER_Y - 9,
            TEXT_COLOR, 16, anchor_x="center",
        )
        arcade.draw_rect_filled(
            arcade.XYWH(
                BACK_BUTTON_CENTER_X,
                BACK_BUTTON_CENTER_Y,
                BACK_BUTTON_WIDTH,
                BACK_BUTTON_HEIGHT,
            ),
            BACK_BUTTON_COLOR,
        )
        arcade.draw_text(
            "VOLTAR",
            panel_x,
            BACK_BUTTON_CENTER_Y - 9,
            TEXT_COLOR,
            16,
            anchor_x="center",
        )
        for index, line in enumerate(wrap(self._status, width=26)):
            self._draw_text(
                line, panel_x, 120 - index * 16,
                SECONDARY_TEXT_COLOR, 10, anchor_x="center",
            )
        if self._statistics is not None:
            generated, expanded = self._statistics
            self._draw_text(
                f"Gerados: {generated}", panel_x, 35,
                SECONDARY_TEXT_COLOR, 10, anchor_x="center",
            )
            self._draw_text(
                f"Expandidos: {expanded}", panel_x, 19,
                SECONDARY_TEXT_COLOR, 10, anchor_x="center",
            )

    def _can_solve(self) -> bool:
        return (
            not self._searching
            and not self._frames
            and bool(self.scenario.waiting)
            and not any(doctor.queue for doctor in self.scenario.doctors)
        )

    def _start_search(self) -> None:
        if not self._can_solve():
            return
        try:
            initialize_prolog()
        except Exception as error:
            traceback.print_exc()
            self._status = str(error)
            return
        self._searching = True
        self._statistics = None
        self._status = "Buscando uma distribuicao..."
        Thread(target=self._search_worker, daemon=True).start()

    def _search_worker(self) -> None:
        try:
            result = solve_scenario(self.scenario)
        except Exception as error:
            traceback.print_exc()
            self._results.put(("error", str(error)))
        else:
            self._results.put(("result", result))

    def on_update(self, delta_time: float) -> None:
        # Somente a thread da interface altera os objetos desenhados.
        try:
            kind, result = self._results.get_nowait()
        except Empty:
            pass
        else:
            self._searching = False
            if kind == "error":
                self._status = result
            elif result is None:
                self._status = "Sem solucao neste cenario."
            else:
                self._statistics = (result["generated"], result["expanded"])
                self._frames = deque(result["frames"])
                self._animation_elapsed = 0.0
                self._status = "Distribuindo pacientes..."

        if self._frames:
            self._animation_elapsed += delta_time
            if self._animation_elapsed >= ANIMATION_INTERVAL:
                self._animation_elapsed = 0.0
                frame = self._frames.popleft()
                self._apply_frame(frame)

    def _apply_frame(self, frame: dict) -> None:
        self.scenario.waiting = [self._patients[pid] for pid in frame["espera"]]
        queues = dict(frame["filas"])
        for doctor in self.scenario.doctors:
            doctor.queue = [self._patients[pid] for pid in queues[doctor.doctor_id]]
        if self._frames:
            self._status = f"{frame['paciente']} para {frame['medico']}."
        else:
            self._status = "Distribuicao concluida!"

    def _draw_tooltip(self) -> None:
        for left, bottom, right, top, lines in self._hotspots:
            if left <= self._mouse_x <= right and bottom <= self._mouse_y <= top:
                break
        else:
            return

        width = max(len(line) for line in lines) * 7 + 16
        height = len(lines) * 18 + 10
        x = min(self._mouse_x + 14, WINDOW_WIDTH - width - 4)
        y = max(self._mouse_y - 14 - height, 4)

        arcade.draw_rect_filled(
            arcade.XYWH(x + width / 2, y + height / 2, width, height),
            PANEL_COLOR,
        )
        arcade.draw_rect_outline(
            arcade.XYWH(x + width / 2, y + height / 2, width, height),
            GRID_LINE_COLOR,
            1,
        )
        for index, line in enumerate(lines):
            self._draw_text(
                line,
                x + 8,
                y + height - 22 - index * 18,
                TEXT_COLOR,
                12,
            )

    def on_mouse_motion(self, x: float, y: float, _dx: float, _dy: float) -> None:
        self._mouse_x = x
        self._mouse_y = y

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self._go_back()
        elif symbol == arcade.key.SPACE:
            self._start_search()

    def on_mouse_press(
        self,
        x: float,
        y: float,
        button: int,
        _modifiers: int,
    ) -> None:
        if (
            button == arcade.MOUSE_BUTTON_LEFT
            and BACK_BUTTON_CENTER_X - BACK_BUTTON_WIDTH / 2 <= x
            <= BACK_BUTTON_CENTER_X + BACK_BUTTON_WIDTH / 2
            and SOLVE_BUTTON_CENTER_Y - BACK_BUTTON_HEIGHT / 2 <= y
            <= SOLVE_BUTTON_CENTER_Y + BACK_BUTTON_HEIGHT / 2
        ):
            self._start_search()
            return
        if (
            button == arcade.MOUSE_BUTTON_LEFT
            and BACK_BUTTON_CENTER_X - BACK_BUTTON_WIDTH / 2 <= x
            <= BACK_BUTTON_CENTER_X + BACK_BUTTON_WIDTH / 2
            and BACK_BUTTON_CENTER_Y - BACK_BUTTON_HEIGHT / 2 <= y
            <= BACK_BUTTON_CENTER_Y + BACK_BUTTON_HEIGHT / 2
        ):
            self._go_back()

    def _go_back(self) -> None:
        if self.previous_view is not None and self.window is not None:
            self.window.show_view(self.previous_view)
