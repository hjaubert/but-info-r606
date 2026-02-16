# reports.py - Generation de rapports et statistiques

class FormateurRapport:
    """Formateur de lignes de rapport"""

    def formater_ligne(self, projet_nom, heures, taux):
        """Formate une ligne de rapport avec le cout"""
        return f"{projet_nom}: {heures:.1f}h - {heures * taux:.2f} EUR"

    def formater_total(self, total_heures, taux):
        """Formate la ligne de total"""
        return f"TOTAL: {total_heures:.1f}h - {total_heures * taux:.2f} EUR"
