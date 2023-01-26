#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


get_ipython().run_cell_magic('time', '', 'df_raw = pd.read_excel("./data/split_purchase_data.xlsx")')


# In[6]:


df_raw.head(10)


# In[7]:


df_raw['Purchase Requisition Date'] = pd.to_datetime(df_raw['Purchase Requisition Date'])
df_raw['Purchase Requisition Number'] = df_raw['Purchase Requisition Number'].astype(str)


# In[8]:


df_raw.info()


# # Calculation of Split Purchase based on Item

# In[9]:


item_field = 'Item'


# In[10]:


df_dept_item_sorted = df_raw.sort_values(['Purchasing Department', item_field,'Purchase Requisition Date'])


# In[11]:


df_dept_item_sorted['Prev PR Date'] = df_dept_item_sorted['Purchase Requisition Date'].shift()


# In[12]:


df_dept_item_sorted['PreGroup'] = df_dept_item_sorted[['Purchasing Department', item_field,'Purchase Requisition Date']].groupby(['Purchasing Department', item_field]).cumcount()


# In[13]:


df_dept_item_sorted.head()


# In[14]:


mask = df_dept_item_sorted['PreGroup'] == 0
df_dept_item_sorted.loc[mask,'Prev PR Date'] = pd.NaT


# In[15]:


#Calculating number of days difference between adjacent records
df_dept_item_sorted['Date_Diff'] = (df_dept_item_sorted['Purchase Requisition Date'] - df_dept_item_sorted['Prev PR Date']).dt.days


# In[16]:


#Set Threshold 
n = 5
df_dept_item_sorted['Flag Out of Range'] = (1 - (df_dept_item_sorted['Date_Diff'] <= n)).astype(int)


# In[17]:


df_dept_item_sorted['Grouping'] = df_dept_item_sorted['Flag Out of Range'].cumsum()


# In[18]:


df_dept_item_sorted.head()


# In[19]:


df_pr_count = df_dept_item_sorted[['Grouping',item_field,'Purchase Requisition Number']].groupby(['Grouping',item_field]).nunique().reset_index()


# In[20]:


df_pr_count.columns = ['Grouping', item_field, 'Count PR']


# In[21]:


# Identifies the groups that are valid split purchase cases
df_split_purchase_group = df_pr_count[df_pr_count['Count PR']>=2]


# In[22]:


# Joining of Split Purchase Groups to initial details
df_split_purchase_details = df_split_purchase_group.merge(df_dept_item_sorted,
                                                          how='inner',
                                                          on= ['Grouping',item_field])


# In[23]:


df_split_purchase_details.head()


# In[24]:


df_split_purchase_details['Date_Diff'] = np.where(df_split_purchase_details['Flag Out of Range'] == 1,
                                                  pd.NaT,
                                                  df_split_purchase_details['Date_Diff'])


# In[25]:


df_split_purchase_details.sort_values(['Grouping','Purchase Requisition Number'], inplace=True)


# In[26]:


df_split_purchase_desc = df_split_purchase_details.groupby(['Grouping',item_field]).agg({'Purchase Requisition Number': '|'.join}).reset_index()


# In[27]:


df_split_purchase_desc.columns = ['Grouping', item_field, 'PR with similar items']


# In[28]:


df_split_purchase_comb = df_split_purchase_details.merge(df_split_purchase_desc,
                                                         how='inner',
                                                         on=['Grouping',item_field])


# In[29]:


df_split_purchase_comb


# ### Derive futher prioritization based on rules
# 
# - Was the threshold avoided due to the split ?
# - Are the splits belonging to the same vendor ?
# - Are the dates diff within one day ?

# In[30]:


df_priority_score = df_split_purchase_comb.groupby(['Grouping']).agg({
    'Total Value':['min','sum'],
    'Date_Diff':'min',
    'Vendor':['nunique','count']
}).reset_index()


# In[31]:


df_priority_score.columns = ['Grouping', 'Min_Value', 'Max_Value', 'Min_Date_Diff', 'Unique_Vendor', 'Count_Vendor']


# In[32]:


value_threshold = 5_000
df_priority_score['Flag_Threshold_Crossed'] = ((df_priority_score['Min_Value'] < value_threshold) & (df_priority_score['Max_Value'] >= value_threshold)).astype(int)


# In[33]:


df_priority_score['Flag_Same_Vendor'] = ((df_priority_score['Unique_Vendor'] == df_priority_score['Count_Vendor'])).astype(int)


# In[34]:


days_threshold = 1
df_priority_score['Flag_Min_Days'] = (df_priority_score['Min_Date_Diff'] <= days_threshold).astype(int)


# In[35]:


df_priority_score['Score'] = df_priority_score['Flag_Threshold_Crossed'] + df_priority_score['Flag_Same_Vendor'] + df_priority_score['Flag_Min_Days']


# In[36]:


df_priority_score


# In[37]:


df_sop_item = df_split_purchase_comb.merge(df_priority_score,
                                           how='left',
                                           on='Grouping')


# In[38]:


df_sop_item.insert(0,'Item Type',f"1_{item_field}")


# In[39]:


df_sop_item.head()


# ## Performing the calculations for Split Purchase based on Item Categories

# In[40]:


item_field = 'Item Category'


# In[41]:


df_dept_item_sorted = df_raw.sort_values(['Purchasing Department', item_field,'Purchase Requisition Date'])


# In[42]:


df_dept_item_sorted['Prev PR Date'] = df_dept_item_sorted['Purchase Requisition Date'].shift()


# In[43]:


df_dept_item_sorted['PreGroup'] = df_dept_item_sorted[['Purchasing Department', item_field,'Purchase Requisition Date']].groupby(['Purchasing Department', item_field]).cumcount()


