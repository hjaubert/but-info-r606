# test_timesheet.py - Tests unitaires pour l'application de feuilles de temps

import unittest
from datetime import date

from models import Employee, Projet, TimeEntry, EmployeManager, Activite
from services import TimesheetService
from notifications import NotificationService, ApprobationWorkflow
from reports import RapportService, FormateurRapport, StatistiquesCalculateur
from utils import DateHelper, valider_email, formater_telephone, calculer_jours_ouvres


class TestModels(unittest.TestCase):
    """Tests pour les classes du modele"""

    def test_employee_creation(self):
        emp = Employee(1, "Dupont", "Marie", "0612345678", "marie@example.com",
                       "15/01/2023", "CDI", 35.0)
        self.assertEqual(emp.id, 1)
        self.assertEqual(emp.nom, "Dupont")
        self.assertEqual(emp.prenom, "Marie")
        self.assertEqual(emp.telephone, "0612345678")
        self.assertEqual(emp.email, "marie@example.com")
        self.assertEqual(emp.date_embauche, "15/01/2023")
        self.assertEqual(emp.type_contrat, "CDI")
        self.assertEqual(emp.taux_horaire, 35.0)

    def test_employee_getters(self):
        emp = Employee(1, "Dupont", "Marie", "0612345678", "marie@example.com",
                       "15/01/2023", "CDI", 35.0)
        self.assertEqual(emp.get_nom(), "Dupont")
        self.assertEqual(emp.get_prenom(), "Marie")
        self.assertEqual(emp.get_telephone(), "0612345678")
        self.assertEqual(emp.get_email(), "marie@example.com")
        self.assertEqual(emp.get_date_embauche(), "15/01/2023")
        self.assertEqual(emp.get_type_contrat(), "CDI")
        self.assertEqual(emp.get_taux_horaire(), 35.0)

    def test_employee_setters(self):
        emp = Employee(1, "Dupont", "Marie", "0612345678", "marie@example.com",
                       "15/01/2023", "CDI", 35.0)
        emp.set_nom("Martin")
        self.assertEqual(emp.get_nom(), "Martin")
        emp.set_prenom("Pierre")
        self.assertEqual(emp.get_prenom(), "Pierre")
        emp.set_telephone("0699887766")
        self.assertEqual(emp.get_telephone(), "0699887766")
        emp.set_email("pierre@example.com")
        self.assertEqual(emp.get_email(), "pierre@example.com")
        emp.set_date_embauche("01/06/2024")
        self.assertEqual(emp.get_date_embauche(), "01/06/2024")
        emp.set_type_contrat("CDD")
        self.assertEqual(emp.get_type_contrat(), "CDD")
        emp.set_taux_horaire(40.0)
        self.assertEqual(emp.get_taux_horaire(), 40.0)

    def test_projet_creation(self):
        projet = Projet(1, "Site Web", "WEB01", 500)
        self.assertEqual(projet.id, 1)
        self.assertEqual(projet.nom, "Site Web")
        self.assertEqual(projet.code, "WEB01")
        self.assertEqual(projet.budget_heures, 500)

    def test_time_entry_creation(self):
        entry = TimeEntry(1, 2, "15/03/2024", 8.0, "Dev page accueil", "brouillon")
        self.assertEqual(entry.employee_id, 1)
        self.assertEqual(entry.project_id, 2)
        self.assertEqual(entry.date, "15/03/2024")
        self.assertEqual(entry.heures, 8.0)
        self.assertEqual(entry.description, "Dev page accueil")
        self.assertEqual(entry.statut, "brouillon")

    def test_employe_manager_creation(self):
        mgr = EmployeManager(10, "Lefevre", "Jean", "0611223344", "jean@example.com",
                             "01/01/2020", "CDI", 50.0, "Equipe Dev")
        self.assertEqual(mgr.id, 10)
        self.assertEqual(mgr.prenom, "Jean")
        self.assertEqual(mgr.equipe, "Equipe Dev")
        self.assertEqual(mgr.taux_horaire, 50.0)
        # Herite de Projet
        self.assertIsInstance(mgr, Projet)

    def test_employe_manager_approuver(self):
        mgr = EmployeManager(10, "Lefevre", "Jean", "0611223344", "jean@example.com",
                             "01/01/2020", "CDI", 50.0, "Equipe Dev")
        entry = TimeEntry(1, 1, "15/03/2024", 8.0, "Dev", "brouillon")
        mgr.approuver_entree(entry)
        self.assertEqual(entry.statut, "approuve")

    def test_employe_manager_rejeter(self):
        mgr = EmployeManager(10, "Lefevre", "Jean", "0611223344", "jean@example.com",
                             "01/01/2020", "CDI", 50.0, "Equipe Dev")
        entry = TimeEntry(1, 1, "15/03/2024", 8.0, "Dev", "brouillon")
        mgr.rejeter_entree(entry, "Heures incorrectes")
        self.assertEqual(entry.statut, "rejete")

    def test_activite_creation(self):
        act = Activite(1, 2, "15/03/2024", 7.5, "Reunion projet")
        self.assertEqual(act.id_employe, 1)
        self.assertEqual(act.id_projet, 2)
        self.assertEqual(act.jour, "15/03/2024")
        self.assertEqual(act.nb_heures, 7.5)
        self.assertEqual(act.commentaire, "Reunion projet")


