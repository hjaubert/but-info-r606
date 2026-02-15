# models.py - Classes metier de l'application de feuilles de temps

from enum import Enum


class TypeContrat(Enum):
    CDI = "CDI"
    CDD = "CDD"
    STAGE = "Stage"
    ALTERNANCE = "Alternance"
    FREELANCE = "Freelance"


class StatutEntree(Enum):
    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    APPROUVE = "approuve"
    REJETE = "rejete"

class Projet:
    """Un projet sur lequel les employes peuvent saisir du temps"""

    def __init__(self, id, nom, code, budget_heures):
        self.id = id
        self.nom = nom
        self.code = code
        self.budget_heures = budget_heures


class Employee:
    """Stocke les informations d'un employe"""

    def __init__(self, id, nom, prenom, telephone, email, date_embauche, type_contrat, taux_horaire):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone          # "0612345678"
        self.email = email
        self.date_embauche = date_embauche  # "2023-01-15"
        self.type_contrat = type_contrat    # "CDI", "CDD", "Stage", "Alternance"
        self.taux_horaire = taux_horaire    # 35.0


class TimeEntry:
    """Une entree de temps saisie par un employe"""

    def __init__(self, employee_id, project_id, date, heures, description, statut):
        self.employee_id = employee_id
        self.project_id = project_id
        self.date = date                # "15/03/2024"
        self.heures = heures            # 8.0
        self.description = description
        self.statut = statut            # "brouillon", "soumis", "approuve", "rejete"


class EmployeManager(Employee):
    """Un manager qui peut approuver les feuilles de temps."""

    def __init__(self, id, nom, prenom, telephone, email, date_embauche, type_contrat, taux_horaire, equipe):
        super().__init__(id, nom, prenom, telephone, email, date_embauche, type_contrat, taux_horaire)
        self.equipe = equipe

    def approuver_entree(self, entree):
        entree.statut = StatutEntree.APPROUVE

    def rejeter_entree(self, entree, raison):
        entree.statut = StatutEntree.REJETE
