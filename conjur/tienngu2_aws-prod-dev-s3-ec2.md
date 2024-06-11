# Conjur Policy
The policy is designed to manage access to AWS resources using Conjur. It includes two layers for access control, two hosts that represent entities (such as services or machines), grants to associate hosts with layers, and individual permits to grant specific privileges to the layers for each variable.

## Table of Contents

- [Policy YAML](#policy-yaml)
- [Explanation of Statements](#explanation-of-statements)
- [Direct Path and Reference](#direct-path-and-reference)
- [CRUD CLI Commands for Managing Secrets](#crud-cli-commands-for-managing-secrets)
- [CRUD API for Managing Secrets Using Python Conjur Client](#crud-api-for-managing-secrets-using-python-conjur-client)

Site note: you can access the backup [here](tienngu2_aws_prod_dev_s3_ec2.yaml)
## Policy YAML

```yaml
# tienngu2_aws_prod_dev_s3_ec2.yaml
- !policy
  id: tienngu2_aws-s3-ec2
  body:
    # Define two layers for grouping access control
    - !layer
      id: aws_prod_access
    - !layer
      id: aws_dev_access

    # Define two hosts that represent different entities (e.g., services or machines)
    - !host
      id: prod_host
    - !host
      id: dev_host

    # Grant each host to the corresponding layer
    - !grant
      role: !layer aws_prod_access
      member: !host prod_host
    - !grant
      role: !layer aws_dev_access
      member: !host dev_host

    # Define sub-policies for managing AWS resources
    # The number of policies can range from 2 to 10 as per your requirements
    - !policy
      id: s3_buckets
      body:
        - !variable
          id: bucket_access_key
        - !variable
          id: bucket_secret_key
    - !policy
      id: ec2_instances
      body:
        - !variable
          id: instance_access_key
        - !variable
          id: instance_secret_key
    # Additional policies can be added here...

    # Define individual permits that grant specified privileges to the layers
    # for each variable
    - !permit
      role: !layer aws_prod_access
      privilege: [read, update, execute]
      resource: !variable s3_buckets/bucket_access_key
    - !permit
      role: !layer aws_prod_access
      privilege: [read, update, execute]
      resource: !variable s3_buckets/bucket_secret_key
    - !permit
      role: !layer aws_dev_access
      privilege: [read, update, execute]
      resource: !variable ec2_instances/instance_access_key
    - !permit
      role: !layer aws_dev_access
      privilege: [read, update, execute]
      resource: !variable ec2_instances/instance_secret_key

```

## Explanation of Statements

`!policy`: This is the root policy named tienngu2_aws-s3-ec2. It serves as a container for all the resources and permissions related to AWS integration.

`!layer`: Layers are used to group related privileges. In this policy, there are two layers: aws_prod_access for production access control and aws_dev_access for development access control.

`!host`: Hosts represent entities that will interact with AWS resources. prod_host could be a production server or service, and dev_host could be a development server or service.

`!grant`: This associates each host with a corresponding layer. prod_host is granted to aws_prod_access, and dev_host is granted to aws_dev_access. This means that the hosts inherit the permissions assigned to their respective layers.

`!policy`: Sub-policies are defined for specific AWS resources. In this example, there are sub-policies for S3 buckets and EC2 instances. Each sub-policy can contain variables, permissions, and other resources related to that specific AWS service.

`!variable`: Variables are used to securely store secrets, such as access keys and secret keys. In the sub-policies, variables are defined for the S3 bucket access key, S3 bucket secret key, EC2 instance access key, and EC2 instance secret key.

`!permit`: These statements grant specific privileges to the layers for each variable. The aws_prod_access layer is given read, update, and execute privileges on the S3 bucket variables, and the aws_dev_access layer is given the same privileges on the EC2 instance variables.

**Reference**: For more detailed information on defining policies and other components, refer to the official CyberArk Conjur documentation:
- [Defining Policies](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/policy-syntax.htm)
- [Layers](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-layer.htm)
- [Hosts](https://docs.cyberark.com/Product-Doc/OnlineHelp/AAM-DAP/Latest/en/Content/Operations/Policy/statement-ref-host.htm)
- [Grants](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-grant.htm)
- [Permits](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-permit.htm)
- [Variable](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-variable.htm?tocpath=Fundamentals%7CPolicy%7CPolicy%20statement%20reference%7C_____12)

## Direct Path and Reference

The direct paths are constructed by combining the policy ID with the sub-policy ID and the variable ID. Here are the paths for the variables defined in the policy:


- For the S3 bucket access key:
```bash
tienngu2_aws-s3-ec2/s3_buckets/bucket_access_key
```
- For the S3 bucket secret key:
```bash
tienngu2_aws-s3-ec2/s3_buckets/bucket_secret_key
```
- For the EC2 instance access key:
```bash
tienngu2_aws-s3-ec2/ec2_instances/instance_access_key
```
- For the EC2 instance secret key:
```
tienngu2_aws-s3-ec2/ec2_instances/instance_secret_key
```

## CRUD CLI Commands for Managing Secrets

To perform CRUD operations on Conjur using the CLI, you first need to log in to the Conjur CLI.

##### CURD Operations

Here are the Conjur CLI commands for creating, reading, updating, and deleting secrets:

[Getting variable values](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Developer/CLI/cli-variable.htm?tocpath=Developer%7CConjur%20CLI%7CConjur%20CLI%20command%20reference%7C_____11#variableget): Use the get subcommand to get the value of one or more Conjur variables.

```bash
conjur variable value tienngu2_aws-s3-ec2/s3_buckets/bucket_access_key
```

[Setting variable values](https://docs.cyberark.com/conjur-enterprise/13.0/en/Content/Operations/Policy/statement-ref-variable.htm#Settingvariablevalues): By design, policy does not set the variable value. Use the CLI, the UI, or the API to set the value.

Set (add) a variable value is:
```bash
conjur variable set -i tienngu2_aws-s3-ec2/ec2_instances/instance_secret_key -v 'new_secret_value'
```

[Deleting variable](): To clear the value of a variable (Conjur does not support deleting a variable via the CLI):
```
conjur variable set -i <policy/path/variable-id> -v ""
```

## CRUD API for Managing Secrets Using Python Conjur Client

This section outlines the usage of two Python scripts designed to interact with a Conjur server running as a Docker container. The Conjur server is an open-source version of CyberArk Conjur, which is used for secrets management. The first script is responsible for loading a Conjur policy into the server, while the second script performs Create, Read, Update, and Delete (CRUD) operations on the secret keys defined within that policy.

### Python Files

#### 1. Policy Loader

The [policy_loader.py](python-conjur-client/conjur-client-admin-load-policy.py) script is responsible for loading a predefined Conjur policy into the Conjur server. This policy defines the roles, permissions, and secrets that will be managed by Conjur.

`Functionality`:
Connects to the Conjur server using the provided credentials and configuration.
Loads the policy file into the Conjur server, establishing the policy's structure and content within the server's database.

`Outcome`:
Upon successful execution, the script will output a confirmation message indicating that the policy has been loaded successfully. An accompanying [image](images/results-running-conjur-client-admin-load-policy.py.png) in the documentation shows the result of this successful policy loading.

#### 2. Secrets Manager

The [conjur-client-crud.py](python-conjur-client/conjur-client-crud.py) script performs CRUD operations on the secrets defined by the loaded Conjur policy.

`Functionality`:

Connects to the Conjur server using the necessary credentials.
Creates new secrets or updates existing ones as defined in the policy.
Retrieves secrets, allowing authorized applications or users to access them.
Optionally, deletes secrets from the Conjur server when they are no longer needed or should be revoked.

`Outcome`:
The script provides output for each operation, confirming the successful creation, retrieval, updating, or deletion of secrets. The documentation includes an [image](images/results-running-conjur-client-crud.png) that demonstrates the results of these CRUD operations on the Conjur policy.


`Execution Environment`

Both scripts are designed to run against a Conjur server deployed as a Docker container. The Conjur server must be properly configured and running before executing the scripts. The scripts assume that the Conjur server is accessible and that the necessary environment variables or configuration files are set up for authentication and interaction.

##### Configuration File Example
When a Python script connects to a Conjur server, it can use the ~/.conjurrc and ~/.netrc files for configuration and authentication purposes. Here's a brief explanation of each file's role:
```sh
~/.conjurrc
```
The ~/.conjurrc file contains the Conjur server's configuration details. This file typically includes the Conjur account name, the URL of the Conjur server, and the certificate file's path (if using HTTPS). Here's an example of what the contents might look like:
```sh
---
account: myConjurAccount
appliance_url: https://proxy
cert_file: "/path/to/conjur.pem"
```
This file is used by the Conjur CLI and client libraries to determine how to connect to the Conjur server.

```sh
~/.netrc
```

The ~/.netrc file is used for storing credentials needed to authenticate with the Conjur server. It keeps the login and password (API key or personal access token) secure and makes them easily accessible to scripts and tools that need to authenticate. An example entry for Conjur might look like this:

```sh
machine https://proxy/authn
login myuser
password myapikey
```
The machine directive specifies the domain of the Conjur server, while login and password provide the necessary credentials.