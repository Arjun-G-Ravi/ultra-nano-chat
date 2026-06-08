from collections import Counter


def format_token(token):
    return token.encode('unicode_escape').decode('ascii')

with open('data/validation.txt') as f:
    text = f.read()

text = text[:1000]
tokens = text.encode('utf-8')
tokens = list(map(int, tokens))
# print(tokens)
vocab = {chr(i):i for i in range(32, 127)} # basic characters
vocab_ct = 127
# print('\nvocab', vocab, '\n')

vocab_size = 256

while vocab_ct < vocab_size:
    combined_tokens = []
    for i in range(len(tokens)-1):
        combined_tokens.append(f'{tokens[i]}_{tokens[i+1]}')
    counter = Counter(combined_tokens)
    ch1, ch2 = str(counter.most_common(1)[0][0]).split('_')
    # print(ch1,ch2)
    vocab[f'{chr(int(ch1))}{chr(int(ch2))}'] = vocab_ct

    l1 = len(tokens)

    index_to_pop = []
    for i in range(len(tokens)-1):
        # print(tokens[i], ch1)
        if tokens[i] == int(ch1) and tokens[i+1] == int(ch2):
            tokens[i] = vocab_ct
            index_to_pop.append(i+1)
    for i in index_to_pop[::-1]:
        tokens.pop(i)
    l2 = len(tokens)

    vocab_ct += 1
    print()
    print(vocab)
    assert l1 == int(counter.most_common(1)[0][1])+l2, 'wrong count'

with open('out/tokenizeer.txt', 'w') as f:
    for token, idx in sorted(vocab.items(), key=lambda item: item[1]):
        f.write(f'{idx}: {format_token(token)}\n')
