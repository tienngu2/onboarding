# Sample Conjur Policy

This sample Conjur policy demonstrates how to define 2 layers, 2 hosts, 2 grants, 2 policies, and a permit within a Conjur policy file. Each component is explained with a reference to the official CyberArk Conjur Secrets Manager Enterprise documentation.

## Table of Contents

- [Policy YAML](#policy-yaml)
- [Explanation of Statements](#explanation-of-statements)
- [Direct Path and Reference](#direct-path-and-reference)
- [CRUD CLI Commands for Managing Secrets](#crud-cli-commands-for-managing-secrets)

Site note: you can access the backup [here](tienngu2_sample2.yaml)
## Policy YAML

```yaml
# policy.yml
- !policy
  id: tienngu2
  body:
    # First layer
    - !layer
      id: web_layer

    # Second layer
    - !layer
      id: db_layer

    # First host
    - !host
      id: web01

    # Second host
    - !host
      id: db01

    # First grant
    - !grant
      role: !layer web_layer
      member: !host web01

    # Second grant
    - !grant
      role: !layer db_layer
      member: !host db01

    # Child policy 1
    - !policy
      id: web_policy
      body:
        - !variable
          id: web_api_key

    # Child policy 2
    - !policy
      id: db_policy
      body:
        - !variable
          id: db_connection_string

    # Permit
    - !permit
      role: !layer web_layer
      privilege: [read, execute]
      resource: !variable web_api_key
```

## Explanation of Statements

`!policy` - The root policy, identified by id: tienngu2, serves as the container for the entire policy structure.

`!layer` - Two layers are defined: web_layer and db_layer. Layers are used to group related hosts and manage their permissions collectively.

`!host` - Two hosts are defined: web01 and db01. Hosts represent machines or processes that can authenticate with Conjur to fetch secrets.

`!grant` - Two grant statements are used to add web01 to the web_layer and db01 to the db_layer, allowing them to inherit permissions assigned to these layers.

`!policy` - Two child policies, web_policy and db_policy, are defined within the parent policy. Each child policy can contain its own resources and permissions.

`!variable` - Secret variables like web_api_key and db_connection_string are defined within child policies. These variables are used to store sensitive information such as API keys or database credentials.

`!permit` - A permit statement grants the web_layer the privileges of read and execute on the web_api_key variable, allowing hosts in this layer to access the secret.


## Direct Path and Reference

**Direct Path**: The direct path to policies and secrets in the Conjur UI is constructed based on your Conjur instance's URL and account name. For example, to access the web_api_key variable, the path would be:

```
https://<Conjur-UI-URL>/secrets/<account>/variable/web_policy/web_api_key
```
Replace `<Conjur-UI-URL>` and `<account>` with the actual values for your Conjur setup.

**Reference**: For more detailed information on defining policies and other components, refer to the official CyberArk Conjur documentation:

- [Defining Policies](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/policy-syntax.htm)
- [Layers](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-layer.htm)
- [Hosts](https://docs.cyberark.com/Product-Doc/OnlineHelp/AAM-DAP/Latest/en/Content/Operations/Policy/statement-ref-host.htm)
- [Grants](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-grant.htm)
- [Permits](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Operations/Policy/statement-ref-permit.htm)


## CRUD CLI Commands for Managing Secrets

To perform CRUD operations on Conjur using the CLI, you first need to log in to the Conjur CLI. Here are the general steps to log in and perform CRUD operations:

**Step 1**: Install the Conjur CLI

You can download it from the official releases page on GitHub or install it using package managers like Homebrew for macOS:
```
brew install conjur-cli
```

**Step 2**: Initialize the Conjur CLI

Before logging in, you need to initialize the CLI with the URL of your Conjur instance:
```
conjur init -u https://<Conjur-URL> -a <account-name>
```

Replace `<Conjur-URL>` with the URL of your Conjur instance and `<account-name>` with the account name you're using.

**Step 3**: Log In to Conjur CLI

To log in to the Conjur CLI, you'll need the username and API key of a Conjur user. If you're using a host, you'll need the host ID and API key.

For a user:
```
conjur authn login -u <username>
```

For a host:
```
conjur authn login -u host/<host-id>
```
After entering the command, you will be prompted to enter the API key. Once authenticated, you can start performing CRUD operations.

##### CURD Operations

Here are the Conjur CLI commands for creating, reading, updating, and deleting secrets:

[Getting variable values](https://docs.cyberark.com/conjur-enterprise/latest/en/Content/Developer/CLI/cli-variable.htm?tocpath=Developer%7CConjur%20CLI%7CConjur%20CLI%20command%20reference%7C_____11#variableget): Use the get subcommand to get the value of one or more Conjur variables.

```
# Gets the most recent value of the variable secrets/mysecret:
conjur variable get -i secrets/mysecret

# Gets the second version of the variable secrets/mysecret:
conjur variable get -i secrets/mysecret --version 2

# Gets the value of more than one variable at a time using the get command.
conjur variable get -i variable_name1,variable_name2
```

[Setting variable values](https://docs.cyberark.com/conjur-enterprise/13.0/en/Content/Operations/Policy/statement-ref-variable.htm#Settingvariablevalues): By design, policy does not set the variable value. Use the CLI, the UI, or the API to set the value.

Set (add) a variable value is:
```
conjur variable set -i <policy/path/variable-id> -v <value>
```
Where:
- `<policy/path/variable-id>` is the variable name, fully qualified to include the policy namespace where the variable is declared.
- `<value>` is the secret value.

[Deleting variable](): To clear the value of a variable (Conjur does not support deleting a variable via the CLI):
```
conjur variable set -i <policy/path/variable-id> -v ""
```

**Step 4**: Log Out of Conjur CLI
Once you're done with your operations, you can log out:
```
conjur authn logout
```