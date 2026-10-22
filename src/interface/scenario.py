"""Dados do cenário da simulação, seguindo o PEAS (docs/PEAS.md)."""

from __future__ import annotations

import math
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
MIN_QUEUE_LIMIT = 5


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
    seed: int | None = None


def queue_limit(num_patients: int, num_doctors: int) -> int:
    """Limite de pacientes por médico: max(5, ceil(pacientes / médicos))."""
    return max(MIN_QUEUE_LIMIT, math.ceil(num_patients / num_doctors))


def build_scenario(
    num_doctors: int,
    num_patients: int,
    seed: int | None = None,
) -> Scenario:
    """Cria uma espera aleatória viável, mantendo vazias as filas dos médicos.

    Sem semente, cada chamada faz um novo sorteio. Uma semente explícita permite
    reproduzir o cenário. O Prolog verifica cada escolha durante a construção;
    a sequência usada nessa verificação não é entregue ao algoritmo de busca.
    """
    try:
        from .prolog_bridge import generate_scenario
    except ImportError:
        from prolog_bridge import generate_scenario

    data = generate_scenario(num_doctors, num_patients, seed)
    doctors = [Doctor(did, tuple(specialties)) for did, specialties in data["doctors"]]
    waiting = [Patient(pid, risk, tuple(groups)) for pid, risk, groups in data["patients"]]
    return Scenario(doctors, waiting, data["queue_limit"], data["seed"])
