# -*- coding: utf-8 -*-
"""
YOUR NAME:陈晗之
YOUR ID:2312410011
"""

"""
Make sure you have install all the modules need for this class
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Exercise Three
"""
#define your directory first
import os
os.chdir("C:\\Users\\KevinChen\\Desktop\\my_python")

#Question one: Derive Gamma 
"""
Just like we did with Delta, we can calculate Gamma using both the exact mathematical formula (closed form) and a numerical approximation.

While Delta measures how much the option price changes for a $1 move in the stock, Gamma measures how much the Delta itself changes for 
a $1 move in the stock. In calculus terms, it's the second derivative of the option price with respect to the underlying stock price.
"""

from math import log, sqrt, exp
import scipy.stats as stats

#The formula for Delta 
tiny=1e-9;S=40;X=40;T=0.5;r=0.01;sigma=0.2

def bsCall(S,X,T,r,sigma):
    d1=(log(S/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))
    d2 = d1-sigma*sqrt(T)
    return S*stats.norm.cdf(d1)-X*exp(-r*T)*stats.norm.cdf(d2)

def delta1_f(S,X,T,r,sigma):
    d1=(log(S/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))
    delta=stats.norm.cdf(d1)
    return(delta) 
#
def delta2_f(S,X,T,r,sigma):
    s1=S
    s2=S+tiny
    c1=bsCall(s1,X,T,r,sigma)
    c2=bsCall(s2,X,T,r,sigma)
    delta=(c2-c1)/(s2-s1)
    return(delta)

#
delta1=round(delta1_f(S,X,T,r,sigma),6)
delta2=round(delta2_f(S,X,T,r,sigma),6)
print(f"delta (close form)={delta1}")
print(f"delta (tiny number)={delta2}")


#Create your own codes for gamma 

# Parameters
tiny = 1e-9
bump = 1e-4 # Used for Gamma numerical approximation (see explanation below)
S = 40; X = 40; T = 0.5; r = 0.01; sigma = 0.2

# 1. Base Pricing Function

def bsCall(S, X, T, r, sigma):
    d1 = (log(S/X) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return S * stats.norm.cdf(d1) - X * exp(-r * T) * stats.norm.cdf(d2)


# 2. Method 1: Analytical Gamma (Closed Form)

def gamma1_f(S, X, T, r, sigma):
    gamma = delta1_f(S, X, T, r, sigma) * (1 / (S * sigma * sqrt(T)))
    return gamma


# 3. Method 2: Numerical Gamma (Finite Difference)

def gamma2_f(S, X, T, r, sigma):
    s1 = S - bump
    s2 = S + bump
    c1 = bsCall(s1, X, T, r, sigma)
    c2 = bsCall(S, X, T, r, sigma)
    c3 = bsCall(s2, X, T, r, sigma)
    
    # Using central difference formula for second derivative
    gamma = (c3 - 2 * c2 + c1) / (bump ** 2)
    return gamma

# 4. Output
gamma1 = round(gamma1_f(S, X, T, r, sigma), 6)

gamma2 = round(gamma2_f(S, X, T, r, sigma), 6)

print(f"gamma (close form)={gamma1}")
print(f"gamma (numerical)={gamma2}")



#Question two: SQL practice question
#based on the SQL example demonstrated, write codes to left join the two datasets

import sqlite3

# 1. Connect to an in-memory database (disappears when the script ends)
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 2. Create the tables
cursor.execute('''
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
)
''')

cursor.execute('''
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    dept_id INTEGER
)
''')

# 3. Insert the mock data
cursor.executemany('INSERT INTO departments VALUES (?, ?)', [
    (10, 'Engineering'),
    (20, 'Sales'),
    (30, 'Marketing')
])

cursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', [
    (1, 'Alice', 10),
    (2, 'Bob', 20),
    (3, 'Charlie', None)  # Charlie has no department
])

# 4. Define ONLY the LEFT JOIN query
left_join_query = '''
    SELECT employees.name, departments.dept_name
    FROM employees
    LEFT JOIN departments ON employees.dept_id = departments.dept_id
'''


#Save and Close the connection
import pandas as pd
df = pd.read_sql_query(left_join_query, conn)
df.to_csv("left_join_employee_data.csv", index=False)
conn.close()


#Question three: Volatility smile practice
#based on the volatility smile example demonstrated, write codes to finish the steps

#Task one: Write a new function that calculates the implied volatility for a Put option using the same brute-force approach.

#Hint: The Black-Scholes formula for a Put option is: P = X  e^{-rT} N(-d_2) - S N(-d_1)

def implied_vol_put_min(S, X, T, r, p): 
    implied_vol = 1.0
    min_value = 100
    for i in range(10000):
        sigma = 0.0001 * (i + 1)
        d1 = (log(S/X) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
        d2 = d1 - sigma * sqrt(T)
        put_price = X * exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
        
        # Calculate the absolute difference between the calculated put price and the market price
        abs_diff = abs(put_price - p)
        
        # Update implied volatility if this is the smallest difference found so far
        if abs_diff < min_value:
            min_value = abs_diff
            implied_vol = sigma
    return implied_vol


#Task two: Use the apply() method to create a new column directly in the DataFrame.

#Hint: In Step 4, we use a for loop to go through the option chain. Your task is to eliminate the for loop completely. Use Pandas vectorization to calculate the Mid Price (c), and then use the df.apply() method to calculate the implied volatility and store it as a new column in the calls DataFrame called Implied_Vol.

# Assuming Step 1, 2, and 3 have already run, and 'calls' is our dataframe.
calls = pd.DataFrame({
    'Bid': [2.5, 3.0, 3.5],
    'Ask': [2.7, 3.2, 3.8],
    'Strike': [40, 45, 50]
})
# 1. Calculate Mid Price for the whole column at once 
calls['Mid_Price'] = (calls['Bid'] + calls['Ask']) / 2.0

# 2. Filter out bad data (where c <= 0)
calls_clean = calls[calls['Mid_Price'] > 0].copy()

# 3. Use lambda and apply to run the function across the dataframe
# axis=1 means "apply this function across each row"
calls_clean['Implied_Vol'] = calls_clean.apply(lambda row: implied_vol_put_min(S, row['Strike'], T, r, row['Mid_Price']), axis=1)