import logging
import os.path

from day22.code.main import play_combat, parse_decks, play_recursive_combat, calc_winning_deck_score

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


def test_sample_input(caplog):
    deck_1, deck_2, winner = play_combat(*parse_decks(sample_input))
    assert calc_winning_deck_score(deck_1 if winner == 1 else deck_2) == 306

    # caplog.set_level(logging.INFO)

    deck_1, deck_2, winner = play_recursive_combat(*parse_decks(sample_input))
    assert calc_winning_deck_score(deck_1 if winner == 1 else deck_2) == 291


def test_big_input(caplog):
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        deck_1, deck_2, winner = play_combat(*parse_decks(content))
        assert calc_winning_deck_score(deck_1 if winner == 1 else deck_2) == 31754

        # caplog.set_level(logging.INFO)

        deck_1, deck_2, winner = play_recursive_combat(*parse_decks(content))
        assert calc_winning_deck_score(deck_1 if winner == 1 else deck_2) == 35436
