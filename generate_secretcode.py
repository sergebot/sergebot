
import random


def secret_code_gen():
    names_list = ["monkey","ant","donkey","dog","cat","superman","batman","hulk",\
    "ironman","fist","strange","lion","tiger","paris","denver","newyork","apple",\
    "carl","tommy","potter","wade","halliday","watts","tesla","edison","iphone",\
    "radio","burger","chandler","car","bottle","martini","bond","time","lennon",\
    "queen","sinatra","lol"]

    final_str = names_list[random.randint(0,len(names_list)-1)] + str(random.randint(1000,9999))
    return str(final_str)

if __name__ == "__main__":
    for x in range(100):
        print(secret_code_gen())
