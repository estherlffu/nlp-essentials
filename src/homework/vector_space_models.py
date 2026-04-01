from typing import TypeAlias
import math
from collections import Counter

# Load data
def load_data(filepath: str) -> list[tuple[int,Document]]:
    docs = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            label, text = line.split('\t', 1) # Split by \t
            tokens = text.split()
            docs.append((int(label), tokens))
    return docs

# Bag of words
Document: TypeAlias = list[str]
Vocab: TypeAlias = dict[str,int]

def vocabulary(documents: list[Document]) -> Vocab:
    vocab = set()

    for document in documents:
        vocab.update(document)

    return {word: i for i, word in enumerate(sorted(list(vocab)))}

def bag_of_words(vocab: Vocab, document: Document) -> SparseVector:
    counts = Counter(document)
    return {vocab[word]: count for word, count in sorted(counts.items()) if word in vocab}

# TF-IDF
def document_frequencies(vocab: Vocab, corpus: list[Document]) -> SparseVector:
    counts = Counter()
    for document in corpus:
        counts.update(set(document))
    return {vocab[word]: count for word, count in sorted(counts.items()) if word in vocab}

def tf_idf(vocab: Vocab, dfs: SparseVector, D: int, document: Document) -> SparseVector:
    tf = lambda count: count / len(document);
    idf = lambda tid: math.log(D / dfs[tid]);
    return {tid: tf(count) * idf(tid) for tid, count in bag_of_words(vocab, document).items() if tid in dfs}

# Cosine similarity
def cosine_similarity(v1: SparseVector, v2: SparseVector) -> float:
    n = sum(v * v2.get(k,0) for k, v in v1.items())
    d = math.sqrt(sum(v ** 2 for k, v in v1.items()))
    d *= math.sqrt(sum(v ** 2 for k, v in v2.items()))
    return n / d

# k-nearest neighbors
def knn(trn_vs: list[tuple[int, SparseVector]], v: SparseVector, k: int = 1) -> tuple[int,float]:
    sims = [(label, cosine_similarity(v, t)) for label, t in trn_vs]
    sims.sort(key=lambda x: x[1], reverse=True)
    predicted_label = Counter(label for label, _ in sims[:k]).most_common(1)[0][0]
    top_sim = sims[0][1]
    return predicted_label, top_sim

def sentiment_analyzer(train_docs, test_docs):

    k = 117 # accuracy: 0.4042

    train_labels = [label for label, _ in train_docs]
    train_tokens = [tokens for _, tokens in train_docs]
    test_tokens = [tokens for _, tokens in test_docs]

    # Training vocab
    vocab = vocabulary(train_tokens)

    # Bag of words, document frequency
    frequencies = document_frequencies(vocab, train_tokens)
    D = len(train_tokens) # total number of training docs

    # TF-IDF
    train_vectors = [(label, tf_idf(vocab, frequencies, D, doc)) for label, doc in zip(train_labels, train_tokens)]
    test_vectors = [tf_idf(vocab, frequencies, D, doc) for doc in test_tokens]

    # Cosine similarity, k-nearest neighbors
    return [knn(train_vectors, v, k) for v in test_vectors]

# print(sentiment_analyzer(train_docs, test_docs))

'''
# Finding optimal k
def evaluate_predictions(predictions, test_docs):
    test = [label for label, _ in test_docs]
    pred = [label for label, _ in predictions]

    correct = sum(g == p for g, p in zip(test, pred))
    accuracy = correct / len(test)

    return accuracy

train_docs = load_data("/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/sst_trn.tsv")
test_docs = load_data("/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/sst_dev.tsv")

predictions = sentiment_analyzer(train_docs, test_docs)
accuracy = evaluate_predictions(predictions, test_docs)
print(accuracy)

for k in range(161, 181):
    predictions = sentiment_analyzer(train_docs, test_docs, k=k)
    accuracy = evaluate_predictions(predictions, test_docs)
    print(f"k={k}: accuracy={accuracy:.4f}")
'''

from string import punctuation

def cosine_similarity_extra(v1: SparseVector, v2: SparseVector) -> float:
    n = sum(v * v2.get(k, 0) for k, v in v1.items())
    d1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    d2 = math.sqrt(sum(v ** 2 for v in v2.values()))

    if d1 == 0 or d2 == 0:
        return 0.0

    return n / (d1 * d2)

def knn_extra(trn_vs: list[tuple[int, SparseVector]], v: SparseVector, k: int = 1) -> tuple[int, float]:
    sims = [(label, cosine_similarity_extra(v, t)) for label, t in trn_vs]
    sims.sort(key=lambda x: x[1], reverse=True)
    predicted_label = Counter(label for label, _ in sims[:k]).most_common(1)[0][0]
    top_sim = sims[0][1]

    return predicted_label, top_sim

def sentiment_analyzer_extra(train_docs: list[tuple[int,Document]], test_docs: list[tuple[int,Document]]) -> list[tuple[int,float]]:

    k = 117

    # Add stopwords
    stopwords = {line.strip().lower() for line in open('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/stopwords.txt')}
    is_stopwords = lambda w: w.lower() in stopwords or w in punctuation

    # Bigram
    def bigram(document: Document) -> Document:
        bigrams = [f"{document[i - 1]} {document[i]}" for i in range(1, len(document))]
        return document + bigrams

    # Tokenizer
    def tokenize(document: Document) -> Document:
        tokens = []

        for token in document:
            token = token.lower()
            token = ''.join(c for c in token if c.isalnum())
            if token and not is_stopwords(token):
                tokens.append(token)

        return bigram(tokens)

    train_labels = [label for label, _ in train_docs]
    train_tokens = [tokenize(tokens) for _, tokens in train_docs]
    test_tokens = [tokenize(tokens) for _, tokens in test_docs]

    # Training vocab
    vocab = vocabulary(train_tokens)

    # Bag of words, document frequency
    frequencies = document_frequencies(vocab, train_tokens)
    D = len(train_tokens)  # total number of training docs

    # TF-IDF
    train_vectors = [(label, tf_idf(vocab, frequencies, D, doc)) for label, doc in zip(train_labels, train_tokens)]
    test_vectors = [tf_idf(vocab, frequencies, D, doc) for doc in test_tokens]

    # Cosine similarity, k-nearest neighbors
    return [knn_extra(train_vectors, v, k) for v in test_vectors]

'''
# Evaluate improved sentiment analyzer
def evaluate_predictions(predictions, test_docs):
    test = [label for label, _ in test_docs]
    pred = [label for label, _ in predictions]

    correct = sum(g == p for g, p in zip(test, pred))
    accuracy = correct / len(test)

    return accuracy
 
train_docs = load_data("/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/sst_trn.tsv")
test_docs = load_data("/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/sst_dev.tsv")

predictions = sentiment_analyzer_extra(train_docs, test_docs)
accuracy = evaluate_predictions(predictions, test_docs)
print(accuracy)

for k in range(30,36):
    predictions = sentiment_analyzer_extra(train_docs, test_docs, k=k)
    accuracy = evaluate_predictions(predictions, test_docs)
    print(f"k={k}: accuracy={accuracy:.4f}")
'''
