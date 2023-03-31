# Power BI Embedded sample in Flask framework


### Requirements

1. [Python 3](https://www.python.org/downloads/)

2. IDE/code editor. We recommended using Visual Studio Code.


### Set up a Power BI app

Follow the steps on [aka.ms/EmbedForCustomer](https://aka.ms/embedforcustomer)


## Setup fo local

### Set up Python Flask on a Windows machine

1. [Install](https://docs.python.org/3/using/index.html) [Python 3](https://www.python.org/downloads/) and add its installation path to the *Path* environment variable.

2. Run the following command in CMD/PowerShell in the path where [requirements.txt](./requirements.txt) file is located.<br>

   `pip3 install -r requirements.txt`


### Run the application on localhost

1. Open IDE.

2. Open [app](./app) folder.

3. Fill in the required parameters in the [config.py](./app/config.py) file related to AAD app, Power BI user account information (If only use MasterUser authentication mode).

4. Run the following command in CMD/PowerShell to start the application.<br>

   `flask run`


5. Open **http://localhost:5000** in browser or follow the direction in the output log.

> **Note:** Whenever you update the config file you must restart the app.


## Setup fo Docker


1. Open IDE.

2. Open [app](./app) folder.

3. Fill in the required parameters in the [config.py](./app/config.py) file related to AAD app, Power BI user account information (If only use MasterUser authentication mode).

4. Run the following command in CMD/PowerShell to build docker image.<br>

   `docker build -t power-bi-service .`

4. Run the following command in CMD/PowerShell to run docker container.<br>

   `docker-compose up -d`

5. Open **http://localhost:5058** in browser or follow the direction in the output log.

#### Supported browsers:

1. Google Chrome

2. Microsoft Edge

3. Mozilla Firefox

### Important

For security reasons, in a real world application, passwords and secrets should not be stored in config files. Instead, consider securing your credentials with an application such as Key Vault.
