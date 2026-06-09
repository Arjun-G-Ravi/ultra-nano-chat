import json
from collections import Counter
from tqdm import tqdm

with open("data/validation.txt", encoding="utf-8") as f:
    text = f.read()

text = text[:1000000]
tokens = list(text)
vocab = {chr(i):i for i in range(32, 127)} # basic characters

for ch in tokens:
    if ch not in vocab:
        vocab[ch] = ord(ch)

# all characters now added to vocab
vocab_ct = max(vocab.values(), default=-1) + 1
vocab_size = 1024*16

with tqdm(total=vocab_size-vocab_ct, desc="Training") as pbar:
    while vocab_ct < vocab_size and len(tokens) > 1:
        counter = Counter(zip(tokens, tokens[1:]))
        (ch1, ch2), _pair_count = counter.most_common(1)[0]

        merged_token = f"{ch1}{ch2}"
        vocab[merged_token] = vocab_ct

        l1 = len(tokens) # just for assertion
        merged_tokens = []
        merge_count = 0
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == ch1 and tokens[i + 1] == ch2:
                merged_tokens.append(merged_token)
                merge_count += 1
                i += 2po
            else:
                merged_tokens.append(tokens[i])
                i += 1
        tokens = merged_tokens
        l2 = len(tokens)

        vocab_ct += 1
        assert l1 == merge_count + l2, "wrong count"
        pbar.update(1)

with open("out/tokenizer_vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, indent=2, ensure_ascii=False)
