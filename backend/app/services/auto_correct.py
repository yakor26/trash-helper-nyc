from spellchecker import SpellChecker
from pathlib import Path
import pandas as pd
import string

spell = SpellChecker()
directory = Path(__file__).parent


def create_word_list():
    """ Builds a word list from NYC item category descriptions and write it to item_categories.txt.,
    strips punctuation, set lowercase, deduplicates them, and to item_categories.txt for spellchecker
    """
    descriptions = pd.read_csv(f"{directory.parent}/utils/NYCItemCategoriesV3.csv")[["description"]].values.tolist()
    words_set = set()
    for row in descriptions:
        filtered_text = "".join(filter(lambda x: x not in string.punctuation, str(row))).split(" ")
        [words_set.add(x.lower()) for x in filtered_text]

    with open(f"{directory}/item_categories.txt", "a") as text_file:
        for word in words_set:
            text_file.write(f"{word}\n")


def spell_correct(search_entry: str) -> str | None:
    """ Return a spell corrected version of entry"""
    search_entry = search_entry.strip()
    print(search_entry)
    if len(search_entry) == 0:
        return None
    # load item categories from csv
    spell.word_frequency.load_text_file(f"{directory}/item_categories.txt")
    corrected = " ".join([spell.correction(word) for word in search_entry.split(" ")])
    return corrected


def main():
    spell_correct("perfuume botttle")


if __name__ == "__main__":
    main()
