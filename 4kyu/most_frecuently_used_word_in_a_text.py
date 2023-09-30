import re

def top_3_words(text):
    word_freq = {}
    for word in re.sub(r"[" + re.escape("/.,:;!?()[]{}\"_-") + r"]", ' ', text).split(' '):
        word = word.lower()
        if re.search('[a-zA-Z]', word):
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    
    return list(dict(sorted(word_freq.items(), key=lambda item: item[1], reverse=True)).keys())[:3]