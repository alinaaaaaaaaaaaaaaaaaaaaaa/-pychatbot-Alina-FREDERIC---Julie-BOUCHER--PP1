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

#Occ

cleaned_directory = "./cleaned"
# Parcourir chaque fichier et imprimer les occurrences de chaque mot
for filename in files_names:
    file_path = os.path.join(cleaned_directory, filename)
    word_occurrences = occurrences(file_path)

    print(f"Occurrences dans {filename}: {word_occurrences}")

# IDF

# Exemple d'utilisation :
corpus_directory = "./cleaned"  # Remplacez par votre répertoire de corpus
idf_scores = calculate_idf(corpus_directory)

# Affichez les scores IDF pour chaque mot
for word, idf_score in idf_scores.items():
    print(f"Mot : {word}, Score IDF : {idf_score}")

print("#############")

##TF IDF
corpus_directory = "./cleaned"
tf_idf_scores = calculate_tf_idf(corpus_directory)

for document, scores in tf_idf_scores.items():
    print(f"Document : {document}")
    for word, tf_idf_score in scores.items():
        print(f"  Mot : {word}, Score TF-IDF : {tf_idf_score}")


print("#############")

#Matrice
corpus_directory = "./cleaned"  # Remplacez par votre répertoire de corpus
tfidf_matrix = generate_tfidf_matrix(corpus_directory)

# Affichez la forme de la matrice TF-IDF
print("la matrice TF-IDF avant transposition :", len(tfidf_matrix), "x", len(tfidf_matrix[0]))

# Transposer la matrice TF-IDF
transposed_tfidf_matrix = transpose_matrix(tfidf_matrix)

# Affichez la forme de la matrice TF-IDF après transposition
print("la matrice TF-IDF après transposition :", len(transposed_tfidf_matrix), "x", len(transposed_tfidf_matrix[0]))

# Exemple d'utilisation :
corpus_directory = "./cleaned"  # Remplacez par votre répertoire de corpus
tfidf_matrix = generate_tfidf_matrix(corpus_directory)

# Affichez la matrice TF-IDF
print("#############################################################################Matrice TF-IDF avant transposition :")
print_tfidf_matrix(tfidf_matrix)

# Transposer la matrice TF-IDF si nécessaire
transposed_tfidf_matrix = transpose_matrix(tfidf_matrix)

# Affichez la matrice TF-IDF après transposition
print("#############################################################################Matrice TF-IDF après transposition :")
print_tfidf_matrix(transposed_tfidf_matrix)



