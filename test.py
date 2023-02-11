import csv

#

with open('datasets/sp500.csv') as f:
        companies = f.read().splitlines()
        print(companies)

