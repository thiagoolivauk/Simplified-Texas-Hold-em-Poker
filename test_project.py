import pytest
from project import evaluate_hand, determine_winner, Player, Deck, deal_hands

def test_evaluate_hand():
    assert evaluate_hand(["A_s", "K_s", "Q_s", "J_s", "10_s"]) == "royal_flush"
    assert evaluate_hand(["10_h", "9_h", "8_h", "7_h", "6_h"]) == "straight_flush"
    assert evaluate_hand(["10_h", "10_s", "10_c", "7_h", "7_d"]) == "full_house"
    assert evaluate_hand(["8_h", "8_s", "9_c", "7_h", "7_d"]) == "two_pairs"
    assert evaluate_hand(["J_h", "10_s", "8_c", "5_h", "3_d"]) == "high_card"
    assert evaluate_hand(["8_h", "8_s", "8_c", "8_d", "7_d"]) == "four_of_a_kind"
    assert evaluate_hand(["J_h", "10_h", "8_h", "5_h", "3_h"]) == "flush"
    assert evaluate_hand(["10_h", "9_s", "8_c", "7_d", "6_d"]) == "straight"
    assert evaluate_hand(["J_h", "J_d", "J_c", "5_h", "3_h"]) == "three_of_a_kind"
    assert evaluate_hand(["J_h", "J_d", "10_c", "5_h", "3_h"]) == "pair"
    assert evaluate_hand(["J_h", "J_d"]) == "pair"
    assert evaluate_hand(["J_h", "8_d"]) == "high_card"


def test_determine_winner():
    player1 = Player("Mario", 500)
    player1.hand = ["A_s", "A_h"]
    player2 = Player("Peach", 500)
    player2.hand = ["K_s", "Q_s"]
    community_cards = ["8_s", "8_c", "9_s", "3_h", "Q_c"]
    winner = determine_winner([player1, player2], community_cards)
    assert winner == player1

    player1 = Player("Mario", 500)
    player1.hand = ["A_s", "K_s"]
    player2 = Player("Peach", 500)
    player2.hand = ["2_h", "Q_d"]
    community_cards = ["Q_s", "J_s", "10_s", "3_h", "7_d"]
    winner = determine_winner([player1, player2], community_cards)
    assert winner == player1

    player1 = Player("Mario", 500)
    player1.hand = ["A_h", "2_d"]
    player2 = Player("Peach", 500)
    player2.hand = ["2_h", "Q_d"]
    player3 = Player("Yoshi", 500)
    player3.hand = ["A_s", "K_s"]
    community_cards = ["A_c", "Q_s", "K_h", "2_c", "7_d"]
    winner = determine_winner([player1, player2, player3], community_cards)
    assert winner == player3


def test_deal_hands():
    deck = Deck()
    player1 = Player("Mario", 500)
    player2 = Player("Peach", 500)
    player3 = Player("Yoshi", 500)
    deal_hands(deck, [player1, player2, player3])
    assert len(player1.hand) == 2
    assert len(player2.hand) == 2
    assert len(player3.hand) == 2
    assert len(deck.cards) == 46
    all_hands = player1.hand + player2.hand + player3.hand
    #checking if cards dealt are unique (set would collapse identical cards)
    assert len(all_hands) == len(set(all_hands))
