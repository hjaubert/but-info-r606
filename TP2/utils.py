# utils.py - Utilitaires divers

def aujourd_hui():
    """Retourne la date du jour au format JJ/MM/AAAA"""
    from datetime import date
    return date.today().strftime("%d/%m/%Y")