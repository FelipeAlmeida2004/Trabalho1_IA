"""Dados do cenário da simulação, seguindo o PEAS (docs/PEAS.md)."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

RISK_WEIGHTS = {"baixa": 1, "media": 2, "alta": 3}
GROUP_WEIGHTS = {
    "geral": 1,
    "deficiente": 2,
    "idoso": 3,
    "crianca": 4,
    "gestante": 5,
}
GROUP_INITIALS = {
    "geral": "",
    "deficiente": "D",
    "idoso": "I",
    "crianca": "C",
    "gestante": "G",
}

GENERALIST_SPECIALTY = "clinico_geral"
SPECIALTIES = (
    "traumatologista",
    "emergencista",
    "cardiologista",
    "intensivista",
    "pediatra",
    "geriatra",
    "obstetra",
    "gastroenterologista",
    "fisiatra",
)

MIN_QUEUE_LIMIT = 5
DEFAULT_SEED = 7


@dataclass(frozen=True)
class Patient:
    """Paciente na fila de espera ou na lista de um médico."""

    patient_id: str
    risk: str
    groups: tuple[str, ...]

    @property
    def priority(self) -> int:
        return RISK_WEIGHTS[self.risk] + max(GROUP_WEIGHTS[g] for g in self.groups)

    @property
    def group_initials(self) -> str:
        return "".join(GROUP_INITIALS[g] for g in self.groups)


@dataclass
class Doctor:
    """Médico com a lista ordenada de pacientes atribuídos a ele."""

    doctor_id: str
    specialties: tuple[str, ...]
    queue: list[Patient] = field(default_factory=list)

    @property
    def is_generalist(self) -> bool:
        return GENERALIST_SPECIALTY in self.specialties


@dataclass
class Scenario:
    """Estado da simulação: fila de espera e lista de cada médico."""

    doctors: list[Doctor]
    waiting: list[Patient]
    queue_limit: int


def queue_limit(num_patients: int, num_doctors: int) -> int:
    """Limite de pacientes por médico: max(5, ceil(pacientes / médicos))."""
    return max(MIN_QUEUE_LIMIT, math.ceil(num_patients / num_doctors))


def build_scenario(
    num_doctors: int,
    num_patients: int,
    seed: int = DEFAULT_SEED,
) -> Scenario:
    """Cria o estado inicial: todos os pacientes na espera, médicos sem pacientes."""
    rng = random.Random(seed)

    doctors = [Doctor("m1", (GENERALIST_SPECIALTY,))]
    for number in range(2, num_doctors + 1):
        specialties = tuple(rng.sample(SPECIALTIES, rng.choice((1, 2))))
        doctors.append(Doctor(f"m{number}", specialties))

    special_groups = tuple(group for group in GROUP_WEIGHTS if group != "geral")
    waiting = []
    for number in range(1, num_patients + 1):
        risk = rng.choice(tuple(RISK_WEIGHTS))
        if rng.random() < 0.4:
            groups = ("geral",)
        else:
            groups = tuple(rng.sample(special_groups, rng.choice((1, 2))))
        waiting.append(Patient(f"p{number}", risk, groups))

    return Scenario(doctors, waiting, queue_limit(num_patients, num_doctors))
