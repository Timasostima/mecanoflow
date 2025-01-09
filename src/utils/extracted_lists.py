import pandas as pd
import random
import duckdb


def read_language_list(language):
    dfs = pd.read_excel(f'res/language_lists/{language}-word-list-total.xls')
    temp = dfs.iloc[:, 0].dropna().tolist()
    return temp


english = read_language_list('english')
french = read_language_list('french')
german = read_language_list('german')
spanish = read_language_list('spanish')
italian = read_language_list('italian')
russian = read_language_list('russian')


def get_language_list(language):
    match language:
        case 'english':
            word_list = english
        case 'french':
            word_list = french
        case 'german':
            word_list = german
        case 'spanish':
            word_list = spanish
        case 'italian':
            word_list = italian
        case 'russian':
            word_list = russian
        case _:
            word_list = None

    if word_list is not None:
        random.shuffle(word_list)
    return word_list


def get_translations(language):
    return duckdb.execute("SELECT * FROM 'res/translations.csv' WHERE Key = ?", [language.capitalize()]).fetchone()
