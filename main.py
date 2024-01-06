from fonction import *

if __name__ == "__main__":


    directory = "./speeches"
    file_extension = "txt"
    cleaned_directory = "./cleaned"

# la liste des noms de fichiers
files_names = list_of_files(directory, file_extension)

#Extraire les noms des présidents
president_names = extract_president_names(files_names)

#Associer nom et prénom
nom_prenom_president={"Chirac": "Jacques" , "Giscard dEstaing": "Valéry", "Hollande" : "Francois" , "Mitterand": "Francois","Macron" : "Emmanuel", "Sarkosy"  : "Nicolas" }


# Obtenir la liste des noms de fichiers dans le répertoire nettoyé
files_names = list_of_files(cleaned_directory, "txt")


# Menu
while True:
        print("\nMenu:")
        print("----Les demandes de base----")
        print("1. Extraire les noms de famille des présidents")
        print("2. Associer nom et prénom des présidents")
        print("3. Afficher les prénoms des présidents")
        print("4. Afficher les occurrences de chaque mot dans les discours")

        print("5. Calculer les scores IDF")
        print("6. Calculer les scores TF")
        print("7: Calculer la matrice TF-IDF")

        print("----Trouver certaines choses dans le texte----")
        print("8. Trouver les mots les moins importants")
        print("9. Trouver les mots les plus importants")
        print("10. Trouver les mots les plus répétés par un président")
        print("11. Trouver les présidents parlant de la 'nation'")
        print("12. Trouver le premier président parlant du climat et/ou de l'écologie")
        print("----Partie 2 ----")
        print("13.Tokenisation d'une question et recherche des mots de la question dans le Corpus ")
        print("14. 3. Calcul du vecteur TF-IDF pour les termes de la question : ")

        print("1. Quitter")

        choice = input("Choisissez une option (1-12): ")

        if choice == '1':
            directory = "./speeches"
            file_extension = "txt"
            files_names = list_of_files(directory, file_extension)
            president_names = extract_president_names(files_names)
            print("Noms des présidents extraits :", president_names)

        elif choice == '2':
            for nom, prenom in nom_prenom_president.items():
                print(f"{prenom} {nom}")


        elif choice == '3':
            prenom_president = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry", "Hollande": "Francois",
                                    "Mitterand": "Francois", "Macron": "Emmanuel", "Sarkosy": "Nicolas"}
            for val in nom_prenom_president.values():
                print(val)

        elif choice == '4':
            cleaned_directory = "./cleaned"
            for filename in list_of_files(cleaned_directory, "txt"):
                file_path = os.path.join(cleaned_directory, filename)
                word_occurrences = occurrences(file_path)
                print(f"Occurrences dans {filename}: {word_occurrences}")

        if choice == "5":
            # calculer la matrice IDF d'un corpus de documents
            x = compute_idf(cleaned_directory)
            print("La matrice IDF du corpus a été calculée")
            print(x)

        elif choice == "6":
            # calculer la matrice TF d'un fichier
            fichier = input("saisir le nom d'un fichier (déjà prétraité) : ")
            if fichier in list_of_files(cleaned_directory, "txt"):
                with open("./" + cleaned_directory + "/" + fichier) as f:
                    texte = f.read()
                x=compute_tf(texte)
                print(x)
                print("La matrice TF du fichier", fichier, "a été calculée")
            else:
                print("Le fichier n'existe pas")

        elif choice == "7":
            # calculer la matrice TF-IDF d'un corpus de documents
            x = compute_tfidf(cleaned_directory)
            print(x)
            print("La matrice TF-TDF du corpus a été calculée")

        elif choice == '8':
            x = compute_tfidf(cleaned_directory)
            unimportant_words = find_unimportant_words(x)

        elif choice == '9':
            x = compute_tfidf(cleaned_directory)
            most_important_words = find_most_important_words(x)
            print("Mot(s) ayant le score TF-IDF le plus élevé :", most_important_words)

        elif choice == '10':
            x = compute_tfidf(cleaned_directory)
            president_name = input("Entrez le nom du président : ")
            common_words = most_common_words_by_president(x, president_name)
            print(f"Mot(s) le(s) plus répété(s) par le président {president_name} :", common_words)

        elif choice == '11':

            presidents_with_theme = find_presidents_with_theme(cleaned_directory)
            mentions_by_president = count_nation_mentions(cleaned_directory)
            for president, mentions in mentions_by_president.items():
                print(f"{president}: {mentions} mention/s de 'nation'")

        elif choice == '12':
            premier_president = find_first_president_with_theme(cleaned_directory)
            if premier_president:
                print(f"Le premier président à parler du climat et/ou de l'écologie est : {premier_president}")
            else:
                print("Aucun président n'a abordé le climat et/ou l'écologie dans ces discours.")

        elif choice == '13':
            question_text = input("Saisir votre phrase:")
            question_tokens = tokenize_question(question_text, remove_stopwords=True)
            print(f"Liste des mots finaux : {question_tokens}")

            mots_a_chercher = question_tokens
            resultats = chercher_mots_dans_dossier(cleaned_directory, mots_a_chercher)

            for fichier, occurrences in resultats.items():
                print(f"\nOccurrences dans le fichier {fichier}:")
                for mot, count in occurrences.items():
                    if count != 0:
                        print(f"{mot}: {count} fois")

        elif choice == '14':

            idf_scores = compute_idf(cleaned_directory)

            question_text = input("Saisir votre phrase:")
            question_tokens = tokenize_question2(question_text, remove_stopwords=True)
            tf_idf_vector = calculate_tf_idf_vector(question_tokens, idf_scores)
            # Affichez le résultat ou utilisez-le comme vous le souhaitez
            print("Vecteur TF-IDF pour la question:", tf_idf_vector)



        elif choice == '17':
            print("Merci d'avoir utilisé le programme. Au revoir!")
            break

        else:
            print("Choix non valide. Veuillez entrer un numéro entre 1 et 11.")

####Partie 2###

print("\nPARTIE 2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      ""
      ":\n")



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




