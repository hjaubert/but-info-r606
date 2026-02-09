# models.py - Classes metier de l'application de feuilles de temps


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

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def get_telephone(self):
        return self.telephone

    def set_telephone(self, telephone):
        self.telephone = telephone

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_date_embauche(self):
        return self.date_embauche

    def set_date_embauche(self, date_embauche):
        self.date_embauche = date_embauche

    def get_type_contrat(self):
        return self.type_contrat

    def set_type_contrat(self, type_contrat):
        self.type_contrat = type_contrat

    def get_taux_horaire(self):
        return self.taux_horaire

    def set_taux_horaire(self, taux_horaire):
        self.taux_horaire = taux_horaire


class TimeEntry:
    """Une entree de temps saisie par un employe"""

    def __init__(self, employee_id, project_id, date, heures, description, statut):
        self.employee_id = employee_id
        self.project_id = project_id
        self.date = date                # "15/03/2024"
        self.heures = heures            # 8.0
        self.description = description
        self.statut = statut            # "brouillon", "soumis", "approuve", "rejete"


class EmployeManager(Projet):
    """Un manager qui peut approuver les feuilles de temps.
    Herite de Projet car les deux ont un id et un nom..."""

    def __init__(self, id, nom, prenom, telephone, email, date_embauche, type_contrat, taux_horaire, equipe):
        super().__init__(id, nom, nom, 0)
        self.prenom = prenom
        self.telephone = telephone
        self.email = email
        self.date_embauche = date_embauche
        self.type_contrat = type_contrat
        self.taux_horaire = taux_horaire
        self.equipe = equipe

    def approuver_entree(self, entree):
        entree.statut = "approuve"

    def rejeter_entree(self, entree, raison):
        entree.statut = "rejete"


class Activite:
    """Enregistre une activite d'un employe sur un projet.
    Ecrit par un autre developpeur."""

    def __init__(self, id_employe, id_projet, jour, nb_heures, commentaire):
        self.id_employe = id_employe
        self.id_projet = id_projet
        self.jour = jour                # "15/03/2024"
        self.nb_heures = nb_heures      # 8.0
        self.commentaire = commentaire
