from DeckOfCards import *   # Imports DeckOfCards and Cards to be used


print("Welcome to BlackJack!\n")

playagain = 'y'     # This runs the code again if they choose to
uwincount = 0
dwincount = 0
while playagain == 'y':
    
    deck = DeckOfCards()    #sets deck to the deck of cards class
    # print("Unshuffled Deck:")
    # deck.print_deck()       #prints unshuffled deck
    deck.shuffle_deck()
    # print("\nShuffled Deck:")
    # deck.print_deck()       #prints shuffled deck
    print()
    
    # deals two cards to the user
    ucard = deck.get_card()
    ucard2 = deck.get_card()
    print()
    print("Card number 1 is: "+ucard.face+" of "+ucard.suit)
    print("Card number 2 is: "+ucard2.face+" of "+ucard2.suit)
    ucardnumber = 2
    
    # calculates the user's hand score to begin
    uscore = 0
    uscore += ucard.val
    uscore += ucard2.val
    print("Your score is:", uscore)
    print()
    
    # calculates the user's number of aces to begin
    uace = 0
    if ucard.face == "Ace":
        uace += 1
    if ucard2.face == "Ace":
        uace += 1
    
    # deals two cards to the dealer
    dcard = deck.get_card()
    dcard2 = deck.get_card()
    dcardnumber = 2
    
    # calculates the dealer's hand score to begin
    dscore = 0
    dscore += dcard.val
    dscore += dcard2.val
    
    # calculates the dealer's number of aces to begin
    dace = 0
    if dcard.face == "Ace":
        dace += 1
    if dcard2.face == "Ace":
        dace += 1
    
    # while hit is 'y' and score <= 21, ask the user if they want to hit
    hit = 'y'
    while hit == 'y' and uscore < 21:
        hit = input("Would you like a hit?(y/n): ")
        print()
        if hit == 'y':      #if they want a hit, give them another card
            ucard_new = deck.get_card()
            ucardnumber += 1        #keep track of how many cards they have
            print("Card number",ucardnumber,"is: "+ucard_new.face+" of "+ucard_new.suit)
            if ucard_new.face == "Ace": #if the new card is an ace, add it to the count
                uace += 1
            uscore += ucard_new.val     #adjust total score
            if uscore > 21 and uace > 0:        #if they have an ace and busted, drop them 10 and remove their ace from the count
                uscore -= 10
                uace -= 1
            print("Your new score is:", uscore)
            print()
        elif hit == 'n':        #if they don't want to hit, jump out of loop
            break
        else:       #if they didn't answer y or n, then try again
            print("Invalid response. Please respond with 'y' or 'n'")
            hit = 'y' #resets the if loop to see if they want to hit
    
    if uscore > 21: #tell them if they busted
        dwincount += 1
        print("User busted, you lose!")
        
    if uscore <=21:     #if they didn't bust, run the dealers cards
        print("Dealer card number 1 is: "+dcard.face+" of "+dcard.suit)     #reveal dealer cards
        print("Dealer card number 2 is: "+dcard2.face+" of "+dcard2.suit)
        while dscore < 17:  #if they have less than 17, hit
            dcard_new = deck.get_card()
            dcardnumber += 1        #keep track of how many cards are hit
            print("Dealer hits, card number",dcardnumber,"is: "+dcard_new.face+" of "+dcard_new.suit)
            if dcard_new.face == "Ace": #if the new card is an ace, add it to the count
                dace += 1
            dscore += dcard_new.val
            if dscore > 21 and dace > 0: #if the dealer busts and has an ace, subtract 10 and remove an ace
                dscore -= 10
                dace -= 1
        print("Dealer score is:", dscore)   #reveal dealer score after hits
        print()
        
        print("User Score:", uscore)    #reveal final scores
        print("Dealer Score:", dscore)
    if dscore > 21:     #if dealer busts, tell user they won
        uwincount += 1
        print("The dealer busted, you win!")
    if dscore >= uscore and dscore <= 21:   #if dealer is less than or equal to 21 and greater than or equal to the user, dealer wins
        dwincount += 1
        print("The dealer wins with a score of %d!" % (dscore))
    if uscore > dscore and uscore <= 21:    #if user is greater than dealer and less than or equal to 21, the user wins. I could've left this with an else but it helps me understand the logic
        uwincount += 1
        print("The user wins with a score of %d!" % (uscore))
    playagain = input("\nWould you like to play again?(y/n): ") #if they play again, it'll run through the loop
    
    
    
    # I added this after but it counts the amount of wins that they both have and announces a final winner
print("\n\nUser win count:",uwincount)
print("Dealer win count:",dwincount)
if uwincount > dwincount:
    print("You are the overall winner!")
elif dwincount > uwincount:
    print("The dealer is the overall winner!")
else:
    print("It's a tie!")
    
    
print("\n\nThanks for playing!")

