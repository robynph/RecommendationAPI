# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 18:24:13 2018

@author: Monika Asawa
"""
from flask import Flask, request

app = Flask(__name__)
from flask import jsonify
from sklearn.externals import joblib
import numpy as np


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
    
TOP_HOW_MANY = 3


@app.route("/recommend", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received value of data :: ",data)
            
            selectedProds = data["selectedProducts"]
            if(len(selectedProds)>0):
                selectedProducts = selectedProds.split(",")
                print("Received value of selectedProducts :: ",selectedProducts)
            else:
                return jsonify("Please provide the selected product names.")
            
            rules = joblib.load("./apriori_product_recommender.pkl")
            
            suggestedProducts = recommendProducts(rules, selectedProducts)
        
        except ValueError:
            return jsonify("Please provide the selected product names.")

        return jsonify(suggestedProducts)

#==============================================================================
# def req_resp_int(selectedProducts):
#     
#     with open("apriori_product_recommender.pkl", "rb") as file_handler:
#         rules = pickle.load(file_handler)
#     
#     return recommendProducts(rules, selectedProducts)
#==============================================================================


def recommendProducts(rules, selectedProducts):
    
    orderedProducts = frozenset((selectedProducts))
    
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
    
    conse = set()
    
    for i in top_3_result['conse']:
    
        print(i)
        
        for j in i:
            print(j)
            conse.add(j)
            
            if(len(conse)>=3):
                break
        
        if(len(conse)>=3):
            break
    
    return conse