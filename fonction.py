import os
import re
from typing import Dict
import string
from collections import Counter
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

# Minuscule
#https://docs.python.org/3/library/re.html
#https://www.w3schools.com/python/python_regex.asp
#https://www.geeksforgeeks.org/python-regex/

def clean_line(line):
    cleaned_line = line.replace("'", " ")
    cleaned_line = cleaned_line.translate(str.maketrans("", "", string.punctuation))
    return cleaned_line

def convert_to_lowercase_and_clean(file_path, output_folder, new_file_name):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = [clean_line(line.lower()) for line in lines]

    cleaned_file_path = os.path.join(output_folder, new_file_name)
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
    word_occurrences_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            cleaned_line = clean_line(line)
            words_in_line = cleaned_line.split()

            word_count = Counter(words_in_line)

            for word, count in word_count.items():
                if word in word_occurrences_dict:
                    word_occurrences_dict[word] += count
                else:
                    word_occurrences_dict[word] = count

    return word_occurrences_dict

#IDFtf premier essaie

# def calculate_idf(corpus_directory):
#     tf_scores[filename] = {word: words_in_line.count(word) / len(words_in_line) if len(words_in_line) > 0 else 0 for
#                            word in unique_words_in_document}
#
#     document_frequency = Counter()
#     total_documents = 0
#
#     for filename in os.listdir(corpus_directory):
#         if filename.endswith(".txt"):
#             total_documents += 1
#
#             file_path = os.path.join(corpus_directory, filename)
#             unique_words_in_document = set()
#
#             with open(file_path, 'r', encoding="utf-8") as file:
#                 for line in file:
#                     cleaned_line = clean_line(line.lower())
#                     words_in_line = cleaned_line.split()
#                     unique_words_in_document.update(words_in_line)
#
#             tf_scores[filename] = {word: words_in_line.count(word) / len(words_in_line) if len(words_in_line) > 0 else 0 for word in unique_words_in_document}
#             document_frequency.update(unique_words_in_document)
#
#     idf_scores = {word: math.log(1 + (total_documents / (document_frequency[word]))) for word in document_frequency}


    # tf_idf_scores = {document: {word: tf_scores[document][word] * idf_scores[word] for word in tf_scores[document]} for document in tf_scores}
    # return tf_idf_scores


#TF*idf soit TF-IDF
# def calculate_tf_idf(corpus_directory):
#     document_frequency = Counter()
#     total_documents = 0
#     tf_scores = {}
#
#     for filename in os.listdir(corpus_directory):
#         if filename.endswith(".txt"):
#             total_documents += 1
#
#             file_path = os.path.join(corpus_directory, filename)
#             unique_words_in_document = set()
#
#             with open(file_path, 'r', encoding="utf-8") as file:
#                 for line in file:
#                     cleaned_line = clean_line(line.lower())
#                     words_in_line = cleaned_line.split()
#                     unique_words_in_document.update(words_in_line)
#
#             # Assurez-vous de déclarer unique_words_in_document ici
#             tf_scores[filename] = {word: words_in_line.count(word) / len(words_in_line) if len(words_in_line) > 0 else 0 for word in unique_words_in_document}
#             document_frequency.update(unique_words_in_document)
#
#     idf_scores = {word: math.log10(1 + (total_documents / (document_frequency[word]))) for word in document_frequency}
#
#
#     tf_idf_scores = {document: {word: tf_scores[document][word] * idf_scores[word] for word in tf_scores[document]} for document in tf_scores}
#     return tf_idf_scores

def clean_line(line):
    cleaned_line = line.replace("'", " ")
    cleaned_line = cleaned_line.translate(str.maketrans("", "", string.punctuation))
    return cleaned_line

def calculate_idf(corpus_directory):

    document_frequency = {}
    total_documents = 0

    for filename in os.listdir(corpus_directory):
        if filename.endswith(".txt"):
            total_documents += 1

            file_path = os.path.join(corpus_directory, filename)
            unique_words_in_document = set()

            with open(file_path, 'r', encoding="utf-8") as file:
                for line in file:
                    cleaned_line = clean_line(line.lower())
                    words_in_line = cleaned_line.split()
                    unique_words_in_document.update(words_in_line)

            for word in unique_words_in_document:
                document_frequency[word] = document_frequency.get(word, 0) + 1

    idf_scores = {word: (math.log10(total_documents / document_frequency[word])) for word in document_frequency}
    return idf_scores

