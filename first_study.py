#############################################
# PROJECT: LEVEL BASED PERSONA
#############################################
# Data Set Information:
# We have two data set. One of them users and the other purchase.
# These data sets belong to a phone application company

# Users Data Set:
# uid: Customer ID
# reg_date: date of registration
# device: phone software information
# gender: gender initials
# Country: Country name.
# age: age information

# Purchase Data Set:
# uid: Customer ID
# date: Purchase date
# price: purchase amount
#########################################################

import pandas as pd

# Data Sets
users = pd.read_csv('C:/Users/Asus/PycharmProjects/bootcamp/Week_2/users.csv')
purchases = pd.read_csv('C:/Users/Asus/PycharmProjects/bootcamp/Week_2/purchases.csv')

# We join data sets according to purchase
df = users.merge(purchases, how='inner', on='uid')
df.head()

# Looking unique customer id
df['uid'].nunique()

# looking at the total number of  each price
df['price'].value_counts()

# looking total price based on country, device, gender and age
agg_df = df.groupby(['country', 'device', 'gender', 'age']).agg({'price': sum}).sort_values('price', ascending=False)

agg_df.head()

# arrange the columns
agg_df = agg_df.reset_index()

# for safety
c_agg_df = agg_df.copy()

# Categorized the age column
agg_df['age'].value_counts(sort=False)
agg_df['age_cat'] = pd.cut(agg_df['age'], bins=[0, 18, 28, 38, 51, 60, agg_df['age'].max()],
                           labels=['0_18', '19_28', '29_38', '39_51', '52_60', '61_' + str(agg_df['age'].max())])
agg_df[['age', 'age_cat']].head(30)

# create to new column as customer level based
agg_df['customers_level_based'] = [col[0] + '_' + col[1].upper() + '_' + col[2] + '_' + col[5] for col in agg_df.values]

# delete old column except except price
agg_df.drop(['age', 'country', 'device', 'gender', 'age_cat'], axis=1, inplace=True)
agg_df = agg_df[agg_df.columns[::-1]]
agg_df.head()

# looking at the total prices of the segments
agg_df.groupby('segment').agg({'price': 'sum'})

# create a new dataframe including total price based on customer_level_based
df_last = agg_df.groupby('customers_level_based').agg({'price': 'sum'}).sort_values('price', ascending=False)
df_last.reset_index(inplace=True)

# making categorized by price range
df_last['segment'] = pd.qcut(df_last["price"], 4, labels=["D", "C", "B", "A"])
df_last.head(50)

# If a new customer sign in, we can compare according to our data.
new_user = "TUR_IOS_F_39_51"
new_user_data = df_last[new_user == df_last['customers_level_based']]
df_last.loc[new_user == df_last['customers_level_based']]







