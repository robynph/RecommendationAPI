# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 18:24:13 2018

@author: Monika Asawa
"""
from flask import Flask, request, jsonify

from ProductRecommender import recommend

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
    
TOP_HOW_MANY = 3


@app.route("/recommend", methods=['POST'])
def genRecommendation():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received value of data :: ",data)
            
            selectedProducts = data["SelectedProducts"]
            if(len(selectedProducts)>0):
                print("Received value of selectedProducts :: ",selectedProducts)
            else:
                return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})
            
            suggestedProducts,discountPerc = recommend(selectedProducts)
        
        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S", "SuggestedProducts": suggestedProducts, "Discount" : discountPerc})


