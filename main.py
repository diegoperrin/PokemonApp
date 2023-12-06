#
# Client-side python app for pokemon app, which is calling
# a set of lambda functions in AWS through API Gateway.
#
# Authors:
#   Diego Perrin
#   Northwestern University
#   CS 310, Final Project
#   Fall 2023
#

import requests
import jsons

import uuid
import pathlib
import logging
import sys
import os
import base64
import time

from configparser import ConfigParser


############################################################
#
# classes
#
class SaveFile:

  def __init__(self, row):
    self.saveid = row[0]
    self.trainername = row[1]

class Inventory:

  def __init__(self, row):
    self.saveid = row[0]
    self.pokeballs = row[1]
    self.coins = row[2]


class Pokedex:

  def __init__(self, row):
    self.saveid = row[0]
    self.pokemonid = row[1]

class Pokemon:

  def __init__(self, row):
    self.pokemonid = row[0]
    self.name = row[1]
    self.nickname = row[2]
    self.type = row[3]
    self.rarity = row[4]
    self.level = row[5]

class AllPokemon:

  def __init__(self, row):
    self.defaultid = row[0]
    self.name = row[1]
    self.type = row[2]
    self.rarity = row[3]

#####
# initial
def initial():
  """
  Prompts the user to load game, start a new game or delete a save
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0,1, 2 or 3)
  """
  print()
  print(">> Welcome to the Pokemonapp!")
  print("   1 => New Game")
  print("   2 => Load Game")
  print("   3 => Delete Game Save")
  print("   0 => Exit")

  cmd = input()
  
  if cmd == "":
    cmd = -1
  elif not cmd.isnumeric():
    cmd = -1
  else:
    cmd = int(cmd)
  
  return cmd


######
# gameplay 

def gameplay():
  
  print()
  print(">> What would you like to do?")
  print("   1 => View Inventory")
  print("   2 => View Pokedex")
  print("   3 => Catch Pokemon")
  print("   4 => Rename Pokemon")
  print("   5 => Sell Pokemon")
  print("   6 => Buy Pokeballs")

  print("   0 => Exit")

  cmd = input()

  if cmd == "":
    cmd = -1
  elif not cmd.isnumeric():
    cmd = -1
  else:
    cmd = int(cmd)

  return cmd
  
  
#######
# new game
def new_game(baseurl):

  print("Welcome Trainer! Let's start your journey! Please enter your name:")
  trainername = input("> ")

  try:
    #
    # call the web service:
    #

    api = '/new_game'
    url = baseurl + api + '/' + trainername

    res = requests.post(url)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return

    #worked!
    saveid = res.json()
    saveid = str(saveid)
    print()
    print("Welcome, " + trainername + "! (saveid: " + saveid + ")")
    print("You can now start your journey!")
    return saveid

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


