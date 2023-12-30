from fonction import *

if __name__ == "__main__":

#Extraire les noms :
    directory = "./speeches"
    file_extension = "txt"

# la liste des noms de fichiers
files_names = list_of_files(directory, file_extension)

#Extraire les noms des présidents
president_names = extract_president_names(files_names)

# Affichez les noms des présidents extraits
print("Noms des présidents extraits :", president_names)

#Associer nom et prénom
nom_prenom_president={"Chirac": "Jacques" , "Giscard dEstaing": "Valéry", "Hollande" : "Francois" , "Mitterand": "Francois","Macron" : "Emmanuel", "Sarkosy"  : "Nicolas" }

#Afficher les prénoms
for val in nom_prenom_president.values():
    print(val)

# Obtenir la liste des noms de fichiers dans le répertoire nettoyé
cleaned_directory = "./cleaned"
files_names = list_of_files(cleaned_directory, "txt")

#Occurence
for filename in files_names:
    file_path = os.path.join(cleaned_directory, filename)
    word_occurrences = occurrences(file_path)

    print(f"Occurrences dans {filename}: {word_occurrences}")

# Calculer IDF
idf_scores = calculate_idf(cleaned_directory)

for word, idf_score in idf_scores.items():
    print(f"Mot : {word}, Score IDF : {idf_score}")

#TF IDF
# Pour TF-IDF scores soit TF * IDF

idf_scores, tf_idf_scores = calculate_idf_tf(cleaned_directory)

    # Accédez aux éléments du tuple correctement
for document, scores in tf_idf_scores.items():
        print(f"Document: {document}, TF-IDF scores: {scores}")
        for word, tf_idf_score in scores.items():
            print(f"  Mot : {word}, Score TF-IDF : {tf_idf_score}")

#Matrice
tfidf_matrix = generate_tfidf_matrix(cleaned_directory)

# Affichez la forme de la matrice TF-IDF
print("la matrice TF-IDF avant transposition :", len(tfidf_matrix), "x", len(tfidf_matrix[0]))

# Transposer la matrice
transposed_tfidf_matrix = transpose_matrix(tfidf_matrix)
print("la matrice TF-IDF après transposition :", len(transposed_tfidf_matrix), "x", len(transposed_tfidf_matrix[0]))

# Affichez la matrice TF-IDF
print("#####Matrice TF-IDF avant transposition :####")
print_tfidf_matrix(tfidf_matrix)

# Transposer la matrice TF-IDF
transposed_tfidf_matrix = transpose_matrix(tfidf_matrix)


print("######Matrice TF-IDF après transposition :#####")
print_tfidf_matrix(transposed_tfidf_matrix)

# Les mots les moins important
from fonction import calculate_idf_tf, find_unimportant_words
unimportant_words = find_unimportant_words(tf_idf_scores)
print("Mots les moins importants (TF-IDF = 0) :", unimportant_words)


# Mot important (TF-idf le plus élévé)
from fonction import calculate_idf_tf, find_most_important_words

most_important_words = find_most_important_words(tf_idf_scores)
print("Mot(s) ayant le score TF-IDF le plus élevé :", most_important_words)


#Chirac mots
from fonction import calculate_idf_tf, most_common_words_by_president
president = "Chirac"
common_words = most_common_words_by_president(tf_idf_scores, president)

# Afficher le(s) mot(s) le(s) plus répété(s)
print(f"Mot(s) le(s) plus répété(s) par le président {president} :", common_words)


# Nation

from fonction import find_presidents_with_theme, load_text

presidents_with_theme = find_presidents_with_theme(cleaned_directory)
mentions_by_president = count_nation_mentions(cleaned_directory)

for president, mentions in mentions_by_president.items():
    print(f"{president}: {mentions} mention/s de 'nation'")

#Climat
premier_president = find_first_president_with_theme(cleaned_directory)

if premier_president:
    print(f"Le premier président à parler du climat et/ou de l'écologie est : {premier_president}")
else:
    print("Aucun président n'a abordé le climat et/ou l'écologie dans ces discours.")



