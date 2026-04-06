import random  # library: https://docs.python.org/3/library/random.html
import sys  # library: https://docs.python.org/3/library/sys.html
from treys import Card, Evaluator  # library: https://github.com/ihendley/treys


class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.role = "regular"
        self.hand = []
        self.current_bet = 0
        self.fold = False


class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["s", "c", "h", "d"]
        cards = []
        for rank in ranks:
            for suit in suits:
                cards.append(rank + "_" + suit)
        random.shuffle(cards)
        self.cards = cards


rankings = {
    "royal_flush": 10,
    "straight_flush": 9,
    "four_of_a_kind": 8,
    "full_house": 7,
    "flush": 6,
    "straight": 5,
    "three_of_a_kind": 4,
    "two_pairs": 3,
    "pair": 2,
    "high_card": 1,
}


def main():
    if len(sys.argv) != 2:
        sys.exit("please only type 'python project.py <your_name>'")
    user = Player(sys.argv[1], 200)
    player_2 = Player("Player_2", 200)
    player_3 = Player("Player_3", 200)
    player_4 = Player("Player_4", 200)
    players = [user, player_2, player_3, player_4]
    round = 1
    # game_loop until only one player in-game
    while len(players) > 1:
        deck = Deck()
        assign_roles(players, round)
        big_blind = 10
        small_blind = 5
        pot = collect_blinds(big_blind, small_blind, players)
        deal_hands(deck, players)
        community_cards = []
        pot, current_bet = betting_round(players, pot, 0, community_cards=[])
        current_bet = 0
        active_players = []
        for player in players:
            if player.fold == False:
                active_players.append(player)
        if len(active_players) == 1:
            winner = active_players[0]
            winner.money = winner.money + pot
            print(f"{winner.name} won this round as others folded and got ${pot}")
            round = round + 1
            players, current_bet = reset(players, community_cards)
            continue
        # flop
        community_cards.append(deck.cards.pop(0))
        community_cards.append(deck.cards.pop(0))
        community_cards.append(deck.cards.pop(0))
        pot, current_bet = betting_round(players, pot, current_bet, community_cards)
        current_bet = 0
        active_players = []
        for player in players:
            if player.fold == False:
                active_players.append(player)
        if len(active_players) == 1:
            winner = active_players[0]
            winner.money = winner.money + pot
            print(f"{winner.name} won this round as others folded and got ${pot}")
            round = round + 1
            players, current_bet = reset(players, community_cards)
            continue

        # turn
        community_cards.append(deck.cards.pop(0))
        pot, current_bet = betting_round(players, pot, current_bet, community_cards)
        current_bet = 0
        active_players = []
        for player in players:
            if player.fold == False:
                active_players.append(player)
        if len(active_players) == 1:
            winner = active_players[0]
            winner.money = winner.money + pot
            print(f"{winner.name} won this round as others folded and got ${pot}")
            round = round + 1
            players, current_bet = reset(players, community_cards)
            continue

        # river
        community_cards.append(deck.cards.pop(0))
        pot, current_bet = betting_round(players, pot, current_bet, community_cards)
        current_bet = 0
        active_players = []
        for player in players:
            if player.fold == False:
                active_players.append(player)
        if len(active_players) == 1:
            winner = active_players[0]
            winner.money = winner.money + pot
            print(f"{winner.name} won this round as others folded and got ${pot}")
            round = round + 1
            players, current_bet = reset(players, community_cards)
            continue
        winner = determine_winner(players, community_cards)
        winner.money = winner.money + pot
        for player in players:
            if player.fold == False:
                print(f"{player.name}")
                Card.print_pretty_cards(convert_cards(player.hand[:2]))
        print(f"{winner.name} won this round and got ${pot}")

        # new round - clearing parameters
        round = round + 1
        players, current_bet = reset(players, community_cards)

    print(f"End game: {players[0].name} won!")


def assign_roles(players, round):
    if round == 1:
        players[0].role = "dealer"
        players[1].role = "small_blind"
        players[2].role = "big_blind"
        players[3].role = "regular"
    else:
        for player in players:
            if player.role == "dealer":
                player.role = "regular"
            elif player.role == "small_blind":
                player.role = "dealer"
            elif player.role == "big_blind":
                player.role = "small_blind"
            elif player.role == "regular":
                player.role = "big_blind"


def deal_hands(deck, players):
    # pop removes a card from the deck and place it in the player's hand
    for player in players:
        player.hand.append(deck.cards.pop(0))
    for player in players:
        player.hand.append(deck.cards.pop(0))


