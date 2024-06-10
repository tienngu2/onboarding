# Conjur Policy
The policy is designed to manage access to AWS resources using Conjur. It includes two layers for access control, two hosts that represent entities (such as services or machines), grants to associate hosts with layers, and individual permits to grant specific privileges to the layers for each variable.

## Table of Contents

- [Policy YAML](#policy-yaml)
- [Explanation of Statements](#explanation-of-statements)
- [Direct Path and Reference](#direct-path-and-reference)
- [CRUD CLI Commands for Managing Secrets](#crud-cli-commands-for-managing-secrets)

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
