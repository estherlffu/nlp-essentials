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
embeddings = read_word_embeddings('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/word_embeddings.txt')
# print(embeddings)

# Task 2
def similar_words(embeddings: dict[str, np.array], target: str, threshold: float) -> list[tuple]:
    target_vector = embeddings[target]
    results = []

    for word, vector in embeddings.items():
        if word == target:
            continue
        cosine_similarity = np.dot(target_vector, vector) / np.linalg.norm(target_vector) * np.linalg.norm(vector)
        if cosine_similarity >= threshold: # return only if >= threshold
            results.append((word, cosine_similarity)) # return tuple with target word and cosine sim

    return sorted(results, key=lambda x: x[1], reverse=True)

# Test for task 2
# print(similar_words(embeddings, target='sugar', threshold=0.8))

# Task 3
def document_similarity(embeddings: dict[str, np.array], doc1: str, doc2: str) -> float:
    def document_embedding(doc):
        vectors = [embeddings[word] for word in doc.split() if word in embeddings]
        return np.mean(vectors, axis=0) # Used Claude to average across rows

    vector1 = document_embedding(doc1)
    vector2 = document_embedding(doc2)

    cosine_sim = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

    return cosine_sim

# Test for task 3
# print(document_similarity(embeddings, 'I love Friday', 'I love Saturday'))
# print(document_similarity(embeddings, 'I love soda', 'I love sugar'))
# print(document_similarity(embeddings, 'I hate baseball', 'I love muffins'))