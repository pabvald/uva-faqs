#!/usr/bin/env python
# coding: utf-8

# Imports
import json
import spacy
import numpy as np 
import sys, getopt

def sentence_embedding(sentences):
    """ Computes the embeddings of a list of sentences, omitting 
        stop_words and punctuation symbols """
    nlp = spacy.load("en_core_web_lg")
    sentence_embeddings = []
    
    for doc in nlp.pipe(sentences, disable=["tagget", "parser", "ner"]):    
        tokens = list(filter(lambda t: t.has_vector and (not t.is_punct) and (not t.is_stop), doc.doc)) 
        vectors = list(map(lambda t: t.vector, tokens))
        embedding = np.average(vectors, axis=0)
        sentence_embeddings.append(embedding)
        
    
    return np.array(sentence_embeddings)


def save_as_json(file_name, data):
    """ Saves the provided data as a json file """
    with open(file_name, 'w', encoding='utf8') as fout:
        json.dump(data , fout, indent=4, sort_keys=True, ensure_ascii=False)


def read_json(file_name):
    """ Reads a json file and returns it content """
    with open(file_name, 'r', encoding='utf8') as file:
        data = json.load(file)
    
    return data


def main(argv):
    """ MAIN """ 
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('add_embeddings -i <input_file.json> -o <output_file.json>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('add_embeddings -i <input_file.json> -o <output_file.json>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    qa_pairs = read_json(input_file)
    questions = list(map(lambda pair: pair['question'].lower(), qa_pairs))
    q_embeddings = sentence_embedding(questions)

    # Add embeddings
    for i in range(len(qa_pairs)):
        pair = qa_pairs[i]
        pair['embedding'] = q_embeddings[i].tolist()

    # Save QA pairs with embeddings
    save_as_json(output_file, qa_pairs)

if __name__ == '__main__':
    main(sys.argv[1:])