class TestTimesheetService(unittest.TestCase):
    """Tests pour le service principal"""

    def setUp(self):
        self.ts = TimesheetService()
        self.ts.ajouter_employe(1, "Dupont", "Marie", "0612345678",
                                "marie@example.com", "15/01/2023", "CDI", 35.0)
        self.ts.ajouter_employe(2, "Martin", "Pierre", "0698765432",
                                "pierre@example.com", "01/06/2022", "CDD", 28.0)
        self.ts.ajouter_employe(3, "Durand", "Sophie", "0655443322",
                                "sophie@example.com", "01/09/2023", "Stage", 15.0)
        self.ts.ajouter_projet(1, "Site Web Corporate", "WEB01", 500)
        self.ts.ajouter_projet(2, "Application Mobile", "MOB01", 300)

    def test_ajouter_employe(self):
        ts = TimesheetService()
        emp = ts.ajouter_employe(99, "Test", "User", "0600000000",
                                 "test@example.com", "01/01/2024", "CDI", 30.0)
        self.assertEqual(len(ts.employees), 1)
        self.assertEqual(emp.id, 99)
        self.assertEqual(emp.get_nom(), "Test")
        self.assertIn("Employe ajoute: Test User", ts.log)

    def test_ajouter_projet(self):
        ts = TimesheetService()
        projet = ts.ajouter_projet(99, "Test Projet", "TST01", 100)
        self.assertEqual(len(ts.projets), 1)
        self.assertEqual(projet.id, 99)
        self.assertEqual(projet.nom, "Test Projet")
        self.assertIn("Projet ajoute: Test Projet", ts.log)

    def test_saisir_entree(self):
        entree = self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev page accueil")
        self.assertEqual(entree.employee_id, 1)
        self.assertEqual(entree.project_id, 1)
        self.assertEqual(entree.heures, 8.0)
        self.assertEqual(entree.statut, "brouillon")
        self.assertEqual(len(self.ts.entrees), 1)

    def test_calculer_heures_employe(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.ts.saisir_entree(1, 1, "02/03/2024", 7.5, "Tests")
        self.ts.saisir_entree(1, 2, "03/03/2024", 6.0, "Revue")
        total = self.ts.calculer_heures_employe(1, 3, 2024)
        self.assertEqual(total, 21.5)

    def test_calculer_heures_employe_autre_mois(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.ts.saisir_entree(1, 1, "01/04/2024", 5.0, "Dev avril")
        total_mars = self.ts.calculer_heures_employe(1, 3, 2024)
        total_avril = self.ts.calculer_heures_employe(1, 4, 2024)
        self.assertEqual(total_mars, 8.0)
        self.assertEqual(total_avril, 5.0)

    def test_calculer_heures_employe_aucune_entree(self):
        total = self.ts.calculer_heures_employe(1, 3, 2024)
        self.assertEqual(total, 0)

    def test_calculer_cout_projet(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.ts.saisir_entree(2, 1, "01/03/2024", 7.0, "Maquettes")
        cout = self.ts.calculer_cout_projet(1, 3, 2024)
        # 8.0 * 35.0 + 7.0 * 28.0 = 280 + 196 = 476
        self.assertEqual(cout, 476.0)

    def test_generer_rapport_mensuel(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev page accueil")
        self.ts.saisir_entree(1, 2, "02/03/2024", 6.0, "Revue mobile")
        rapport = self.ts.generer_rapport_mensuel(1, 3, 2024)
        self.assertIn("Dupont", rapport)
        self.assertIn("Marie", rapport)
        self.assertIn("Site Web Corporate", rapport)
        self.assertIn("Application Mobile", rapport)
        self.assertIn("14.0h", rapport)
        self.assertIn("CDI", rapport)
        self.assertIn("35.00 EUR", rapport)

    def test_generer_rapport_employe_inconnu(self):
        rapport = self.ts.generer_rapport_mensuel(999, 3, 2024)
        self.assertEqual(rapport, "Employe non trouve")

    def test_valider_entree_ok(self):
        erreurs = self.ts.valider_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.assertEqual(erreurs, [])

    def test_valider_entree_depassement_cdi(self):
        erreurs = self.ts.valider_entree(1, 1, "01/03/2024", 9.0, "Trop")
        self.assertEqual(len(erreurs), 1)
        self.assertIn("8.0h max", erreurs[0])

    def test_valider_entree_depassement_stage(self):
        erreurs = self.ts.valider_entree(3, 1, "01/03/2024", 7.0, "Trop")
        self.assertEqual(len(erreurs), 1)
        self.assertIn("6.0h max", erreurs[0])

    def test_valider_entree_employe_inexistant(self):
        erreurs = self.ts.valider_entree(999, 1, "01/03/2024", 5.0, "Dev")
        self.assertIn("Employe inexistant", erreurs)

    def test_valider_entree_projet_inexistant(self):
        erreurs = self.ts.valider_entree(1, 999, "01/03/2024", 5.0, "Dev")
        self.assertIn("Projet inexistant", erreurs)

    def test_valider_entree_heures_negatives(self):
        erreurs = self.ts.valider_entree(1, 1, "01/03/2024", -1.0, "Invalide")
        self.assertIn("Les heures doivent etre positives", erreurs)

    def test_valider_entree_format_date_invalide(self):
        erreurs = self.ts.valider_entree(1, 1, "2024-03-01", 5.0, "Mauvais format")
        self.assertTrue(any("Format de date invalide" in e for e in erreurs))

    def test_formater_date_fr(self):
        self.ts.config_format_date = "FR"
        self.assertEqual(self.ts.formater_date("15/03/2024"), "15/03/2024")

    def test_formater_date_us(self):
        self.ts.config_format_date = "US"
        self.assertEqual(self.ts.formater_date("15/03/2024"), "03/15/2024")

    def test_formater_date_iso(self):
        self.ts.config_format_date = "ISO"
        self.assertEqual(self.ts.formater_date("15/03/2024"), "2024-03-15")

    def test_exporter_csv(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev page accueil")
        self.ts.saisir_entree(1, 2, "02/03/2024", 6.0, "Revue mobile")
        csv = self.ts.exporter_csv(1, 3, 2024)
        lignes = csv.split("\n")
        self.assertEqual(len(lignes), 3)  # header + 2 data lines
        self.assertIn("Date;Projet;Heures;Description;Cout (EUR)", lignes[0])
        self.assertIn("Site Web Corporate", lignes[1])
        self.assertIn("Application Mobile", lignes[2])
        self.assertIn("EUR", lignes[1])

    def test_envoyer_notification(self):
        self.ts.envoyer_notification(1, "Test message")
        self.assertEqual(len(self.ts.notifications), 1)
        self.assertIn("Dupont", self.ts.notifications[0])
        self.assertIn("Test message", self.ts.notifications[0])

    def test_envoyer_notification_employe_inexistant(self):
        self.ts.envoyer_notification(999, "Rien")
        self.assertEqual(len(self.ts.notifications), 0)

    def test_calculer_statistiques(self):
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.ts.saisir_entree(2, 2, "02/03/2024", 6.0, "Maquettes")
        stats = self.ts.calculer_statistiques(3, 2024)
        self.assertEqual(stats["total_heures"], 14.0)
        self.assertEqual(stats["nb_entrees"], 2)
        self.assertEqual(stats["moyenne_heures"], 7.0)

    def test_calculer_statistiques_vide(self):
        stats = self.ts.calculer_statistiques(3, 2024)
        self.assertEqual(stats["total_heures"], 0)
        self.assertEqual(stats["nb_entrees"], 0)
        self.assertEqual(stats["moyenne_heures"], 0)

    def test_trouver_employe(self):
        emp = self.ts._trouver_employe(1)
        self.assertIsNotNone(emp)
        self.assertEqual(emp.get_nom(), "Dupont")

    def test_trouver_employe_inexistant(self):
        emp = self.ts._trouver_employe(999)
        self.assertIsNone(emp)

    def test_trouver_projet(self):
        projet = self.ts._trouver_projet(1)
        self.assertIsNotNone(projet)
        self.assertEqual(projet.nom, "Site Web Corporate")

    def test_trouver_projet_inexistant(self):
        projet = self.ts._trouver_projet(999)
        self.assertIsNone(projet)


class TestNotificationService(unittest.TestCase):
    """Tests pour le service de notifications"""

    def setUp(self):
        self.ns = NotificationService()

    def test_notifier_soumission(self):
        self.ns.notifier_soumission("Dupont", "Manager", "Site Web", 8.0,
                                    "01/03/2024", "01/03/2024")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Soumission", self.ns.notifications_envoyees[0])
        self.assertIn("Dupont", self.ns.notifications_envoyees[0])

    def test_notifier_approbation(self):
        self.ns.notifier_approbation("Dupont", "Lefevre", "Site Web", 8.0,
                                     "01/03/2024", "01/03/2024")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Approbation", self.ns.notifications_envoyees[0])
        self.assertIn("Lefevre", self.ns.notifications_envoyees[0])

    def test_notifier_rejet(self):
        self.ns.notifier_rejet("Dupont", "Lefevre", "Site Web", 8.0,
                               "01/03/2024", "01/03/2024", "Heures incorrectes")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Rejet", self.ns.notifications_envoyees[0])
        self.assertIn("Heures incorrectes", self.ns.notifications_envoyees[0])


class TestApprobationWorkflow(unittest.TestCase):
    """Tests pour le workflow d'approbation"""

    def setUp(self):
        self.ts = TimesheetService()
        self.ts.ajouter_employe(1, "Dupont", "Marie", "0612345678",
                                "marie@example.com", "15/01/2023", "CDI", 35.0)
        self.ts.ajouter_projet(1, "Site Web Corporate", "WEB01", 500)
        self.ns = NotificationService()
        self.workflow = ApprobationWorkflow(self.ts, self.ns)

    def test_soumettre(self):
        entree = self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.workflow.soumettre(entree)
        self.assertEqual(entree.statut, "soumis")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Soumission", self.ns.notifications_envoyees[0])

    def test_approuver(self):
        entree = self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.workflow.approuver(entree, "Lefevre")
        self.assertEqual(entree.statut, "approuve")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Approbation", self.ns.notifications_envoyees[0])

    def test_rejeter(self):
        entree = self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.workflow.rejeter(entree, "Lefevre", "Heures non conformes")
        self.assertEqual(entree.statut, "rejete")
        self.assertEqual(len(self.ns.notifications_envoyees), 1)
        self.assertIn("Rejet", self.ns.notifications_envoyees[0])


class TestRapports(unittest.TestCase):
    """Tests pour les services de rapports"""

    def setUp(self):
        self.ts = TimesheetService()
        self.ts.ajouter_employe(1, "Dupont", "Marie", "0612345678",
                                "marie@example.com", "15/01/2023", "CDI", 35.0)
        self.ts.ajouter_projet(1, "Site Web Corporate", "WEB01", 500)
        self.ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Dev")
        self.ts.saisir_entree(1, 1, "02/03/2024", 7.5, "Tests")

    def test_rapport_service_rapport_mensuel(self):
        rs = RapportService(self.ts)
        rapport = rs.rapport_mensuel(1, 3, 2024)
        self.assertIn("Dupont", rapport)
        self.assertIn("15.5h", rapport)

    def test_rapport_service_heures_employe(self):
        rs = RapportService(self.ts)
        heures = rs.heures_employe(1, 3, 2024)
        self.assertEqual(heures, 15.5)

    def test_rapport_service_cout_projet(self):
        rs = RapportService(self.ts)
        cout = rs.cout_projet(1, 3, 2024)
        # 15.5 * 35.0 = 542.5
        self.assertEqual(cout, 542.5)

    def test_rapport_service_export_csv(self):
        rs = RapportService(self.ts)
        csv = rs.export_csv(1, 3, 2024)
        self.assertIn("Site Web Corporate", csv)

    def test_rapport_service_statistiques(self):
        rs = RapportService(self.ts)
        stats = rs.statistiques(3, 2024)
        self.assertEqual(stats["total_heures"], 15.5)
        self.assertEqual(stats["nb_entrees"], 2)

    def test_formateur_ligne(self):
        fmt = FormateurRapport()
        ligne = fmt.formater_ligne("Site Web", 21.5, 35.0)
        self.assertEqual(ligne, "Site Web: 21.5h - 752.50 EUR")

    def test_formateur_total(self):
        fmt = FormateurRapport()
        total = fmt.formater_total(21.5, 35.0)
        self.assertEqual(total, "TOTAL: 21.5h - 752.50 EUR")

    def test_statistiques_calculateur_moyenne(self):
        calc = StatistiquesCalculateur()
        self.assertEqual(calc.calculer_moyenne([8.0, 6.0, 7.0]), 7.0)

    def test_statistiques_calculateur_moyenne_vide(self):
        calc = StatistiquesCalculateur()
        self.assertEqual(calc.calculer_moyenne([]), 0)

    def test_statistiques_calculateur_total(self):
        calc = StatistiquesCalculateur()
        self.assertEqual(calc.calculer_total([8.0, 6.0, 7.0]), 21.0)

    def test_statistiques_calculateur_max(self):
        calc = StatistiquesCalculateur()
        self.assertEqual(calc.calculer_max([8.0, 6.0, 7.0]), 8.0)

    def test_statistiques_calculateur_max_vide(self):
        calc = StatistiquesCalculateur()
        self.assertEqual(calc.calculer_max([]), 0)


class TestUtils(unittest.TestCase):
    """Tests pour les utilitaires"""

    def test_date_helper_aujourd_hui(self):
        dh = DateHelper()
        resultat = dh.aujourd_hui()
        today = date.today().strftime("%d/%m/%Y")
        self.assertEqual(resultat, today)

    def test_valider_email_valide(self):
        self.assertTrue(valider_email("user@example.com"))

    def test_valider_email_sans_arobase(self):
        self.assertFalse(valider_email("userexample.com"))

    def test_valider_email_sans_point(self):
        self.assertFalse(valider_email("user@examplecom"))

    def test_formater_telephone(self):
        self.assertEqual(formater_telephone("0612345678"), "06 12 34 56 78")

    def test_calculer_jours_ouvres(self):
        # 01/01/2024 (lundi) au 05/01/2024 (vendredi) = 5 jours ouvres
        jours = calculer_jours_ouvres("01/01/2024", "05/01/2024")
        self.assertEqual(jours, 5)

    def test_calculer_jours_ouvres_avec_weekend(self):
        # 01/01/2024 (lundi) au 07/01/2024 (dimanche) = 5 jours ouvres
        jours = calculer_jours_ouvres("01/01/2024", "07/01/2024")
        self.assertEqual(jours, 5)


if __name__ == "__main__":
    unittest.main()
