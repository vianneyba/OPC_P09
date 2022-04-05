# LITReview
#### LITReview est une application permettant à une communauté de consulter ou de solliciter une critique de livres à la demande.

## Création de l'environnement virtuel

Taper dans le dossier de LITReview: *python -m venv env*

Activer l'environement: *source env/bin/activate*

Installer les dependance: *pip install -r requirements.txt*

Pour démarrer le serveur tapez: *python3 manage.py runserver*

Dans un navigateur: *127.0.0.1:8000*

## utilisateurs en base

|utilisateur|mot de passe|
|-----------|------------|
|vianney    |lille59000  |
|pascal     |lille59000  |
|marcel     |lille59000  |
|aymeric    |lille59000  |
|gérald     |lille59000  |

## Fonctionnalités

La première page permet de s'inscrire ou de se connecté avec un compte existant pour avoir accés a l'application.

une fois connecté on arrive a la page flux ou l'utilisateur voit ses tickets ou ses critiques et aussi ceux des personnes qu'on suit.

le menu permet de:

- **Flux**: revenir au flux avec ses tickets, critiques et ceux des personnes qu'on suit. Sur cette page il est possible d'écrire une critique en réponse a un ticket.
- **Posts**: pour voir ses tickets et critiques, on peut modifier ses tickets, et ses critiques ou effacer ses critiques et tickets si il n'y a pas de critique associer, on peut aussi écrire un critique sur un ticket.
- **Abonnements**: il est possible de suivre un utilisateur avec son nom, voir les personnes que l'on suit ou voir les personnes qui nous suivent.
- **Deconnexion**: permet de se déconnecter de l'application.

sur la page de flux et sur les posts est présent deux bountons:

- **Demander une critique**: pour écrire un ticket
- **Créer une critique**: pour écrire un ticket et la critique qui correspont.
