import logging
import sys
from copy import deepcopy
from functools import lru_cache

logger = logging.getLogger(__name__)


def parse_decks(inp):
    player1_raw, player2_raw = inp.split("\n\n")
    deck_1 = [int(x) for x in player1_raw.split("\n")[1:]]
    deck_2 = [int(x) for x in player2_raw.split("\n")[1:]]

    return tuple(deck_1), tuple(deck_2)


def play_combat(deck_1, deck_2):
    round_number = 1

    deck_1 = list(deck_1)
    deck_2 = list(deck_2)

    while deck_1 and deck_2:
        logger.info("")
        logger.info(f"-- Round {round_number} --")
        logger.info(f"Deck 1: {deck_1}")
        logger.info(f"Deck 2: {deck_2}")

        top_1, deck_1 = deck_1[0], deck_1[1:]
        top_2, deck_2 = deck_2[0], deck_2[1:]

        logger.info(f"Player 1 plays: {top_1}")
        logger.info(f"Player 2 plays: {top_2}")

        if top_1 > top_2:
            logger.info(f"Player 1 wins the round!")
            deck_1.append(top_1)
            deck_1.append(top_2)

        else:
            logger.info(f"Player 2 wins the round!")
            deck_2.append(top_2)
            deck_2.append(top_1)

        round_number += 1

    logger.info(f"Final player 1 deck: {deck_1}")
    logger.info(f"Final player 2 deck: {deck_2}")

    winner = 1 if deck_1 else 2

    return deck_1, deck_2, winner


@lru_cache()
def play_recursive_combat(deck_1, deck_2):
    round_number = 1

    game_cache = set()

    deck_1 = list(deck_1)
    deck_2 = list(deck_2)

    logger.info("")
    logger.info(f"== New recursive game ==")

    while deck_1 and deck_2:
        logger.info("")
        logger.info(f"-- Round {round_number} --")
        logger.info(f"Deck 1:      {deck_1}")
        logger.info(f"Deck 2:      {deck_2}")

        deck_state = (tuple(deck_1), tuple(deck_2))
        if deck_state in game_cache:
            logger.info("Decks didn't change, player 1 wins")
            return deck_1, deck_2, 1

        game_cache.add(deck_state)

        top_1, deck_1 = deck_1[0], deck_1[1:]
        top_2, deck_2 = deck_2[0], deck_2[1:]

        logger.info(f"Player 1 plays: {top_1}")
        logger.info(f"Player 2 plays: {top_2}")

        if len(deck_1) >= top_1 and len(deck_2) >= top_2:
            logger.info("Playing a sub-game to determine the winner")
            _, _, winner = play_recursive_combat(tuple(deck_1[:top_1]), tuple(deck_2[:top_2]))
            logger.info("")
            logger.info(f"...anyway, back to previous parent game")

        else:
            winner = 1 if top_1 > top_2 else 2

        if winner == 1:
            logger.info(f"Player 1 wins the round!")
            deck_1.append(top_1)
            deck_1.append(top_2)

        else:
            logger.info(f"Player 2 wins the round!")
            deck_2.append(top_2)
            deck_2.append(top_1)

        round_number += 1

    logger.info(f"Final player 1 deck: {deck_1}")
    logger.info(f"Final player 2 deck: {deck_2}")

    winner = 1 if deck_1 else 2
    logger.info(f"Player {winner} wins round {round_number}!")

    return deck_1, deck_2, winner


def calc_winning_deck_score(winning_deck):
    return sum(winning_deck[i] * (len(winning_deck) - i) for i in range(len(winning_deck)))
