import json
import boto3
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_pokedex**")
    
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
        
    print("jobid:", saveid)

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
    
    #
    # now retrieve all the pokemon:
    #
    print("**Retrieving data**")

    sql = "SELECT * FROM gamesave WHERE saveid = %s";

    row = datatier.retrieve_one_row(dbConn, sql, [saveid])

    if row == ():  # no such saveid
      print("**saveid doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such saveid...")
      }
    

    #we know saveid is valid, grab all the pokemon for this trainer
    sql = "SELECT * FROM pokedex WHERE saveid = %s";
    
    rows = datatier.retrieve_all_rows(dbConn, sql, [saveid])
    num_pokemon = len(rows)
    
    print("You have " + str(num_pokemon) + " pokemon!")
    print()
    for row in rows:
      print(row)

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning pokemon**")
    
    return {
      'statusCode': 200,
      'body': json.dumps(rows)
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
