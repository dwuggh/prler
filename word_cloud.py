from collections import Counter
from wordcloud import WordCloud
import re

def read_data():
    with open("data.txt", "r") as f:
        titles = []
        abstracts = []
        i = 0
        for line in f.readlines():
            if i % 2 == 1:
            # title line
                title = line.split(',')[0]
                titles.append(title.strip())
            else:
                abstracts.append(line.strip())
            i = i + 1

    return titles, abstracts

titles, abstracts = read_data()

def to_words(texts):
    all_words = []
    for text in texts:
        words = text.split()
        for w in words:
            w = w.lower()
            if len(w) > 3 and not re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be|this|which|from|while|method|using", w):
                all_words.append(w)
            
        # all_words.extend(words)

    return all_words

title_words = to_words(titles)
abstracts_words = to_words(abstracts)

title_counter = Counter(title_words)
abs_counter = Counter(abstracts_words)
abs_counter.update(title_words)


wc = WordCloud(width=2560, height=1440, max_words=500)
wc.generate_from_frequencies(title_counter)

wc.to_file("title.png")
wc = WordCloud(width=2560, height=1440, max_words=500)
wc.generate_from_frequencies(abs_counter)

wc.to_file("abs.png")

# svg = wc.to_svg()
# print(svg)

