import random      #brings in random for shuffling


class Card(): #creates cards class
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.val = value
        
    def __str__(self):
        return self.face + " of " + self.suit + ", value: " + str(self.val)


class DeckOfCards():    #creates deck of cards class
    def __init__(self):
        self.deck = []
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.play_idx = 0
        
        for suit in self.suits:
            i = 0
            for i in range(len(self.faces)):
                self.deck.append(Card(suit, self.faces[i], self.values[i]))
                
                
    def shuffle_deck(self):     #allows us to shuffle deck
        random.shuffle(self.deck)
        self.play_idx = 0
        
    def print_deck(self):       #allows us to print deck
        for card in self.deck:
            print(card.face, "of", card.suit, end=", ")
        print("---")
        
    def get_card(self):     #allows us to get a card from the deck
        self.play_idx += 1
        return self.deck[self.play_idx - 1]
        
        

