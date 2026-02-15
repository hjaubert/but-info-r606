# notifications.py - Service de notifications et workflow d'approbation

from models import StatutEntree

class NotificationService:
    """Service de notification des employes et managers"""

    def __init__(self):
        self.notifications_envoyees = []

    def notifier_soumission(self, employee_nom, manager_nom, projet_nom, heures, date_debut, date_fin):
        """Notifie la soumission d'une feuille de temps"""
        message = f"Soumission de {employee_nom} sur {projet_nom}: {heures:.1f}h ({date_debut} - {date_fin})"
        self.notifications_envoyees.append(message)
        print(message)
        if heures > 40:
            cout = heures * 35.0
            print(f"  ALERTE: Depassement heures pour {employee_nom} - Cout estime: {cout:.2f} EUR")

    def notifier_approbation(self, employee_nom, manager_nom, projet_nom, heures, date_debut, date_fin):
        """Notifie l'approbation d'une feuille de temps"""
        message = f"Approbation par {manager_nom} pour {employee_nom} sur {projet_nom}: {heures:.1f}h ({date_debut} - {date_fin})"
        self.notifications_envoyees.append(message)
        print(message)
        if heures > 40:
            cout = heures * 35.0
            print(f"  INFO: Heures supplementaires pour {employee_nom} - Cout: {cout:.2f} EUR")

    def notifier_rejet(self, employee_nom, manager_nom, projet_nom, heures, date_debut, date_fin, raison):
        """Notifie le rejet d'une feuille de temps"""
        message = f"Rejet par {manager_nom} pour {employee_nom} sur {projet_nom}: {heures:.1f}h - Raison: {raison}"
        self.notifications_envoyees.append(message)
        print(message)


class ApprobationWorkflow:
    """Gestion du workflow d'approbation des feuilles de temps"""

    def __init__(self, timesheet_service, notification_service):
        self.timesheet_service = timesheet_service
        self.notification_service = notification_service

    def soumettre(self, entree):
        """Soumet une entree de temps pour approbation"""
        entree.statut = StatutEntree.SOUMIS
        emp_nom = self.timesheet_service._trouver_employe(entree.employee_id).nom
        projet_nom = self.timesheet_service._trouver_projet(entree.project_id).nom
        self.notification_service.notifier_soumission(
            emp_nom, "Manager", projet_nom, entree.heures, entree.date, entree.date
        )

    def approuver(self, entree, manager_nom):
        """Approuve une entree de temps"""
        entree.statut = StatutEntree.APPROUVE
        emp_nom = self.timesheet_service._trouver_employe(entree.employee_id).nom
        projet_nom = self.timesheet_service._trouver_projet(entree.project_id).nom
        self.notification_service.notifier_approbation(
            emp_nom, manager_nom, projet_nom, entree.heures, entree.date, entree.date
        )

    def rejeter(self, entree, manager_nom, raison):
        """Rejette une entree de temps"""
        entree.statut = StatutEntree.REJETE
        emp_nom = self.timesheet_service._trouver_employe(entree.employee_id).nom
        projet_nom = self.timesheet_service._trouver_projet(entree.project_id).nom
        self.notification_service.notifier_rejet(
            emp_nom, manager_nom, projet_nom, entree.heures, entree.date, entree.date, raison
        )
