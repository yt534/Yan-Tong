import random


def play_hangman():
    print('\n')
    # print('The game will be available soon.')

    word_list = ['python', 'java', 'kotlin', 'javascript']
    word_selected = word_list[random.randint(0,3)]
    l = len(word_selected)
    output = ['-']*l
    word_guessed = ''.join(output)

    attempts = 8
    letter_guessed = []
    while attempts > 0:
        print('')
        print(''.join(output))
        letter = input('Input a letter:')

        if letter in word_selected and letter not in letter_guessed:
            # letter_guessed.append(letter)
            index = [pos for pos, char in enumerate(word_selected) if char == letter]
            for i in range(len(output)):
                if i in index:
                    output[i]=letter  
        elif len(letter) != 1:
            print('You should input a single letter') 
        elif letter.islower() == False:
            print('It is not an ASCII lowercase letter')
        elif letter in letter_guessed:
            print('You already typed this letter')   
        else:
            print('No such letter in the word')
            attempts -= 1
        letter_guessed.append(letter)
        word_guessed = ''.join(output)
        if word_guessed == word_selected:
            print('You guessed the word!')
            break

    if word_guessed == word_selected:
        print('You survived!')
    else:
        print('You are hanged!')

    # print('\nThanks for playing!')
    # print("We'll see how well you did in the next stage")
    
    
print('H A N G M A N')
f = 0
while f == 0:
    play_exit = input('Type "play" to play the game, "exit" to quit:')
    if play_exit == 'play':
        play_hangman()
    elif play_exit == 'exit':
        f=1
    
        

