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

To write a Conjur policy, create a YAML file with the necessary definitions. Here's an example of a policy sets up a basic structure where a host (myapp-host) can read and execute the database_password secret, and a group of administrators (admins) can manage the permissions of the layer that contains the host.

```yaml
# policy.yml
- !policy
  id: myapp
  body:
    - !layer

    - !host
      id: myapp-host

    - !variable
      id: database_password

    - !permit
      role: !layer
      privilege: [read, execute]
      resource: !variable database_password

    - !group
      id: admins

    - !grant
      role: !group admins
      member: !layer

```
#### Explanation of the policy:

`!policy`: This is the root of the policy document. The id field specifies the unique identifier for this policy, which in this case is myapp.

`!layer`: Layers are used to group related hosts and to manage their permissions collectively. In this example, a layer is created without an explicit id, so it will inherit the id from the parent policy, resulting in myapp.

`!host`: This defines a host entity, which can represent a machine or a service that will interact with Conjur. The host is given an id of myapp-host.

`!variable`: Variables are used to securely store secrets. Here, a variable with the id of database_password is created to hold the password for a database.

`!permit`: This statement grants permissions to a role over a resource. In this example, the layer (which implicitly has the id myapp) is granted read and execute privileges on the database_password variable.

`!group`: Groups are used to manage user or host permissions collectively. A group with the id of admins is created here.

`!grant`: This statement adds members to a role. The admins group is granted membership over the myapp layer, allowing administrators to manage access for the hosts in this layer.


## Policy Sample

This Conjur policy [tienngu2_aws-prod-dev-s3-ec2](tienngu2_aws-prod-dev-s3-ec2.md) demonstrates how to define 2 layers, 2 hosts, 2 grants, 2 policies, and a permit within a Conjur policy file. Each component is explained with a reference to the official CyberArk Conjur Secrets Manager Enterprise documentation.

## More Policy Samples
[tienngu2_aws-ec2-rds](tienngu2_aws-ec2-rds.yaml): This policy is designed to manage access to secrets related to AWS EC2 and RDS instances within Conjur, a security service that manages secrets and other sensitive data. The policy is structured to define roles, permissions, and secrets for EC2 and RDS resources.

[tienngu2_aws_prod_dev_s3_ec2_group_variables](tienngu2_aws_prod_dev_s3_ec2_group_variables.yaml): This policy is using a group that includes all the variables and then grant permissions to that group.