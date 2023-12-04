import json
import boto3
import os
import datatier

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: final_inventory**")
    
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
    # now retrieve inventory:
    #
    print("**Retrieving inventory data**")

    sql = "SELECT * FROM inventory WHERE saveid = %s";

    row = datatier.retrieve_one_row(dbConn, sql, [saveid])

    if row == ():  # no such saveid
      print("**saveid doesn't exist, returning...**")
      return {
        'statusCode': 400,
        'body': json.dumps("no such saveid...")
      }
    
    print(row)

    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning pokemon**")
    
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
