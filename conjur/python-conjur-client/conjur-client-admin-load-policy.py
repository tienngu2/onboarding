"""
Initializes the Conjur client with the admin user's credentials.
Attempts to load the policy from the specified file.
If the policy load is successful, it prints a success message.
Attempts to retrieve the value of a specific variable defined in the policy to validate that the policy elements are accessible.

If the policy load fails or the variable cannot be retrieved, an exception will be raised, and an error message will be printed.

Please note that this script assumes that the variable 'tienngu2_aws-s3-ec2/ec2_instances/instance_access_key' is defined in the policy and that
the admin user has the necessary permissions to retrieve it. You may need to adjust the variable ID based on the actual contents
of your policy.
"""
# https://pypi.org/project/conjur-client/
from conjur import Client
import time

# Initialize the Conjur client (it will use the ~/.conjurrc file and ~/.netrc for configuration)
client = Client()

policy_file = 'tienngu2_aws_prod_dev_s3_ec2.yaml'

# Load the policy
policy_id = 'root'  # 'root' is typically used for the main policy branch
try:
    policy_result = client.apply_policy_file(policy_id, policy_file)
    print("Policy loaded successfully.")
    print(policy_result)  # This will print the result of the policy load, which includes data about the loaded policy

    # Wait for 1 minute (60 seconds)
    print("Wait for 1 minute before validating the policy loaded successfully")
    time.sleep(60)
    # Check if a specific variable from the policy exists
    variable_id = 'tienngu2_aws-s3-ec2/ec2_instances/instance_access_key'
    try:
        secret_value = client.get(variable_id)
        print(f"Variable '{variable_id}' exists. Policy loaded successfully.")
    except Exception as e:
        print(f"Failed to retrieve variable '{variable_id}': {e}")

except Exception as e:
    print(f"Failed to load policy: {e}")
