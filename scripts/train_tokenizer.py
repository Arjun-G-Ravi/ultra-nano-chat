import json
from collections import Counter

with open("data/validation.txt", encoding="utf-8") as f:
    text = f.read()

text = text[:1000]
tokens = list(text)
vocab = {}

for ch in tokens:
    if ch not in vocab:
        vocab[ch] = ord(ch)

print(vocab)
vocab_ct = max(vocab.values(), default=-1) + 1
print(vocab_ct)
vocab_size = 256

while vocab_ct < vocab_size and len(tokens) > 1:
    combined_tokens = [(tokens[i], tokens[i + 1]) for i in range(len(tokens) - 1)]
    counter = Counter(combined_tokens)
    (ch1, ch2), pair_count = counter.most_common(1)[0]
    merged_token = f"{ch1}{ch2}"
    vocab[merged_token] = vocab_ct

    l1 = len(tokens)
    merged_tokens = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and tokens[i] == ch1 and tokens[i + 1] == ch2:
            merged_tokens.append(merged_token)
            i += 2
        else:
            merged_tokens.append(tokens[i])
            i += 1
    tokens = merged_tokens
    l2 = len(tokens)

    vocab_ct += 1
    print()
    print(vocab)
    assert l1 == pair_count + l2, "wrong count"

with open("out/tokenizer_vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, indent=2, ensure_ascii=False)
