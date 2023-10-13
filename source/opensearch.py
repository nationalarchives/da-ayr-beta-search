# python3 -m source.opensearch

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json
import logging
from source import parameter
import requests

# host = 'search-ayr-talendtest-opensearch-22ltdv57rxkcvvfcy5bxwmfjlm.eu-west-2.es.amazonaws.com'
# idx = 'ayr-consignment-idx'
default_aws_profile = "tna-ayr-sandbox"


def get_aws_environment_prefix():
    return "/" + parameter.get_parameter_store_key_value("ENVIRONMENT_NAME", False, default_aws_profile) + "/"


def get_aws_auth():
    awsauth = ''
    try:
        AWS_ENVIRONMENT_PREFIX = get_aws_environment_prefix()
        AWS_REGION = parameter.get_parameter_store_key_value(AWS_ENVIRONMENT_PREFIX + "AWS_REGION")
        service = 'es'

        if default_aws_profile:
            credentials = boto3.Session(profile_name=default_aws_profile).get_credentials()
        else:
            credentials = boto3.Session().get_credentials()

        # print(credentials.token)
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, AWS_REGION, service,
                           session_token=credentials.token)
        # print(awsauth.session_token)
    except Exception as e:
        logging.error("Failed to get aws auth details : " + str(e))
    finally:
        logging.info("AWS auth details has been retrieved successfully")

    return awsauth


def generate_open_search_client():
    search_client = ''
    try:
        AWS_ENVIRONMENT_PREFIX = get_aws_environment_prefix()
        OPEN_SEARCH_HOST = parameter.get_parameter_store_key_value(AWS_ENVIRONMENT_PREFIX + "AWS_OPEN_SEARCH_HOST")

        aws_auth = get_aws_auth()
        if aws_auth:
            # Create the client.
            search_client = OpenSearch(
                hosts=[{'host': OPEN_SEARCH_HOST, 'port': 443}],
                http_auth=aws_auth,
                use_ssl=True,
                verify_certs=True,
                http_compress=True,  # enables gzip compression for request bodies
                ssl_assert_hostname=False,
                ssl_show_warn=False,
                connection_class=RequestsHttpConnection
            )
    except Exception as e:
        logging.error("Failed to get open search client : " + str(e))
    finally:
        logging.info("Search result has been return successfully")
    return search_client


def get_search_results_using_open_client():
    try:
        AWS_ENVIRONMENT_PREFIX = get_aws_environment_prefix()
        OPEN_SEARCH_INDEX = parameter.get_parameter_store_key_value(AWS_ENVIRONMENT_PREFIX + "AWS_OPEN_SEARCH_INDEX")
        query = {
            "size": 25,
            "query": {
                "parent_id": {
                    "type": "file",
                    "id": "TDR-2023-TMT"
                }
            }
        }

        # Send the request.
        search_client = generate_open_search_client()
        # print(search_client.info())
        if search_client:
            result = search_client.search(body=query, index=OPEN_SEARCH_INDEX)
            # print(result)
            # Create the response and add some extra content to support CORS
            response = {"statusCode": 200, "headers": {
                "Access-Control-Allow-Origin": '*'
            }, "isBase64Encoded": False, 'body': result.text}
        else:
            response = {"statusCode": 400, "headers": {
                "Access-Control-Allow-Origin": '*'
            }, "isBase64Encoded": False, 'body': "Failed to get open search client"}

        # Add the search results to the response
        return response
    except Exception as e:
        msg = "Failed to get open search client : " + str(e)
        response = {"statusCode": 400, "headers": {
            "Access-Control-Allow-Origin": '*'
        }, "isBase64Encoded": False, 'body': msg}

        logging.error(msg)
    finally:
        logging.info("Search result has been return successfully")
    return response


def get_search_results_using_request():
    try:
        AWS_ENVIRONMENT_PREFIX = get_aws_environment_prefix()
        OPEN_SEARCH_HOST = parameter.get_parameter_store_key_value(AWS_ENVIRONMENT_PREFIX + "AWS_OPEN_SEARCH_HOST")
        OPEN_SEARCH_INDEX = parameter.get_parameter_store_key_value(AWS_ENVIRONMENT_PREFIX + "AWS_OPEN_SEARCH_INDEX")
        query = {
            "size": 25,
            "query": {
                "parent_id": {
                    "type": "file",
                    "id": "TDR-2023-TMT"
                }
            }
        }

        headers = {"Content-Type": "application/json"}

        search_url = 'https://' + OPEN_SEARCH_HOST + '/' + OPEN_SEARCH_INDEX + '/_search'
        aws_auth = get_aws_auth()
        if aws_auth:
            # Make the signed HTTP request
            result = requests.get(search_url, auth=aws_auth, headers=headers, data=json.dumps(query))
            # print(result)

            # Create the response and add some extra content to support CORS
            response = {"statusCode": 200, "headers": {
                "Access-Control-Allow-Origin": '*'
            }, "isBase64Encoded": False, 'body': result.text}
        else:
            response = {"statusCode": 400, "headers": {
                "Access-Control-Allow-Origin": '*'
            }, "isBase64Encoded": False, 'body': "Failed to get open search client"}
    except Exception as e:
        msg = "Failed to get response from the request, Error : " + str(e)
        response = {"statusCode": 400, "headers": {
            "Access-Control-Allow-Origin": '*'
        }, "isBase64Encoded": False, 'body': msg}

        logging.error(msg)
    finally:
        logging.info("Search result has been return successfully")
    return response


if __name__ == "__main__":
    # awsauth_test = get_aws_auth()
    # print(awsauth_test.session_token)
    # open_search_client_result = generate_open_search_client()
    # print(open_search_client_result.features.client)
    search_result = get_search_results_using_open_client()
    print(search_result)
    # search_result = get_search_results_using_request()
    # print(search_result)
