import markdown
import webbrowser
import matplotlib.pyplot as plt
from collections import Counter

# Lecture du fichier
try:
    with open(r"DumpFile.txt", "r", encoding='utf-8') as fh:
        ress = fh.read().split('\n')

    valeur = []

    def lecture():
        for row in ress:
            if not row.startswith("\t"):
                construction_liste(row)

    def construction_liste(row):
        if "IP" in row:
            txt_split = row.split(">")
            txt_split2 = txt_split[0].split("IP")
            heure = txt_split2[0].strip()
            IP_source_with_port = txt_split2[1].strip()

            # Extraire le port source
            IP_source, port_source = IP_source_with_port.rsplit(".", 1) if '.' in IP_source_with_port else (IP_source_with_port, "Vide")

            IP_destination_with_port = txt_split[1].split(":")[0].strip()
            IP_destination, port_destination = IP_destination_with_port.rsplit(".", 1) if '.' in IP_destination_with_port else (IP_destination_with_port, "Vide")

            txt_split6 = txt_split[1].split(": ")[1]
            txt_split7 = txt_split6.split(", ")

            # Gérer les colonnes optionnelles et longueur
            option = txt_split7[4].strip() if len(txt_split7) > 4 and 'options' in txt_split7[4] else "Vide"
            length = txt_split7[-1].strip() if txt_split7 else "Vide"

            evenement = f"{heure};{IP_source};{IP_destination};{port_source};{port_destination};{option};{length}"
            valeur.append(evenement)

    lecture()

    # Générer le contenu Markdown
    headers = ["Heure", "IP Source", "IP Destination", "Port Source", "Port Destination", "Option", "Length"]
    markdown_content = f"| {' | '.join(headers)} |\n"
    markdown_content += f"| {' | '.join(['---'] * len(headers))} |\n"

    for row in valeur:
        markdown_content += f"| {' | '.join(row.split(';'))} |\n"

    # Convertir le Markdown en HTML avec style
    html_content = markdown.markdown(markdown_content, extensions=['tables'])

    # Ajouter du style CSS au tableau HTML
    html_with_structure = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Résultat TCPDump</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f9f9f9;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background-color: #ffffff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border: 1px solid #dddddd;
            }}
            th {{
                background-color: #00BFFF;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        <h1>Analyse des données TCPDump</h1>
        {html_content}
    </body>
    </html>
    """

    # Sauvegarder dans un fichier HTML
    html_file = r'resultat.html'
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_with_structure)

    # Ouvrir automatiquement dans le navigateur
    webbrowser.open(html_file)

    # Analyse des données pour le graphique
    options = [row.split(";")[5] for row in valeur]
    options_counter = Counter(options)

    # Création du graphique en camembert
    plt.figure(figsize=(8, 8))
    plt.pie(
        options_counter.values(),
        labels=options_counter.keys(),
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title("Répartition des Options")
    plt.show()

    print(f"Tableau Markdown converti en HTML avec style et ouvert dans le navigateur : {html_file}")

except FileNotFoundError:
    print("Le fichier DumpFile.txt n'existe pas.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")