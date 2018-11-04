import os

from bot import ScriBot
from scrape import scrape
import markovify

NUM_SCRIPTS = 20

scrape(NUM_SCRIPTS)

scripts = []
DIRECTORY = "data"
for num in range(NUM_SCRIPTS):
    with open(DIRECTORY + "/script" + str(num) + ".txt") as f:
        scripts.append(f.read())

bot = ScriBot(scripts, retain_original=False)
while True:
    x = input("a: ")
    if x == "n":
        exit()
    print(bot.make_sentence())
