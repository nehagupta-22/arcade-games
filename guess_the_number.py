# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

higher = 100
number_of_guesses = 0
number_of_tries = 7

# helper function to start and restart the game
def new_game():
    global secret_number
    secret_number = random.randrange(0, higher)
    print "New game. Range is 0 to " + str(higher) + "."
    print "You have", number_of_tries, "guesses left."
    print

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global higher, number_of_guesses, number_of_tries
    higher = 100
    number_of_guesses = 0
    number_of_tries = 7
    new_game()


def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global higher, number_of_guesses, number_of_tries
    higher = 1000
    number_of_tries = 10
    number_of_guesses = 0
    new_game()
    
def input_guess(guess):
    global secret_number, number_of_guesses
    
    print "Guess was", guess
    
    guess = int(guess)
    if guess == secret_number:
        print "Correct!"
        print
        new_game()
    elif number_of_tries - number_of_guesses == 1:
        print "Sorry, that's wrong! You lost!"
        print
        new_game()
    elif guess > secret_number:
        print "Lower!"
        number_of_guesses += 1
        if number_of_tries - number_of_guesses == 1:
            print "You have 1 guess left."
        else:
            print "You have", number_of_tries - number_of_guesses, "guesses left."
        print
    elif guess < secret_number:
        print "Higher!"
        number_of_guesses += 1
        if number_of_tries - number_of_guesses == 1:
            print "You have 1 guess left."
        else:
            print "You have", number_of_tries - number_of_guesses, "guesses left."
        print
        
# create frame
frame = simplegui.create_frame("guess the Number", 200, 200)

# register event handlers for control elements and start frame

frame.add_button("0-100", range100, 100)
frame.add_button("0-1000", range1000, 100)
frame.add_input("Enter a Guess", input_guess, 200)


# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
