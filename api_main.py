# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 18:24:13 2018

@author: Monika Asawa
"""
from flask import Flask, request, jsonify

from ProductRecommender import recommend

app = Flask(__name__)
#from cStringIO import StringIO

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
            
            
            if(data["SelectedProducts"]):
                
                selectedProducts = data["SelectedProducts"]
                
                if(len(selectedProducts)>0):
                    print("Received value of selectedProducts :: ",selectedProducts)
                    
                else:
                    return jsonify({"Status" : "F", "Message" : "Please provide atleast one selected product name."})
                
                suggestedProducts,discountPerc = recommend(selectedProducts)
            
            else:
                return jsonify({"Status" : "F", "Message" : "SelectedProducts parameter not passed"})
            
            
        
        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S", "SuggestedProducts": suggestedProducts, "Discount" : discountPerc})
    

@app.route("/loadStoreData", methods=['POST','PUT'])
def loadStoreData():
    
    if request.method == 'POST':
        try:
             
            print("Received value of request :: ", request)  
            
            req = request.get_json()
            print("Received value of req :: ", jsonify(req))
            
            
            f = request.files['files']
            if not f:
                return "No file"
            #file_contents = StringIO(f.stream.read())
            print("Received file with file contents :: ",f)
            
            reqJSON = request.files["json"]
            print("reqJSON :: " , reqJSON)
            
            if(reqJSON["StoreID"]):
                
                storeID = req["StoreID"]
                
                if(len(storeID)>0):
                    print("Received value of StoreID :: ",storeID)
                else:
                    return jsonify({"Status" : "F", "Message" : "StoreID parameter cannot be blank."})
                
            
            else:
                return jsonify({"Status" : "F", "Message" : "StoreID parameter not passed"})

            
            
            
            #result = csv2json(file_contents)
            #response = make_response(result)
            #response.headers["Content-Disposition"] = "attachment; filename=Converted.json"
            #return response
            
        
        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S"})
    
