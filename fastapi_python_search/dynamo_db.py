
"""
Uses the AWS SDK for Python (Boto3) with Amazon DynamoDB to
create a table that stores data from the site-specific search results.

"""

import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class UrlInfo_db:
    """Encapsulates an Amazon DynamoDB table ."""
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def exists(self, table_name):
        """
        Determines whether a table exists. 

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        else:
            self.table = table
        return exists
    
    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store search data
        This table uses the URL as the partition key and the
        term as the sort key.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'url', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'content_present', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'url', 'AttributeType': 'S'},
                    {'AttributeName': 'content_present', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.table
    
    def save_to_dynamodb(self, Item):
            """
            Saves item to dynamodb table.
            """
            return self.table.put_item(Item=Item)

    def get_info_by_url_term(self, url, term):
        """
        Gets url info by url and term.

        :param url: The base url
        :param term: The search term
        :return: Data about the requested url and term
        """
        try:
            response = self.table.get_item(Key={'url': url, 'content_present': term})
        except ClientError as err:
            logger.error(
                "Couldn't get data for %s from table %s. Here's why: %s: %s",
                url, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']

    def get_all_entries_url(self, url):
        """
        Gets all url search data from the table for a specific url.

        :param url: The base url
        :return: The data about the requested url.
        """
        try:
            response = self.table.query(KeyConditionExpression=Key('url').eq(url))
        except ClientError as err:
            logger.error(
                "Couldn't query for url %s. Here's why: %s: %s", url,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Items']

def create_dyn_resource(table_name, dyn_resource):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    ui_table = UrlInfo_db(dyn_resource)
    ui_table_exists = ui_table.exists(table_name)
    if not ui_table_exists:
        print(f"\nCreating table {table_name}...")
        table_obj = ui_table.create_table(table_name)
        print(f"\nCreated table {ui_table.table.name}.")
    return ui_table

def get_dynamodb():
    try:
        UrlInfo_obj = create_dyn_resource(
            'table-for-url-info', boto3.resource('dynamodb'))
    except Exception as e:
        print(f"Something went wrong! Here's what: {e}")
    return UrlInfo_obj    

    