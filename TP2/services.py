# services.py - Service principal de gestion des feuilles de temps

from models import Employee, TimeEntry, Projet, TypeContrat, StatutEntree


class TimesheetService:
    """Service de gestion des feuilles de temps.
    Gere les employes, projets, entrees de temps, rapports, export CSV,
    validation et notifications."""

    def __init__(self):
        self.employees = []
        self.projets = []
        self.entrees = []
        self.notifications = []
        self.log = []
        self.config_separateur_csv = ";"
        self.config_devise = "EUR"
        self.validation_service = ValidationService()

    def ajouter_employe(self, employe):
        """Ajoute un employe au systeme"""
        self.employees.append(employe)
        self.log.append(f"Employe ajoute: {employe.nom} {employe.prenom}")
        return employe

    def ajouter_projet(self, id, nom, code, budget_heures):
        """Ajoute un projet au systeme"""
        projet = Projet(id, nom, code, budget_heures)
        self.projets.append(projet)
        self.log.append(f"Projet ajoute: {nom}")
        return projet

    def saisir_entree(self, employee_id, project_id, date, heures, description):
        """Saisit une entree de temps"""
        entree = TimeEntry(employee_id, project_id, date, heures, description, StatutEntree.BROUILLON)
        self.entrees.append(entree)
        return entree

    def generer_rapport_mensuel(self, employee_id, mois, annee):
        """Genere un rapport mensuel pour un employe"""
        employe = self._trouver_employe(employee_id)
        if employe is None:
            return "Employe non trouve"

        entrees_mois = self._filtrer_entrees_mois(employee_id, mois, annee)
        heures_par_projet = self._calculer_heures_par_projet(entrees_mois)
        total_heures = sum(heures_par_projet.values())
        cout_total = total_heures * employe.taux_horaire

        rapport = self.construire_rapport(employe, mois, annee)

        for projet_id, heures in heures_par_projet.items():
            projet = self._trouver_projet(projet_id)
            projet_nom = projet.nom if projet else "Inconnu"
            cout = heures * employe.taux_horaire
            rapport += f"  {projet_nom}: {heures:.1f}h - {cout:.2f} EUR\n"

        rapport += "-" * 40 + "\n"
        rapport += f"Total: {total_heures:.1f}h - {cout_total:.2f} EUR\n"
        rapport += self._verifier_depassement(employe, total_heures)

        return rapport

    def construire_rapport(self, employe, mois, annee):
        """Construit un rapport mensuel pour un employe"""
        rapport = f"=== Rapport mensuel {mois:02d}/{annee} ===\n"
        rapport += f"Employe: {employe.nom} {employe.prenom}\n"
        rapport += f"Contrat: {employe.type_contrat.value}\n"
        rapport += f"Taux horaire: {employe.taux_horaire:.2f} EUR\n"
        rapport += "-" * 40 + "\n"
        return rapport

    def _filtrer_entrees_mois(self, employee_id, mois, annee):
        """Filtre les entrees de temps pour un employe sur un mois donne"""
        entrees_mois = []
        for entree in self.entrees:
            parties = entree.date.split("/")
            entry_mois = int(parties[1])
            entry_annee = int(parties[2])
            if entree.employee_id == employee_id and entry_mois == mois and entry_annee == annee:
                entrees_mois.append(entree)
        return entrees_mois

    def _calculer_heures_par_projet(self, entrees):
        """Calcule les heures regroupees par projet"""
        heures_par_projet = {}
        for entree in entrees:
            if entree.project_id not in heures_par_projet:
                heures_par_projet[entree.project_id] = 0
            heures_par_projet[entree.project_id] += entree.heures
        return heures_par_projet

    def _verifier_depassement(self, employe, total_heures):
        """Verifie si les heures depassent le forfait mensuel"""
        seuils = {
            TypeContrat.CDI: 151.67,
            TypeContrat.CDD: 140,
            TypeContrat.STAGE: 120,
        }
        seuil = seuils.get(employe.type_contrat)
        if seuil and total_heures > seuil:
            return "ATTENTION: Depassement du forfait mensuel!\n"
        return ""

    def calculer_heures_employe(self, employee_id, mois, annee):
        """Calcule le total des heures pour un employe sur un mois"""
        entrees = self._filtrer_entrees_mois(employee_id, mois, annee)
        return sum(e.heures for e in entrees)

    def calculer_cout_projet(self, project_id, mois, annee):
        """Calcule le cout d'un projet sur un mois"""
        total_cout = 0
        entrees = self._filtrer_entrees_par_projet(project_id, mois, annee)
        for entree in entrees:
            emp = self._trouver_employe(entree.employee_id)
            if emp:
                total_cout += entree.heures * emp.taux_horaire
        return total_cout

    def _filtrer_entrees_par_projet(self, project_id, mois, annee):
        """Filtre les entrees de temps pour un projet sur un mois donne"""
        entrees_mois = []    
        for entree in self.entrees:
            parties = entree.date.split("/")
            entry_mois = int(parties[1])
            entry_annee = int(parties[2])
            if entree.project_id == project_id and entry_mois == mois and entry_annee == annee:
                entrees_mois.append(entree)
        return entrees_mois

    def valider_entree(self, employee_id, project_id, date, heures, description):
        """Valide une entree de temps avant saisie (delegue a ValidationService)"""
        return self.validation_service.valider_entree(
            self._trouver_employe(employee_id),
            self._trouver_projet(project_id),
            date, heures
        )

    def formater_date(self, date_str):
        """Formate une date (delegue a ValidationService)"""
        return self.validation_service.formater_date(date_str)

    def exporter_csv(self, employee_id, mois, annee):
        """Exporte les entrees de temps au format CSV"""
        sep = self.config_separateur_csv
        lignes = [f"Date{sep}Projet{sep}Heures{sep}Description{sep}Cout (EUR)"]

        entrees = self._filtrer_entrees_mois(employee_id, mois, annee)
        for entree in entrees:
            projet = self._trouver_projet(entree.project_id)
            projet_nom = projet.nom if projet else "Inconnu"
            emp = self._trouver_employe(employee_id)
            cout = entree.heures * emp.taux_horaire
            date_formatee = self.formater_date(entree.date)
            lignes.append(f"{date_formatee}{sep}{projet_nom}{sep}{entree.heures}{sep}{entree.description}{sep}{cout:.2f} EUR")

        return "\n".join(lignes)

    def envoyer_notification(self, employee_id, message):
        """Envoie une notification a un employe"""
        emp = self._trouver_employe(employee_id)
        if emp:
            notification = f"[{emp.nom}] {message}"
            self.notifications.append(notification)
            print(notification)

    def calculer_statistiques(self, mois, annee):
        """Calcule des statistiques globales"""
        total_heures = 0
        nb_entrees = 0
        for entree in self.entrees:
            parties = entree.date.split("/")
            entry_mois = int(parties[1])
            entry_annee = int(parties[2])
            if entry_mois == mois and entry_annee == annee:
                total_heures += entree.heures
                nb_entrees += 1
        moyenne = total_heures / nb_entrees if nb_entrees > 0 else 0
        return {
            "total_heures": total_heures,
            "nb_entrees": nb_entrees,
            "moyenne_heures": moyenne
        }

    def _trouver_employe(self, employee_id):
        for emp in self.employees:
            if emp.id == employee_id:
                return emp
        return None

    def _trouver_projet(self, project_id):
        for p in self.projets:
            if p.id == project_id:
                return p
        return None

