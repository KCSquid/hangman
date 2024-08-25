import os
import sys
import time
import json
import random
import requests
import colorama as cr

# Makes it easier to do colors
cr.init(autoreset = True)

# Word API (for random words)
word_source = "https://raw.githubusercontent.com/ZionPF/python_class/master/hangman/words.txt"

# Dictionary API (for definitions)
dictionary_api = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# Create a player to store name, chances and guesses
class Player:
  def __init__(self, name: str, chances, guesses):
    self.name = name
    self.chances = chances
    self.guesses = guesses

player = Player(input("What is your name? "), 6, set())

# Create a typing animation (to look cool)
def type(input: str) -> None:
  for character in input:
    time.sleep(0.05)
    sys.stdout.write(character)
    sys.stdout.flush()

  sys.stdout.write("\n")
  sys.stdout.flush()

# Use a Dictionary API to get the definition
def get_defintion(word):
  response = requests.get(dictionary_api + word).text

  data = json.loads(response)

  return data[0]["meanings"][0]["definitions"][0]["definition"]

def reveal(chosen, definition):
  type(f"\nThe word was: {chosen.upper()}")
  type(f"Definition: {definition}\n")

# Start the game
def run_game():
  # Set the variables
  player.chances = 6
  player.guesses = set()
  
  correct_letters = set()
  response = requests.get(word_source)
  words = response.content.split()

  while True:
    # Choose the random word, format it, and set it's definition
    chosen = str(random.choice(words)).replace("b'", "").replace("'", "")

    if chosen[:-1] != "s":
      chosen = chosen[:-1]
  
    try:
      definition = get_defintion(chosen)
      break
    except KeyError:
      # Unkown word -> restarts to find new
      continue

  os.system("clear")

  # Start a while loop for guessing letters
  while True:
    length = ""
    
    for i in range(0, len(chosen)):
      try:
        if i in correct_letters:
          length += chosen[i]
        else:
          length += "_"
      except IndexError:
        length += "_"

    # If player wins
    if chosen == length:
         os.system("clear")
         type(f"YOU WON!")
         time.sleep(0.5)
         reveal(chosen, definition)
         break

    # Style & Format the text
    # (Format Set)
    formatted_guesses = str(player.guesses).replace('{', "").replace("'", "").replace('}', "")

    if formatted_guesses == "set()":
      formatted_guesses = ""

    # (Style guesses with colors & add image)
    if player.chances == 6:
      print(f"{cr.Fore.GREEN}{player.chances} guesses left")
      print("  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========")
      
    elif player.chances == 5:
      print(f"{cr.Fore.GREEN}{player.chances} guesses left")
      print("  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========")
      
    elif player.chances == 4:
      print(f"{cr.Fore.YELLOW}{player.chances} guesses left")
      print("  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========")
      
    elif player.chances == 3:
      print(f"{cr.Fore.YELLOW}{player.chances} guesses left")
      print("  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========")

    elif player.chances == 2:
      print(f"{cr.Fore.RED}{player.chances} guesses left")
      print("  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========")
      
    elif player.chances == 1:
      print(f"{cr.Fore.RED}{player.chances} guesses left")
      print("  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========")
      

    # Print out the important game texts
    print(f"{cr.Fore.CYAN}You already guessed: {formatted_guesses}")
    print(f"{cr.Fore.MAGENTA}Known letters: {length} ({len(length)})\n\n")
      
    letter = input("Guess a letter: ").lower()

    if len(letter) == 1 and ord(letter) > 64 and ord(letter) < 128:
      os.system("clear")
  
      # Check if the letter is correct
      if letter in chosen:
        for i in range(0, len(chosen)):
          if chosen[i] == letter:
            correct_letters.add(int(i))
      elif letter in player.guesses:
        pass
      else:
        player.chances -= 1
  
        # Player loses
        if player.chances == 0:
          os.system("clear")
          print("  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========")
          type(f"GAME OVER. You were hanged and ended up dying a slow death :l")
          time.sleep(0.5)
          reveal(chosen, definition)
          break

      player.guesses.add(letter)
    else:
      os.system("clear")
      type("You can only guess a letter")

# Intro
if __name__ == "__main__":
  os.system("clear")
  type(f"Welcome to Hangman, {player.name.upper()}!")
  time.sleep(0.5)
  
  while True:
    type("Would you like to start a new game?\n\n")
    
    while True:
      # Start game?
      answer = input("Yes/No: ").lower()
  
      # (Yes)
      if answer == "y" or "yes" in answer:
        type("Okay! Starting...")
  
        time.sleep(1)
        os.system("clear")
        run_game()
        type("Would you like to start a new game?\n\n")
  
      # (No) 
      elif answer == "n" or "no" in answer:
        type("Okay, goodbye!")
        
        time.sleep(0.5)
        exit(0)
      else:
        type("Please only enter \"Yes\" or \"No\"\n\n")
