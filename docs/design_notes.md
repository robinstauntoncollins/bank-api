## Initial Design

* Customers collection, Accounts collection, Transactions collection

* 'Internal' RESTful API based on these collections and another 'Intent' API which may not be so RESTful using verbs instead
of nouns like '/transfer', '/openAccount'.

* Relationship between customer db model and account db model - view list of accounts owned by that customer

* Relationship between account db model and transaction db model - view list of transaction owned by that account

* Intent API endpoints: '/openAccount', '/transfer', '/customerInfo' - these could call the Internal API in whatever combination required to fulfill the request.

### Random thoughts

* I like snake_case for endpoints, parameters etc. however many developers (from Java backgrounds) may prefer camelCase. Internal API will use snake_case while Intent API will use camelCase. 

* Will go for two separate collections for '/accounts' and '/transactions' rather than having the transactions for the account accessible through '/accounts/<account_id>/transactions/<transaction_id>' as it's more straightforward initially. That can always be added as a convenience later. 

* Two tables - one for Accounts another for Transactions

### Considerations

### Architecture

* Separate services might be fairly straightforward (two separate Flask application). In the interest of project time and scope these could call eeachother directly however some sort of service registry would be a good idea to avoid using IP and PORT.


### Database

How to ensure a transaction is not performed twice? Idempotent operations somehow? 

Having some sort of append only ledger type database for transactions and calculating the account balance from that when required would be important to ensure data consistency. However, how exactly to achieve this not yet known.


### Security

* Proper authentication should be used tokens, OAuth, that sort of thing. Not used here for sake of time and project scope

* HTTPS should be used. Not used here for the sake of time and project scope


