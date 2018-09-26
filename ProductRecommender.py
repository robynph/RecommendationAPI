# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:32:43 2018

@author: Monika Asawa
"""

import pandas as pd
import numpy as np

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from sklearn.externals import joblib

import os


TOP_HOW_MANY = 3

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

def getOrderData(app_ID, ordersDF):
    'Step 1: Generate folder for the received app ID if it doesnot exist'
    'Step 2: Generate Rules'
    'Step 3: Store the rules in pickle format in the folder created in step 1'
    
    'Step 1'
    if not (os.path.isdir(app_ID)):
        os.mkdir(app_ID)
    
    'Step 2'
    rules = generateRules(ordersDF)    
    'Step 3'
    joblib.dump(rules, app_ID + "/apriori_product_recommender_NEW.pkl")
    print("Rules shape :: ",np.shape(rules))

def generateRules(orders):
    
    print("Shape of orders data : ", np.shape(orders))
    
    'Removing the records which doesnt have OrderID'
    orders.dropna(axis=0, subset=['Order ID'], inplace=True)
    
    basket = pd.crosstab(orders['Order ID'],orders['SKU'])
    
    basket_sb = basket.applymap(encode_units)
    
    print("Shape of basket_sb data : ", np.shape(basket_sb))
    
    #----------------------------------------------------------------------
    
    'Generating frequent item sets that have a support of at least 0.1%'

    frequent_itemsets = apriori(basket_sb, min_support=0.00001, use_colnames=True)

    'Determining length of each itemset'
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    
    print("Shape of frequent_itemsets data : ", np.shape(frequent_itemsets))
    
    #----------------------------------------------------------------------

    'Generating the rules with their corresponding support, confidence and lift'
    
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    print("Shape of rules data : ", np.shape(rules))
    print("Printing top 5 rules generated", rules.head())
    
    'Creating new column to store value of consequents from frozen set format'
    rules['conse'] = [list(x) for x in rules.consequents]
    
    
    #----------------------------------------------------------------------
    'Lift should be minimum 6 and confidence should be 80%'
    #rules = rules[ (rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
    rules = rules[ (rules['lift'] >= 1) & (rules['confidence'] >= 0.1)]
    'Converting lift(float) to lift(int)'
    rules['lift'] = rules['lift'].apply(lambda x: int(x))
    
    print("Shape of rules data : ", np.shape(rules))
    print("Printing top 5 rules generated", rules.head())
    
    return rules


#==============================================================================
# Alternate Approach
# import pickle
# 
# with open("apriori_product_recommender_pickle.pkl", "wb") as file_handler:
#     pickle.dump(rules, file_handler)
#     
# with open("apriori_product_recommender_pickle.pkl", "rb") as file_handler:
#     loaded_pickle = pickle.load(file_handler)
#     
# loaded_pickle
#==============================================================================


#from sklearn.externals import joblib
#
#joblib.dump(rules, "apriori_product_recommender.pkl")


def recommend(app_id, listselprod):
    
    #rules = joblib.load("apriori_product_recommender.pkl")
    rules = joblib.load(app_id + "/apriori_product_recommender_NEW.pkl") 
                       
    suggestedProducts = recommendProducts(rules, listselprod)
    
    #Dummy value
    discountPerc = 15
    
    print("Selected Products ::", listselprod)
    return suggestedProducts,discountPerc

def recommendProducts(rules, listselprod):
    
    orderedProducts = frozenset((listselprod))
    
    'extracting rules which has selected products as antecedents'
    prodRules = rules[ rules['antecedents'] == orderedProducts ]
    
    print("Shape of prodRules data : ", np.shape(prodRules))
    print("Printing top 5 prodRules generated", prodRules.head())
    
    'sorting out product rules by lift, confidence and support'
    result = prodRules.sort_values(by=['lift', 'confidence','support'],axis=0, ascending=[0, 0, 0])
    
    print("Shape of result data : ", np.shape(result))
    print("Printing top 5 result generated", result.head())
    
    'Determing best 3 rules for the selected products'
    top_3_result = result[:TOP_HOW_MANY]
    
    conse = []
    
    for i in top_3_result['conse']:
    
        print("Conse :: ",i)
        
        for j in i:
            print("Conse item :: ",j)
            conse.append(j)
            
            if(len(conse)>=3):
                break
        
        if(len(conse)>=3):
            break
    
    print(conse)   
    return conse

def revenuelift(df_primary, df_recommended, discount):
    temp1 = pd.to_numeric(df_primary["Price"])
    temp2 = pd.to_numeric(df_recommended["Price"])
    discount = pd.to_numeric(discount)
    
    rev = temp1.sum()
    extra_rev = temp2.sum()
    print("Main revenue is :: ", rev)
    print("extra revenue is :: ", extra_rev)
    print("Discount offered is :: ", discount)
    
    rev_lift = round(rev + extra_rev - discount,2)
    
    print("revenue lift is ::", rev_lift)
    
    return rev_lift

