from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    type: str
    name: str



ELIXIR_CARDS = [
    Card(type="Elixir", name="Barbarian"),
    Card(type="Elixir", name="Archer"),
    Card(type="Elixir", name="Giant"),
    Card(type="Elixir", name="Goblin"),
    Card(type="Elixir", name="Wall Breaker"),
    Card(type="Elixir", name="Balloon"),
    Card(type="Elixir", name="Wizard"),
    Card(type="Elixir", name="Healer"),
    Card(type="Elixir", name="Dragon"),
    Card(type="Elixir", name="P.E.K.K.A."),
    Card(type="Elixir", name="Baby Dragon"),
    Card(type="Elixir", name="Miner"),
    Card(type="Elixir", name="Electro Dragon"),
    Card(type="Elixir", name="Yeti"),
    Card(type="Elixir", name="Dragon Rider"),
    Card(type="Elixir", name="Electro Titan"),
    Card(type="Elixir", name="Root Rider"),
    Card(type="Elixir", name="Thrower"),
    Card(type="Elixir", name="Meteor Golem")
]

DARK_ELIXIR_CARDS = [
    Card(type="Dark Elixir", name="Minion"),
    Card(type="Dark Elixir", name="Hog Rider"),
    Card(type="Dark Elixir", name="Valkyrie"),
    Card(type="Dark Elixir", name="Golem"),
    Card(type="Dark Elixir", name="Witch"),
    Card(type="Dark Elixir", name="Lava Hound"),
    Card(type="Dark Elixir", name="Bowler"),
    Card(type="Dark Elixir", name="Ice Golem"),
    Card(type="Dark Elixir", name="Head Hunter"),
    Card(type="Dark Elixir", name="Apprentice Warden"),
    Card(type="Dark Elixir", name="Druid"),
    Card(type="Dark Elixir", name="Furnace"),
    Card(type="Dark Elixir", name="Ruin Witch")
]

BUILDER_BASE_CARDS = [
    Card(type="Builder Base", name="Raged Barbarian"),
    Card(type="Builder Base", name="Sneaky Archer"),
    Card(type="Builder Base", name="Boxer Giant"),
    Card(type="Builder Base", name="Beta Minion"),
    Card(type="Builder Base", name="Bomber"),
    Card(type="Builder Base", name="Raged Baby Dragon"),
    Card(type="Builder Base", name="Cannon Cart"),
    Card(type="Builder Base", name="Night Witch"),
    Card(type="Builder Base", name="Drop Ship"),
    Card(type="Builder Base", name="Power P.E.K.K.A."),
    Card(type="Builder Base", name="Hog Glider")
]

SUPER_TROOP_CARDS = [
    Card(type="Super Troop", name="Super Barbarian"),
    Card(type="Super Troop", name="Super Archer"),
    Card(type="Super Troop", name="Super Giant"),
    Card(type="Super Troop", name="Sneaky Goblin"),
    Card(type="Super Troop", name="Super Wall Breaker"),
    Card(type="Super Troop", name="Rocket Balloon"),
    Card(type="Super Troop", name="Super Wizard"),
    Card(type="Super Troop", name="Super Dragon"),
    Card(type="Super Troop", name="Inferno Dragon"),
    Card(type="Super Troop", name="Super Miner"),
    Card(type="Super Troop", name="Super Yeti"),
    Card(type="Super Troop", name="Super Minion"),
    Card(type="Super Troop", name="Super Hog Rider"),
    Card(type="Super Troop", name="Super Valkyrie"),
    Card(type="Super Troop", name="Super Witch"),
    Card(type="Super Troop", name="Ice Hound"),
    Card(type="Super Troop", name="Super Bowler")
]