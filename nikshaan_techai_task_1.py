import random
from collections import Counter

class colors:
    green = '\033[92m'
    yellow = '\033[93m'
    white = '\033[97m'

def prepare_word_set():
    try:
        word_set = set()

        with open("./valid-wordle-words.txt", 'r') as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    word_set.add(word)

        return word_set
    
    except FileNotFoundError:
        print("File does not exist!")
        return None

def word_checker(guess, secret_word):
    guessed = True
    secret_counter = Counter(secret_word)
    result = ['#'] * 5

    for i in range(5):
        if guess[i] == secret_word[i]:
            result[i] = f'{colors.green + guess[i] + colors.white}'
            secret_counter[guess[i]] -= 1
    
    for letter in secret_counter:
        if secret_counter[letter] != 0:
            guessed = False
            break

    if guessed == False:
        for i in range(5):
            if result[i] == '#':
                if guess[i] in secret_word and secret_counter[guess[i]] > 0:
                    result[i] = f'{colors.yellow + guess[i] + colors.white}'
                    secret_counter[guess[i]] -= 1
                else:
                    result[i] = f'{colors.white + guess[i]}'

    return ["".join(result), guessed]

def wordle(words, score):
    secret_word = random.choice(list(words))
    # print(secret_word)
    guess_count = 6
    attempts = []

    while guess_count != 0:
        guess = input(f"Attempts left: {guess_count}. Enter your guess: ").strip().lower()

        if len(guess) != 5:
            print("Word needs to have only 5 letters! Try again")
            continue
        elif guess not in words:
            print("Word does not exist in our set. Try again")
            continue

        result = word_checker(guess, secret_word)
        attempts.append(result[0])

        print("Attempts till now:")
        for attempt in attempts:
            print(attempt)

        if result[1] == True:
            print(f"You have guessed {secret_word} correctly!")
            score += 1
            return score

        guess_count -= 1
    
    if guess_count == 0:
        print(f"Attempts over! Correct word was: {secret_word}")
        return score

words = prepare_word_set()

print("WELCOME TO WORDLE!")
score = 0
game = True

while game:
    print("NEW GAME STARTED")

    score = wordle(words, score)
    print(f"Your score is: {score}")

    ans = ""
    while ans not in ['y', 'n']:
        ans = input("Do you want to play again? (y/n): ").strip().lower()
        if ans == 'n':
            print(f"GAME OVER. FINAL SCORE: {score}")
            game = False
            break
        elif ans == 'y':
            break
        else:
            print("Invalid answer try again!")
            