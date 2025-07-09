# Hist Website / Application

## Overview
Hist is a website which allows you to see how Indexes and Stocks performed over very specific time frames which you can pick.

## How to Launch

### AWS Elasticbean Stalk
This application is supposed to be a SaaS for the user hosted on AWS Elastic Beanstalk but due to monetary reasons the Website is not currently available.

For future use it is fairly simple to launch on Elastic Beanstalk just do the following. 

1. Clone down Repo
2. Uncompress CSVs if Compressed (Larger ones are currently compressed, S&P and Russell)
3. Run update.py as CSVs are not dynamically / automatically updated (May have to set up venv using flask steps below) 
4. Compress whole repo and upload to Elastic Beanstalk in AWS
5. May have to configure Loadbalancer

Note: Make sure histfinance.com is still owned
Note: Step 3 is not necessary, but website will be using out of date data otherwise

### Flask
We can also host this website locally through Flask

#### Set up venv
```
#In project directory, create venv however you prefer (conda, vscode, python, pip, etc.)
python3.11 -m venv venvname 

# Activate venv
source venvname/bin/activate

# Install reqs. Note: You may have to upgrade version of yfinance
pip install -r requirements.txt
```
#### Run app.py using venv
Note: May have to adjust systems firewall rules or whatnot if you want to connect from another device


#### Future Work
1. Set up Beanstalk / Loadbalancer through IaC such as terraform. Not really necessary as Elastic Beanstalk is almost serverless.
2. Dynamically update CSVs or retrofit code to directly call API rather than reading CSVs
3. Add more categories / indicators to compare on and plot ( not much code changes to do for this)

## Website!!