def calculate_idf_tf(corpus_directory):
    document_frequency = Counter()
    total_documents = 0
    tf_scores = {}

    for filename in os.listdir(corpus_directory):
        if filename.endswith(".txt"):
            total_documents += 1

            file_path = os.path.join(corpus_directory, filename)
            unique_words_in_document = set()

            with open(file_path, 'r', encoding="utf-8") as file:
                for line in file:
                    cleaned_line = clean_line(line)
                    words_in_line = cleaned_line.split()
                    unique_words_in_document.update(words_in_line)

                # Calcul du score TF pour chaque mot dans le document
                tf_scores[filename] = {word: words_in_line.count(word) / len(words_in_line) if len(words_in_line) > 0 else 0 for word in unique_words_in_document}

                # Mise à jour de la fréquence des termes dans tous les documents
                document_frequency.update(unique_words_in_document)

    # Calcul du score IDF pour chaque mot
    idf_scores = {word: math.log10((total_documents / (document_frequency[word]))) for word in document_frequency}

    # Calcul du score TF-IDF pour chaque document
    tf_idf_scores = {document: {word: tf_scores[document][word] * idf_scores[word] for word in tf_scores[document]} for document in tf_scores}

    return idf_scores, tf_idf_scores


#Matrice

def generate_tfidf_matrix(corpus_directory):
    idf_scores = calculate_idf(corpus_directory)
    unique_words = sorted(idf_scores.keys())

    tfidf_matrix = []

    for filename in os.listdir(corpus_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_directory, filename)

            try:
                with open(file_path, 'r', encoding="utf-8") as file:
                    cleaned_lines = [clean_line(line.lower()) for line in file]
                    words_in_document = ' '.join(cleaned_lines).split()

                    if len(words_in_document) > 0:
                        tfidf_row = [0] * len(unique_words)
                        for i in range(len(unique_words)):
                            word = unique_words[i]
                            score = idf_scores[word] * words_in_document.count(word) / len(words_in_document)
                            tfidf_row[i] = round(score, 2)
                        tfidf_matrix.append(tfidf_row)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return tfidf_matrix

#Transposition de la matrice

def transpose_matrix(matrix):

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    transposed_matrix = [[0] * num_rows for _ in range(num_cols)]

    for i in range(num_rows):
        for j in range(num_cols):
            transposed_matrix[j][i] = matrix[i][j]

    return transposed_matrix

def print_tfidf_matrix(matrix):
    for row in matrix:
        print(row)

#Les mots les moins importants en score

def find_unimportant_words(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
    unimportant_words = set()

    # Parcourir chaque mot dans le premier document
    first_document = list(tf_idf_scores.keys())[0]
    for word in tf_idf_scores[first_document]:
        # Vérifier si le mot est présent dans tous les documents et si le score TF-IDF est égal à zéro
        if all(word in tf_idf_scores[filename] and tf_idf_scores[filename][word] == 0 for filename in tf_idf_scores):
            unimportant_words.add(word)

    return unimportant_words

# Mot important en score

from typing import Dict

def find_most_important_words(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
    most_important_words = set()

    for filename, scores in tf_idf_scores.items():
        max_score = max(scores.values())
        most_important_words.update(word for word, score in scores.items() if score == max_score)

    return most_important_words

# Mot moins important
def find_unimportant_words(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
    unimportant_words = set()

    first_document = list(tf_idf_scores.keys())[0]
    for word in tf_idf_scores[first_document]:
        if all(word in tf_idf_scores[filename] and tf_idf_scores[filename][word] == 0 for filename in tf_idf_scores):
            unimportant_words.add(word)

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
                print(f"Warning: File not found: {file_path}. Skipping.")

    max_count = max(all_occurrences.values())
    common_words.update(word for word, count in all_occurrences.items() if count == max_count)

    return common_words

# Nation

def load_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

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

    presidents = os.listdir(directory_path)

    for president in presidents:
        file_path = os.path.join(directory_path, president)
        if president.endswith(".txt"):
            text = load_text(file_path)
            mentions_by_president[president] = text.lower().split().count("nation")

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
            text = load_text(file_path)
            if detect_climate_ecology(text):
                return president.split(".")[0]

    return None


# Par tous les présidents

from typing import Dict

def find_common_words_except_unimportant(tf_idf_scores: Dict[str, Dict[str, float]]) -> set:
    unimportant_words = find_unimportant_words(tf_idf_scores)
    first_document = list(tf_idf_scores.keys())[0]
    common_words_except_unimportant = set()

    for word in tf_idf_scores[first_document]:
        if word not in unimportant_words and all(word in tf_idf_scores[filename] for filename in tf_idf_scores):
            common_words_except_unimportant.add(word)

    return common_words_except_unimportant









