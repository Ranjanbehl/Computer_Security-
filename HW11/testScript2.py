#!/usr/bin/env python3

import os

for i in range(1,51):
    command = "procmail .procmailrc < Mail/junkMail/junkMail_%d" % i
    #print(command)
    os.system(command)
    if os.stat("Mail/recipe_1").st_size > 0:
        print("Test", i, "Passed")
        os.system("> Mail/recipe_1")
    else:
        print("Test", i, "failed")
        if os.stat("Mail/recipe_2").st_size > 0:
            print("went to recipe 2")
        os.system("> Mail/recipe_2")
        if os.stat("Mail/recipe_3").st_size > 0:
            print("went to recipe 3")
        os.system("> Mail/recipe_3")
        if os.stat("Mail/recipe_4").st_size > 0:
            print("went to recipe 4")
        os.system("> Mail/recipe_4")
        exit()

for i in range(51,64):
    command = "procmail .procmailrc < Mail/junkMail/junkMail_%d" % i
    #print(command)
    os.system(command)
    if os.stat("Mail/recipe_2").st_size > 0:
        print("Test", i, "Passed")
        os.system("> Mail/recipe_2")
    else:
        print("Test", i, "failed")
        if os.stat("Mail/recipe_1").st_size > 0:
            print("went to recipe 1")
        os.system("> Mail/recipe_1")
        if os.stat("Mail/recipe_3").st_size > 0:
            print("went to recipe 3")
        os.system("> Mail/recipe_3")
        if os.stat("Mail/recipe_4").st_size > 0:
            print("went to recipe 4")
        os.system("> Mail/recipe_4")
        exit()

for i in range(64,67):
    command = "procmail .procmailrc < Mail/junkMail/junkMail_%d" % i
    #print(command)
    os.system(command)
    if os.stat("Mail/recipe_3").st_size > 0:
        print("Test", i, "Passed")
        os.system("> Mail/recipe_3")
    else:
        print("Test", i, "failed")
        if os.stat("Mail/recipe_1").st_size > 0:
            print("went to recipe 1")
        os.system("> Mail/recipe_1")
        if os.stat("Mail/recipe_2").st_size > 0:
            print("went to recipe 2")
        os.system("> Mail/recipe_2")
        if os.stat("Mail/recipe_4").st_size > 0:
            print("went to recipe 4")
        os.system("> Mail/recipe_4")
        exit()

for i in range(67,75):
    command = "procmail .procmailrc < Mail/junkMail/junkMail_%d" % i
    #print(command)
    os.system(command)
    if os.stat("Mail/recipe_4").st_size > 0:
        print("Test", i, "Passed")
        os.system("> Mail/recipe_4")
    else:
        print("Test", i, "failed")
        if os.stat("Mail/recipe_1").st_size > 0:
            print("went to recipe 1")
        os.system("> Mail/recipe_1")
        if os.stat("Mail/recipe_2").st_size > 0:
            print("went to recipe 2")
        os.system("> Mail/recipe_2")
        if os.stat("Mail/recipe_3").st_size > 0:
            print("went to recipe 3")
        os.system("> Mail/recipe_3")
        exit()