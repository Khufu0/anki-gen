import os
from card import AnkiGenerator
import argparse
from Dictionary import Dictionary

PWD = os.path.dirname(__file__)
VERSION = "0.0.1"


class App:
    def __init__(self, deck_name, deck_id=None):
        self.__wrongs = []
        self.__generator = AnkiGenerator(deck_name, deck_id)
        self.__dictionary = Dictionary()

    def __gen_html(defs):
        html_parts = []
        for definition in defs:
            defs_html = "".join(f"<li>{d}</li>" for d in definition["defs"])
            html = f"""\
<div class="sense">
<header class="pos">{definition["pos"]}: <span class="id">{definition["word"]}</span></header>
<ol class="defs-list">
{defs_html}
</ol>
<header class="examples-header">examples:</header>
<ul class="examples">
<li>Add</li>
</ul>
</div>
"""
            html_parts.append(html)
        return "".join(html_parts)

    def gen_deck(self, words: list[str], output: str):
        total_words = len(words)
        for index, word in enumerate(words, 1):
            progress = f"[{index}/{total_words}] Processing: {word}"
            print(f"\r{progress:<120}", end="", flush=True)
            data = self.__dictionary.get_definition(word)
            if data is None or len(data) == 0:
                continue
            body = App.__gen_html(data)
            self.__generator.add_card(word, body)
        print()  # New line after completion
        self.__generator.save(output)
        for word in self.__dictionary.wrongs:
            print(word)


def main():
    parser = argparse.ArgumentParser(description="Dictionary-based Anki deck generator")
    parser.add_argument(
        "--name",
        type=str,
        default="Dictionary Deck",
        help="Name of the Anki deck (default: Dictionary Deck)",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file path for the Anki deck (.apkg)",
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="File containing words to process (one per line)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    # Read words from file or use defaults
    if args.file:
        try:
            with open(args.file, "r") as f:
                words = [line.strip() for line in f if line.strip()]
            if not words:
                print(f"Error: No words found in file '{args.file}'")
                return
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            return

    app = App(args.name)
    app.gen_deck(words, args.output)


if __name__ == "__main__":
    main()
