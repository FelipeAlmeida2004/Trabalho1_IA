"""Executa a busca Prolog usando o cenário exibido na interface."""

from __future__ import annotations

from pathlib import Path
from secrets import randbits
from threading import Lock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scenario import Scenario

SEARCH_TIMEOUT_SECONDS = 15
_PROLOG_LOCK = Lock()
_BRIDGE_FILE = Path(__file__).resolve().parents[1] / "interface_bridge.pl"


def initialize_prolog():
    """Importa o Janus na thread da interface antes de criar os workers."""
    try:
        import janus_swi as janus
    except (ImportError, OSError) as error:
        raise RuntimeError(
            "Não foi possível carregar o Janus. Execute poetry install e "
            "confira se o SWI-Prolog está instalado e no PATH."
        ) from error
    return janus


def generate_scenario(num_doctors: int, num_patients: int, seed: int | None) -> dict:
    """Sorteia um cenário viável usando os próprios perfis e regras Prolog."""
    if num_doctors < 1 or num_patients < 0:
        raise ValueError("É necessário ao menos um médico e zero ou mais pacientes.")
    if seed is None:
        seed = randbits(31)
    janus = initialize_prolog()
    with _PROLOG_LOCK:
        janus.consult(str(_BRIDGE_FILE))
        result = janus.query_once(
            "gerar_cenario_interface(NumeroMedicos, NumeroPacientes, Semente, "
            "Medicos, Pacientes, Limite)",
            {"NumeroMedicos": num_doctors, "NumeroPacientes": num_patients,
             "Semente": seed},
        )
    if not result["truth"]:
        raise RuntimeError("Não foi possível gerar um cenário com os perfis cadastrados.")
    return {"doctors": result["Medicos"], "patients": result["Pacientes"],
            "queue_limit": result["Limite"], "seed": seed}


def solve_scenario(scenario: Scenario) -> dict | None:
    """Devolve os quadros da solução, ou None se não existir distribuição.

    A chamada deve ocorrer fora do evento de desenho. Não modifica o cenário
    Python: a interface aplica os quadros quando recebe o resultado.
    """
    if any(doctor.queue for doctor in scenario.doctors):
        raise ValueError("Abra um novo cenário antes de executar outra busca.")

    janus = initialize_prolog()

    inputs = {
        "Medicos": [
            [doctor.doctor_id, list(doctor.specialties)]
            for doctor in scenario.doctors
        ],
        "Pacientes": [
            [patient.patient_id, patient.risk, list(patient.groups)]
            for patient in scenario.waiting
        ],
        "Limite": scenario.queue_limit,
        "Tempo": SEARCH_TIMEOUT_SECONDS,
    }

    # Serializa o carregamento do arquivo e as consultas entre telas distintas.
    # Os dados de cada busca também são isolados por snapshot/1 no Prolog.
    with _PROLOG_LOCK:
        janus.consult(str(_BRIDGE_FILE))
        result = janus.query_once(
            "catch((call_with_time_limit(Tempo, "
            "resolver_interface(Medicos, Pacientes, Limite, "
            "Quadros, Gerados, Expandidos)), Status = sucesso), "
            "time_limit_exceeded, "
            "(Status = tempo_esgotado, Quadros = [], Gerados = 0, Expandidos = 0))",
            inputs,
        )

    if not result["truth"]:
        return None
    if result["Status"] == "tempo_esgotado":
        raise TimeoutError(
            f"A busca excedeu {SEARCH_TIMEOUT_SECONDS} segundos. "
            "Tente um cenário menor."
        )

    return {
        "frames": result["Quadros"],
        "generated": result["Gerados"],
        "expanded": result["Expandidos"],
    }