def collect_blinds(big_blind, small_blind, players):
    pot = big_blind + small_blind
    for player in players:
        if player.role == "big_blind":
            player.money = player.money - big_blind
        if player.role == "small_blind":
            player.money = player.money - small_blind
    return pot


def evaluate_hand(hand):
    global rankings
    ranks = []
    suits = []
    # assigning values to face cards to allow for consecutive numbers assessment
    face_cards = {"J": 11, "Q": 12, "K": 13, "A": 14}
    numeric_ranks = []
    for card in hand:
        rank, suit = card.split("_")
        ranks.append(rank)
        suits.append(suit)
    for rank in ranks:
        if rank in face_cards:
            rank = int(face_cards[rank])
        else:
            rank = int(rank)
        numeric_ranks.append(rank)
    numeric_ranks.sort()

    # royal_flush and straight_flush
    # checking if players has 5 cards with the same suit
    if (
        suits.count("s") == 5
        or suits.count("c") == 5
        or suits.count("d") == 5
        or suits.count("h") == 5
    ):
        # checking if player has 5 cards with the higher ranks
        if (
            "A" in ranks
            and "K" in ranks
            and "Q" in ranks
            and "J" in ranks
            and "10" in ranks
        ):
            return "royal_flush"
        # checking if player has consecutive cards
        for numeric_rank in range(1, len(numeric_ranks)):
            if numeric_ranks[numeric_rank] - numeric_ranks[(numeric_rank - 1)] != 1:
                break
        else:
            return "straight_flush"

    # four of a kind
    for rank in ranks:
        if ranks.count(rank) == 4:
            return "four_of_a_kind"

    # full_house
    three_cards = False
    pair = False
    for rank in ranks:
        if ranks.count(rank) == 3:
            three_cards = True
        if ranks.count(rank) == 2:
            pair = True
    if three_cards is True and pair is True:
        return "full_house"

    # flush
    if (
        suits.count("s") == 5
        or suits.count("c") == 5
        or suits.count("d") == 5
        or suits.count("h") == 5
    ):
        return "flush"

    # straight
    for numeric_rank in range(1, len(numeric_ranks)):
        if numeric_ranks[numeric_rank] - numeric_ranks[(numeric_rank - 1)] != 1:
            break
    else:
        return "straight"

    # three_of_a_kind
    for rank in ranks:
        if ranks.count(rank) == 3:
            return "three_of_a_kind"

    # two_pairs
    counted = []
    for rank in ranks:
        if ranks.count(rank) == 2 and rank not in counted:
            counted.append(rank)
    if len(counted) == 2:
        return "two_pairs"

    # pair
    for rank in ranks:
        if ranks.count(rank) == 2:
            return "pair"

    # high_card
    return "high_card"


def determine_winner(players, community_cards):
    # bringing in treys library to facilitate the handling of ties
    active_players = []
    for player in players:
        if player.fold == False:
            active_players.append(player)
    players = active_players
    evaluator = Evaluator()
    results = {}
    for player in players:
        treys_hand = convert_cards(player.hand)
        treys_community_cards = convert_cards(community_cards)
        score = evaluator.evaluate(treys_hand, treys_community_cards)
        player.hand.extend(community_cards)
        results[player] = (evaluate_hand(player.hand), score)

    # using max() to find the highest result; results[player] = most powerful card combination of each player
    # [0]gets to the first value in the tuple
    highest_ranking_player = max(
        results, key=lambda player: rankings[results[player][0]]
    )
    best_rank = rankings[results[highest_ranking_player][0]]
    tied_players = []
    for player in players:
        if rankings[results[player][0]] == best_rank:
            tied_players.append(player)
    if len(tied_players) == 1:
        winner = highest_ranking_player
        return winner
    if len(tied_players) > 1:
        winner = min(tied_players, key=lambda player: results[player][1])
        return winner


def convert_cards(cards):
    converted_cards = []
    for card in cards:
        treys_card = card.replace("_", "").replace("10", "T")
        converted_cards.append(Card.new(treys_card))
    return converted_cards


