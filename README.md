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
python3.11 -m venv venvname (python3.11.9)

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

### Homepage

Tabs at top bring you to the other screens, each box on homescreen describes the application of the screen
<img width="1440" alt="Screenshot 2025-07-07 at 10 00 11 PM" src="https://github.com/user-attachments/assets/0911ad8c-3f6a-44fd-98ae-339ed1e7dcf3" />

<img width="1440" alt="Screenshot 2025-07-07 at 10 00 27 PM" src="https://github.com/user-attachments/assets/ee010a4c-f91d-47c9-b37b-e963cf6fbc21" />

<img width="1440" alt="Screenshot 2025-07-07 at 10 00 42 PM" src="https://github.com/user-attachments/assets/6a180f4a-3b05-4b38-b754-98ae875d93c0" />

Here we added the volume being plotted underneath as well.

<img width="1440" alt="Screenshot 2025-07-07 at 10 00 55 PM" src="https://github.com/user-attachments/assets/42d3b447-7e15-4a2a-b136-68b5136cb96a" />

## Historical Analysis

Choose a Ticker, the data you would like to plot it on, the interval type (days, weeks, months, quarters, years), choose if you want to see the volume plotted below as well.

<img width="1440" alt="Screenshot 2025-07-07 at 10 02 53 PM" src="https://github.com/user-attachments/assets/a4c77c79-d7f9-473a-88bb-a5483f73ad82" />

<img width="1436" alt="Screenshot 2025-07-07 at 10 03 14 PM" src="https://github.com/user-attachments/assets/43a1d74d-5c3a-4966-a6fe-36b1034e4407" />

<img width="1439" alt="Screenshot 2025-07-07 at 10 04 21 PM" src="https://github.com/user-attachments/assets/ce59afd0-1ab5-42c1-9143-c4fdbb9e1985" />

As you can see we plotted Nvidia stock over the two weeks around July 4th over the past 5 years. This can be usefull for timing up when to buy stocks. Like seeing if a stock typically does good around Christmas time.

<img width="1440" alt="Screenshot 2025-07-08 at 12 01 27 AM" src="https://github.com/user-attachments/assets/e968d701-e72f-4b11-864f-977e21b26eb4" />

<img width="1440" alt="Screenshot 2025-07-08 at 12 01 43 AM" src="https://github.com/user-attachments/assets/f44a75f3-c0fd-4911-ac17-25a5f5f06836" />

<img width="1440" alt="Screenshot 2025-07-08 at 12 09 19 AM" src="https://github.com/user-attachments/assets/e92945fb-9c4c-42fb-b5d9-bbb830c36a69" />

## Stock Comparison

This next screen has similar inputs but can compare what stocks do the best within a bunch of different indexes. This can help you determine what stock you want to buy and then you can research it more in depth on the previous screen.

<img width="1440" alt="Screenshot 2025-07-08 at 12 09 37 AM" src="https://github.com/user-attachments/assets/ba1db037-0098-4014-b29d-36fe610e3041" />

<img width="1440" alt="Screenshot 2025-07-08 at 12 11 23 AM" src="https://github.com/user-attachments/assets/4ff02eb8-13df-49d7-9e1c-b8fb41cc2f1f" />

Here we can see the top 10 movers from the Consumer Discretionary Sector of the S&P500 around July 4th time over the past 5 years.

<img width="1440" alt="Screenshot 2025-07-08 at 12 22 48 AM" src="https://github.com/user-attachments/assets/f0d49c9f-0f63-4d18-ab2a-8a9613ab0598" />


## Other Screens

Unfortunatly the other screens fall under future work. But you can read about the plan for them on the Homepage!

<img width="1440" alt="Screenshot 2025-07-08 at 12 23 13 AM" src="https://github.com/user-attachments/assets/27fbae71-e35a-4638-86a8-ea5a3f1df7ec" />












