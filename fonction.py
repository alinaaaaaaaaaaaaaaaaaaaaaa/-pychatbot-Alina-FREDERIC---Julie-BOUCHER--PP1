import os # manipulation de fichiers, navigation dans les répertoires, exécution de commandes système.
import re #motif qui aide pour la recherche
from typing import Dict
import string #manipulation de chaînes de caractères.
from collections import Counter # ompter le nombre d'occurrences des éléments
import math


#Extraire les noms :
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def extract_president_names(files_names):
    president_names = set()

    for filename in files_names:
        name_without_prefix = filename[11:-4]
        name_without_digits = ''.join(char for char in name_without_prefix if not char.isdigit())
        president_names.add(name_without_digits)

    return list(president_names)

#prend un chemin d'accès vers un fichier, nettoie chaque ligne de ce fichier en supprimant les apostrophes
# et les signes de ponctuation tout en convertissant toutes les lettres en minuscules
def clean_line(line):
    cleaned_line = line.replace("'", " ") #remplace chaque occurrence de l'apostrophe (') dans la ligne par un espace
    cleaned_line = cleaned_line.translate(str.maketrans("", "", string.punctuation))#supprime tous les signes de ponctuation de la ligne
    return cleaned_line

def convert_to_lowercase_and_clean(file_path, output_folder, new_file_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = [clean_line(line.lower()) for line in lines]

    cleaned_file_path = os.path.join(output_folder, new_file_name)#chemin d'accès
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.writelines(cleaned_lines)

speeches_directory = "./speeches"
cleaned_directory = "./cleaned"

os.makedirs(cleaned_directory, exist_ok=True)

files_names = list_of_files(speeches_directory, "txt")
for filename in files_names:
    new_file_name = f"Cleaned_{filename}"

    file_path = os.path.join(speeches_directory, filename)
    convert_to_lowercase_and_clean(file_path, cleaned_directory, new_file_name)

#Occurence
def occurrences(file_path):
    word_occurrences_dict = {} #initialise un dictionnaire vide

    with open(file_path, 'r') as file: # with garantit que le fichier sera correctement fermé après son utilisation
        for line in file:
            cleaned_line = clean_line(line)
            words_in_line = cleaned_line.split()#divise la ligne nettoyée en mots en utilisant l'espace comme délimiteur

            word_count = Counter(words_in_line)

            for word, count in word_count.items():
                if word in word_occurrences_dict:
                    word_occurrences_dict[word] += count
                else:
                    word_occurrences_dict[word] = count

    return word_occurrences_dict


def tf(ch):
    # prend en paramètre une chaîne de caractères correspondant au contenu d'un fichier
    #et renvoie sa matrice (dictionnaire) TF

    tf_score = {}


    mots = ch.split(" ")# extraction de tous les mots de la chaîne de caractère "ch"


    for mot in mots:# création d'un score tf pour chaque mot de la chaîne "ch"
        tf_score[mot] = float(tf_score.get(mot, 0) + 1)


    if '' in tf_score:  # suppression des chaînes de caractères vides
        del tf_score['']

    return tf_score


def idf(repertoire):
    #prend en paramètre un répertoire, calcule le score IDF pour chaque mot du corpus
    # et renvoie la matrice (dictionnaire) IDF du corpus """

    matrice_tdf = {}


    docs = list_of_files(repertoire, "txt")# extraction des fichiers de "dossier"
    nb_doc = len(docs)

    occurrences_mots_dans_corpus = {}

    for fichier in docs:

        with open(repertoire + "/" + fichier, "r") as f:

            # calcul du nombre de documents dans lesquels chaque mots du le corpus apparait
            mots_fichier = set(f.read().split())# set=collection non ordonnée et sans doublons d'éléments distincts
            for mot in mots_fichier:
                occurrences_mots_dans_corpus[mot] = occurrences_mots_dans_corpus.get(mot, 0) + 1



    for mot, occurrence in occurrences_mots_dans_corpus.items():
        matrice_tdf[mot] = math.log10(nb_doc / occurrence)

    return matrice_tdf

def creation_matrices_tf_idf(repertoire):
    #prend en paramètre un répertoire et renvoie les matrices TF et IDF de celui-ci

    doc = list_of_files(repertoire, "txt")


    matrice_idf = idf(repertoire)# création de la matrice IDF


    matrice_tf = dict.fromkeys(doc, None)# création de la matrice TF
    for fichier in doc:
        with open("./" + repertoire + "/" + fichier, "r") as f:

            texte_fichier = f.read()
            matrice_tf[fichier] = tf(texte_fichier)

    return matrice_tf, matrice_idf #sous forme de tuple : une fois qu'ils sont créés on ne peut pas modifier les éléments

def tfidf(repertoire):
    #prend en paramètre un répertoire et renvoie la matrice TF-IDF
    #(dictionnaire de dictionnaire du type { fichier : { mot1 : score1, mot2 : score2 } } )
     #de chaque mot du corpus

    doc = list_of_files(repertoire, "txt")


    matrice_tf, matrice_idf = creation_matrices_tf_idf(repertoire)# création des matrices IDF et TF

    matrice_tfidf = {}


    for fichier in doc:  # on remplie la matrice TF-IDF
        matrice_tfidf[fichier] = {}
        for mot in matrice_idf.keys():
            matrice_tfidf[fichier][mot] = matrice_tf[fichier].get(mot, 0) * matrice_idf[mot]

    return matrice_tfidf

# Mot important en score

def find_most_important_words(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
    most_important_words = set()

    for filename, scores in tf_idf_scores.items():
        max_score = max(scores.values())
        most_important_words.update(word for word, score in scores.items() if score == max_score)

    return most_important_words

# Mot moins important
def find_unimportant_words(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
        unimportant_words = set()


        words_in_first_document = list(tf_idf_scores.values())[0]# Utilisez n'importe quel document pour obtenir la liste des mots

        for word in words_in_first_document:

            if all(word in document and document[word] == 0 for document in tf_idf_scores.values()):# Vérifier si le mot est présent dans tous les documents et si le score TF-IDF est égal à zéro
                #all= vérifier si un mot est présent dans tous les documents + si le score TF-IDF associé est égal à zéro
                unimportant_words.add(word)

        print("Mots non importants :", unimportant_words)

        return unimportant_words


# Chirac mots

def most_common_words_by_president(tf_idf_scores: Dict[str, Dict[str, float]], president_name: str) -> set:
    common_words = set()
    all_occurrences = Counter()


    for filename, scores in tf_idf_scores.items():
        if president_name.lower() in filename.lower():
            file_path = os.path.join("./cleaned", filename)
            if os.path.exists(file_path):
                all_occurrences.update(occurrences(file_path))
            else:
                print(f"Erreur fichier introuvable {file_path}.")

    max_count = max(all_occurrences.values())
    common_words.update(word for word, count in all_occurrences.items() if count == max_count)

    return common_words

# Nation

def load_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()


def detect_nation(text):
    keywords = ["nation","Nation"]
    for keyword in keywords:
        if keyword in text:
            return True
    return False


def find_presidents_with_theme(directory_path):
    presidents_with_theme = []

    for president in os.listdir(directory_path):
        file_path = os.path.join(directory_path, president)

        if president.endswith(".txt"):
            text = load_text(file_path)

            if detect_nation(text):
                president_name = president.split(".")[0]
                presidents_with_theme.append(president_name)

    return presidents_with_theme
def count_nation_mentions(directory_path):
    mentions_by_president = {}

    presidents = os.listdir(directory_path)#obtenir la liste des fichiers dans le répertoire spécifié

    for president in presidents:
        file_path = os.path.join(directory_path, president)
        if president.endswith(".txt"):

            president_name = president.split("_")[2].split(".")[0]# Extraire le nom du président du nom du fichier

            text = load_text(file_path)
            mentions_by_president[president_name] = text.lower().split().count("nation")

    return mentions_by_president

# Climat

def load_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def detect_climate_ecology(text):
    keywords = ["climat", "écologie", "environnement","Climat","Écologie","Environnement"]
    for keyword in keywords:
        if keyword in text:
            return True
    return False

def find_first_president_with_theme(directory_path):
    presidents = os.listdir(directory_path)

    for president in presidents:
        file_path = os.path.join(directory_path, president)
        if president.endswith(".txt"):

            president_name = president.split("_")[2].split(".")[0]# Extraire le nom du président du nom du fichier

            text = load_text(file_path)
            if detect_climate_ecology(text):
                return president_name

    return None


from typing import Dict, Set

def find_common_words_except_unimportant(tf_idf_scores: Dict[str, Dict[str, float]]) -> Set[str]:
    unimportant_words = find_unimportant_words(tf_idf_scores)
    first_document = list(tf_idf_scores.keys())[0]
    common_words_except_unimportant = set(tf_idf_scores[first_document].keys())

    for filename in tf_idf_scores:
        common_words_except_unimportant.intersection_update(tf_idf_scores[filename].keys())

    # Retirez les mots non importants
    common_words_except_unimportant.difference_update(unimportant_words)#difference update=retirer les mots non importants

    return common_words_except_unimportant



#### Partie 2 ####

def tokenize_question(question, remove_stopwords=False):
    print(f"Question originale : {question}")

    question = question.lower()
    print(f"Après conversion en minuscules : {question}")

    # Suppression de la ponctuation en conservant les espaces autour des articles
    question = ''.join(char if char not in string.punctuation or (char in {' '} and "'" not in question[i-1:i+2]) else ' ' for i, char in enumerate(question))
    print(f"Après suppression de la ponctuation : {question}")

    question = ' '.join(question.split())
    print(f"Après suppression des espaces supplémentaires : {question}")


    question = question.replace("'", "")# Suppression de l'apostrophe
    print(f"Après suppression de l'apostrophe : {question}")

    if remove_stopwords:
        stopwords = ["le", "l", "la", "les", "de", "du", "des", "et", "et", "ou", "mais", "si", "que"]
        question_words = [word for word in question.split() if word not in stopwords]
    else:
        question_words = question.split()

    return question_words

def tokenize_question2(question, remove_stopwords=False):
    print(f"Question originale : {question}")

    question = question.lower()

    # Suppression de la ponctuation en conservant les espaces autour des articles
    question = ''.join(char if char not in string.punctuation or (char in {' '} and "'" not in question[i-1:i+2]) else ' ' for i, char in enumerate(question))

    question = ' '.join(question.split())


    question = question.replace("'", "")# Suppression de l'apostrophe

    if remove_stopwords:
        stopwords = ["le", "l", "la", "les", "de", "du", "des", "et", "et", "ou", "mais", "si", "que","une","un"]
        question_words = [word for word in question.split() if word not in stopwords]
    else:
        question_words = question.split()

    return question_words


def find_word(chemin_dossier, liste_mots):
    resultats = {}


    for nom_fichier in os.listdir(chemin_dossier):# Parcours de tous les fichiers dans le dossier
        if nom_fichier.endswith(".txt"):
            chemin_fichier = os.path.join(chemin_dossier, nom_fichier)


            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:# Ouverture et lecture du fichier
                contenu = fichier.read()


                occurrences = {}# Recherche des occurrences de mots dans le contenu du fichier
                for mot in liste_mots:
                    occurrences[mot] = contenu.count(mot)


                if nom_fichier not in resultats:# Ajout des résultats au dictionnaire des résultats
                    resultats[nom_fichier] = occurrences
                else:
                    resultats[nom_fichier].update(occurrences)

    return resultats

# def calculate_tf_idf_vector(question_tokens, idf_scores):
#     tf_idf_vector = []
#
#     # Calculer le nombre total de mots dans la question
#     total_words_in_question = len(question_tokens)
#
#     # Calculer le TF pour chaque mot de la question
#     for word in idf_scores.keys():
#         tf2 = question_tokens.count(word) / total_words_in_question
#
#         # Calculer le score TF-IDF pour le mot en multipliant TF par IDF
#         tf_idf = tf2 * idf_scores[word]
#         tf_idf_vector.append(tf_idf)
#
#     return tf_idf_vector


#4


# def norme_vecteur(vecteur):
#     # Calculer la norme (longueur) du vecteur
#     return math.sqrt(sum(x ** 2 for x in vecteur))
#
#
# def cosine_similarity(vecteur_a, vecteur_b):
#     # Calculer le produit scalaire entre les vecteurs A et B
#     produit_scalaire = sum(x * y for x, y in zip(vecteur_a, vecteur_b))
#
#     # Calculer la norme du vecteur B
#     norme_b = norme_vecteur(vecteur_b)
#
#     # Vérifier si le dénominateur est nul
#     if norme_b == 0:
#         return "Le calcul est impossible car le dénominateur est nul."
#
#     # Calculer la norme du vecteur A
#     norme_a = norme_vecteur(vecteur_a)
#
#     # Calculer la similarité cosinus
#     similarity = produit_scalaire / (norme_a * norme_b)
#
#     return similarity















