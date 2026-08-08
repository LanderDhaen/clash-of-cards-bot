from dataclasses import dataclass

@dataclass(frozen=True)
class Clan:
    name: str
    tag: str



CLANS = [
    Clan(name="Dutch Legion 3", tag="28UYR0CVU"),
    Clan(name="Dutch Legion CW", tag="29RPVGYU8"),
    Clan(name="Dutch Legion 4", tag="2J0C28R2J"),
    Clan(name="DL Gold", tag="2RV80YRPY"),
    Clan(name="DL Azure", tag="2JJ22CPUV"),
    Clan(name="DL Silver", tag="2RPQRYRUY"),
    Clan(name="DL Mini", tag="2JY9C0L0P"),
    Clan(name="DL Ruby", tag="2RCQPJGQY"),
    Clan(name="DL eSports", tag="2R0GUP2Q8"),
    Clan(name="DL eSports X", tag="2CYCCVQLL"),
]