class ValidationService:
    """Service de validation des entrees de temps et formatage de dates"""

    def __init__(self, config_format_date="FR"):
        self.config_format_date = config_format_date

    def valider_entree(self, emp, projet, date, heures):
        """Valide une entree de temps avant saisie"""
        erreurs = []

        if emp is None:
            erreurs.append("Employe inexistant")
            return erreurs

        if projet is None:
            erreurs.append("Projet inexistant")
            return erreurs

        max_heures = self.verifier_heures_max(emp)

        if heures > max_heures:
            erreurs.append(f"Depassement: {heures}h > {max_heures}h max pour {emp.type_contrat.value}")

        if heures <= 0:
            erreurs.append("Les heures doivent etre positives")

        erreurs = self.valider_date(date, erreurs)

        return erreurs

    def formater_date(self, date_str):
        """Formate une date selon la configuration"""
        if self.config_format_date == "FR":
            parties = date_str.split("/")
            if len(parties) == 3:
                return f"{parties[0]}/{parties[1]}/{parties[2]}"
        elif self.config_format_date == "US":
            parties = date_str.split("/")
            if len(parties) == 3:
                return f"{parties[1]}/{parties[0]}/{parties[2]}"
        elif self.config_format_date == "ISO":
            parties = date_str.split("/")
            if len(parties) == 3:
                return f"{parties[2]}-{parties[1]}-{parties[0]}"
        return date_str

    def valider_date(self, date, erreurs):
        if self.config_format_date == "FR":
            parties = date.split("/")
            if len(parties) != 3:
                erreurs.append("Format de date invalide (attendu: JJ/MM/AAAA)")
        elif self.config_format_date == "US":
            parties = date.split("/")
            if len(parties) != 3:
                erreurs.append("Format de date invalide (attendu: MM/DD/YYYY)")
        elif self.config_format_date == "ISO":
            parties = date.split("-")
            if len(parties) != 3:
                erreurs.append("Format de date invalide (attendu: AAAA-MM-JJ)")
        
        return erreurs

    def verifier_heures_max(self, emp):
        max_heures_par_contrat = {
            TypeContrat.CDI: 8.0,
            TypeContrat.CDD: 7.5,
            TypeContrat.STAGE: 6.0,
            TypeContrat.ALTERNANCE: 7.0,
            TypeContrat.FREELANCE: 10.0,
        }
        max_heures = max_heures_par_contrat.get(emp.type_contrat, 8.0)
        return max_heures