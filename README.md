# R606 - TP2 : Chasse aux Code Smells

## Description

Ce projet contient une application Python de **gestion de feuilles de temps** (timesheet).
Le code fonctionne, mais il est truffé de **code smells** (défauts de conception) qu'il vous faudra identifier et corriger.

L'application se trouve dans le répertoire `TP2/` et comprend :
- `main.py` : Point d'entrée
- `models.py` : Classes métier (employés, projets, entrées de temps)
- `services.py` : Service principal de gestion
- `reports.py` : Génération de rapports
- `notifications.py` : Notifications et workflow d'approbation
- `utils.py` : Utilitaires divers

## Objectif

Vous devez identifier et corriger les **15 code smells** suivants, présents au moins une fois chacun dans le code :

1. **Long Method** (Méthode trop longue)
2. **Large Class** (Classe trop grande / God Class)
3. **Primitive Obsession** (Obsession des primitives)
4. **Too Many Parameters** (Trop de paramètres)
5. **Switch Statements** (Abus de switch/if-elif)
6. **Inappropriate Inheritance** (Mauvais héritage)
7. **Duplicate Class** (Deux classes, une fonctionnalité)
8. **Divergent Change** (Changement divergent)
9. **Shotgun Surgery** (Chirurgie au fusil à pompe)
10. **Message Chains** (Chaînes de messages)
11. **Middle Man** (Homme du milieu)
12. **Duplicate Code** (Code dupliqué)
13. **Lazy Class** (Classe paresseuse)
14. **Data Class** (Classe de données)
15. **Dead Code** (Code mort)

## Instructions

### 1. Récupérer le projet

Clonez le dépôt du projet :

```bash
git clone https://git.unicaen.fr/nkarageuzian/but-info-r606.git
cd but-info-r606
```

Pour conserver votre historique entre vos postes de travail, vous pouvez créer un projet **privé** sur GitLab et y pousser votre copie :

```bash
git remote set-url origin https://git.unicaen.fr/<votre-login>/but-info-r606.git
git push -u origin main
```

### 3. Lancer l'application

```bash
cd TP2
python3 main.py
```

Vérifiez que l'application fonctionne correctement avant de commencer vos modifications.

### 4. Identifier et corriger les code smells

Pour chaque code smell :
- Identifiez où il se trouve dans le code
- Appliquez le réusinage approprié
- Vérifiez que l'application fonctionne toujours après correction

Committez vos changements régulièrement avec des messages clairs :

```bash
git add -A
git commit -m "Réusinage : correction du code smell <nom du smell>"
```

### 5. Soumettre votre travail

Une fois toutes vos corrections terminées, créez une archive zip du répertoire `.git` et déposez-la sur **ecampus** :

```bash
zip -r git_directory.zip .git
```

Déposez le fichier `git_directory.zip` sur ecampus dans l'espace de dépôt prévu.

## Critères d'évaluation

- Identification correcte des 15 code smells
- Qualité des réusinages appliqués
- Le code fonctionne toujours après les corrections
- Clarté des messages de commit
