import csv

def lire_ics(fichier_ics):
    """
    Lit un fichier ICS et retourne une liste de dictionnaires représentant les événements.
    """
    evenements = []
    evenement = {}
    with open(fichier_ics, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()
    
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne.startswith("BEGIN:VEVENT"):
            evenement = {}  # Réinitialiser l'événement
        elif ligne.startswith("END:VEVENT"):
            # Ajouter l'événement complet à la liste
            evenements.append(evenement)
        elif ":" in ligne:
            # Extraire la clé et la valeur
            cle, valeur = ligne.split(":", 1)
            if cle in evenement:
                # Gérer les valeurs multiples comme une liste
                if isinstance(evenement[cle], list):
                    evenement[cle].append(valeur)
                else:
                    evenement[cle] = [evenement[cle], valeur]
            else:
                evenement[cle] = valeur
    
    return evenements


def convertir_en_tableau(evenements):
    """
    Convertit une liste d'événements en tableau de chaînes CSV.
    """
    tableau = []
    for evenement in evenements:
        # Récupérer les valeurs des champs avec "vide" comme défaut
        dtstart = evenement.get("DTSTART", "vide")
        dtend = evenement.get("DTEND", "vide")
        summary = evenement.get("SUMMARY", "vide")
        location = evenement.get("LOCATION", "vide")
        description = evenement.get("DESCRIPTION", "vide")
        # Convertir les listes en chaînes séparées par des virgules si nécessaire
        if isinstance(location, list):
            location = ", ".join(location)
        if isinstance(description, list):
            description = ", ".join(description)
        
        # Générer une chaîne pour l'événement
        ligne = f"{dtstart}, {dtend}, {summary}, {location}, {description}"
        tableau.append(ligne)
    
    return tableau


def ecrire_tableau(tableau, fichier_csv):
    """
    Écrit le tableau dans un fichier CSV.
    """
    with open(fichier_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["DTSTART", "DTEND", "SUMMARY", "LOCATION", "DESCRIPTION"])  # En-têtes
        for ligne in tableau:
            writer.writerow(ligne.split(", "))  # Split pour convertir la chaîne en liste


if __name__ == "__main__":
    # Fichier source ICS
    fichier_ics = "ADE_RT1_Septembre2023_Decembre2023.ics"
    # Fichier de sortie CSV
    fichier_csv = "ADE_RT1_Septembre2023_Decembre2023.csv"
    
    # Lire et convertir le fichier ICS
    evenements = lire_ics(fichier_ics)
    tableau = convertir_en_tableau(evenements)
    
    # Écrire le tableau dans un fichier CSV
    ecrire_tableau(tableau, fichier_csv)
    
    # Afficher le tableau dans la console pour vérification
    for ligne in tableau:
        print(ligne)