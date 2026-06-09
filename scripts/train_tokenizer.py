import json
import regex as re
from collections import Counter
from tqdm import tqdm

with open("data/validation.txt", encoding="utf-8") as f:
    text = f.read()

text = text[:100000]
gpt2pat = re.compile(
    r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""",
    flags=re.IGNORECASE,
) # regex to separate tokens (as used in gpt2)
pieces = gpt2pat.findall(text)
tokens = [list(piece) for piece in pieces if piece]
vocab = {chr(i):i for i in range(1, 257)} # basic characters

for piece in tokens:
    for ch in piece:
        if ch not in vocab:
            vocab[ch] = ord(ch)

# all characters now added to vocab
vocab_ct = max(vocab.values(), default=-1) + 1
vocab_size = 1024*1

with tqdm(total=vocab_size-vocab_ct, desc="Training") as pbar:
    while vocab_ct < vocab_size and any(len(piece) > 1 for piece in tokens):
        counter = Counter()
        for piece in tokens:
            counter.update(zip(piece, piece[1:]))
        (ch1, ch2), _pair_count = counter.most_common(1)[0]

        merged_token = f"{ch1}{ch2}"
        vocab[merged_token] = vocab_ct

        l1 = sum(len(piece) for piece in tokens) # just for assertion
        merged_tokens = []
        merge_count = 0
        for piece in tokens:
            merged_piece = []
            i = 0
            while i < len(piece):
                if i < len(piece) - 1 and piece[i] == ch1 and piece[i + 1] == ch2:
                    merged_piece.append(merged_token)
                    merge_count += 1
                    i += 2
                else:
                    merged_piece.append(piece[i])
                    i += 1
            merged_tokens.append(merged_piece)
        tokens = merged_tokens
        l2 = sum(len(piece) for piece in tokens)

        vocab_ct += 1
        assert l1 == merge_count + l2, "wrong count"
        pbar.update(1)

with open("out/tokenizer_vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, indent=2, ensure_ascii=False)
