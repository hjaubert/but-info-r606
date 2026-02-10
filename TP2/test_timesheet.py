# test_timesheet.py - Tests fonctionnels pour l'application de feuilles de temps
# Ces tests lancent main.py et verifient la sortie produite.

import unittest
import subprocess
import sys
import os


def run_main():
    """Lance main.py et retourne (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    return result.returncode, result.stdout, result.stderr


class TestTimesheet(unittest.TestCase):
    """Tests fonctionnels basees sur la sortie de main.py"""

    @classmethod
    def setUpClass(cls):
        cls.exit_code, cls.output, cls.stderr = run_main()

    # --- Execution sans erreur ---

    def test_exit_code_zero(self):
        self.assertEqual(self.exit_code, 0, f"main.py a echoue:\n{self.stderr}")

    # --- Validation des entrees ---

    def test_validation_depassement_stage(self):
        self.assertIn("Depassement", self.output)
        self.assertIn("6.0h max", self.output)
        self.assertIn("Stage", self.output)

    # --- Rapport mensuel ---

    def test_rapport_titre(self):
        self.assertIn("Rapport mensuel 03/2024", self.output)

    def test_rapport_employe(self):
        self.assertIn("Dupont Marie", self.output)

    def test_rapport_contrat(self):
        self.assertIn("CDI", self.output)

    def test_rapport_taux_horaire(self):
        self.assertIn("35.00 EUR", self.output)

    def test_rapport_projet_web(self):
        self.assertIn("Site Web Corporate", self.output)
        self.assertIn("15.5h", self.output)
        self.assertIn("542.50 EUR", self.output)

    def test_rapport_projet_mobile(self):
        self.assertIn("Application Mobile", self.output)
        self.assertIn("6.0h", self.output)
        self.assertIn("210.00 EUR", self.output)

    def test_rapport_total(self):
        self.assertIn("21.5h", self.output)
        self.assertIn("752.50 EUR", self.output)

    # --- Export CSV ---

    def test_csv_header(self):
        self.assertIn("Date;Projet;Heures;Description;Cout (EUR)", self.output)

    def test_csv_entree_1(self):
        self.assertIn("01/03/2024;Site Web Corporate;8.0;Developpement page accueil;280.00 EUR", self.output)

    def test_csv_entree_2(self):
        self.assertIn("02/03/2024;Site Web Corporate;7.5;Tests unitaires page accueil;262.50 EUR", self.output)

    def test_csv_entree_3(self):
        self.assertIn("03/03/2024;Application Mobile;6.0;Revue de code mobile;210.00 EUR", self.output)

    # --- RapportService ---

    def test_rapport_service_employe(self):
        self.assertIn("Rapport via RapportService pour: Dupont", self.output)

    def test_rapport_service_heures(self):
        self.assertIn("Heures totales: 21.5h", self.output)

    def test_rapport_service_cout(self):
        self.assertIn("Cout projet WEB01: 542.50 EUR", self.output)

    # --- Workflow d'approbation ---

    def test_workflow_soumission(self):
        self.assertIn("Soumission de Dupont sur Site Web Corporate: 8.0h", self.output)

    def test_workflow_approbation(self):
        self.assertIn("Approbation par Lefevre pour Dupont sur Site Web Corporate: 8.0h", self.output)

    def test_workflow_rejet(self):
        self.assertIn("Rejet par Lefevre pour Durand sur Migration Base de Donnees: 5.0h", self.output)
        self.assertIn("Heures non conformes au contrat stage", self.output)

    # --- Lignes formatees ---

    def test_formateur_ligne(self):
        self.assertIn("Site Web Corporate: 21.5h - 752.50 EUR", self.output)

    def test_formateur_total(self):
        self.assertIn("TOTAL: 21.5h - 752.50 EUR", self.output)


if __name__ == "__main__":
    unittest.main()
