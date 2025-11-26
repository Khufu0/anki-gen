import random
import genanki
import os


class AnkiGenerator:
    """Simple Anki deck generator for creating cards with name, pronunciation, and body fields."""

    def __init__(self, deck_name: str, deck_id: int = None):
        """
        Initialize the Anki generator.

        Args:
            deck_name: Name of the deck to create
            deck_id: Optional ID for the deck (auto-generated if not provided)
        """
        self.deck_name = deck_name
        self.deck_id = deck_id or random.randint(1000000000, 9999999999)
        self.deck = genanki.Deck(self.deck_id, deck_name)

        # Read CSS file
        css_path = os.path.join(os.path.dirname(__file__), "style.css")
        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, "r") as f:
                css_content = f.read()

        # Define the note model with three fields
        self.model = genanki.Model(
            random.randint(1000000000, 9999999999),
            f"{deck_name} Model",
            fields=[
                {"name": "Name"},
                {"name": "Body"},
            ],
            templates=[
                {
                    "name": "Card",
                    "qfmt": "<h1 class='name'>{{Name}}</h1>",
                    "afmt": "{{FrontSide}}<hr id='answer' /><div class=\"body\">{{Body}}</div>",
                }
            ],
            css=css_content,
        )

    def add_card(self, name: str, body: str) -> None:
        """
        Add a card to the deck.

        Args:
            name: The name/word for the card
            pronunciation: The pronunciation of the word
            body: The body/definition content of the card
        """
        note = genanki.Note(
            model=self.model,
            fields=[name, body],
        )
        self.deck.add_note(note)

    def add_cards(self, cards: list) -> None:
        """
        Add multiple cards to the deck.

        Args:
            cards: List of dictionaries with keys 'name' and 'body'
        """
        for card in cards:
            self.add_card(
                card.get("name", ""),
                card.get("body", ""),
            )

    def save(self, filepath: str) -> None:
        """
        Save the deck to a file.

        Args:
            filepath: Path where the deck file should be saved (e.g., 'deck.apkg')
            audio_files: Optional list of audio file paths to include in the package
        """
        package = genanki.Package(self.deck)
        package.write_to_file(filepath)
