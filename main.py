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
    self.originaldatafile = row[3]
    self.datafilekey = row[4]
    self.resultsfilekey = row[5]

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
# main
#
try:
  print('** Welcome to PokemonApp **')
  print()

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0

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
