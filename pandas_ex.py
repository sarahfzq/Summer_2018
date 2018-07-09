# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 17:07:35 2018

@author: Sarah
"""
import os
import numpy as np
import pandas as pd
pd.__version__

abc={}
lst=['a','b','c','d','a']
for keys in lst:
    abc[keys]=abc.get(keys,0)
print(abc)

#######################Creating dataframes###############################
####DataFrame(content, index, column) separated by ','.  Can use [ ] or { } to say multiple lines
############lists#########################
### the first list is the content, the second list is the index
df1=pd.DataFrame([1,2,3],[4,5,6],columns=['c1'])
print(df1)

############nested lists#########################
###the inner lists are all content, index is the row, columns are the columns
df2=pd.DataFrame([[1,2,3],[4,5,6]],columns=['c1','c2','c3'], index=['r1','r2'])
print(df2)

## if you use do loops to write into an empty dataframe, you have to use nexted lists, otherwise, the data being written
## into is vertical

############dictionary#########################
### key of the dictionary is the column names
df31=pd.DataFrame({'c1':[1,4],'c2':[2,5],'c3':[3,6]}, index=['r1','r2'])
print(df31)

### Nested disctionary to create row names#######################
df32=pd.DataFrame({'c1':{'r1':1, 'r2':4},'c2':{'r1':2, 'r2':5},'c3':{'r1':3,'r2':6}})
print(df32)
###with an available dictionary##################################
dic={'c1':[1,4],'c2':[2,5],'c3':[3,6]}
df4=pd.DataFrame(dic,index=['r1','r2'])
print(df4)
type(df4)
#####numpy and pandas together##################################
row_name=pd.date_range('20180501',periods=6)
column_name=list('abcde')
df5=pd.DataFrame(np.random.randn(6,5),index=row_name, columns=column_name)
print(df5)

##########another example using append######################
column_name1=list('abcde')
row_name1=pd.date_range('20180501',periods=5)
df7=pd.DataFrame()
for i in range(5):
    a=pd.DataFrame([np.linspace(i,i*5,5)], index=[row_name1[i]],columns=column_name1)
    df7=df7.append(a)
print(df7)

#####combining two series to create dataframes################
a=pd.Series(range(7))
b=pd.Series(np.linspace(1,30,7))
df6=pd.concat([a,b], axis=1)
df6.columns=['c1','c2']
print(df6)


##### difference between lists and arrays#######################3
#####numpy's array allows mathematical operations to be applied to all elements in one go
a=[1,2,3]
b=a*3
print(b)

c=np.array(a)
d=c*3
print(d)

e=[]
for i in range(3):
    e.append(a[i]*3)
print(e)
### when e is empty, cannot assign e[i]=; have to use append

################Query###########################
###### Display including index##################
df7.iloc[:,[0]]
######one specific element######################
df7.iat[0,0]
df7.loc['2018-05-01']
df7.drop('a', axis=1)
df7.drop('2018-05-01', axis=0)

df = pd.DataFrame(np.arange(10).reshape(-1, 5), columns=['a','b','c','d','e'])
m = df % 3 == 0
df.where(m, df*2)

#### -1 in reshape function allows numpy to figure out given the number of columnes, how many rows to be needed to reshape

#####Practicing SQL using Pandas#################################
#####Selecting using two conditions ### Need to use parenthesis to avoid ambiguity

df8=df7[(df7['b']>5)&(df7['c']>8)]
print(df8)

#####Swaping two lines#######################apply --case when#####
df8=df7.copy()
df8['a']=df8['a'].apply(lambda x: 100 if x<2 else 50)
print(df8)

#####lambda only takes expressions and can't take assigment#########

#####Selecting duplicate items##################groupby().function-/filter or isin-group by xx having xx
df8['a'].unique()

df8['a'].unique()[df8['a'].value_counts()>2]
#####Imputing missing Fico values###################
os.getcwd()
employee=pd.read_csv('Desktop/Python/python_data_ex.csv')
employee

#####select employees that earn more than their managers#############

df10=pd.merge(employee, employee[['id','salary']],how='left',left_on='managerid',right_on='id', indicator=True)
df11=df10[df10['salary_x']>df10['salary_y']][['name']]
print(df11)

df12=df10.loc[df10['salary_x']>df10['salary_y'], ['name']]
print(df12)
####slicing syntax#########
##df[condition][['column','column1']]##### or
##df.loc[condition,['column','column1']]

###################Using .isin function####################################
customer=pd.read_csv('Desktop/Python/customerid.csv')
customer
transaction=pd.read_csv('Desktop/Python/transaction.csv')
transaction

customer[customer['id'].isin(transaction['customerid'])==False][['name']]

######################checking numbers in a vertical manner#####################
#### can use lag or created reshaped dataframe so that functions could apply####

###############result of Groupby is the index plus one column###### 

class_=pd.read_csv('Desktop/Python/class.csv')
class_

chck=class_.groupby('class').count()>2
chck1=chck[chck['student']==True]
group_class=pd.DataFrame(class_['class'].unique())
abc=group_class[group_class[0].isin(chck1.index)][[0]]
abc.rename(columns={0:'class'})

###0 in python system does not need quotation mark here######

#####Second highest salary###
employee.sort_values('salary')[['name']].loc[[1]]

### loc[] generates series, but loc[[]] generates dataframe that operate as dataframes in pandas
###python can use index to easiy select second highest salary
####calculating cancellation rate###################
## Methold 1
cancelation=pd.read_csv('Desktop/Python/cancelation.csv')
cancelation['status_1']=cancelation['status'].apply(lambda x: 1 if x=='canceled' else 0)
((cancelation.groupby('date').sum()/cancelation.groupby('date').count()).drop(['status'], axis=1)).rename(columns={'status_1':'cancelation_rate'})
## Method 2
((cancelation[cancelation['status']=='canceled'].groupby('date').count()/cancelation.groupby('date').count())).rename(columns={'status':'cancelation_rate'})

####swaping seats####
customer=customer.append(pd.DataFrame({'id':[5],"name":['Sarah']}, index=[4]))
customer
list(customer)
### dictionary within dataframes:  series after common even if this is only one item; index is a series as well
### method 1 creating through dataframes
customer_new=pd.DataFrame()
for i in range(len(customer)):
    if (i+1==len(customer)) & (i%2==0):
        aa=pd.DataFrame(customer.loc[[i]][['name']])
        customer_new=customer_new.append(aa)
    elif i%2==0:
        aa=pd.DataFrame(customer.loc[[i+1]][['name']])
        customer_new=customer_new.append(aa)
    else:
        aa=pd.DataFrame(customer.loc[[i-1]][['name']])
        customer_new=customer_new.append(aa)
customer_new=customer_new.reset_index(drop=True)
customer_new_1=pd.concat((pd.DataFrame({'id':list(range(1,6))},index=list(range(5))),customer_new), axis=1)    
print(customer_new_1)

### consecutive three times show-up############
j=0
count1=1
abd=pd.DataFrame()
ab=class_[['class']].loc[[j]].reset_index(drop=True)
for i in range(len(class_)-1):
   j=j+1
   if ((class_[['class']].loc[[j]].reset_index(drop=True)==ab)).bool():
       count1=count1+1
       ##print('count='+str(count1))
       if count1>=3:
          bd=class_[['class']].loc[[j-1]].reset_index(drop=True)
          abd=abd.append(bd)
   else:
      
       count1=1
       ##print('count1='+str(count1))
       ab=class_[['class']].loc[[j]].reset_index(drop=True)
print(abd.drop_duplicates().reset_index(drop=True))       
       
######Test if groupby() will give you other values along with agg function######
employee_dpt=pd.concat([employee,pd.DataFrame({'dept':['1','1','2','2']})],axis=1)
employee_max=employee_dpt[['dept','salary']].groupby('dept').max()
pd.merge(employee_dpt,employee_max,how='right',left_on='salary', right_on='salary')


### top n salary by dept####################
employee_dpt[['salary']].where(employee_dpt[['salary','dept']].groupby('dept').rank(ascending=False)<2).dropna()

####fill na in pandas#####################

fico=pd.read_csv('Desktop/Python/fico.csv')
####use backfill and forwardfill to populate the fico score
fico
fico_t=fico.copy()
forward_1=fico_t.groupby('id').fillna(method='ffill')
forward=pd.concat((forward_1,fico[['id']]), axis=1)
backward_1=fico_t.groupby('id').fillna(method='bfill')
backward=pd.concat((backward_1,fico[['id']]), axis=1)
fico_t.groupby('id').first() 
fico_t.groupby('id').last()

## for forwardfill, find the second closest non-na number down the list

for i in range(len(forward)):
    if pd.isnull(forward.loc[i,'fico'])==True:
        count=0
        for j in range(i+1,len(forward)):
            if  pd.isnull(forward.loc[j,'fico'])==True:
                continue
            elif (pd.isnull(forward.loc[j,'fico'])==False) & (forward.loc[j,'id']==forward.loc[i,'id']): 
                count=count+1
                if count==2:
                    forward.loc[i,'fico']=forward.loc[j,'fico']
                    break
    
print(forward)
## for backwardfill, find the second closest non-na number up on the list
for i in range(len(backward)-1,-1,-1):
    if pd.isnull(backward.loc[i,'fico'])==True:
        count=0
        for j in range(i-1,-1,-1):
            if  pd.isnull(backward.loc[j,'fico'])==True:
                continue
            elif (pd.isnull(backward.loc[j,'fico'])==False) & (backward.loc[j,'id']==backward.loc[i,'id']): 
                count=count+1
                if count==2:
                    backward.loc[i,'fico']=backward.loc[j,'fico']
                    break
    
print(backward)
### average the above result and combine the final dataset
fico_f=0.5*forward[['fico']]+0.5*backward[['fico']]
fico_vf=pd.concat([fico[['id','period']], fico_f],join='outer', axis=1)


#########Using median by ID to fill NA#########################
fico
fico['fico']=fico.groupby('id').transform(lambda x:x.fillna(x.median()))
fico.groupby('id').sum().rename(columns={'fico':'fico_mean'})
fico.groupby('id').agg(np.mean)

####Test out index change####################################
employee
employee_new=employee[employee['name'].str.contains('|'.join(['Henry','Sam']))].copy()
X = pd.DataFrame(employee_new.values.reshape(-1,4))
#####When changed to array using value.reshape, the index is lost#################3



