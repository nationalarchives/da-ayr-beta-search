import unittest
import json

import parameter
import lambda_function

# run following command to perform unit testing on all test cases
# python3 -m unittest test


# set config environment for testing
AWS_PROFILE = "tna-ayr-sandbox"

AWS_ENVIRONMENT = parameter.get_parameter_store_key_value("ENVIRONMENT_NAME",
                                                          encrypted=False,
                                                          default_aws_profile=AWS_PROFILE)
PREFIX = "/" + AWS_ENVIRONMENT + "/"

test_keycloak_username = parameter.get_parameter_store_key_value(PREFIX + "KEYCLOAK_TEST_USER",
                                                                 encrypted=False,
                                                                 default_aws_profile=AWS_PROFILE)
test_keycloak_password = parameter.get_parameter_store_key_value(PREFIX + "KEYCLOAK_TEST_USER_PASSWORD",
                                                                 encrypted=False, default_aws_profile=AWS_PROFILE)


class TestParameter(unittest.TestCase):
    def test_get_parameter_value_with_valid_key(self):
        """
        Test that it can return parameter value
        :return: parameter value
        """
        key = PREFIX + "KEYCLOAK_BASE_URI"  # config.PREFIX +
        result = parameter.get_parameter_store_key_value(
            key, encrypted=False, default_aws_profile=AWS_PROFILE
        )
        self.assertEqual(result, "https://auth.tdr-integration.nationalarchives.gov.uk")

    def test_get_parameter_value_with_invalid_key(self):
        """
        Test that it can return parameter value
        :return: ""
        """
        key = "KEYCLOAK_BASE_URI_NOT"  # invalid key
        result = parameter.get_parameter_store_key_value(
            key, encrypted=False, default_aws_profile=AWS_PROFILE
        )
        self.assertEqual(result, "")


class TestLambdaFunction(unittest.TestCase):
    def test_lambda_function_valid_response_with_value_parameter(
            self,
    ):
        """
        Check token is valid and active
        :return:
        """
        lambda_event = {"value": "1"}
        result = json.loads(
            json.dumps(lambda_function.lambda_handler(event=lambda_event, context=""))
        )
        self.assertEqual(result["statusCode"], 200)

    def test_lambda_function_failed_response_without_value_parameter(
            self,
    ):
        """
        Check token is valid and active
        :return:
        """
        lambda_event = {}
        result = json.loads(
            json.dumps(lambda_function.lambda_handler(event=lambda_event, context=""))
        )
        self.assertEqual(result["statusCode"], 200)

    def test_lambda_function_failed_response_with_invalid_value(
            self,
    ):
        """
        Check token is valid and active
        :return:
        """
        lambda_event = {"value": "0"}
        result = json.loads(
            json.dumps(lambda_function.lambda_handler(event=lambda_event, context=""))
        )
        self.assertEqual(result["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
