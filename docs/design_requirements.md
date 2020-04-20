# Task

Design an API to be used for opening a new current account of an already existing customer.

### Requirements

* The API will expose an endpoint which accepts the user information (customerID, initialCredit)
* Once the endpoint is called, a new account will be opened and connected to the user whose ID is customerID
* If initialCredit is not zero, a transaction will be sent to the new account.
* Another endpoint will output the user information showing Name, Surname, Balance and the transactions of the account

### Bonus

* Accounts and Transactions are different services
* Front end (simple is ok)
* Attention to CI/CD

### Constraints

* Use any open source tool or framework

* An in-memory database can be used

#### Other info

* Consider layers (boundaries?), abstractions, testability, enterprise-level architecture

* Demonstrate good git practise and workflow in team environment

* Testability will be assessed

* Show knowledge beyond boilerplate endpoints


