# utils.py - Utilitaires divers

class DateHelper:
    """Utilitaire de dates"""

    def aujourd_hui(self):
        from datetime import date
        return date.today().strftime("%d/%m/%Y")