
attempts = 6
playing = True
correct = False
word = input("Please type in a word:  ")
display = ["_"] * len(word)
while playing:
    print(display)
    guess = input("Type in a letter")
    for index,letters in enumerate(word):
        if guess.lower() == letters.lower():
            display[index] = letters
            correct = True
            break

        elif guess == 'stop':
            playing = False
            break
        elif not guess:
            correct = True
        else:
            correct = False
    if correct == False:
        attempts = attempts-1
        print(f"you have {attempts} left ")

    if attempts == 0:
        print("You have failed the game")
        break
    
    if "".join(display) == word:
        print("You win!")
        playing = False
