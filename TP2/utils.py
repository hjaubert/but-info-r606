# utils.py - Utilitaires divers

VERSION = "0.1.0"
TAUX_TVA = 0.20
LIMITE_HEURES_ANNUELLES = 1607
JOURS_OUVRES_PAR_AN = 218


class DateHelper:
    """Utilitaire de dates"""

    def aujourd_hui(self):
        from datetime import date
        return date.today().strftime("%d/%m/%Y")


class ConfigManager:
    """Gestionnaire de configuration de l'application"""

    def __init__(self):
        self.format_date = "FR"
        self.devise = "EUR"
        self.langue = "fr"
        self.max_heures_jour = 10
        self.jours_feries = []

    def charger_config(self, fichier):
        """Charge la configuration depuis un fichier"""
        with open(fichier, "r") as f:
            for ligne in f:
                cle, valeur = ligne.strip().split("=")
                setattr(self, cle, valeur)

    def sauvegarder_config(self, fichier):
        """Sauvegarde la configuration dans un fichier"""
        with open(fichier, "w") as f:
            f.write(f"format_date={self.format_date}\n")
            f.write(f"devise={self.devise}\n")
            f.write(f"langue={self.langue}\n")
            f.write(f"max_heures_jour={self.max_heures_jour}\n")

    def get_jours_feries(self, annee):
        """Retourne la liste des jours feries pour une annee"""
        return self.jours_feries


def valider_email(email):
    """Valide le format d'un email"""
    return "@" in email and "." in email


def formater_telephone(tel):
    """Formate un numero de telephone francais"""
    return f"{tel[:2]} {tel[2:4]} {tel[4:6]} {tel[6:8]} {tel[8:10]}"


def calculer_jours_ouvres(date_debut, date_fin):
    """Calcule le nombre de jours ouvres entre deux dates"""
    from datetime import datetime, timedelta
    d1 = datetime.strptime(date_debut, "%d/%m/%Y")
    d2 = datetime.strptime(date_fin, "%d/%m/%Y")
    jours = 0
    current = d1
    while current <= d2:
        if current.weekday() < 5:
            jours += 1
        current += timedelta(days=1)
    return jours
