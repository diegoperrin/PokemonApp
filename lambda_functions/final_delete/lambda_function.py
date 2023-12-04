import json
import boto3
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_delete**")
    
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

    if "trainername" in event:
      trainername = event["trainername"]
    elif "pathParameters" in event:
      if "trainername" in event["pathParameters"]:
        trainername = event["pathParameters"]["trainername"]
      else:
        raise Exception("requires trainername parameter in pathParameters")
    else:
        raise Exception("requires trainername parameter in event")
        
    print("trainername:", trainername)

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)


    #SaveID to delete
    
    sql = "SELECT * FROM gamesave WHERE trainername = %s";

    saveid_to_delete =  datatier.retrieve_one_row(dbConn, sql, [trainername])

    if saveid_to_delete == ():  # no such trainername
      print("**trainer doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such trainer..")
      }

    #Extract saveid
    saveid_to_delete = saveid_to_delete[0]

    # Select pokemonid(s) associated with the specified saveid in pokedex
    select_pokemon_query = "SELECT pokemonid FROM pokedex WHERE saveid = %s"
    pokemon_ids = datatier.retrieve_all_rows(dbConn, select_pokemon_query, [saveid_to_delete])

    # Extract pokemonid(s) from the retrieved rows
    pokemon_ids_list = [pokemon[0] for pokemon in pokemon_ids]

    for id in pokemon_ids_list:
        # Delete entries from the pokemon table for the associated pokemonids
        delete_pokemon_query = "DELETE FROM pokemon WHERE pokemonid = (%s)"
        datatier.perform_action(dbConn, delete_pokemon_query, id)

    # Delete entries from the pokedex table for the specified saveid
    delete_pokedex_query = "DELETE FROM pokedex WHERE saveid = %s"
    datatier.perform_action(dbConn, delete_pokedex_query, [saveid_to_delete])

    # Delete entry from the inventory table for the specified saveid
    delete_inventory_query = "DELETE FROM inventory WHERE saveid = %s"
    datatier.perform_action(dbConn, delete_inventory_query, [saveid_to_delete])

    # Delete entry from the gamesave table for the specified saveid
    delete_gamesave_query = "DELETE FROM gamesave WHERE saveid = %s"
    datatier.perform_action(dbConn, delete_gamesave_query, [saveid_to_delete])

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning the generated saveid**")
    
    return {
      'statusCode': 200,
      'body': json.dumps("success")
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
