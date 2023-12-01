from fonction import *

if __name__ == "__main__":

#Extraire les noms :
    directory = "./speeches"
file_extension = "txt"

# la liste des noms de fichiers
files_names = list_of_files(directory, file_extension)

# extraire les noms des présidents
president_names = extract_president_names(files_names)

# Affichez les noms des présidents extraits
print("Noms des présidents extraits :", president_names)

#Associer nom et prénom
nom_prenom_president={"Chirac": "Jacques" , "Giscard dEstaing": "Valéry", "Hollande" : "Francois" , "Mitterand": "Francois","Macron" : "Emmanuel", "Sarkosy"  : "Nicolas" }

#Afficher les prénoms

for val in nom_prenom_president.values():
    print(val)

#Miniscule

# Définir le répertoire où se trouvent les fichiers nettoyés
cleaned_directory = "./cleaned"

# Obtenir la liste des noms de fichiers dans le répertoire nettoyé
files_names = list_of_files(cleaned_directory, "txt")

#TF

cleaned_directory = "./cleaned"
# Parcourir chaque fichier et imprimer les occurrences de chaque mot
for filename in files_names:
    file_path = os.path.join(cleaned_directory, filename)
    word_occurrences = occurrences(file_path)

    print(f"Occurrences dans {filename}: {word_occurrences}")





