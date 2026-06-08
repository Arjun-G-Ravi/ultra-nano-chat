import torch
import pandas
from collections import Counter

with open('data/validation.txt') as f:
    text = f.read()

text = text[:100]
tokens = text.encode('utf-8')
tokens = list(map(int, tokens))
# print(tokens)
vocab = {chr(i):i for i in range(32, 127)} # basic characters
vocab_ct = 127
# print('\nvocab', vocab, '\n')

vocab_size = 1024

while vocab_ct < vocab_size:
    combined_tokens = []
    for i in range(len(tokens)-1):
        combined_tokens.append(f'{tokens[i]}_{tokens[i+1]}')
    counter = Counter(combined_tokens)
    ch1, ch2 = str(counter.most_common(1)[0][0]).split('_')
    # print(ch1,ch2)
    vocab[f'{chr(int(ch1))}{chr(int(ch2))}'] = vocab_ct
    vocab_ct += 1

    print(vocab)





    break

        


