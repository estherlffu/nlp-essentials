from collections import Counter, defaultdict
from typing import TypeAlias
import math
import string

# Define unigram and bigram type
Unigram: TypeAlias = dict[str, float]
Bigram: TypeAlias = dict[str, Unigram | float]

UNKNOWN = '' # unknown probabilities
INIT = '[INIT]' # initial probabilities

# Task 1: Bigram Modeling
def bigram_model(text_file):

    # Get bigram counts
    counts = defaultdict(Counter)

    for line in open(text_file):
        words = [INIT] + line.split() # INIT token to precede first word of each line
        for i in range(1, len(words)):
            counts[words[i - 1]].update([words[i]])

    # Return vocab with bigram smoothing
    vocab = set(counts.keys())
    for _, css in counts.items():
        vocab.update(css.keys())
    vocab.discard(INIT) # Need to remove, used Claude to check logic
    vocab.add(UNKNOWN) # Need to add bc it can be key for current word

    bigrams = dict()
    for prev, ccs in counts.items():
        vi = len(ccs) + 1 # to normalize bigram distribution, add 1 to account for UNKNOWN key
        total = sum(ccs.values()) + vi
        d = {curr: (count + 1) / total for curr, count in ccs.items()}
        d[UNKNOWN] = 1 / total
        bigrams[prev] = d

    bigrams[UNKNOWN] = 1 / len(vocab)

    return bigrams

# Test for task 1, used Claude to generate top 10 words that start each line
# if __name__ == '__main__':
    # bigrams = bigram_model('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/chronicles_of_narnia.txt')

    # print(INIT)
    # bigram_list = [(curr, prob) for curr, prob in sorted(bigrams[INIT].items(), key=lambda x: x[1], reverse=True)]
    # for curr, prob in bigram_list[:10]:
        # print(f'{curr:>10} {prob:.6f}')

# Task 2: Sequence Generation
def sequence_generator(model, in_word, length):
    output = [in_word]
    max_punctuation = length // 5  # floor of length / 5
    punctuation_count = 0
    log_likelihood = 0.0

    # Check if word in bigram output
    if in_word not in model:
        return output, log_likelihood

    while len(output) < length:
        prev_word = output[-1]
        distr = model[prev_word]

        # Sort distribution items and take highest prob
        sorted_distr = sorted(distr.items(), key=lambda item: item[1], reverse=True) # Pycharm autofilled

        add_word = None
        word_prob = None

        # Iterate through sorted distribution and take top word that fulfills conditions
        for word, prob in sorted_distr:
            if word == UNKNOWN:
                continue # ensures word is a real token
            if (word in string.punctuation) and punctuation_count >= max_punctuation: # Used Claude to for string.punctuation check function
                continue # ensures punctuation count rule pass
            if (word not in string.punctuation) and word in output:
                continue # ensures no word redundancy
            add_word = word
            word_prob = prob
            break

        # If there is no valid word to add, break while loop
        if add_word is None:
            break

        if add_word in string.punctuation:
            punctuation_count += 1
        log_likelihood += math.log(word_prob)

        output.append(add_word)

    return output, log_likelihood

# Test for task 2
# bigrams = bigram_model('/Users/esther/Documents/Emory/Classes/2026 Spring/cs329/nlp-essentials/dat/chronicles_of_narnia.txt')
# sentence, log_likelihood = sequence_generator(bigrams, 'Jill', 30)
# print(sentence)
# print(log_likelihood)

# Used Claude to check
# for i in range(len(sentence) - 1):
    # prev = sentence[i]
    # next_word = sentence[i + 1]
    # prob = bigrams[prev][next_word]
    # print(f'{prev} -> {next_word}: {prob:.6f}')