def betting_round(players, pot, current_bet, community_cards):
    global rankings
    for player in players:

        # logic for user
        if player.name == sys.argv[1]:
            # skipping in case the user folded
            if player.fold == True:
                continue
            print(
                f"the two cards to the left are the player's cards; other cards are community cards"
            )
            Card.print_pretty_cards(convert_cards(player.hand + community_cards))
            print(
                f"current pot is {pot}; current bet is {current_bet}; amount of money left: {player.money}"
            )
            while True:
                action = input("check, bet, call, raise or fold? ")
                if action not in ["check", "bet", "call", "raise", "fold"]:
                    print("Please type 'check', 'bet', 'call', 'raise' or 'fold'")
                    continue
                if current_bet > 0 and action == "check":
                    print("Can't check when there's a bet on the table!")
                elif current_bet == 0 and action == "call":
                    print("Nothing to call, please check instead!")
                elif current_bet == 0 and action == "raise":
                    print("Nothing to raise, please bet instead!")
                else:
                    break
            if action == "bet":
                while True:
                    try:
                        current_bet = int(
                            input("value to bet(please, only type numbers): ")
                        )
                        if current_bet > 0 and current_bet <= player.money:
                            break
                        print(f"value must be between 1 and {player.money}")
                    except ValueError:
                        print(f"please enter a valid number")
                        continue
                player.money = player.money - current_bet
                pot = pot + current_bet
            elif action == "call":
                player.money = player.money - current_bet
                pot = pot + current_bet
            elif action == "raise":
                while True:
                    try:
                        raise_amount = int(
                            input("value to raise(please, only type numbers): ")
                        )
                        if raise_amount > 0 and raise_amount <= player.money:
                            break
                        print(f"value must be between 1 and {player.money}")
                    except ValueError:
                        print(f"please enter a valid number")
                        continue
                player.money = player.money - raise_amount
                current_bet = current_bet + raise_amount
                pot = pot + raise_amount
            elif action == "fold":
                player.fold = True

        # logic for automated player
        if player.name != sys.argv[1]:
            if player.fold == False and player.money > 0:
                hand_power = evaluate_hand(player.hand)
                if rankings[hand_power] >= 6:
                    # fixing a bug here: using min() to make sure player doesn't bet more than they have (:
                    if current_bet == 0:
                        bet_amount = max(round(player.money * 0.2), 1) #adding max here so bet is at least 1
                        current_bet = current_bet + bet_amount
                        pot = pot + bet_amount
                        player.money = player.money - bet_amount
                        print(
                            f"{player.name} is betting {bet_amount}; pot is now {pot}; player money is ${player.money}"
                        )
                    else:
                        raise_amount = min(2 * (current_bet + 10), player.money)
                        player.money = player.money - raise_amount
                        current_bet = current_bet + raise_amount
                        pot = pot + raise_amount
                        print(
                            f"{player.name} raised by {raise_amount}; pot is now {pot}; player money is ${player.money}"
                        )
                elif 5 >= rankings[hand_power] >= 2:
                    if current_bet == 0:
                        if random.random() <= 0.50:
                            bet_amount = max(round(player.money * 0.1), 1) #adding max here so bet is at least 1
                            current_bet = current_bet + bet_amount
                            pot = pot + bet_amount
                            player.money = player.money - bet_amount
                            print(
                                f"{player.name} is betting {bet_amount}; pot is now {pot}; player money is ${player.money}"
                            )
                        else:
                            print(
                                f"{player.name} checked; pot remains {pot}; player money is ${player.money}"
                            )
                    else:
                        # fixing a bug here: using min() to make sure player doesn't bet more than they have (:
                        call_amount = min(current_bet, player.money)
                        player.money = player.money - call_amount
                        pot = pot + call_amount
                        print(
                            f"{player.name} called; pot is now {pot}; player money is ${player.money}"
                        )
                elif rankings[hand_power] <= 1:
                    if current_bet == 0:
                        print(
                            f"{player.name} checked; pot remains {pot}; player money is ${player.money}"
                        )
                    elif random.random() <= 0.30:
                        raise_amount = min(2 * (current_bet + 10), player.money)
                        player.money = player.money - raise_amount
                        current_bet = current_bet + raise_amount
                        pot = pot + raise_amount
                        print(
                            f"{player.name} raised by {raise_amount}; pot is now {pot}; player money is ${player.money}"
                        )
                    else:
                        player.fold = True
                        print(
                            f"{player.name} folded; pot remains {pot}; player money is ${player.money}"
                        )
            active_players = []
            for player in players:
                if player.fold == False:
                    active_players.append(player)
            if len(active_players) == 1:
                break

    return pot, current_bet


def reset(players, community_cards):
    community_cards.clear()
    current_bet = 0
    new_list = []
    for player in players:
        player.hand.clear()
        player.fold = False
        new_list.append(player)
        if player.money == 0:
            new_list.remove(player)
    players = new_list
    return players, current_bet


if __name__ == "__main__":
    main()
