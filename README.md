# Log Analysis Project # 
Log Analysis is a python program that reports against a mock psql news database. It prints out to the terminal the three most popular articles, the popularity of authors ranked by views, and the days which had request errors greater than 1% in that order. The program is split into three functions which each make seperate db calls to generate the three reports. 

# Installation #
You can get the newsdata.sql file for the mock database [I'm an inline-style link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once you have that zip file downloaded and unzip it. Start by creating the news database first. Make sure you are in the psql command line and run:

`CREATE DATABASE news;`

You can now exit the psql command line. To import the schema and data into the news database run the following command from the terminal:

`psql -d news -f newsdata.sql`

If you do not have the psycopg2 module installed, from the terminal run:

`pip install psycopg2`

To run the reports type the following from the command line:

`python log_analysis.py`
