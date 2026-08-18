# API Archivyne

## Description

Cette API est développée avec Django REST Framework et permet de gérer :

- les utilisateurs de l’application,
- l’authentification JWT,
- les formations disponibles dans la plateforme.

Le projet est structuré en deux applications principales :

1. `users`
   - gestion de l’inscription,
   - gestion des profils utilisateurs,
   - rôles disponibles : `admin` et `student`.

2. `formations`
   - gestion des formations,
   - consultation publique des formations,
   - création, modification et suppression réservées aux administrateurs.

---

## Structure du projet

```text
Api/
├── api/
│   ├── api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   ├── formations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   └── manage.py
└── README.md
```

---

## Modèles principaux

### `users.User`

Le modèle utilisateur hérite de `AbstractUser` et ajoute :

- `role` : `admin` ou `student`
- `bio` : description du profil
- `username`, `email`, `first_name`, `last_name` : champs standard Django

### `formations.Formations`

Le modèle formation contient :

- `title`
- `description`
- `prix`
- `created_at`
- `updated_at`

---

## Authentification

L’API utilise JWT via `rest_framework_simplejwt`.

### Endpoints JWT

- `POST /api/login/`
  - connexion et génération du token JWT
- `POST /api/refresh/`
  - rafraîchissement du token d’accès

---

## Routing de l’API

### Routes générales

- `GET /admin/`
  - interface d’administration Django
- `POST /api/login/`
  - connexion utilisateur
- `POST /api/refresh/`
  - renouvellement du token

### Application `users`

- `POST /api/users/signup/`
  - inscription d’un nouvel utilisateur

### Application `formations`

Les routes sont générées avec `DefaultRouter`.

- `GET /api/formations/formations/`
  - liste toutes les formations
- `POST /api/formations/formations/`
  - créer une formation (admin uniquement)
- `GET /api/formations/formations/<id>/`
  - détail d’une formation
- `PUT /api/formations/formations/<id>/`
  - modification complète d’une formation (admin uniquement)
- `PATCH /api/formations/formations/<id>/`
  - modification partielle d’une formation (admin uniquement)
- `DELETE /api/formations/formations/<id>/`
  - suppression d’une formation (admin uniquement)

---

## Permissions

### 1. Inscription utilisateur

- `RegisterView` utilise : `permissions.AllowAny`
- tout le monde peut créer un compte.

### 2. Authentification

- Les endpoints protégés utilisent `JWTAuthentication` via le framework DRF.

### 3. Formations

La permission est définie dans `IsAdminOrReadOnly` :

- `GET`, `HEAD`, `OPTIONS` : accessibles à tous
- `POST`, `PUT`, `PATCH`, `DELETE` : réservés aux utilisateurs authentifiés ayant le rôle `admin`

En pratique :

```python
if request.method in permissions.SAFE_METHODS:
    return True
return request.user.is_authenticated and request.user.role == 'admin'
```

Cela signifie que :

- un visiteur peut lire la liste des formations,
- un étudiant ne peut pas créer ou modifier une formation,
- un administrateur peut gérer les formations.

---

## Rôles utilisateur

| Rôle | Description | Droits |
| --- | --- | --- |
| `student` | Utilisateur standard | lecture des formations, inscription |
| `admin` | Administrateur | gestion des formations et accès admin |

---

## Exemple de flux

### Inscription

```http
POST /api/users/signup/
```

Body:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123",
  "first_name": "Alice",
  "last_name": "Martin",
  "role": "student"
}
```

### Connexion

```http
POST /api/login/
```

Body:

```json
{
  "username": "alice",
  "password": "secret123"
}
```

Retour attendu :

```json
{
  "refresh": "...",
  "access": "..."
}
```

### Consultation des formations

```http
GET /api/formations/formations/
```

---

## Lancer l’API

Depuis le dossier `Api/api` :

```bash
python manage.py migrate
python manage.py runserver
```

---

## Notes

- L’API est conçue pour un usage simple et sécurisé pour les opérations CRUD sur les formations.
- La logique actuelle exige une vérification du rôle `admin` pour les modifications.
- Le système d’authentification est basé sur JWT, ce qui est adapté à un frontend séparé comme Next.js.
