import json
import boto3
import os
import datatier
import random

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_rename**")
    
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
    # Grab the pokemonid
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

    
    #pokemon exists, rename it

    #access JSON body
    
    if "body" not in event:
      raise Exception("event has no body")
      
    body = json.loads(event["body"]) # parse the json
    
    if "nickname" not in body:
      raise Exception("event has a body but no nickmane was passed in")
    
    nickname = body["nickname"]


    update_query = "UPDATE pokemon SET nickname = %s WHERE pokemonid = %s"
    datatier.perform_action(dbConn, update_query, [nickname, pokemonid])
    
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #

    #return the sale price for the pokemon
    print("**DONE, **")
    
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
