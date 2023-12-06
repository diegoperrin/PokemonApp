import json
import boto3
import os
import datatier
import random

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_buy**")
    
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
    # see if we have enough coins:
    #

    sql = "SELECT * FROM inventory WHERE saveid = %s";

    row = datatier.retrieve_one_row(dbConn, sql, [saveid])

    if row == ():  # no such saveid
      print("**saveid doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such saveid...")
      }
    
    coins = row[2]

    #Access JSON body
    
    if "body" not in event:
      raise Exception("event has no body")
      
    body = json.loads(event["body"]) # parse the json
    
    if "pokeball_amount" not in body:
      raise Exception("event has a body but no amount given")
    
    pokeball_amount = body["pokeball_amount"]

    cost = pokeball_amount * 10

    if coins < cost :  # not enough
      print("**not enough coins, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("not enough coins! sell pokemon to get more!")
      }

    #you have enough coins

    update_query = "UPDATE inventory SET coins = %s WHERE saveid = %s"
    rows_modified = datatier.perform_action(dbConn, update_query, [coins - cost, saveid])
    update_query = "UPDATE inventory SET pokeballs = pokeballs + %s WHERE saveid = %s"
    rows_modified = datatier.perform_action(dbConn, update_query, [pokeball_amount, saveid])
    



    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
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
