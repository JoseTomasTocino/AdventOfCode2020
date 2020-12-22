import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


def parse_decks(inp):
    player1_raw, player2_raw = inp.split("\n\n")
    deck_1 = [int(x) for x in player1_raw.split("\n")[1:]]
    deck_2 = [int(x) for x in player2_raw.split("\n")[1:]]

    return deck_1, deck_2


def play_combat(deck_1, deck_2):
    round_number = 1

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

    winning_deck = deck_1 if deck_1 else deck_2
    winning_score = sum(winning_deck[i] * (len(winning_deck) - i) for i in range(len(winning_deck)))

    winner = 1 if deck_1 else 2
    return deck_1, deck_2, winner

    return winning_score


def play_recursive_combat(deck_1, deck_2, game_depth=1):
    round_number = 1

    last_deck_1 = None
    last_deck_2 = None

    logger.info("")
    logger.info(f"== Game {game_depth} ==")

    while deck_1 and deck_2:
        logger.info("")
        logger.info(f"-- Round {round_number} (Game {game_depth}) --")
        logger.info(f"Deck 1:      {deck_1}")
        logger.info(f"Deck 2:      {deck_2}")
        logger.info(f"Last deck 1: {last_deck_1}")
        logger.info(f"Last deck 2: {last_deck_2}")

        if deck_1 == last_deck_1 and deck_2 == last_deck_2:
            logger.info("Decks didn't change, player 1 wins")
            return deck_1, deck_2, 1

        last_deck_1 = deck_1
        last_deck_2 = deck_2

        top_1, deck_1 = deck_1[0], deck_1[1:]
        top_2, deck_2 = deck_2[0], deck_2[1:]

        logger.info(f"Player 1 plays: {top_1}")
        logger.info(f"Player 2 plays: {top_2}")

        if len(deck_1) >= top_1 and len(deck_2) >= top_2:
            logger.info("Playing a sub-game to determine the winner")
            _, _, winner = play_recursive_combat(deepcopy(deck_1[:top_1]), deepcopy(deck_2[:top_2]), game_depth=game_depth+1)
            logger.info("")
            logger.info(f"...anyway, back to game {game_depth}")

        else:
            winner = 1 if top_1 > top_2 else 2

        if winner == 1:
            logger.info(f"Player 1 wins the round of game {game_depth}!")
            deck_1.append(top_1)
            deck_1.append(top_2)

        else:
            logger.info(f"Player 2 wins the round of game {game_depth}!")
            deck_2.append(top_2)
            deck_2.append(top_1)

        round_number += 1

    logger.info(f"Final player 1 deck in game {game_depth}: {deck_1}")
    logger.info(f"Final player 2 deck in game {game_depth}: {deck_2}")

    winner = 1 if deck_1 else 2
    logger.info(f"Player {winner} wins round {round_number} of game {game_depth}!")

    return deck_1, deck_2, winner


def calc_winning_deck_score(winning_deck):
    return sum(winning_deck[i] * (len(winning_deck) - i) for i in range(len(winning_deck)))
