import json
import logging


def lambda_handler(event, context):
    """
    return authorization of user.
    :param event: lambda handler event.
    :param context: lambda handler context.
    :return: return open search result
    """
    print(event)
    json_file = ""
    try:
        input_value = 1
        if (event.get("value", None)) is not None:
            input_value = event["value"]
        # print(input_value)
        x = 10 / int(input_value)

        # read json file
        json_file = open('source/sample.json')
        data = json.load(json_file)
        # json_file.close()

        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # You can specify specific origins instead of '*' for production
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET, PUT, DELETE',  # Include the allowed methods
            },
            'body': json.dumps(data)  # ('Hello from Lambda!')
        }
    except Exception as e:
        response = {
            'statusCode': 400,
            'body': json.dumps('')
        }
        logging.error("Failed to get search response : " + str(e))
    finally:
        if not json_file.closed:
            json_file.close()
        logging.info("Search result has been return successfully")

    return response
