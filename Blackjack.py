import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True
# Trying something

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        pass

    def get_suit(self):
        return self.suit
        pass

    def get_rank(self):
        return self.rank
        pass

    def __str__(self):
        print("%s of %s" % (self.rank, self.suit))
        pass


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))  # Append a card to the deck
                pass

    def __str__(self):
        for card in self.deck:
            card.__str__()
        pass

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

        pass


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        # Add a card to the hand
        self.cards.append(card)
        self.value += values[card.rank]
        # Checks to see if the card is an ace and how to fix it if its over 21
        if values[card.rank] == 11:
            self.aces += 1
            if self.value > 21:
                self.value -= 10
        pass

    def draw(self, hidden):
        # Don't show the first card of the dealer until specified
        if hidden:
            starting_card = 1
        else:
            starting_card = 0

        for x in range(starting_card, len(self.cards)):
            self.cards[x].__str__()
        pass


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        self.winnings = 0

    def win_bet(self):
        self.total += self.bet
        self.winnings += self.bet
        pass

    def lose_bet(self):
        self.total -= self.bet
        self.winnings -= self.bet
        pass

    def show_bet(self):
        return self.bet
        pass


def take_bet():
    bet_input = int(input("How much would you like to bet? (Enter a whole number)"))
    if 1 <= bet_input <= player_chips.total:
        player_chips.bet = bet_input
    else:
        print("You only have" + player_chips.total + " chips remaining")

    pass


def hit(deck, hand):
    if hand.value <= 21:
        new_card = deck.deal()
        hand.add_card(new_card)

    pass


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    if playing:
        print("Would you like to Stand(s) or Hit(h)")
        choice = input().lower()

        # If they want to hit run the hit function
        if choice == 'h':
            hit(deck, hand)
            return 'h'
        else:
            playing = False

    pass


def show_some(p, d):
    print("Players hand is: ")
    p.draw(hidden=False)

    print("Players hand total is: " + p.total)

    print("Dealers hand is: ")
    d.draw(hidden=True)

    pass


def show_all(p, d):
    print("Players hand is: ")
    p.draw(hidden=False)

    print("Players hand total is: " + p.total)

    print("Dealers hand is: ")
    d.draw(hidden=False)

    pass


def player_busts(player_chips):
    print("BUSTED! You lose")
    player_chips.total -= player_chips.bet
    pass


def player_wins(player_chips):
    print("You beat the Dealer. YOU WIN!")
    player_chips.total += player_chips.bet
    pass


def dealer_busts(player_chips):
    print("Dealer Busted. YOU WIN!")
    player_chips.total += player_chips.bet
    pass


def dealer_wins(player_chips):
    print("Dealer Wins, you lose")
    player_chips.total -= player_chips.bet
    print("PLAYER CHIPS TOTAL = ", player_chips.total)
    pass


def push():
    print("It's a tie, push!")
    pass


# *************************** Game Begins Here ***************************
playAgain = True
# Create & shuffle the deck, deal two cards to each player
deck = Deck()
deck.shuffle()

while playAgain:
    # Print an opening statement
    print("Welcome to BlackJack! Try and get as close to 21 as you can without going over!\nDealer stands on a 17. "
          "Aces are either 1 or 11\n\n")

    # playing = True
    while playing:  # recall this variable from our hit_or_stand function

        # get the player beginning 2 cards
        card1 = deck.deal()
        card2 = deck.deal()
        player = Hand()
        player.add_card(card1)
        player.add_card(card2)

        # get the dealer beginning 2 cards
        card1 = deck.deal()
        card2 = deck.deal()
        dealer = Hand()
        dealer.add_card(card1)
        dealer.add_card(card2)

        # Set up the Player's chips
        player_chips = Chips()

        # Prompt the Player for their bet

        take_bet()
        hitting = 'h'
        while hitting == 'h':

            # Show cards (but keep one dealer card hidden)
            print("Player has: ")
            player.draw(hidden=False)
            print("PLAYER SCORE: ", player.value)

            print("Dealer has: ")
            dealer.draw(hidden=True)

            # Prompt for Player to Hit or Stand
            hitting = hit_or_stand(deck, player)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            playerBust = False
            if player.value > 21:
                player_busts(player_chips)
                playerBust = True
                break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        while playerBust == False:
            while dealer.value < 17:
                hit(deck, dealer)

            # Show all cards
            print("\nPlayer has: ")
            player.draw(hidden=False)

            print("Dealer has: ")
            dealer.draw(hidden=False)

            print("PLAYER SCORE: ", player.value)

            # Run different winning scenarios
            if dealer.value > 21:
                dealer_busts(player_chips)
                playing = False
            elif dealer.value > player.value:
                dealer_wins(player_chips)
                playing = False
            elif dealer.value < player.value:
                player_wins(player_chips)
                playing = False
            else:
                push()
                playing = False

            playerBust = True

        # Inform Player of their chips total
        print("Your chip total is: ", player_chips.total)

        # Ask to play again
        ra = input("Would you like to continue playing? (y or Y for yes, anything else for no)")
        if ra == 'y' or ra == 'Y':
            playing = True
        else:
            playing = False
    break
