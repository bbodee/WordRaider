# WordRaider
A command-line Wordle clone in Python.  Used as a portfolio project from Dataquest.

## Example Output
```text
Welcome to Word Raider, my attempt at rebuild wordle!
A mystery word has been loaded!
There are 5 letters in the word
We are on turn 1 of 6
Guess a 5 letter word! crane 
['_', '_', '_', '_', 'e']
These letters are in the word: {'e'}
These letters are absent from the word: {'n', 'a', 'c', 'r'}
We are on turn 2 of 6
Guess a 5 letter word! stink
['s', '_', '_', '_', 'e']
These letters are in the word: {'t', 's', 'e'}
These letters are absent from the word: {'a', 'i', 'r', 'c', 'n', 'k'}
...
We are on turn 6 of 6
Guess a 5 letter word! spote
Invalid Guess - Not in Valid Guess Library
We are on turn 6 of 6
Guess a 5 letter word! smote
['s', 'm', 'o', 't', 'e']
These letters are in the word: {'t', 'm', 'e', 's', 'o'}
These letters are absent from the word: {'h', 'a', 'i', 'r', 'c', 'n', 'k'}
Congratulations! You guessed correctly in 6 turns! 
Your guesses were ['crane', 'stink', 'shore', 'stone', 'soote', 'smote']
```

## How to Run
- Python 3.9+
- No external dependencies

```bash
git clone https://github.com/bbodee/WordRaider.git
cd WordRaider
python WordRaider.py
```

## How it works
It will read in your guesses as an input.

It will then go through basic validation to make sure the guess is a valid guess:
- Same length as the solution
- Only Alpha values (no numeric or special characters)
- Check if the guess is from an approved list (the valid_guesses file coupled with the answers file)
- If you repeat the same word.

Failing any of these validations will output an error

Once the guess is validated it will then go through scoring.

Scoring is a two pass system, because exact matches take priority over misplaced ones.  So we have pass 1 test
if the letter is correct and the location is correct. Pass 2 tests if the letter is located in the word, but is in 
the wrong spot. Each letter is a 1-to-1 match. So if your guess has 3 "E"s but the answer only has 2 "E"s it will 
say that 2 "E"s are present and 1 "E" is absent.

To ensure the user can see the full picture after each guess, we set up a "saving" mechanism that aggregates
each letter so you can see everything post guess.

## Project Structure
`ref/` is the directory that houses the words.
- answers.txt is past answers from wordle
- valid_guesses.txt is a full list of approved words from wordle.

I got these from cfreshman on github:
- [answers list](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b)
- [valid guesses list](https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c)

## Next Steps
- GUI integration to mimic wordle to practice my UI work.
- "No memory mode" where you lose the prior information and only see the turn output.
- "Hard Mode" any revealed hints must be used in later guesses.
