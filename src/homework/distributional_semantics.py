# Task 1
import numpy as np

def read_word_embeddings(path: str) -> dict[str, np.array]:
    embeddings = {}
    with open(path, 'r') as f:
        for line in f:
            items = line.split('\t')
            embeddings[items[0]] = np.array([float(x) for x in items[1:]])

    return embeddings

# Test for task 1
read_word_embeddings('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/word_embeddings.txt')