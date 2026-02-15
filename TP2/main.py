# main.py - Point d'entree de l'application de feuilles de temps

from models import Employee, Projet, TimeEntry, EmployeManager, Activite
from services import TimesheetService
from reports import RapportService, FormateurRapport
from notifications import NotificationService, ApprobationWorkflow
from utils import aujourd_hui


def main():
    # Initialisation du service
    ts = TimesheetService()

    # Ajouter des employes
    ts.ajouter_employe(1, "Dupont", "Marie", "0612345678", "marie@example.com", "15/01/2023", "CDI", 35.0)
    ts.ajouter_employe(2, "Martin", "Pierre", "0698765432", "pierre@example.com", "01/06/2022", "CDD", 28.0)
    ts.ajouter_employe(3, "Durand", "Sophie", "0655443322", "sophie@example.com", "01/09/2023", "Stage", 15.0)

    # Ajouter des projets
    ts.ajouter_projet(1, "Site Web Corporate", "WEB01", 500)
    ts.ajouter_projet(2, "Application Mobile", "MOB01", 300)
    ts.ajouter_projet(3, "Migration Base de Donnees", "DB01", 200)

    # Saisir des entrees de temps
    ts.saisir_entree(1, 1, "01/03/2024", 8.0, "Developpement page accueil")
    ts.saisir_entree(1, 1, "02/03/2024", 7.5, "Tests unitaires page accueil")
    ts.saisir_entree(1, 2, "03/03/2024", 6.0, "Revue de code mobile")
    ts.saisir_entree(2, 2, "01/03/2024", 7.0, "Maquettes ecran principal")
    ts.saisir_entree(2, 2, "02/03/2024", 7.5, "Integration maquettes")
    ts.saisir_entree(3, 3, "01/03/2024", 5.0, "Analyse schema existant")
    ts.saisir_entree(3, 3, "02/03/2024", 6.0, "Script de migration")

    # Validation d'une entree
    erreurs = ts.valider_entree(3, 3, "03/03/2024", 7.0, "Trop d'heures pour un stage")
    if erreurs:
        print("Erreurs de validation:", erreurs)

    # Generer un rapport mensuel
    print("\n" + ts.generer_rapport_mensuel(1, 3, 2024))

    # Exporter en CSV
    print("\n--- Export CSV ---")
    print(ts.exporter_csv(1, 3, 2024))

    # Utilisation du service de rapports
    rapport_service = RapportService(ts)
    nom = rapport_service.timesheet_service._trouver_employe(1).nom
    print(f"\nRapport via RapportService pour: {nom}")
    print(f"Heures totales: {rapport_service.heures_employe(1, 3, 2024):.1f}h")
    print(f"Cout projet WEB01: {rapport_service.cout_projet(1, 3, 2024):.2f} EUR")

    # Workflow d'approbation
    ns = NotificationService()
    workflow = ApprobationWorkflow(ts, ns)
    print("\n--- Workflow d'approbation ---")
    workflow.soumettre(ts.entrees[0])
    workflow.approuver(ts.entrees[0], "Lefevre")
    workflow.rejeter(ts.entrees[5], "Lefevre", "Heures non conformes au contrat stage")

    # Formateur de rapport
    fmt = FormateurRapport()
    print("\n--- Lignes formatees ---")
    print(fmt.formater_ligne("Site Web Corporate", 21.5, 35.0))
    print(fmt.formater_total(21.5, 35.0))


if __name__ == "__main__":
    main()