# In[44]:


df_dept_item_sorted.head()


# In[45]:


mask = df_dept_item_sorted['PreGroup'] == 0
df_dept_item_sorted.loc[mask,'Prev PR Date'] = pd.NaT


# In[46]:


#Calculating number of days difference between adjacent records
df_dept_item_sorted['Date_Diff'] = (df_dept_item_sorted['Purchase Requisition Date'] - df_dept_item_sorted['Prev PR Date']).dt.days


# In[47]:


#Set Threshold 
n = 5
df_dept_item_sorted['Flag Out of Range'] = (1 - (df_dept_item_sorted['Date_Diff'] <= n)).astype(int)


# In[48]:


df_dept_item_sorted['Grouping'] = df_dept_item_sorted['Flag Out of Range'].cumsum()


# In[49]:


df_dept_item_sorted.head()


# In[50]:


df_pr_count = df_dept_item_sorted[['Grouping',item_field,'Purchase Requisition Number']].groupby(['Grouping',item_field]).nunique().reset_index()


# In[51]:


df_pr_count.columns = ['Grouping', item_field, 'Count PR']


# In[52]:


# Identifies the groups that are valid split purchase cases
df_split_purchase_group = df_pr_count[df_pr_count['Count PR']>=2]


# In[53]:


# Joining of Split Purchase Groups to initial details
df_split_purchase_details = df_split_purchase_group.merge(df_dept_item_sorted,
                                                          how='inner',
                                                          on= ['Grouping',item_field])


# In[54]:


df_split_purchase_details.head()


# In[55]:


df_split_purchase_details['Date_Diff'] = np.where(df_split_purchase_details['Flag Out of Range'] == 1,
                                                  pd.NaT,
                                                  df_split_purchase_details['Date_Diff'])


# In[56]:


df_split_purchase_details.sort_values(['Grouping','Purchase Requisition Number'], inplace=True)


# In[57]:


df_split_purchase_desc = df_split_purchase_details.groupby(['Grouping',item_field]).agg({'Purchase Requisition Number': '|'.join}).reset_index()


# In[58]:


df_split_purchase_desc.columns = ['Grouping', item_field, 'PR with similar items']


# In[59]:


df_split_purchase_comb = df_split_purchase_details.merge(df_split_purchase_desc,
                                                         how='inner',
                                                         on=['Grouping',item_field])


# In[60]:


df_split_purchase_comb


# ### Derive futher prioritization based on rules
# 
# - Was the threshold avoided due to the split ?
# - Are the splits belonging to the same vendor ?
# - Are the dates diff within one day ?

# In[61]:


df_priority_score = df_split_purchase_comb.groupby(['Grouping']).agg({
    'Total Value':['min','sum'],
    'Date_Diff':'min',
    'Vendor':['nunique','count']
}).reset_index()


# In[62]:


df_priority_score.columns = ['Grouping', 'Min_Value', 'Max_Value', 'Min_Date_Diff', 'Unique_Vendor', 'Count_Vendor']


# In[63]:


value_threshold = 5_000
df_priority_score['Flag_Threshold_Crossed'] = ((df_priority_score['Min_Value'] < value_threshold) & (df_priority_score['Max_Value'] >= value_threshold)).astype(int)


# In[64]:


df_priority_score['Flag_Same_Vendor'] = ((df_priority_score['Unique_Vendor'] == df_priority_score['Count_Vendor'])).astype(int)


# In[65]:


days_threshold = 1
df_priority_score['Flag_Min_Days'] = (df_priority_score['Min_Date_Diff'] <= days_threshold).astype(int)


# In[66]:


df_priority_score['Score'] = df_priority_score['Flag_Threshold_Crossed'] + df_priority_score['Flag_Same_Vendor'] + df_priority_score['Flag_Min_Days']


# In[67]:


df_priority_score


# In[68]:


df_sop_itemcat = df_split_purchase_comb.merge(df_priority_score,
                                           how='left',
                                           on='Grouping')


# In[69]:


df_sop_itemcat.insert(0,'Item Type',f"2_{item_field}")


# In[70]:


df_sop_itemcat.head()


# ## Combine Details

# In[71]:


df_sop_comb = pd.concat([df_sop_item, df_sop_itemcat])


# In[72]:


df_sop_comb


# In[73]:


# With the different methods, there will be Groupings with the exact same PR combination and items flagged, we can remove those
df_sop_comb.sort_values(['Grouping','Item'], inplace=True)


# In[74]:


df_sop_grouping_check = df_sop_comb.groupby(['Grouping','Item Type','PR with similar items','Score']).agg({'Item': '|'.join}).reset_index()


# In[75]:


df_sop_grouping_check.columns = ['Grouping', 'Item Type', 'PR with similar items', 'Score', 'Items in Group']


# In[76]:


df_sop_grouping_check.sort_values(['PR with similar items','Items in Group','Item Type','Score'],
                                  ascending = [True, True, True, False],
                                  inplace=True)


# In[77]:


#Identify Groups with the same PRs and Items
df_sop_grouping_check[df_sop_grouping_check.duplicated(subset=['PR with similar items','Items in Group'],
                                                       keep=False)]


# In[78]:


df_sop_grouping_unique = df_sop_grouping_check.drop_duplicates(subset=['PR with similar items','Items in Group'],
                                                       keep='first')
valid_groupings = set(df_sop_grouping_unique['Grouping'].tolist())


# In[79]:


df_sop_comb_final = df_sop_comb[df_sop_comb['Grouping'].isin(valid_groupings)]


# In[80]:


df_sop_comb_final


# In[ ]:




