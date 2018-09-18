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

            flag,value = validator(req, "Orders")
            if(flag):

                orders = value

                for eachOrder in orders:
                        print(eachOrder["Ids"],eachOrder["line_items"])

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

            flag,value = validator(req, "Ids")
            if(flag):
                orderId = value
                print("Validated ",orderId)
            else:
                return jsonify({"Status" : "F", "Message" : value})


            flag,value = validator(req, "SelectedProducts")
            if(flag):
                selectedProducts = value
                suggestedProducts,discountPerc = recommend(selectedProducts)
            else:
                return jsonify({"Status" : "F", "Message" : value})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the selected product names."})

        return jsonify({"Status" : "S",  "Ids" : orderId ,"SuggestedProducts": suggestedProducts, "Discount" : discountPerc})


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

    except ValueError:
        return jsonify({"Status" : "F", "Message" : "Please provide the valid data."})

    return jsonify({"Status" : "S"})



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
    
    print("Validating value received for ",parameterName)

    if(req[parameterName]):

        value = req[parameterName]

        if(len(value)>0):

            print("Received value of parameter :: ",value)
            flag = True

        else:
            value = ('%s parameter cannot be blank.'.format(parameterName))

    else:
        value = ('%s parameter not passed.'.format(parameterName))

    return flag,value
