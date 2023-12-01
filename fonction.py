import os
import re
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

import os
import re
import string

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

#TF

from collections import Counter
import os

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

#IDF

import math
from collections import Counter

def calculate_idf(corpus_directory):
    # Compteur pour stocker le nombre de documents dans lesquels chaque mot apparaît
    document_frequency = Counter()

    # Nombre total de documents dans le corpus
    total_documents = 0

    # Parcourez tous les fichiers dans le répertoire du corpus
    for filename in os.listdir(corpus_directory):
        if filename.endswith(".txt"):
            total_documents += 1

            file_path = os.path.join(corpus_directory, filename)

            # Utilisez un ensemble pour éviter de compter plusieurs fois le même mot dans un document
            unique_words_in_document = set()

            with open(file_path, 'r') as file:
                for line in file:
                    cleaned_line = clean_line(line.lower())
                    words_in_line = cleaned_line.split()
                    unique_words_in_document.update(words_in_line)

            # Mettez à jour le compteur de fréquence des documents pour chaque mot unique dans ce document
            document_frequency.update(unique_words_in_document)

    # Calcul du score IDF pour chaque mot
    idf_scores = {word: math.log(1 +(total_documents / (document_frequency[word]))) for word in document_frequency}

    return idf_scores

# Exemple d'utilisation :
corpus_directory = "./cleaned"  # Remplacez par votre répertoire de corpus
idf_scores = calculate_idf(corpus_directory)

# Affichez les scores IDF pour chaque mot
for word, idf_score in idf_scores.items():
    print(f"Mot : {word}, Score IDF : {idf_score}")




