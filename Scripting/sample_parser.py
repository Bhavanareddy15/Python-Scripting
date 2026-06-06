from pathlib import Path
import re

file_path = Path(__file__).parent / "sample.txt"

count = {}

with open(file_path , 'r') as file:
    for line in file:
        line_text = re.sub(r"[^\w\s]", "", line)
        words = line_text.strip().split()
        for word in words:
            word= word.lower()
            if word not in count:
                count[word] = 0
            count[word]+=1


top_5 = sorted(count.items(), key=lambda x: x[1], reverse=True)[:5]

for word, freq in top_5:
    print(f"{word}: {freq}")


