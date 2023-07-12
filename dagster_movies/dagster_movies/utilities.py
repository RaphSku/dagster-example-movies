import pandas as pd


def convert_to_list(x: str) -> list[str]:
    result = []
    term = False
    word = ""
    for char in x:
        if char == "'" and term == False:
            term = True
            continue
        elif char == "'" and term == True:
            result.append(word)
            word = ""
            term = False
        if term == True:
            word += char

    return result

def count_words_in_series(x: pd.Series) -> dict:
    counter = {}
    for elements in x:
        for element in elements:
            if not element in counter:
                counter[element] = 1
                continue
            counter[element] += 1
    
    return counter