# ASSET
concisely known as **Analysis** that is super **Superb**, calculated using **Stock** and cash **Entry Trackers** (ASSET)

### [API link]: https://pfinancer.herokuapp.com/

## Project Overview

ASSET is an API used for storing, tracking and analyzing personal financial assets. Based off my own personal need to get *my* messy finances and impulsive stock purchases in order, ASSET stores a user's cash and financial market assets in its database, and can be used to conduct real time analytics both across time periods and at any particular instant in the user's financial history. 

ASSET was created in Python using Django REST framework, connected to a MongoDB database and deployed using Heroku. Real time financial data is scraped from yahoo finance using  Python's YFinance library. Analytics code can be found in the module nwtracker. 

## Features
ASSET can currently conduct analytics across time for any two dates - the notable ones include:
- Raw and percent total growth
- Raw and percent portfolio growth
- Raw Profit and Loss
- Raw Non Market Growth (ie raw total growth - raw profit and loss)

ASSET will store any stock transactions and cash entries that a user logs, and use these for analysis. ASSET uses token-based user authentication. 

## Use Case Tutorial
ASSET API works by reading the data field of any HTTP requests, and returning info in the data fields. All data fields are in JSON. 

### 1. Create an account
To begin, create a new account with a unique username. This will create a user in the database and return a token which is required for all activities associated with the user.

##### Request:
API Endpoint: /signup
HTTP Method: POST
Example data:
```json
{
    "username": "myusername",   
    "password": "hopefullystrongpassword"
}
```

##### Response:
Example response data:
```json
{
    "token":"9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 2. Add Stock Transactions
Now that we have our authentication token, I can begin to populate my profile with all my GME diamong hand longs. Remember to add the token as a string `"Token " + <my_token>` with the token obtained from before in the http authorization header, or else the request will fail. 

##### Request:
API Endpoint: /stocktrxn/
HTTP Method: POST
HTTP Authorization header = `"Token <my_token>"`
Example data:
```json
{
    "date": "2022-01-01", // yyyy-mm-dd
    "ticker": "BABA", // must be valid ticker found in yahoo finance
    "quantity": 100,
    "price": 101,
    "type": "b" // must either be 'b' or 's' for buy or sell
}
```

##### Response:
Expected response code: 200 OK

### 3. Add Cash Entries
We do the same for cash entries. Note that as a design choice, unlike stock transactions, cash entries is simply the total balance of cash the user has at any date, for the currencies indicated. 

##### Request:
API Endpoint: /cashentries/
HTTP Method: POST
HTTP Authorization header = `"Token <my_token>"`
Example data:
```json
{
	"date": "2022-01-01",
	"single_entries": [
	    {
	        "currency": "USD",
	        "quantity": 1000
	    },
	    {
	        "currency": "SGD",
	        "quantity": 2000
	    },
	    {
	        "currency": "HKD",
	        "quantity": 3000
	    }
	]
}
```       

##### Response:
Expected response code: 200 OK

### 4. Get analysis across time
Now that we have populated our profile with transactions and cash, we can ping the API to conduct some analysis. Excitinggg.

##### Request:
API Endpoint: /acrosstime/
HTTP Method: POST
HTTP Authorization header = `"Token <my_token>"`
Example data:
```json
{
	"date_bef":"2022-1-1", // yyyy-mm-dd
	"date_aft":"2022-1-2", // yyyy-mm-dd, must be after date_bef
	"currency":"HKD" // currency used to calculate raw growth
}
```       

##### Response:
Expected data:
```json
{
	"raw_total-growth": 1000, 
	"percent_total_growth": 80.2,
	"raw_portfolio_growth": 800.4,
	"raw_profit_and_loss": 67.4,
	"raw_non_market_growth": 703
}
```      
## API Endpoints
## `/`
#### GET
Provides a list of all IDs of all stock transactions and cash entries associated with the user

## /login
#### POST
Request provides username and password of previous user, response provides authentication token. 

Required data fields:
- Username
- Password

## /signup
#### POST
Request provides username and password to create user for the first time, response provides authentication token. 

Required data fields:
- Username
- Password

## /stocktrxns
#### GET
Get a detailed list of all associated stock transactions with the user

#### POST
Add a new stock transaction. 
Required data fields:
```
{
    "date" //"yyyy-mm-dd"
    "ticker",
    "quantity",
    "price",
    "type", // must either be 'b' or 's' for buy or sell
}
```


### /stocktrxns/`<id>`
#### DEL
Deletes the transaction with id=`<id>`, if it is owned by the user currently logged in

#### PUT
Updates the transaction with id=`<id>` using the same format as posting a stock transaction, if it is owned by the user currently logged in

## /cashentries
#### GET
Get a detailed list of all associated cash entries with the user

#### POST
Add a new cash entry.

Required fields:
```
{
	"date" // "yyyy-mm-dd"
	"single_entries": [
	    {
	        "currency",
	        "quantity",
	    }
	]
}
```       


### /cashentries/`<d>`
#### DEL
Deletes the cash entry with id=`<id>`, if it is owned by the user currently logged in

#### PUT
Updates the cash entry with id=`<id>` using the same format as posting a cash entry, if it is owned by the user currently logged in

## /acrosstime

#### POST
Get analysis on financial performance between any two dates, and a given currency. Currently, the analytics fields supported are:

- Raw and percent total growth
- Raw and percent portfolio growth
- Raw Profit and Loss
- Raw Non Market Growth (ie raw total growth - raw profit and loss)

Required fields:
```
{
	"date_bef" // yyyy-mm-dd
	"date_aft" // yyyy-mm-dd, must be after date_bef
	"currency"// Format: "XXX" e.g. HKD, SGD, USD
}
```   

## Future Work
In order of priority
1. Streamline yfinance scraping process, as this is currently slowing down analytics since we scrape yfinance every time we conduct analytics. The current plan is to store a local copy of historical stock data and only scrape from yfinance when a user needs real-time data or the historical data needs updating (ie we moved on to the next day).
2. Further analytics 
a. Analytics on portfolios at any instant in time e.g. total stocks at any point in time, breakdown by industry, average P/E values etc
3. Create a front-end facing application for users to interact with on browser / mobile

## Design choices
Why Django REST framework? I chose it for its quick pipeline and simplicity, and its large library of in-built support for testing. I was also working with yfinance module in python beforehand and Django was a good choice for creating a back-end app in python. 

## License

MIT


