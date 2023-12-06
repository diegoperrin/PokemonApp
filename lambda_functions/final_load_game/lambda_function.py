import json
import boto3
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_load_game**")
    
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
    
    sql = "SELECT saveid FROM gamesave WHERE trainername = %s";

    row = datatier.retrieve_one_row(dbConn, sql, [trainername])

    if not row:  # no such trainer
      print("**trainername doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such trainer...")
      }
    

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning the saveid**")
    
    return {
      'statusCode': 200,
      'body': json.dumps(row)
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
