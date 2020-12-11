import random
import os
import time
import const

#number of guesses we have
lives = 7

#start timer
time_start = time.time()

#guessed letter sets
letters = set()
bad_letters = set()

#other global variables
drawn = ""
scores = []
lives_crnt = lives
guesses = 0

def new_city_new_life():
    global drawn
    global lives_crnt
    global time_start
    global scores
    global guesses

    #empty sets, lists, vars
    letters.clear()
    bad_letters.clear()
    scores = []
    guesses = 0
    #set current lives to predefined number
    lives_crnt = lives
    #reset timer
    time_start = time.time()
    #get random number and use it as index of puzzle words list,to get random one
    rand_numb = random.randint(0, len(capitals_list)-1)
    drawn = capitals_list[rand_numb]

 #check how many spaces we need to make columns straight
def fill (check, length, filler, multipler):
    space = ""
    for i in range(len(check)*multipler, length):
        space += filler
    return space

#play again?
def again():
    answer = input("\tDo you want to play again? Yes/no ")
    if answer.lower() == "yes":

        #pick new city and restart variables
        new_city_new_life()
        #start game
        game()

#get user name and display highscores
def highscores():
    global scores
    global drawn

    #count time passed and print it
    time_end = time.time() - time_start
    your_time = "{0:.2f}".format(time_end)
    print("\n\tYour time: " + your_time + " s")

    name = input("\tPlease enter your name: ").strip()[:15]
    print()
    name = name.replace(";", "")

    if name == "":
        name = "Anonymous"
    
    #define sorting by second list column in 2D list
    def sortBySecond(elem):
        return elem[1]
    
    #open file with scores
    with open('scores.txt', "r+") as f:
        for line in f:
            entry = line.split(";")
            scores.append(entry)
        scores.append([name, your_time, drawn, str(guesses) + "\n"])
        scores.sort(key=lambda x: float(x[1]))

        #update highscore list in file / overwrite it
        f.seek(0)
        for row in scores:
            f.write(";".join(map(str,row)))
            #f.write("\n")
        f.truncate()

    #highlight our score with arrow
    def highlight(row):
        if row[0] == name and row[1] == your_time:
            return "\t█▒ -->  "
        else:
            return "\t█▒\t"

    #display highscores nicely
    print(const.hc_top)
    for row in scores:
        print(highlight(row), end="")
        print(row[0] + fill(row[0], 22, " ",1) + str(row[1]) + fill(row[1], 22, " ",1) + row[2] + fill(row[2], 22, " ",1) + str(row[3]).strip() + "\t█▒")
    print(const.hc_bottom)
    
#show animation
def animate():
    global scores
    animation_delay = 0.3

    os.system('clear')
    print(const.win_text3)
    time.sleep(animation_delay + 0.2)

    for i in range(0,4):
        os.system('clear')
        print(const.win_text1)

        time.sleep(animation_delay)
        os.system('clear')
        print(const.win_text2)
        time.sleep(animation_delay)

    os.system('clear')
    print(const.win_text3)

#define WINING, display animation after we solve the puzzle
def win():
    animate()
    highscores()
    again()

#this shows after we run out of chances/lives
def lose():
    os.system('clear')
    print("\n\tNo more chances!\n\tGAME OVER")
    print(const.lose_text)
    again()

def pause():
    input("\tPress any key to continue")

################################# DEFINE MAIN GAME FUNCTION #############################################
def game():

    global drawn
    global lives_crnt
    global guesses

    #show hidden soltion in top right
    print("\t\t\t\t\t\t\t\t\tpsst... " + drawn)

    #clear screen to draw it again and print ascii art logo
    os.system('clear')
    print(const.hangman_banner)

    uncovered = 0

    #print list with hidden characters in one line
    print("\t", end="")
    for i in range(0, len(drawn)):
        if drawn[i].lower() in letters:
            print(drawn[i] + ' ', end="")
            uncovered += 1
        else: 
            print("_ ", end="")
        if drawn[i].lower() in letters == " ":
                print("  ", end="")

    #print as many blank spaces as needed to keep ASCII art in correct place
    print(fill(drawn, 74, " ", 2), end="")
    
    #ascii art footer
    print(const.hangman_footer)

    #if all letters are uncovered call win()
    if uncovered == len(drawn):
        win()
        return
    
    print("""\tGuess a letter to uncover it. If you know the capital city, just type it! 
    \tYou have """ + str(lives_crnt) + """ chances left!""")

    #check if there are any bad letter guesses
    if len(bad_letters) != 0:
        #print wrongly guessed letters
        print("\tUsed letters: ", end="")
        for x in bad_letters:
            print(x + " ", end="")
        print()

    #ask for guess in input
    guess = input("\n\tYour guess: """).strip()
    
    #number of guesses
    guesses += 1

    #if user typed 1 character
    if len(guess) == 1:
        l = guess.lower()

        if l in letters or l in bad_letters:
            print("\t!!! You already tried that !!!\n")
            pause()
        elif l in drawn or l.upper() in drawn:
            letters.add(l)
            print("\tCorrect!\n")
            pause()
        else:
            print("\tWRONG! You lost 1 chance.")
            lives_crnt -= 1
            bad_letters.add(l)
            print()
            pause()

    #if user typed a word and correctly solved the puzzle
    elif guess.lower() == drawn.lower():
        win()
        return
    #if user forgot to type answer
    elif len(guess) == 0:
        print("\t!!! Enter your guess !!!\n")
        pause()
    #if user typed a word, but it's incorrect
    else:
        print("\n\tWRONG! You lost 2 chances.")
        lives_crnt -= 2
        pause()

    if lives_crnt > 0:
        game()
    else:
        lose()
        return

#open file with phrases
with open('capitals.txt') as f:
    capitals_list = f.readlines()
capitals_list = [x.strip() for x in capitals_list] 

################## SET STARTING PARAMS #############
new_city_new_life()
################## START THE GAME ##################
game()

