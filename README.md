# 📚 AnkiGen

Generate Anki flashcard decks from a word list using dictionary definitions.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ankigen.py --file words.txt --output deck.apkg --name "My Deck"
```

### Arguments

| Argument    | Required | Description                            |
| ----------- | -------- | -------------------------------------- |
| `--file`    | ✅       | Text file with words (one per line)    |
| `--output`  | ✅       | Output `.apkg` file                    |
| `--name`    | ❌       | Deck name (default: "Dictionary Deck") |
| `--version` | ❌       | Show version                           |

## Features

-   🚀 Batch process hundreds of words
-   📖 Auto-fetch definitions & examples
-   📊 Live progress indicator
-   ⚙️ Customizable deck names

## How It Works

1. Read words from file
2. Fetch definitions from dictionary
3. Generate styled HTML cards
4. Create Anki deck (`.apkg`)
5. Import into Anki
