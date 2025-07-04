from abc import ABC, abstractmethod

#nom et prenom :
#Klai Sawsen

#La classe Ilivre oblige la classe livre d'herite des methodes inutile 
#par exemple livre audio n'utilise pas nb_page()
#livre papier n'utilise pas narrateur()
#alors, je supprime la classe Ilivre, mettre classe livre comme classe mere
#creer deux classe LivreAudio et LivrePapier qui herite du livre et ont de plus leurs propres methodes
class Livre:
    def __init__(self, isbn: str, titre: str,
                 auteur: str, genre: str):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self._genre = genre

    def genre(self) -> str:
        return self._genre

    def valider_isbn(self):
        """Logique de validation de l'ISBN."""
        if len(self.isbn.replace('-', '')) not in (10, 13):
            raise ValueError("ISBN invalide")
        # autres règles de validation...

    def afficher_format_long(self) -> str:
        # Affichage simple
        return f"{self.titre} - {self.auteur} (ISBN: {self.isbn})"
class LivrePapier(Livre):
    def __init__(self, isbn: str, titre: str,
                 auteur: str, genre: str,
                 nb_pages: int):
        super().__init__(isbn, titre, auteur, genre)
        self._nb_pages = nb_pages

    def nb_pages(self) -> int:
        return self._nb_pages

    def afficher_format_long(self) -> str:
        return f"{self.titre} - {self.auteur} ({self.genre()}, {self._nb_pages} pages, ISBN: {self.isbn})"


class LivreAudio(Livre):
    def __init__(self, isbn: str, titre: str,
                 auteur: str, genre: str,
                 narrateur: str):
        super().__init__(isbn, titre, auteur, genre)
        self._narrateur = narrateur

    def narrateur(self) -> str:
        return self._narrateur

    def afficher_format_long(self) -> str:
        return f"{self.titre} - {self.auteur} ({self.genre()}, Narrateur: {self._narrateur}, ISBN: {self.isbn})"

#1. SRP – Principe de Responsabilité Unique
#open/close : plusieurs if et else
class Bibliotheque:
    def __init__(self):
        self.inventaire: dict[str, int] = {}
        self.notif_service = NotificationServiceMail()
        self.notif_service_sms = NotificationServiceSMS()

    def ajouter_livre(self, livre: Livre, quantite: int):
        self.inventaire[livre.isbn] = self.inventaire.get(livre.isbn, 0) + quantite

    def generer_rapport_et_notification(self, type_rapport: str, type_notification: str) -> str:
        """Génère un rapport et l'envoie par email."""
        # Génération du rapport 
        if type_rapport == "pdf":
            rapport = RapportService().generer_pdf(self.inventaire)
        elif type_rapport == "csv":
            rapport = RapportService().generer_csv(self.inventaire)
        elif type_rapport == "html":
            rapport = RapportService().generer_html(self.inventaire)
        else:
            rapport = f"Rapport inventaire : {len(self.inventaire)} titres"

        # Envoie de la notification
        if type_notification == "email":
            self.notif_service.envoyer_email(
                "admin@biblio.local", "Rapport inventaire", rapport
            )
        elif type_notification == "sms":
            self.notif_service_sms.envoyer_sms(
                "1234567890", f"Rapport inventaire: {rapport}"
            )
        else:
            raise ValueError("Type de notification inconnu")
        return rapport

#la fonction generer_rapport_disponibilite n'utilise aucun attribut de la classe Utilisateur
class Utilisateur:
    def __init__(self, nom: str, mail: str):
        self.nom = nom
        self.mail = mail

    def generer_rapport_disponibilite(self, inventaire: dict[str, int]) -> str:
        """Génère un rapport d'emprunts."""
        lignes = [f"{isbn}: {qte}" for isbn, qte in inventaire.items()]
        return "\n".join(lignes)


class GestionnaireEmprunt:
    def __init__(self):
        self.emprunts: list[tuple[str, str]] = []
        self.notif_service = NotificationServiceMail()

    def emprunter(self, utilisateur: Utilisateur, livre: Livre):
        # logique de vérification minimaliste
        self.emprunts.append((utilisateur.mail, livre.isbn))
        message = f"{utilisateur.nom} a emprunté '{livre.titre}'"
        self.notif_service.envoyer_email(
            utilisateur.mail, "Emprunt confirmé", message
        )

    def retourner(self, utilisateur: Utilisateur, livre: Livre):
        self.emprunts.remove((utilisateur.mail, livre.isbn))
        message = f"{utilisateur.nom} a retourné '{livre.titre}'"
        self.notif_service.envoyer_email(
            utilisateur.mail, "Retour confirmé", message
        )


class NotificationServiceMail:
    def envoyer_email(self, to: str, subject: str, body: str):
        # Logique d'envoi d'e-mail (mock)
        print(f"Envoi e‑mail à {to} : '{subject}' – {body}")

#3. LSP – Principe de Substitution de Liskov
class NotificationServiceSMS(NotificationServiceMail):
    def envoyer_sms(self, number: str, message: str):
        # Logique d'envoi de SMS (mock)
        print(f"Envoi SMS à {number} : {message}")
    
    def envoyer_email(self, to: str, subject: str, body: str):
        raise NotImplementedError("Envoi d'e-mail non supporté par NotificationServiceSMS")


#1. SRP – Principe de Responsabilité Uniqueclass RapportService:

    def generer_pdf(self, inventaire: dict[str, int]) -> str:
        # Génération de PDF, logique mélangée
        return f"PDF – {len(inventaire)} titres dans l'inventaire"

    def generer_csv(self, inventaire: dict[str, int]) -> str:
        # Génération de CSV et HTML dans la même classe
        lignes = [f"{isbn},{qte}" for isbn, qte in inventaire.items()]
        return "isbn,qte\n" + "\n".join(lignes)

    def generer_html(self, inventaire: dict[str, int]) -> str:
        rows = "".join(f"<tr><td>{isbn}</td><td>{qte}</td></tr>" for isbn, qte in inventaire.items())
        return f"<table>{rows}</table>"
