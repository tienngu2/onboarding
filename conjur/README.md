# Conjur Onboarding Documentation

Welcome to the Conjur onboarding documentation. This repository contains information and resources to help you understand how to work with Conjur for managing secrets and other sensitive data.

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

- [tutorial-template.yml](https://wwwin-github.cisco.com/EnterpriseSecurity/cyberark-snippets/blob/main/secrets_tutorial/tutorial-template.yml)
- [example-nesting.yml](https://wwwin-github.cisco.com/secrets/conjur-nonprod-it-hc_service_account/blob/main/example-nesting.yml)


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


## Policy Samples

This Conjur policy [tienngu2_sample2](tienngu2_sample2.md) demonstrates how to define 2 layers, 2 hosts, 2 grants, 2 policies, and a permit within a Conjur policy file. Each component is explained with a reference to the official CyberArk Conjur Secrets Manager Enterprise documentation.