#
# # Menu
# while True:
#         print("\nMenu:")
#         print("----Les demandes de base----")
#         print("1. Extraire les noms de famille des présidents")
#         print("2. Associer nom et prénom des présidents")
#         print("3. Afficher les prénoms des présidents")
#         print("4. Afficher les occurrences de chaque mot dans les discours")
#         print("5. Calculer les scores TF-IDF")
#         print("----Trouver certaines choses dans le texte----")
#         print("6. Trouver les mots les moins importants")
#         print("7. Trouver les mots les plus importants")
#         print("8. Trouver les mots les plus répétés par un président")
#         print("9. Trouver les présidents parlant de la 'nation'")
#         print("10. Trouver le premier président parlant du climat et/ou de l'écologie")
#         print("11. Quitter")
#
#         choice = input("Choisissez une option (1-12): ")
#
#         if choice == '1':
#             directory = "./speeches"
#             file_extension = "txt"
#             files_names = list_of_files(directory, file_extension)
#             president_names = extract_president_names(files_names)
#             print("Noms des présidents extraits :", president_names)
#
#         elif choice == '2':
#             for nom, prenom in nom_prenom_president.items():
#                 print(f"{prenom} {nom}")
#
#
#         elif choice == '3':
#             prenom_president = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry", "Hollande": "Francois",
#                                     "Mitterand": "Francois", "Macron": "Emmanuel", "Sarkosy": "Nicolas"}
#             for val in nom_prenom_president.values():
#                 print(val)
#
#         elif choice == '4':
#             cleaned_directory = "./cleaned"
#             for filename in list_of_files(cleaned_directory, "txt"):
#                 file_path = os.path.join(cleaned_directory, filename)
#                 word_occurrences = occurrences(file_path)
#                 print(f"Occurrences dans {filename}: {word_occurrences}")
#
#         elif choice == '5':
#             corpus_directory = "./cleaned"
#             idf_scores, tf_idf_scores = calculate_idf_tf(corpus_directory)
#             for document, scores in tf_idf_scores.items():
#                 print(f"Document : {document}")
#                 for word, tf_idf_score in scores.items():
#                     print(f"  Mot : {word}, Score TF-IDF : {tf_idf_score}")
#
#         elif choice == '6':
#             unimportant_words = find_unimportant_words(tf_idf_scores)
#             print("Mots les moins importants (TF-IDF = 0) :", unimportant_words)
#
#         elif choice == '7':
#             most_important_words = find_most_important_words(tf_idf_scores)
#             print("Mot(s) ayant le score TF-IDF le plus élevé :", most_important_words)
#
#         elif choice == '8':
#             president_name = input("Entrez le nom du président : ")
#             common_words = most_common_words_by_president(tf_idf_scores, president_name)
#             print(f"Mot(s) le(s) plus répété(s) par le président {president_name} :", common_words)
#
#         elif choice == '9':
#             directory_path2 = "./Cleaned"
#             presidents_with_theme = find_presidents_with_theme(directory_path2)
#             directory_path = "./Cleaned"
#             mentions_by_president = count_nation_mentions(directory_path)
#             for president, mentions in mentions_by_president.items():
#                 print(f"{president}: {mentions} mention/s de 'nation'")
#
#         elif choice == '10':
#             directory_path2 = "./Cleaned"
#             premier_president = find_first_president_with_theme(directory_path2)
#             if premier_president:
#                 print(f"Le premier président à parler du climat et/ou de l'écologie est : {premier_president}")
#             else:
#                 print("Aucun président n'a abordé le climat et/ou l'écologie dans ces discours.")
#
#         elif choice == '11':
#             print("Merci d'avoir utilisé le programme. Au revoir!")
#             break
#
#         else:
#             print("Choix non valide. Veuillez entrer un numéro entre 1 et 11.")

####Partie 2###

print("\nPARTIE 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      ""
      ":\n")
question_text = "Quelle est l'importance de l'écologie dans la politique actuelle?"
question_tokens = tokenize_question(question_text, remove_stopwords=True)
print(question_tokens)

mots_a_chercher = question_tokens
resultats = chercher_mots_dans_dossier(cleaned_directory, mots_a_chercher)


for fichier, occurrences in resultats.items():
    print(f"\nOccurrences dans le fichier {fichier}:")
    for mot, count in occurrences.items():
        if count != 0 :
            print(f"{mot}: {count} fois")


tf_idf_vector = calculate_tf_idf_vector(question_tokens, idf_scores, tfidf_matrix)
# Affichez le résultat ou utilisez-le comme vous le souhaitez
print("Vecteur TF-IDF pour la question:", tf_idf_vector)

#4

similarites = []

for vecteur in tfidf_matrix:
    similarity = cosine_similarity(tf_idf_vector, vecteur)

    if isinstance(similarity, float):
        similarites.append(similarity)
        print(f"Similarité avec le vecteur {vecteur} : {similarity}")
    else:
        print(f"Similarité avec le vecteur {vecteur} : {similarity}")

# Si le calcul est possible, trouver l'indice du vecteur le plus similaire
if similarites:
    indice_max_similarity = max(range(len(similarites)), key=similarites.__getitem__)
    print(f"\nLe vecteur le plus similaire dans la matrice est à l'indice {indice_max_similarity}")
    print(f"Similarité : {similarites[indice_max_similarity]}")

