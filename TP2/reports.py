# reports.py - Generation de rapports et statistiques


class RapportService:
    """Service de rapports - interface pour la generation de rapports"""

    def __init__(self, timesheet_service):
        self.timesheet_service = timesheet_service

    def rapport_mensuel(self, employee_id, mois, annee):
        return self.timesheet_service.generer_rapport_mensuel(employee_id, mois, annee)

    def heures_employe(self, employee_id, mois, annee):
        return self.timesheet_service.calculer_heures_employe(employee_id, mois, annee)

    def cout_projet(self, project_id, mois, annee):
        return self.timesheet_service.calculer_cout_projet(project_id, mois, annee)

    def export_csv(self, employee_id, mois, annee):
        return self.timesheet_service.exporter_csv(employee_id, mois, annee)

    def statistiques(self, mois, annee):
        return self.timesheet_service.calculer_statistiques(mois, annee)

    def nom_employe(self, employee_id):
        """Retourne le nom d'un employe par son id"""
        emp = self.timesheet_service._trouver_employe(employee_id)
        return emp.nom if emp else None


class FormateurRapport:
    """Formateur de lignes de rapport"""

    def formater_ligne(self, projet_nom, heures, taux):
        """Formate une ligne de rapport avec le cout"""
        return f"{projet_nom}: {heures:.1f}h - {heures * taux:.2f} EUR"

    def formater_total(self, total_heures, taux):
        """Formate la ligne de total"""
        return f"TOTAL: {total_heures:.1f}h - {total_heures * taux:.2f} EUR"
