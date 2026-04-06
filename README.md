# **SIMPLIFIED TEXAS HOLD'EM POKER**

**Date: April 3, 2026**

## Video Demo:  <https://youtu.be/i4dkOJWWCHo>

## Description:
As the name says, this is a simplified version of the Texas Hold'em Poker game. Limitations are discussed in more detail below. This is the final project I submitted for the completion of CS50's Introduction to Programming with Python course at HarvardX. The project is composed by a main file, with all relevant classes and functions, as well as a "test_" file that tests 3 of the project's main functions, a requirements.txt file and this README.md file.

### How to run:
[from requirements.txt]

pip install treys

When starting the game, type "python project.py " and <your_name>. The program used a command-line argument to name the user in the game.

python project.py <your_name>

### How to play:
The user plays together with three automated players. It works as a regular Texas Hold'em Poker game: you are dealt two cards, then community cards are open on the table (three at once, then one, then a final one). The player with the best combinations of cards wins. In between the opening of community cards on the table, players do betting rounds, at which they may do one of the following actions: **check** (keep in the game without betting, if there is no ongoing bet); **call** (match an ongoing bet to continue in the game); **bet** (put the first bet on the table); **raise** (increase the current bet); **fold** (quit after a bet is made). The goal is winning the pot money until all other players go down to money = 0 and are pushed all of the game. Winner is the final player standing. Starting money is $200; blind amounts are $5/$10.

The ranking of power between cards is (from strongest to weakest):
**royal straight flush** (combination from A to 10 with all cards with same suit)
**straight flush** (combination of 5 sequential cards with the same suit)
**four of a kind** (4 cards with the same face/number)
**full house** (a pair + three of a kind)
**straight** (combination of 5 sequential cards with different suits)
**flush** (5 cards with the same suit)
**three of a kind** (3 cards with the same face/number)
**two pairs** (2 pairs of cards with the same face/number)
**pair** (1 pair of cards with the same face/number)
**high card** (no pair or other combination)

### Design decisions:
The main file contains 2 classes (Deck and Players) that I used to structured the game around, and 9 functions, including main(), of different complexity. Key functions include deal_hands(), evaluate_hand(), determine_winner() - the ones that are tested at the _test file - and betting_round(), which handles the logic for player action, both for the user and for the automated players. A conscious design choice was attempting to handle the card evaluation myself with evaluate_hand(). I eventually did, but was still not able to handle ties between same hand types (e.g., two users had two pairs each). I then decided to import treys to handle the tiebreak, in order to avoid further increasing the complexity of the code. Another conscious choice was handling automated player logic through tiers based on how strong their hands are (strong, medium and weak) with a little bit of randomness to simulate bluffs.

### Known limitations:
After a raise, other players are not required to match the raise to continue in game. There's also no split pot for true ties and no blind escalation. Also, players don't go all-in strategically. These would further increase the code complexity beyond the scope of this project.

### Libraries used:
treys, random, sys
