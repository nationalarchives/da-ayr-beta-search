import botocore
import boto3
import datetime
from dateutil.tz import tzlocal

assume_role_cache: dict = {}


def assumed_role_session(role_arn: str, base_session: botocore.session.Session = None):
    base_session = base_session or boto3.session.Session()._session
    fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator=base_session.create_client,
        source_credentials=base_session.get_credentials(),
        role_arn=role_arn,
        extra_args={
            #    'RoleSessionName': None # set this if you want something non-default
        }
    )
    creds = botocore.credentials.DeferredRefreshableCredentials(
        method='assume-role',
        refresh_using=fetcher.fetch_credentials,
        time_fetcher=lambda: datetime.datetime.now(tzlocal())
    )
    botocore_session = botocore.session.Session()
    botocore_session._credentials = creds
    return boto3.Session(botocore_session=botocore_session)


# usage:
session = assumed_role_session('arn:aws:iam::173163141187:role/IAM_Admin_Role')
s3_client = session.client('s3')
objects = s3_client.list_objects_v2(Bucket='ayr-beta-lambda-repository')

for obj in objects['Contents']:
    print(obj['Key'])