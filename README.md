# SeniorDesign

## Overall Description

  - A platform that allows a user to a company (such as Amazon) to not have their personal information leaked. This includes: names, addresses, credit card numbers, etc.
       These items will be encrypted, only the user has direct access to this.
       This will help with identify theft: https://www.fastcompa.com/3055875/how-amazons-customer-service-could-open-you-up-to-identity-theft

## Actionable Requirements

Client/Customer Side:
- User AKA Customer Account Creation
- User Login
- User Access Orders

Customer Service Representative (CSR) Side:
  - Company Account Creation
  - Company Login
  - Company Access Orders
  - Order information is hashed or anonymized
  
  Company Side:
  - Admin Login
  - Admin can manage database and see unencrypted information
  - Special and access to information, does not speak to customers
  - Testing
  
  Testing:
  - CSR cannot see any of the client's personal information
  - CSR is able to use client's name encrypted, and customer sees their own information
  - Customer cannot 'break' system (by putting in their encrypted name, unbeknowingly)

## SetUp 
Make Prod
  - makes the "make tests" unit tests in the SoftEng repository
  - commits and pushes all modifications

  make dev_env
  - Running this will install all of the requirements from the requirements-dev.txt file, requirements.txt and the heroku requirements file. 

  make tests 
  - makes unit tests in the SoftEng repository 

  make deploy
  - runs ./venv/app/app.py which will run MySQL database and Heroku (if logged in)

  Run Heroku 
  - Its located in the venv/ folder (make sure to be logged in)
  - pip install -r requirements.txt  (make sure to have correct installations)
  - heroku login 
  - heroku local web (http://127.0.0.1:5000/)

  Update Heroku 
  - git push heroku main (update from the main branch)

  Database Setup
  - Prerequisites: PyMySQL, MAMP, PhpMyAdmin, MySQL
  - Start Servers on MAMP
  - Have commands run in Create.sql
  - Have app.py run (either on CLI or via tests)
  - Located on Port 5000 (or your own defined port)

## Run App 
  - clone repo
  - Go through SetUp 
    - make dev_env
  - heroku login 
  - WAMP login for access to database and local host
  - make deploy (or navigate to ./venv and heroku local web)
