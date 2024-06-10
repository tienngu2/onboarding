# Conjur Onboarding Documentation

Welcome to the Conjur onboarding documentation. This repository contains information and resources to help you understand how to work with Conjur for managing secrets and other sensitive data.

For how Conjur works, see [here](https://www.conjur.org/get-started/why-conjur/how-conjur-works/).

## Table of Contents

- [Defining Policies](#defining-policies)
- [Policy Samples](#policy-samples)

## Defining Policies

Conjur policies are YAML files that define the roles, permissions, and secrets within the Conjur system. Policies are the core of the Conjur authorization model and are used to manage access to secrets.

### Policy Structure

A typical Conjur policy includes:

- Resources: Variables, hosts, users, groups, etc.
- Roles: Users or machines that can have permissions on resources.
- Permissions: Defines what actions roles can perform on resources.
- Annotations: Additional information about the resources.

### Writing a Policy

To write a Conjur policy, create a YAML file with the necessary definitions. Here's an example of a simple policy:

```yaml
# policy.yml
- !policy
  id: myapp
  body:
    - !layer

    - !host
      id: myapp01

    - !variable
      id: database/username

    - !variable
      id: database/password

    - !permit
      role: !layer
      privilege: [read, execute]
      resource: !variable database/username

    - !permit
      role: !layer
      privilege: [read, execute]
      resource: !variable database/password

    - !grant
      role: !layer
      member: !host myapp01
```
#### Explanation of the policy:

1. `Policy Block (!policy)`:
  **id: myapp**: This creates a new policy with the identifier myapp. Policies are used to organize and manage related security objects like hosts, users, groups, variables, etc.
2. `Layer Block (!layer)`:
  This creates a new layer, which is a collection of related hosts (machines or processes). Layers are used to group hosts that have similar functions or security requirements. No id is specified, so it inherits the id from the parent policy, becoming myapp.
3. `Host Block (!host)`:
  id: myapp01: This defines a new host entity with the identifier myapp01. Hosts typically represent machines or services that can authenticate with Conjur and fetch secrets.
4. `Variable Blocks (!variable)`:
  id: database/username: This creates a new variable to store the database username. Variables are used to securely store and manage secrets like passwords, API keys, etc.
id: database/password: Similarly, this creates a new variable to store the database password.
5. `Permit Blocks (!permit)`:
These blocks define permissions for the previously created layer to access the variables:
The first !permit gives the myapp layer the privileges read and execute on the database/username variable.
The second !permit gives the myapp layer the same privileges (read and execute) on the database/password variable.
The read privilege typically allows the role to fetch the value of the variable, while execute might be used for executing actions related to the variable, depending on the system's specific implementation.
6. `Grant Block (!grant)`:
role: !layer: This specifies the myapp layer as the role that will receive a new member.
member: !host myapp01: This adds the myapp01 host as a member of the myapp layer.
By granting membership, the myapp01 host inherits the permissions assigned to the myapp layer, which means it can read and execute (or fetch) the database/username and database/password variables.


## Policy Samples

This Conjur policy [tienngu2_aws_prod_dev_s3_ec2](tienngu2_aws_prod_dev_s3_ec2.md) demonstrates how to define 2 layers, 2 hosts, 2 grants, 2 policies, and a permit within a Conjur policy file. Each component is explained with a reference to the official CyberArk Conjur Secrets Manager Enterprise documentation.

## More Policy Samples
[tienngu2_aws-ec2-rds](tienngu2_aws-ec2-rds.yaml): This policy is designed to manage access to secrets related to AWS EC2 and RDS instances within Conjur, a security service that manages secrets and other sensitive data. The policy is structured to define roles, permissions, and secrets for EC2 and RDS resources.

[tienngu2_aws_prod_dev_s3_ec2_group_variables](tienngu2_aws_prod_dev_s3_ec2_group_variables.yaml): This policy is using a group that includes all the variables and then grant permissions to that group.