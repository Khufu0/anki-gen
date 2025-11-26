import requests
import os
from dotenv import load_dotenv


# THESAURUS_API_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
# LEARNER_API_URL = "https://www.dictionaryapi.com/api/v3/references/learners/json/"
COLLEGIATE_API_URL = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"


class Dictionary:
    def __init__(self):
        load_dotenv()
        # self._thesaurus_api_key = os.getenv("THESAURUS_API_KEY")
        # self._learner_api_key = os.getenv("LEARNER_API_KEY")
        self._collegiate_api_key = os.getenv("COLLEGIATE_API_KEY")
        self.wrongs = []

    def get_definition(self, word: str):
        data = self._get_response(word)
        if data is None:
            return None
        result = []
        for entry in data:
            parsed = self._parse(entry)
            if parsed is None:
                continue
            result.append(parsed)
        if len(result) == 0:
            print(f"Could not find sufficient data for: {word}")
            return None
        return result

    def _get_response(self, word: str):
        try:
            res = requests.get(
                f"{COLLEGIATE_API_URL}{word}?key={self._collegiate_api_key}", timeout=5
            )
            res.raise_for_status()
            data = res.json()
            if isinstance(data[0], dict):
                return data
            else:
                self.wrongs.append(word)
                return None
        except requests.RequestException as e:
            self.wrongs.append(word)
            print(f"A network/HTTP error occurred for '{word}': {e}")
            return None

    def _parse(self, data):
        part_of_speech = None
        word = None
        defs = None
        # ipa = set()

        try:
            word = data["meta"]["id"].split(":")[0]
            defs = data["shortdef"]

            if word == "" or len(defs) == 0:
                raise Exception
        except Exception:
            print(f"Could not find sufficient data for: {word}")
            return None

        try:
            part_of_speech = data["fl"]
            if part_of_speech in ("biographical name", "geographical name"):
                return None
        except Exception:
            pass
        # try:
        #     for entry in data["hwi"]["prs"]:
        #         ipa.add(entry["ipa"])
        # except Exception:
        #     pass
        # try:
        #     for entry in data["hwi"]["altprs"]:
        #         ipa.add(entry["ipa"])
        # except Exception:
        #     pass
        # ipa = list(ipa)

        return {
            "pos": part_of_speech,
            "word": word,
            "defs": defs,
            # "ipa": ipa,
        }
