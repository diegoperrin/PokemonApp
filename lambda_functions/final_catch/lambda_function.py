import json
import boto3
import os
import datatier
import random

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_catch**")
    
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

    if "saveid" in event:
      saveid = event["saveid"]
    elif "pathParameters" in event:
      if "saveid" in event["pathParameters"]:
        saveid = event["pathParameters"]["saveid"]
      else:
        raise Exception("requires saveid parameter in pathParameters")
    else:
        raise Exception("requires saveid parameter in event")
        
    print("saveid:", saveid)

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
    
    #
    # see if we have enough pokeballs:
    #

    sql = "SELECT * FROM inventory WHERE saveid = %s";

    row = datatier.retrieve_one_row(dbConn, sql, [saveid])

    if row == ():  # no such saveid
      print("**saveid doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such saveid...")
      }
    
    pokeball_count = row[1]

    if pokeball_count == 0 :  # not enough
      print("**not enough pokeballs, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("out of pokeballs! buy more")
      }

    #update num pokeballs

    update_query = "UPDATE inventory SET pokeballs = %s WHERE saveid = %s"
    rows_modified = datatier.perform_action(dbConn, update_query, [pokeball_count - 1, saveid])


    #catch the pokemon!
    random_number = random.randint(1,100)
    if random_number == 7: # 1 in 100 chance! you caught a legendary
      select_query = "SELECT * FROM allpokemon WHERE rarity = 'Legendary' ORDER BY RAND() LIMIT 1"
    else:
      select_query = "SELECT * FROM allpokemon WHERE rarity = 'Common' ORDER BY RAND() LIMIT 1"

    random_pokemon = datatier.retrieve_one_row(dbConn, select_query)

    #our pokemon's info
    pokemon_name = random_pokemon[1]
    pokemon_type = random_pokemon[2]
    pokemon_rarity = random_pokemon[3]
    pokemon_nickname = "none"
    pokemon_level = 1
     

    #
    # insert into the pokemon table:
    #
    print("**Inserting...**")

    sql = "INSERT INTO pokemon (name,nickname,type,rarity,level) VALUES (%s,%s,%s,%s,%s)";

    rows_modified = datatier.perform_action(dbConn, sql, [pokemon_name, pokemon_nickname, pokemon_type, pokemon_rarity, pokemon_level])

    if rows_modified > 0:
       # Fetch the last autogenerated ID after the INSERT
        sql_get_last_id = "SELECT LAST_INSERT_ID() AS last_id"
        last_inserted_row = datatier.retrieve_one_row(dbConn, sql_get_last_id)
        
        # Extract the last autogenerated ID from the retrieved row
        generated_pokemonid = last_inserted_row[0] 

    else: 
      print("**Couldn't create a new game, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("insert failed")
      }
    
    #
    # insert into inventory table
    #
    print("**inserting into pokedex...**")

    sql = "INSERT INTO pokedex (saveid, pokemonid) VALUES (%s, %s)";

    rows_modified = datatier.perform_action(dbConn, sql, [saveid, generated_pokemonid])

    if rows_modified < 0:
      print("**Couldn't insert into pokedex, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("insert into pokedex failed")
      }

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning the pokemon's info**")
    
    return {
      'statusCode': 200,
      'body': json.dumps(random_pokemon)
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
