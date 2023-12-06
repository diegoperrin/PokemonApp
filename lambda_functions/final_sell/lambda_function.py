import json
import boto3
import os
import datatier
import random

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_sell**")
    
    #
    # setup AWS based on config file:
    #
    config_file = 'config.ini'
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
    
    configur = ConfigParser()
    configur.read(config_file)

    #
    # configure for RDS access
    #
    rds_endpoint = configur.get('rds', 'endpoint')
    rds_portnum = int(configur.get('rds', 'port_number'))
    rds_username = configur.get('rds', 'user_name')
    rds_pwd = configur.get('rds', 'user_pwd')
    rds_dbname = configur.get('rds', 'db_name')


    #
    # Grab the saveid of the player
    #

    if "pokemonid" in event:
      pokemonid = event["pokemonid"]
    elif "pathParameters" in event:
      if "pokemonid" in event["pathParameters"]:
        pokemonid = event["pathParameters"]["pokemonid"]
      else:
        raise Exception("requires pokemonid parameter in pathParameters")
    else:
        raise Exception("requires pokemonid parameter in event")
        
    print("pokemonid:", pokemonid)

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
    
  
    #select the pokemon
    sql = "SELECT * FROM pokemon WHERE pokemonid = %s";

    pokemon = datatier.retrieve_one_row(dbConn, sql, [pokemonid])

    if pokemon == ():  # no such saveid
      print("**pokemon doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such pokemonid...")
      }

    #figure out sale price
    rarity = pokemon[4]

    if rarity == "Legendary":
      sale_price = random.randint(50,150)
    else:
      sale_price = random.randint(7,15)


    #find owner of this pokemon (find saveid)
    sql = "SELECT saveid FROM pokedex WHERE pokemonid = %s";

    saveid = datatier.retrieve_one_row(dbConn, sql, [pokemonid])

    if not saveid: # not found
      print("**pokemon doesn't have an owner?, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("pokemon not in pokedex / no owner...")
      }

    update_query = "UPDATE inventory SET coins = coins + %s WHERE saveid = %s"
    rows_modified = datatier.perform_action(dbConn, update_query, [sale_price, saveid])
    

    #now delete the pokemon
    # Delete from the pokemon table for the associated pokemonid
    delete_pokemon_query = "DELETE FROM pokemon WHERE pokemonid = (%s)"
    datatier.perform_action(dbConn, delete_pokemon_query, [pokemonid])

    # Delete from the pokedex table for the specified pokemonid
    delete_pokedex_query = "DELETE FROM pokedex WHERE pokemonid = %s"
    datatier.perform_action(dbConn, delete_pokedex_query, [pokemonid])


    
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #

    #return the sale price for the pokemon
    print("**DONE, **")
    
    return {
      'statusCode': 200,
      'body': json.dumps(sale_price)
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
