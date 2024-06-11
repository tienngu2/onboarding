"""
Replace <TIENNGU2_API_KEY> with the actual API key for the user tienngu2. The script performs the following operations:

Initializes the Conjur client with the user's credentials.
Defines the variable IDs for the secrets within the tienngu2_aws-ec2-rds policy.
Creates (adds) new secrets with placeholder values.
Reads (retrieves) the values of the secrets and prints them.
Updates (replaces) the secrets with new placeholder values.

Please note that the Conjur API does not support the deletion of variable values.
If you need to "delete" a secret, you can rotate it to a new value that is not used or remove permissions for all users
to access that secret.
"""
# https://pypi.org/project/conjur-client/
from conjur import Client

# Initialize the Conjur client (it will use the ~/.conjurrc file and ~/.netrc for configuration)
client = Client()

print(" ")
whoami = client.whoami()
print(f"The value of whoami is: {whoami}")
print(" ")

# Define the variable IDs
variable_ids = {
    'instance_access_key': 'tienngu2_aws-s3-ec2/ec2_instances/instance_access_key',
    'instance_secret_key': 'tienngu2_aws-s3-ec2/ec2_instances/instance_secret_key',
    'bucket_access_key': 'tienngu2_aws-s3-ec2/s3_buckets/bucket_access_key',
    'bucket_secret_key': 'tienngu2_aws-s3-ec2/s3_buckets/bucket_secret_key'
}

# Create (Add) new secrets
for var_id, value in variable_ids.items():
    print(f"Set var_id: {var_id} --> var_value: {value}")
    client.set(value, f'secret-value-for-{var_id}')

# Read (Retrieve) the secrets' values
for var_id in variable_ids.values():
    secret_value = client.get(var_id)
    print(f"The secret value for {var_id} is: {secret_value}")

# Update (Replace) the secrets' values
for var_id in variable_ids.values():
    client.set(var_id, f'new-secret-value-for-{var_id}')

# results-after-policy-load-with-key-apis.json: Conjur does not support deleting variable values via the API.
# To "delete" a secret, you would typically rotate it to an unusable value
# or remove permissions to access it.

# Example of rotating a secret to a new value
client.set(variable_ids['bucket_secret_key'], 'new-rotated-db-password')
