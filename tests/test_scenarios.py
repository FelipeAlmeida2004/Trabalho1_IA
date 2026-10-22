"""Regressões da geração e das distribuições devolvidas pelo Prolog.

Execute: poetry run python -m unittest discover -s tests -v
"""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interface.prolog_bridge import initialize_prolog, solve_scenario
from interface.scenario import Doctor, Patient, Scenario, build_scenario


class ScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.janus = initialize_prolog()
        cls.janus.consult(str(ROOT / "src/interface_bridge.pl"))
        cls.facts_before = (ROOT / "src/facts.pl").read_bytes()
        data = cls.janus.query_once(
            "findall([_E,_R,_G],perfil(_E,_R,_G),Perfis), "
            "findall(_E,generalista(_E),Gerais), "
            "findall([_R,_P],taxa_critica(_R,_P),Riscos), "
            "findall([_G,_P],grupo_critico(_G,_P),Grupos)"
        )
        cls.profiles = data["Perfis"]
        cls.generalists = set(data["Gerais"])
        cls.risk_weights = dict(data["Riscos"])
        cls.group_weights = dict(data["Grupos"])

    def is_specialist(self, patient, doctor):
        return any(
            specialty in doctor.specialties
            and specialty not in self.generalists
            and risk == patient.risk and group in patient.groups
            for specialty, risk, group in self.profiles
        )

    def assert_valid_solution(self, scenario):
        self.assertTrue(all(not doctor.queue for doctor in scenario.doctors))
        result = solve_scenario(scenario)
        self.assertIsNotNone(result)
        self.assertEqual(len(result["frames"]), len(scenario.waiting))
        patients = {p.patient_id: p for p in scenario.waiting}
        doctors = {d.doctor_id: d for d in scenario.doctors}
        waiting = list(patients)
        queues = {did: [] for did in doctors}

        def priority(pid):
            p = patients[pid]
            return self.risk_weights[p.risk] + max(
                self.group_weights[g] for g in p.groups
            )

        for frame in result["frames"]:
            pid, did = frame["paciente"], frame["medico"]
            self.assertEqual(pid, waiting[0])
            self.assertIn(did, doctors)
            self.assertLess(len(queues[did]), scenario.queue_limit)
            if not self.is_specialist(patients[pid], doctors[did]):
                self.assertTrue(self.generalists.intersection(doctors[did].specialties))
                self.assertFalse(any(
                    self.is_specialist(patients[pid], doctor)
                    and len(queues[other_id]) < scenario.queue_limit
                    for other_id, doctor in doctors.items()
                ))
            waiting.pop(0)
            queues[did].append(pid)
            queues[did].sort(key=priority, reverse=True)
            self.assertEqual(frame["espera"], waiting)
            self.assertEqual(dict(frame["filas"]), queues)

        self.assertFalse(waiting)
        assigned = [pid for queue in queues.values() for pid in queue]
        self.assertCountEqual(assigned, patients)
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertTrue(all(len(queue) <= scenario.queue_limit for queue in queues.values()))
        # Resolver não altera os objetos usados para desenhar o estado inicial.
        self.assertEqual(list(patients), [p.patient_id for p in scenario.waiting])
        self.assertTrue(all(not doctor.queue for doctor in scenario.doctors))

    def test_all_300_interface_configurations(self):
        for doctors in range(1, 11):
            for patients in range(1, 31):
                with self.subTest(doctors=doctors, patients=patients):
                    self.assert_valid_solution(build_scenario(doctors, patients, seed=7))

    def test_200_seeds_for_formerly_failing_default(self):
        for seed in range(200):
            with self.subTest(seed=seed):
                self.assert_valid_solution(build_scenario(2, 8, seed=seed))

    def test_larger_scenarios_with_other_seeds(self):
        for doctors in (3, 5, 10):
            for seed in range(20):
                with self.subTest(doctors=doctors, seed=seed):
                    self.assert_valid_solution(build_scenario(doctors, 30, seed=seed))

    def test_seed_reproduces_scenario(self):
        self.assertEqual(build_scenario(4, 20, seed=7), build_scenario(4, 20, seed=7))

    def test_default_requests_a_new_seed(self):
        with patch("interface.prolog_bridge.randbits", side_effect=[7, 8]):
            first, second = build_scenario(2, 8), build_scenario(2, 8)
        self.assertEqual((first.seed, second.seed), (7, 8))

    def test_general_is_exclusive(self):
        scenario = build_scenario(10, 30, seed=7)
        for patient in scenario.waiting:
            if "geral" in patient.groups:
                self.assertEqual(patient.groups, ("geral",))

    def test_invalid_counts(self):
        for doctors, patients in ((0, 8), (-1, 8), (2, -1)):
            with self.subTest(doctors=doctors, patients=patients):
                with self.assertRaises(ValueError):
                    build_scenario(doctors, patients)

    def test_empty_waiting_queue(self):
        scenario = build_scenario(2, 0, seed=7)
        self.assert_valid_solution(scenario)

    def test_manually_infeasible_data_is_still_rejected(self):
        impossible = Scenario(
            [Doctor("m1", ("clinico_geral",)), Doctor("m2", ("pediatra",))],
            [Patient(f"p{i}", "media", ("idoso",)) for i in range(1, 9)],
            5,
        )
        self.assertIsNone(solve_scenario(impossible))

    def test_reference_distribution_is_preserved(self):
        result = self.janus.query_once(
            "resolver(_Listas,_Acoes,estatisticas(Gerados,Expandidos)), "
            "findall([_Id,_Ps],member(fila(_Id,_Ps),_Listas),Filas)"
        )
        self.assertEqual(result["Filas"], [
            ["m1", ["p5", "p8", "p3"]],
            ["m2", ["p1", "p2", "p4", "p6", "p7"]],
        ])

    def test_generation_reads_the_actual_profile_catalog(self):
        # A mudança existe apenas neste processo e é desfeita pelo snapshot.
        self.janus.query_once("dynamic(perfil/3)")
        result = self.janus.query_once(
            "snapshot((retractall(perfil(_,_,_)), "
            "assertz(perfil(especialidade_de_teste,media,idoso)), "
            "gerar_cenario_interface(2,8,7,Medicos,Pacientes,Limite)))"
        )
        self.assertTrue(result["truth"])
        self.assertEqual(result["Medicos"][1][1], ["especialidade_de_teste"])
        self.assertEqual(self.janus.query_once(
            "findall([_E,_R,_G],perfil(_E,_R,_G),Perfis)"
        )["Perfis"], self.profiles)

    def test_generation_preserves_reference_facts_and_random_state(self):
        random_before = self.janus.query_once("getrand(Estado)")["Estado"]
        build_scenario(10, 30, seed=7)
        self.assertEqual(self.janus.query_once("getrand(Estado)")["Estado"], random_before)
        self.assertEqual(self.janus.query_once("medico(m1,Nome,_)")["Nome"], "Roberto")
        ids = self.janus.query_once("findall(_P,paciente(_P,_,_,_),Pacientes)")["Pacientes"]
        self.assertEqual(ids, [f"p{i}" for i in range(1, 9)])
        self.assertEqual((ROOT / "src/facts.pl").read_bytes(), self.facts_before)


if __name__ == "__main__":
    unittest.main()
