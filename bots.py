import random
# list with actions that have already been suggested
bot_list = ["Joy", "Sadness", "Fear", "Anger"]
used_words = []

# Extract the action from the message
def split(msg):

    # common library
    library = ["play", "eat", "read", "sing", "fight", "gossip", "complain", "quarrel"]

    # splits the words
    words = msg.split()

    # returns the common word
    for word in words:
        if word in library:
            return word


# Runs when called in client.py
def bot(msg, bot_name):
    # calls upon the split function and set "word" to be the common action
    word = split(msg)

    # finds the bot that has been called and get a response
    if bot_name == "Joy":
        return joy(word)
    elif bot_name == "Sadness":
        return sadness(word)
    elif bot_name == "Fear":
        return fear(word)
    elif bot_name == "Anger":
        return anger(word)
    else:
        pass


def joy(word):

    # Library of good and bad things for this bot
    good_things = ["play", "eat", "read", "sing"]
    bad_things = ["fight", "gossip", "complain", "quarrel"]

    # Run this code if word is in good_things
    if word in good_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"Yes! I love to {word}."
        else:
            return "YES, YES, YES"
    # Run this code if word is in bad_things
    elif word in bad_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"No! {word}ing is wrong."
        else:
            return "No, i told you that"
    # Run if the word is not defined in the bots library
    else:
        return "Sorry! I didn't quite get you."


def sadness(word):

    # Library of good and bad things for this bot
    good_things = ["play", "eat", "read", "sing"]
    bad_things = ["fight", "gossip", "complain", "quarrel"]

    # Run this code if word is in good_things
    if word in good_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"Maybe {word}ing will cheer me up."
        else:
            return f"OK! I will {word}"
    # Run this code if word is in bad_things
    elif word in bad_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"{word}ing makes me sad."
        else:
            return "Do you really want me to cry?"
    # Run if the word is not defined in the bots library
    else:
        return "Everything i boring."


def fear(word):
    # Library of good and bad things for this bot
    bad_things = ["play", "eat", "read", "sing"]
    good_things = ["fight", "gossip", "complain", "quarrel"]

    # Run this code if word is in good_things
    if word in good_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"I am too afraid to {word}. It is little scary."
        else:
            return f"I told you! I am afraid to {word}"
    # Run this code if word is in bad_things
    elif word in bad_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"No {word}ing for me."
        else:
            return "Nope 3x"
    # Run if the word is not defined in the bots library
    else:
        return "That sounds dangerous!"


def anger(word):
    # Library of good and bad things for this bot
    bad_things = ["play", "eat", "read", "sing"]
    good_things = ["fight", "gossip", "complain", "quarrel"]

    suggestion = ["throwing eggs", "pepper spraying", "stare someone to death", "hit and run"]

    # Run this code if word is in good_things
    if word in good_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            return f"Finally something sensible. I love to {word}."
        else:
            return f"I don't like people asking me same thing twice"
    # Run this code if word is in bad_things
    elif word in bad_things:
        # If the word had not been used earlier, add it in the "used_words" list and return the response.
        if word not in used_words:
            used_words.append(word)
            # Denies and suggests a new random activity from the "suggestion" list
            return f"I am not down for it, but what about {random.choice(suggestion)}?"
        else:
            return f"Don't ask me to {word} again."
    # Run if the word is not defined in the bots library
    else:
        return "DON'T ANGRY MEEEE!!!"