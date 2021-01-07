# Acceptance Test

To run the acceptance test, run the commands below.

```shell
node install
node run test
```
To clean the database (devices, templates and flows) and run the acceptance test, run the commands below.

```shell
node install
node run test:clearDb
```

There are 2 types of scenarios: Basic and Advanced.
In order to run each scenario, run the following command:

```shell
node run test:basic
node run test:adv
```
