import re

# Turn a plain text dump of Simple Wikipedia from a single file into multiple files, one for each article.
# Get the dump from https://github.com/LGDoor/Dump-of-Simple-English-Wiki, extract it to resources/corpus.txt.
# The individual files will be written to resources/corpus/<article name>.txt.

with open('resources/corpus.txt', 'r') as f:
    data = f.read()

# Append at least two newlines, otherwise the regex won't work
data += "\n\n"
found = re.findall(r'(^[^\n]+$)\n(.*?)\n\n', data, re.M | re.S)

for (title, content) in found:
    clean_title = re.sub(r'\W+', '_', title)
    with open('resources/corpus/' + str(clean_title) + '.txt', 'w') as f:
        f.write(content)