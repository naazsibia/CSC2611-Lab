from gensim.models import KeyedVectors
import nltk
nltk.download('brown')
from nltk.corpus import brown
from nltk.probability import FreqDist


def filter_analogy_tests(filename, word2vec_model, lsa_vocab):
    """
    Filter the analogy questions in the provided file to include only those where all words
    are present in the given vocabularies.

    :param filename: The path to the original analogy test file.
    :param word2vec_model: The loaded word2vec model.
    :param lsa_vocab: The vocabulary set of the LSA model.
    :return: A list of filtered analogy questions.
    """
    
    filtered_questions = []
    
    with open(filename, 'r') as f:
        for line in f:
            # Skip lines that are section headers (e.g., ": capital-common-countries")
            if line.startswith(":"):
                filtered_questions.append(line)
                continue
            
            a, a_star, b, b_star = line.lower().strip().split()
            # Check if all words are in both vocabularies
            if all(word in word2vec_model for word in [a, a_star, b, b_star]) and all(word in lsa_vocab for word in [a, a_star, b, b_star]):
                filtered_questions.append(line)
    
    return filtered_questions


if __name__ == '__main__':
    words_lower = [word.lower() for word in brown.words()] # ignore case
    fdist = FreqDist(words_lower)
    top5000 = fdist.most_common(5000)
    W = top5000.copy()
    # words from RG65
    words = [
        "cord", "rooster", "noon", "fruit", "autograph", "automobile", "mound", "grin", "asylum",
        "asylum", "graveyard", "glass", "boy", "cushion", "monk", "asylum", "coast", "grin", 
        "shore", "monk", "boy", "automobile", "mound", "lad", "forest", "food", "cemetery", 
        "shore", "bird", "coast", "furnace", "crane", "smile", "voyage", "string", "furnace", 
        "shore", "wizard", "stove", "implement", "fruit", "monk", "madhouse", "magician", 
        "rooster", "jewel", "slave", "cemetery", "forest", "lad", "woodland", "oracle", "sage", 
        "cushion", "shore", "wizard", "graveyard", "rooster", "woodland", "voyage", "woodland", 
        "hill", "implement", "hill", "car", "cemetery", "glass", "magician", "crane", "brother", 
        "sage", "oracle", "bird", "bird", "food", "brother", "asylum", "furnace", "magician", 
        "hill", "cord", "glass", "grin", "serf", "journey", "autograph", "coast", "forest", 
        "implement", "cock", "boy", "cushion", "cemetery", "automobile", "midday", "gem", 
        "woodland", "journey", "mound", "jewel", "oracle", "implement", "lad", "wizard", "sage", 
        "crane", "cock", "fruit", "monk", "madhouse", "stove", "wizard", "mound", "string", 
        "tumbler", "smile", "slave", "voyage", "signature", "shore", "woodland", "tool", 
        "rooster", "lad", "pillow", "graveyard", "car", "noon", "jewel"]

    fdist = FreqDist(words)
    words_freq = list(fdist.items())
    existing_words = set([word[0] for word in W])

    # Trying not to add duplicates
    for word in words_freq:
        if word[0] not in existing_words:
            W.append(word)
    W = sorted(W, key=lambda x: x[1])
    W = [word[0] for word in W]

    lsa_vocab = set(W)
    word2vec_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

    filtered_semantic = filter_analogy_tests('semantic-test.txt', word2vec_model, lsa_vocab)
    with open('filtered-semantic-test.txt', 'w') as f:
        f.writelines(filtered_semantic)

    filtered_syntactic = filter_analogy_tests('syntactic-test.txt', word2vec_model, lsa_vocab)
    with open('filtered-syntactic-test.txt', 'w') as f:
        f.writelines(filtered_syntactic)

    print(f"Filtered semantic analogies: {len(filtered_semantic)}")
    print(f"Filtered syntactic analogies: {len(filtered_syntactic)}")
