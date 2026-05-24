import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv', encoding='latin1')

print("Data Loaded!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

print("Missing values:\n", df.isnull().sum())

df.dropna(inplace=True)

df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]


df['TotalSale'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['Month'] = df['InvoiceDate'].dt.month
df['InvoiceDate'].dt.year   
df['InvoiceDate'].dt.day   
df['InvoiceDate'].dt.hour  

df['MonthName'] = df['InvoiceDate'].dt.strftime('%B')

df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()

df[['Quantity', 'UnitPrice', 'TotalSale', 'Month', 'MonthName', 'DayOfWeek']].head()


print("="*40)

print(f"Total Orders: {df['InvoiceNo'].nunique()}")
print(f"Total Revenue: £{df['TotalSale'].sum():,.2f}")
print(f"Avg Order Value: £{df.groupby('InvoiceNo')['TotalSale'].sum().mean():,.2f}")

monthly_revenue = df.groupby('MonthName')['TotalSale'].sum().round(2)
print("\n📅 Monthly Revenue:\n", monthly_revenue.sort_values(ascending=False))

top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print("\n🏆 Top 10 Products:\n", top_products)

top_countries = df.groupby('Country')['TotalSale'].sum().sort_values(ascending=False).head(5)
print("\n🌍 Top 5 Countries:\n", top_countries)

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 5)

# Month order
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

monthly_sorted = monthly_revenue.reindex(month_order).dropna()

plt.figure(figsize=(12,5))
bars = plt.bar(monthly_sorted.index, monthly_sorted.values, 
               color='steelblue', edgecolor='white')

plt.title('📈 Monthly Revenue Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Revenue (£)')
plt.xticks(rotation=45)


for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 1000,
             f'£{bar.get_height():,.0f}', 
             ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('graph1_monthly_revenue.png', dpi=150)
plt.show()
print("Graph 1 Save!")

#graph 2

plt.figure(figsize=(12,6))

top_products.sort_values().plot(kind='barh', 
                                 color='coral', 
                                 edgecolor='white')

plt.title('🏆 Top 10 Best Selling Products', fontsize=16, fontweight='bold')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Name')
plt.tight_layout()
plt.savefig('graph2_top_products.png', dpi=150)
plt.show()
print("Graph 2 Save!")

#Graph 3 — Countries Pie Chart

plt.figure(figsize=(8,5))

top_countries.plot(kind='pie', 
                   autopct='%1.1f%%',
                   startangle=140,
                   colors=['#2196F3','#FF5722','#4CAF50','#FF9800','#9C27B0'])

plt.title('🌍 Revenue by Country (Top 5)', fontsize=16, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.savefig('graph3_countries.png', dpi=150)
plt.show()
print("Graph 3 Save")

#Graph 4 — Best Day of Week 
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Sunday']
day_revenue = df.groupby('DayOfWeek')['TotalSale'].sum().reindex(day_order)

plt.figure(figsize=(10,5))

day_revenue.plot(kind='bar', 
                 color='mediumseagreen', 
                 edgecolor='white')

plt.title('📅 Revenue by Day of Week', fontsize=16, fontweight='bold')
plt.xlabel('Day')
plt.ylabel('Total Revenue (£)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('graph4_dayofweek.png', dpi=150)
plt.show()
print("Graph 4 Save")

print("\nPROJECT COMPLETE!")