# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:36:42 2018

@author: Viraj
"""

from flask import Flask, request, jsonify

from ProductRecommender import recommend, getOrderData, revenuelift
import pandas as pd
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/loadStoreData", methods=['POST','PUT'])
def loadStoreData():
    
    if request.method == 'POST':
        try:
             
            print("Received value of request :: ", request)  
            
            req = request.get_json()
            print("Received value of req :: ", jsonify(req))
            
            flag,value = validator(req, "app_id")
            if(flag):
                app_id = value
                print("Validated ",app_id)
            else:
                return jsonify({"Status" : "F", "Message" : value})
            
            flag,value = validator(req, "orders")
            if(flag):
                
                orders = value
                
                print("Total orders :: ",len(orders))
                df = pd.DataFrame(columns=['Order ID', 'SKU'])
                count = 0
                for eachOrder in orders:
                    orderId = eachOrder['id']
                    lineItems = eachOrder['line_items']
                    
                    for item in lineItems:
                        #print("items ::", item['sku'])
                        df.loc[count] = [orderId, item['sku']]
                        count+=1
                        
                getOrderData(app_id, df)
                        
                print("Validated ",app_id)
            else:
                return jsonify({"Status" : "F", "Message" : value})

            
            message = ("Data for App Id {} uploaded successfully." .format(app_id))
        
        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message})
    

@app.route("/recommend", methods=['POST'])
def genRecommendation():
    if request.method == 'POST':
        try:
            req = request.get_json()
            print("Received value of req :: ",req)
            
            
            flag,value = validator(req, "app_id")
            if(flag):
                app_id = value
                print("Validated ",app_id)
            else:
                return jsonify({"Status" : "F", "Message" : value})
                       
            flag,value = validator(req, "products")
            if(flag):
                selectedProducts = value
                
                tempList = []                
                #df = pd.DataFrame(columns=['SKU'])
                count = 0
                
                for eachProduct in selectedProducts:
                    variants = eachProduct['variants']
                    
                    for item in variants:
                        print("items ::", [item['sku']])
                        #df.loc[count] = [item['sku']]
                        tempList.append(item['sku'])                              
                        count+=1
                       
                #print(df)
                print("templist ::", tempList)
                suggestedProducts,discountPerc = recommend(app_id,tempList)
                
            else:
                return jsonify({"Status" : "F", "Message" : value})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S" ,"SuggestedProducts": suggestedProducts, "Discount" : discountPerc})
       
    
@app.route("/feedback", methods=['POST'])
def feedback():
    
    try:
        req = request.get_json()
        print("Received value of req :: ",req)
        
        flag,value = validator(req, "app_id")
        if(flag):
            app_id = value
            print("Validated ",app_id)
        else:
            return jsonify({"Status" : "F", "Message" : value})
        
        flag,value = validator(req, "orders")
        if(flag):
                
            orders = value       
            print("Total orders :: ",len(orders))
            df = pd.DataFrame(columns=['Order ID', 'SKU'])
            count = 0
            for eachOrder in orders:
                orderId = eachOrder['id']
                lineItems = eachOrder['line_items']
                
                for item in lineItems:
                    #print("items ::", item['sku'])
                    df.loc[count] = [orderId, item['sku']]
                    count+=1
                    
            getOrderData(app_id, df)
                
            print("Validated ",app_id)
        else:
            return jsonify({"Status" : "F", "Message" : value})
        
        flag,value = validator(req, "products")
        if(flag):
            selectedProducts = value
            
            tempList = []                
            df_sel = pd.DataFrame(columns=['ID','SKU','Price'])
            count = 0
            
            for eachProduct in selectedProducts:
                variants = eachProduct['variants']
                
                for item in variants:
                    #print("items ::", [item['sku']])
                    #This is for feedback module
                    tempList.append(item['sku'])                              
                    
                    #This is for revenue lift calculations
                    df_sel.loc[count] = [item['id'],item['sku'],item['price']]
                    count+=1
            
            print("selected df",df_sel)                   
            print("templist ::", tempList)
            suggestedProducts,discountPerc = recommend(app_id,tempList)
            revenue_lift = revenuelift(df_sel)    
        else:
            return jsonify({"Status" : "F", "Message" : value})
                
        '''
        flag,value = validator(req, "Ids")
        if(flag):
            orderId = value
            print("Validated ",orderId)
        else:
            return jsonify({"Status" : "F", "Message" : value})
        
        
        flag,value = validator(req, "SelectedProducts")
        if(flag):
            selectedProducts = value
            
            'TO DO'
            'Write code here for reinforcement learning'
            
        else:
            return jsonify({"Status" : "F", "Message" : value})
        '''
        
    except ValueError:
        return jsonify({"Status" : "F", "Message" : "Please provide the valid data."})

    return jsonify({"Status" : "S  = Feedback module implemented","Revenue Lift": revenue_lift})


@app.route("/revlift", methods=['POST'])
def revlift():
    
    try:
        req = request.get_json()
        print("Received value of req :: ",req)
        
        flag,value = validator(req, "app_id")
        if(flag):
            app_id = value
            print("Validated ",app_id)
        else:
            return jsonify({"Status" : "F", "Message" : value})
        
        flag,value = validator(req, "products")
        if(flag):
            selectedProducts = value
                       
            df_sel = pd.DataFrame(columns=['ID','SKU','Price'])
            count = 0
            
            for eachProduct in selectedProducts:
                variants = eachProduct['variants']
                
                for item in variants:
                    #This is for revenue lift calculations
                    df_sel.loc[count] = [item['id'],item['sku'],item['price']]
                    count+=1
                       
            revenue_lift = revenuelift(df_sel)    
        else:
            return jsonify({"Status" : "F", "Message" : value})
                
      
    except ValueError:
        return jsonify({"Status" : "F", "Message" : "Please provide the valid data."})

    return jsonify({"Status" : "S  = Feedback module implemented","Revenue Lift": revenue_lift})


@app.route("/extra", methods=['POST','PUT'])
def extra():
    
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

        
        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S"})
    

def validator(req, parameterName):
    
    flag = False
    value = ""
    
    print("Validating value received for ",parameterName)
    
    if(req[parameterName]):
        
        value = req[parameterName]
                
        if(len(value)>0):
            
            print("Received value of parameter :: ",value)
            flag = True
        
        else:
            value = ('{}.format parameter cannot be blank.'.format(parameterName))
    
    else:
        value = ('{}.format parameter not passed.'.format(parameterName))
    
    return flag,value