import os

import boto3


def get_aws_secret(secret_arn):
    """Return the secret value from an AWS secret."""
    secrets_client = boto3.client("secretsmanager")
    secret = secrets_client.get_secret_value(SecretId=secret_arn)
    return secret["SecretString"]


def get_environ_or_aws_secret(env_var):
    """
    Return the value of an environment variable or AWS secret.

    It received the name of an environment variable, and if it
    points to an AWS secret, retrieve it and return it instead.
    """
    env_var_value = os.environ.get(env_var)
    if env_var_value and env_var_value[:23] == "arn:aws:secretsmanager:":
        # Use `get_aws_secret()` from previous example.
        return get_aws_secret(env_var_value)

    return env_var_value
