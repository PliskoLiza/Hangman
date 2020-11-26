# Problem Set 2, hangman.py
# Name: Плиско Єлизавета, КМ-03, ФПМ
# Collaborators:Рутов Олег, КМ-03, ФПМ
# Time spent: 9 годин

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"
############################


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    N = 0
    for i in secret_word:
        if i in letters_guessed:
            N += 1
    if N == len(secret_word):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word_spaces = ''
    for l in secret_word:
        if l in letters_guessed:
            word_spaces += l
        else:
            word_spaces += '_ '
    return word_spaces


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    for i in letters_guessed:
        all_letters = all_letters.replace(i, "")
    return all_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    trigger: string, the letter to switch the versions of the game.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    chance = 6
    warnings = 3
    vowel_list = ['a', 'e', 'u', 'i', 'o']
    print(f'You have {warnings} warnings left.')
    print('-' * 40)
    while not (is_word_guessed(secret_word, letters_guessed)) and chance > 0:
        print(f'You have {chance} guesses left.')
        print(get_available_letters(letters_guessed))
        letter = input('Please guess a letter: ').lower()
        if (not letter.isalpha()) or (letter in letters_guessed):
            if not letter.isalpha():
                print('Oops! That is not a valid letter. ', end='')
            else:
                print("Oops! You've already guessed that letter. ", end='')
            if warnings <= 0:
                chance -= 1
                print(f'You have no warnings left so you lose one guess: '
                      f'{get_guessed_word(secret_word, letters_guessed)}')
            else:
                warnings -= 1
                print(f'You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)} ')
        else:
            letters_guessed.append(letter)
            if letter not in secret_word:
                if letter in vowel_list:
                    chance -= 2
                else:
                    chance -= 1
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
        print('-' * 40)

    if chance <= 0:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    else:
        total_score = chance * len(set(secret_word))
        print(f'Congratulations, you won! Your total score for this game is: {total_score}')


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(my_word) == len(other_word):
        for i in range(0, len(my_word)):
            if my_word[i] != '_':
                if my_word[i] != other_word[i] or my_word.count(my_word[i]) != other_word.count(my_word[i]):
                    return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
    if len(matches) == 0:
        return 'No matches found'
    else:
        return str(matches).replace('[', '').replace(']', '').replace("'", '').replace(',', '')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    chance = 6
    warnings = 3
    vowel_list = ['a', 'e', 'u', 'i', 'o']
    print(f'You have {warnings} warnings left.')
    print('-' * 40)
    while not (is_word_guessed(secret_word, letters_guessed)) and chance > 0:
        print(f'You have {chance} guesses left.')
        print(get_available_letters(letters_guessed))
        letter = input('Please guess a letter: ').lower()
        if letter == '*':
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed).replace(' ', '')))
        elif (not letter.isalpha()) or (letter in letters_guessed):
            if not letter.isalpha():
                print('Oops! That is not a valid letter. ', end='')
            else:
                print("Oops! You've already guessed that letter. ", end='')
            if warnings <= 0:
                chance -= 1
                print(f'You have no warnings left so you lose one guess: '
                      f'{get_guessed_word(secret_word, letters_guessed)}')
            else:
                warnings -= 1
                print(f'You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)} ')
        else:
            letters_guessed.append(letter)
            if letter not in secret_word:
                if letter in vowel_list:
                    chance -= 2
                else:
                    chance -= 1
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
        print('-' * 40)

    if chance <= 0:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    else:
        total_score = chance * len(set(secret_word))
        print(f'Congratulations, you won! Your total score for this game is: {total_score}')

#hangman(secret_word)

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    #############################################
###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    #hangman(secret_word)



