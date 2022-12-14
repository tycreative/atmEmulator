# ATM Emulator
This software is slightly old and may no longer work with modern versions of Python and Django framework.
You might need to test out different versions of Python and Django to see which will run it and make sure to follow Django initialization steps.

## About
ATM emulator made using Python and Django framework. Designed to emulate how an actual ATM (Automatic Teller Machine) works.
Pages are constructed when loaded using multiple template files so raw html files may look incomplete.
These template files may also use variables to fit the desired page or to present the data available consistently.

This software allow users to
1. Transfer Cash
  - Either between own accounts or from user's account to another bank user
  - Cannot transfer more funds than have
2. Withdraw Cash
  - Select from own accounts
  - Can withdraw more than available in account (like a bank loan)
3. Deposit Cash
4. Inquire Balance
5. View Transaction History
  - Able to sort transactions by machine, account, type, amount, or date
6. Change Card PIN

This software allows admins to
1. Manage ATM Cards
  - Activate/deactivate
  - Create/delete
  - Change other details
2. Manage Accounts
  - Create/delete
  - Assign/deassign cards
  - Change other details
3. Manage ATM Machines
  - Activate/deactivate
  - Create/delete
  - Update balance
  - Set minimum balance

## Emulation
Starts with a location/machine selection page
![Welcome page](screenshots/welcome_page.png?raw=true)

Once machine is selected, a login prompt will appear
![Login page](screenshots/login_page.png?raw=true)

Once logged in, user dashboard page is loaded
![Dashboard page](screenshots/dashboard_page.png?raw=true)
From here you can make transfers, deposits, and withdrawals. You can also view transactions, accounts, and cards. There are quick actions as well.

Transfers page - also shows recent transfers
![Transfers page](screenshots/transfers_page.png?raw=true)

Start new transfer page
![New transfer page](screenshots/new_transfer_page.png?raw=true)

Deposits page - also shows recent deposits
![Deposits page](screenshots/deposits_page.png?raw=true)

Start new deposit page
![New deposit page](screenshots/new_deposit_page.png?raw=true)

Withdrawals page - also shows recent withdrawals
![Withdrawals page](screenshots/withdrawals_page.png?raw=true)

Start new withdrawal page
![New withdrawal page](screenshots/new_withdrawal_page.png?raw=true)

Transactions history page - sortable by column
![Transactions page](screenshots/transactions_page.png?raw=true)

Account details page - quick actions available as well
![Account details page](screenshots/account_details_page.png?raw=true)

Card details page - quick actions available as well
![Card details page](screenshots/card_details_page.png?raw=true)

Changing account phone number
![Change phone number page](screenshots/change_phone_number_page.png?raw=true)

Changing card PIN
![Change pin page](screenshots/change_pin_page.png?raw=true)
