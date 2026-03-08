#!/usr/bin/env python3
import sys
import os
import json
from collections import Counter

import numpy as np
import nltk
nltk.download('averaged_perceptron_tagger_eng')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag, RegexpParser
from sklearn.cluster import AgglomerativeClustering

stop_words = set(stopwords.words("english"))

# --- Classification ---

categories = {
    "science":    {"physics", "experiment", "theory", "model", "data"},
    "politics":   {"government", "policy", "state", "election", "law"},
    "technology": {"software", "computer", "algorithm", "network", "system"},
    "economics":  {"market", "price", "capital", "trade", "production"},
}

def classify(tokens):
    counts = Counter(tokens)
    scores = {cat: sum(counts[w] for w in kw) for cat, kw in categories.items()}
    return "unknown" if max(scores.values()) == 0 else max(scores, key=scores.get)

def process_file(path):
    text = open(path, encoding="utf8").read().lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return classify(tokens)

# --- Phrase extraction ---

grammar  = r"NP: {<JJ>*<NN.*>+}"
chunker  = RegexpParser(grammar)

def extract_phrases(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tagged = pos_tag(tokens)
    tree   = chunker.parse(tagged)
    return [
        " ".join(w for w, _ in subtree.leaves())
        for subtree in tree.subtrees()
        if subtree.label() == "NP"
    ]

# --- Vectorisation ---

def vectorize(docs):
    vocab = {}
    for doc in docs:
        for phrase in doc:
            if phrase not in vocab:
                vocab[phrase] = len(vocab)
    matrix = np.zeros((len(docs), len(vocab)))
    for i, doc in enumerate(docs):
        for phrase, count in doc.items():
            matrix[i, vocab[phrase]] = count
    return matrix, vocab

# --- Clustering ---

def hierarchical_clusters(matrix, n_clusters=8):
    return AgglomerativeClustering(n_clusters=n_clusters, linkage="ward").fit_predict(matrix)

def summarize_clusters(docs, labels, vocab, top_k=10):
    clusters = {}
    for i, label in enumerate(labels):
        clusters.setdefault(label, []).append(docs[i])
    return {
        label: Counter(w for doc in members for w in doc).most_common(top_k)
        for label, members in clusters.items()
    }

# --- Persistence ---

def save_index(names, labels, summaries, outdir):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "documents.json"), "w") as f:
        json.dump({name: int(label) for name, label in zip(names, labels)}, f, indent=2)
    with open(os.path.join(outdir, "cluster_summaries.json"), "w") as f:
        json.dump(
            {str(k): v for k, v in summaries.items()},
            f, indent=2,
        )

# --- Entry points ---
TEXT_EXT = {".txt", ".md", ".tex", ".rst", ".html"}

def load_corpus(corpus_dir):
    docs, names = [], []

    for fname in sorted(os.listdir(corpus_dir)):
        path = os.path.join(corpus_dir, fname)

        if not os.path.isfile(path):
            continue

        ext = os.path.splitext(fname)[1].lower()
        if ext not in TEXT_EXT:
            continue

        try:
            with open(path, encoding="utf8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print("Skipping:", fname, e)
            continue

        phrases = extract_phrases(text)
        docs.append(Counter(phrases))
        names.append(fname)

    return docs, names

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Single-file classification mode
        print(process_file(sys.argv[1]))
    elif len(sys.argv) == 3:
        # Corpus clustering mode
        corpus, outdir = sys.argv[1], sys.argv[2]
        docs, names    = load_corpus(corpus)
        matrix, vocab  = vectorize(docs)
        labels         = hierarchical_clusters(matrix)
        summaries      = summarize_clusters(docs, labels, vocab)
        save_index(names, labels, summaries, outdir)
    else:
        print("Usage:")
        print("  pipeline.py <file>              # classify a single file")
        print("  pipeline.py <corpus> <outdir>   # cluster a corpus directory")
        sys.exit(1)