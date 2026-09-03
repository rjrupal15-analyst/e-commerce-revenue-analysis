The Business Problem:
At an e-commerce company. The CEO asks:
"Our revenue has been inconsistent. I need to understand: which customers are most valuable, which products drive growth, and where are we losing money?"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

np.random.seed(42)

# Customers
customers = pd.DataFrame({
    'customer_id': range(1, 201),
    'name':        [f'Customer_{i}' for i in range(1, 201)],
    'segment':     np.random.choice(['Premium', 'Standard', 'Basic'], 200),
    'signup_date': pd.date_range('2023-01-01', periods=200, freq='2D')
})

# Products
products = pd.DataFrame({
    'product_id':  range(1, 21),
    'name':        [f'Product_{i}' for i in range(1, 21)],
    'category':    np.random.choice(['Electronics', 'Fashion', 'Grocery'], 20),
    'cost_price':  np.random.randint(100, 1000, 20),
    'sale_price':  np.random.randint(200, 2000, 20)
})

# Transactions
n = 1000
transactions = pd.DataFrame({
    'txn_id':      range(1, n+1),
    'customer_id': np.random.choice(range(1, 201), n),
    'product_id':  np.random.choice(range(1, 21), n),
    'date':        pd.date_range('2024-01-01', periods=n, freq='8H'),
    'quantity':    np.random.randint(1, 5, n),
    'status':      np.random.choice(['completed', 'returned', 'cancelled'], n,
                                    p=[0.7, 0.15, 0.15])
})
#here i checked the data quality

def data_quality_check(df, name):
    print(f"\n{'='*40}")
    print(f"Dataset: {name}")
    print(f"Shape: {df.shape}")
    print(f"\nNull values:\n{df.isnull().sum()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nSample:\n{df.head(3)}")

data_quality_check(customers, 'Customers')
data_quality_check(products, 'Products')
data_quality_check(transactions, 'Transactions')

#building a master data set by merging different tables
master = (transactions
          .merge(customers, on='customer_id', how='left')
          .merge(products,  on='product_id',  how='left'))

# Add calculated columns
master['revenue']      = master['quantity'] * master['sale_price']
master['cost']         = master['quantity'] * master['cost_price']
master['profit']       = master['revenue'] - master['cost']
master['profit_margin']= round(master['profit'] / master['revenue'] * 100, 2)
master['month']        = master['date'].dt.to_period('M')
master['weekday']      = master['date'].dt.day_name()

# Keep only completed transactions for revenue analysis
completed = master[master['status'] == 'completed'].copy()

#now here my analytical work to answer the question of ceo
# first i do revenue aanalysis 
# Monthly revenue trend
monthly = completed.groupby('month')['revenue'].sum().reset_index()
plt.figure(figsize=(12, 5))
plt.plot(monthly['month'].astype(str), monthly['revenue'],
         marker='o', color='blue', label='Revenue')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Revenue by segment
segment_rev = completed.groupby('segment')['revenue'].sum().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=segment_rev, x='segment', y='revenue', palette='Set2')
plt.title('Revenue by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()

# Revenue by category
category_rev = completed.groupby('category')['revenue'].sum().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=category_rev, x='category', y='revenue', palette='Set1')
plt.title('Revenue by Product Category')
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()

# Top 10 products
top_10 = (completed.groupby('pname')['revenue']
           .sum()
           .reset_index()
           .sort_values('revenue', ascending=False)
           .head(10))
plt.figure(figsize=(10, 5))
sns.barplot(data=top_10, x='revenue', y='pname', palette='viridis')
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue')
plt.tight_layout()
plt.show()

# Weekend vs Weekday
completed['is_weekend'] = completed['date'].dt.dayofweek >= 5
weekend_rev = completed.groupby('is_weekend')['revenue'].sum().reset_index()
weekend_rev['day_type'] = weekend_rev['is_weekend'].map(
    {True: 'Weekend', False: 'Weekday'}
)
plt.figure(figsize=(6, 5))
sns.barplot(data=weekend_rev, x='day_type', y='revenue', palette='Set2')
plt.title('Weekend vs Weekday Revenue')
plt.tight_layout()
plt.show()

# customer Analysis
# Customer lifetime value
cust_rev = (completed.groupby('customer_id')['revenue']
             .sum()
             .reset_index())
cust_rev.columns = ['customer_id', 'total_revenue']
print(cust_rev.sort_values('total_revenue', ascending=False).head(10))

# Segment customers
cust_rev['customer_segment'] = cust_rev['total_revenue'].apply(
    lambda x: 'VIP'        if x > 10000 else
              'Regular'    if x >= 5000 else
              'Occasional'
)
print(cust_rev['customer_segment'].value_counts())

# Churn risk
last_purchase = completed.groupby('customer_id')['date'].max()
customer_churn = pd.DataFrame({'last_purchase': last_purchase}).reset_index()
customer_churn['days_since'] = (
    pd.Timestamp.today() - customer_churn['last_purchase']
).dt.days
customer_churn['churn_risk'] = customer_churn['days_since'].apply(
    lambda x: 'Churn Risk' if x > 60 else 'Active'
)
print(customer_churn['churn_risk'].value_counts())

# Average order frequency
avg_frequency = completed.groupby('customer_id')['txn_id'].count().mean()
print(f"Average orders per customer: {avg_frequency:.1f}")

# product Analysis
#Profit margin per category
category_profit = completed.groupby('category').agg(
    total_revenue = ('revenue', 'sum'),
    total_profit  = ('profit', 'sum'),
    avg_margin    = ('profit_margin', 'mean')
).reset_index()
category_profit['avg_margin'] = category_profit['avg_margin'].round(2)
print(category_profit)

# Visualize
plt.figure(figsize=(8, 5))
sns.barplot(data=category_profit, x='category', y='avg_margin', palette='Set2')
plt.title('Average Profit Margin by Category')
plt.ylabel('Margin %')
plt.show()

# Return rate per product
return_rate = (master.groupby('pname')
               .apply(lambda x: round(
                   (x['status'] == 'returned').sum() / len(x) * 100, 2))
               .reset_index())
return_rate.columns = ['product', 'return_rate_pct']
return_rate = return_rate.sort_values('return_rate_pct', ascending=False)
print(return_rate.head(10))

# Best selling product per category
best_per_category = (completed.groupby(['category', 'pname'])['revenue']
                     .sum()
                     .reset_index()
                     .sort_values('revenue', ascending=False)
                     .groupby('category')
                     .first()
                     .reset_index())
print(best_per_category[['category', 'pname', 'revenue']])

# Products with negative profit
negative_profit = products[products['cost_price'] > products['sale_price']]
print(f"Products with negative profit margin: {len(negative_profit)}")
print(negative_profit[['pname', 'category', 'cost_price', 'sale_price']])

