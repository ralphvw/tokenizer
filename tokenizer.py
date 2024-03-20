word = "Unicode, formally The Unicode Standard, is a text encoding standard maintained by the Unicode Consortium designed to support the use of text written in all of the world's major writing systems"

#Get tokens
tokens = word.encode("utf-8")
#Convert tokens into ints
tokens = list(map(int, tokens))

#Get tuple and frequency
def get_stats(ids):
    counts = {}
    
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    
    return counts

def merge(ids, pair, idx):
    new_ids = []
    i = 0
    
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            new_ids.append(idx)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    
    return new_ids

vocab_size = 276
num_merges = vocab_size - 256

ids = list(tokens)

merges = {}

#Compression
for i in range(num_merges):
    stats = get_stats(ids)
    top_pair = max(stats, key=stats.get)
    idx = 256 + i
    print(f"Merging {top_pair} into new token {idx}")
    ids = merge(ids, top_pair, idx)
    merges[top_pair] = idx

vocab = {idx: bytes([idx]) for idx in range(256)}
for (p0, p1), idx in merges.items():
    vocab[idx] = vocab[p0] + vocab[p1]

#Decoding
def decode(ids):
    token_string = b"".join(vocab[idx] for idx in ids)
    text = token_string.decode("utf-8", errors="replace")
    return text

#Encoding
def encode(text):
    tokens = list(text.encode("utf-8"))
    while len(tokens) >= 2:
        stats = get_stats(tokens)
        pair = min(stats, key=lambda p: merges.get(p, float("inf")))
        if pair not in merges:
            break
        idx = merges[pair]
        tokens = merge(tokens, pair, idx)
    return tokens

sentence = """<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
<|im_end|>
<|im_start|>assistant"""

encoding = encode(sentence)
print(encoding)
print(decode(encoding))