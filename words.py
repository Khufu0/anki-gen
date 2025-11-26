import re
import sys

if len(sys.argv) > 2:
    input_path = sys.argv[1]
    out_path = sys.argv[2]
else:
    sys.exit("Please provide a file name")

# Your big paragraph goes here
with open(input_path, "r") as file:
    paragraph = file.read()

# 1. Make everything lowercase to treat "This" and "this" as the same word
text = paragraph.lower()

# 2. Find all words (sequences of letters)
#    This regex finds one or more alphabetic characters
word_list = re.findall(r"\b[a-z]+\b", text)

# 3. Use a 'set' to automatically get only the unique words
unique_words = set(word_list)

# 4. Convert back to a list and sort it alphabetically (optional)
sorted_unique_words = sorted(list(unique_words), key=lambda x: (len(x), x))

# 5. Print the results
with open(out_path, "w") as file:
    for word in sorted_unique_words:
        file.write(word + "\n")

print(f"\nTotal words: {len(word_list)}")
print(f"Distinct words: {len(sorted_unique_words)}")