def load_game(baseurl):

  print("Welcome Back Trainer! Please enter your name:")
  trainername = input("> ")
  
  try:
    #
    # call the web service:
    #
  
    api = '/load_game'
    url = baseurl + api + '/' + trainername
  
    res = requests.get(url)
  
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return
  
    #worked!
    saveid = res.json()
    saveid = saveid[0]
    saveid = str(saveid)
    print()
    print("Welcome back, " + trainername + "! (saveid: " + saveid + ")")
    print("Let's get back to it!")
    return saveid
  
  except Exception as e:
    logging.error("load_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


#######
# delete

def delete(baseurl):

  print("Please enter the Trainer name of the game you want to delete:")

  trainername = input("> ")

  print("Are you sure you want to do this? (y/n)")
  confirmation = input("> ")
  confirmation = confirmation.lower()
  
  if confirmation != "y":
    print("Aborting...")
    return
  
  try:
    #
    # call the web service:
    #
    api = '/delete'
    url = baseurl + api + '/' + trainername

    res = requests.delete(url)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #worked
    body = res.json()
    msg = body
    print()
    print(msg)
    print(trainername + " has been deleted.")

    return

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

####
# inventory
def inventory(baseurl, saveid):

  try:
    #
    # call the web service:
    #
    api = '/inventory'
    url = baseurl + api + '/' + saveid

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    body = res.json()

    #
    # let's map to a inventory item
    #
    print()
    items = Inventory(body)

    pokeballs = str(items.pokeballs)
    coins = str(items.coins)
    print("**Inventory**")
    print()
    print("You have " + pokeballs + " pokeballs and " + coins + " coins.")

    return

  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


####
# pokedex
def pokedex(baseurl, saveid):

  try:
    #
    # call the web service:
    #
    api = '/pokedex'
    url = baseurl + api + '/' + saveid

    res = requests.get(url)
    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return


    body = res.json()
    if not body:
      print()
      print("No pokemon found.")
    #
    # let's map each row into a Pokemon object:
    #
    pokemons = []
    for row in body:
      pokemon = Pokemon(row)
      pokemons.append(pokemon)
  


    for i, pokemon in enumerate(pokemons, 1):
      print()
      num = str(i)
      
      if pokemon.nickname != "none":
        print(num + ") " + pokemon.nickname + " (" + pokemon.name + ")"  )
      else:
        print(num + ") " + pokemon.name )
      print("ID:", pokemon.pokemonid)
      print("Type:", pokemon.type)
      print("Rarity:", pokemon.rarity)
      print("Level:", pokemon.level)

    #
    return


  except Exception as e:
    logging.error("users() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

#######
# catch
def catch(baseurl, saveid):
  print()
  print("You throw a pokeball into the tall grass..." )

  try:
    #
    # call the web service:
    #

    api = '/catch'
    url = baseurl + api + '/' + saveid

    res = requests.post(url)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return

    #worked!

    body = res.json()
    pokemon = AllPokemon(body)
    print()

    if pokemon.rarity == "Legendary":
      print("wait a minute...")
      print()
      time.sleep(2)
      print("this is no ordinary pokemon...")
      print()
      time.sleep(2)
      print("it's a legendary pokemon!")
      print()
      time.sleep(2)

    print("You caught a wild " + pokemon.name + "!")

    return 

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

#######
# sell
def sell(baseurl, saveid):
  print()
  print("Which pokemon would you like to sell?")
  print("Please enter the pokemon's ID number:")

  pokemonid = input("> ")
  try:
    #
    # call the web service:
    #
    data = {"user_saveid": saveid}
    
    api = '/sell'
    url = baseurl + api + '/' + pokemonid

    res = requests.post(url, json=data)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return

    #worked!

    saleprice = res.json()
  
    print()
    
    print("Your pokemon has been sold for " + str(saleprice) + " coins!")

    return 

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

#######
# buy
def buy(baseurl, saveid):
  print()
  print("How many pokeballs would you like to buy?")
  print("Each pokeball costs 10 coins.")
  pokeball_amount = input("> ")
  try:
    #
    # call the web service:
    #
    data = {"pokeball_amount": pokeball_amount}

    api = '/buy'
    url = baseurl + api + '/' + saveid

    res = requests.post(url, json=data)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return

    #worked!

    print("You have bought " + pokeball_amount + " pokeballs!")

    return 

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


##########
#rename
def rename(baseurl, saveid):
  print()
  print("Which pokemon would you like to rename?")
  print("Please enter the pokemon's ID number:")
  pokemonid = input("> ")
  
  print("What would you like to rename it to?")
  nickname = input("> ")
  
  try:
    #
    # call the web service:
    #
    data = {"nickname" : nickname, "user_saveid": saveid}

    api = '/rename'
    url = baseurl + api + '/' + pokemonid

    res = requests.post(url, json=data)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
        sys.exit(0)
      #
      return

    #worked!
    print("Your pokemon has been renamed to " + nickname + "!")

    return 

  except Exception as e:
    logging.error("new_game() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
#####
# main
#
try:
  print('**PokemonApp**')

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0
  config_file = 'pokemonapp-client-config.ini'
  configur = ConfigParser()
  configur.read(config_file)
  baseurl = configur.get('client', 'webservice')

  #
  # make sure baseurl does not end with /, if so remove:
  #
  if len(baseurl) < 16:
    print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
    sys.exit(0)

  lastchar = baseurl[len(baseurl) - 1]
  if lastchar == "/":
    baseurl = baseurl[:-1]

  #
  # main processing loop:
  #

  ## Initial loop
  cmd = initial()
  saveid = -999

  while cmd != 0:
    #
    if cmd == 1:
      saveid = new_game(baseurl)
      break
    elif cmd == 2:
      saveid = load_game(baseurl)
      break
    elif cmd == 3:
      delete(baseurl)
    elif cmd == 0:
      print("Exiting...")
      sys.exit(0)
    else:
      print("** Unknown command, try again...")
    #
    cmd = initial()


  ### Gameplay loop
  cmd = gameplay()

  while cmd != 0:
    #
    if cmd == 1:
      inventory(baseurl, saveid)
    elif cmd == 2:
      pokedex(baseurl, saveid)
    elif cmd == 3:
      catch(baseurl, saveid)
    elif cmd == 4:
      rename(baseurl, saveid)
    elif cmd == 5:
      sell(baseurl,saveid)
    elif cmd == 6:
      buy(baseurl,saveid)
    elif cmd == 0:
      print("Exiting...")
      sys.exit(0)
    else:
      print("** Unknown command, try again...")
    #
    cmd = gameplay()
  #
  # done
  #
  print()
  print('** done **')
  sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)
