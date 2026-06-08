import torch
import pandas

with open('data/validation.txt') as f:
    text = f.read()

print(text[:100])

vocab = {chr(i) for i in range(32, 127)} # basic characters
# print(vocab)

vocab_size = 1024

while len(vocab) < vocab_size:
    pass 