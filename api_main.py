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


@app.route("/ques", methods=['POST', 'PUT'])
def ques():

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

            message = ("Data for App Id {} uploaded successfully." .format(app_id))
            ques = ({"app_id":"appID","model_id":{"Model id1":[{"Q1":"What will be the flat rate discount?","Type":"float","Range":"0-100","A1":"answer"},\
            {"Q2":"Which items (if any) will have modified discounts?","Type":"JSON (python dictionary)","Key":"string (ID) - product picker","Table Format":"polaris comp table to add new line","Value":"Type:float,Range:0-100","A2":"answer"},\
            {"Q3":"Which items will be exluded from any bundle?","Type":"stack, dynamic list","Key":"string (ID) - product picker","Table Format":"polaris comp table to add new line","A3":"answer"}]}})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message,"Questions" : ques})


@app.route("/revTable", methods=['POST', 'PUT'])
def revTable():

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

            message = ("Data for App Id {} uploaded successfully." .format(app_id))
            tabledata = ({"app_id":app_id,"period":{"Week 1":{"Order Count":"150","Total Bundles Recommended":"1500","Total Bundles Purchased":"250","Original Revenue":"$####","Total Bundled Revenue":"$#####","% Revenue Increase":"##%"},"Week 2":{"Order Count":"300","Total Bundles Recommended":"2000", \
            "Total Bundles Purchased":"500","Original Revenue":"$####","Total Bundled Revenue":"$#####","% Revenue Increase":"##%"},"Week 3":{"Order Count":"250","Total Bundles Recommended":"1700","Total Bundles Purchased":"500","Original Revenue":"$####","Total Bundled Revenue":"$#####","% Revenue Increase":"##%"}, \
            "Week 4":{"Order Count":"300","Total Bundles Recommended":"2500","Total Bundles Purchased":"750","Original Revenue":"$####","Total Bundled Revenue":"$#####","% Revenue Increase":"##%"}}})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message, "Table Data" : tabledata})


@app.route("/revChart", methods=['POST', 'PUT'])
def revChart():

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

            message = ("Data for App Id {} uploaded successfully." .format(app_id))
            chartdata = ({"app_id":"appID","actual":{"Week 1":  {"Original Revenue" : "$####", "Total Bundled Revenue" : "$#####"}, \
            "Week 2":  {"Original Revenue" : "$####", "Total Bundled Revenue" : "$#####"}, \
            "Week 3":  {"Original Revenue" : "$####", "Total Bundled Revenue" : "$#####"}, \
            "Week 4":  {"Original Revenue" : "$####", "Total Bundled Revenue" : "$#####"}, \
            },"forecast":{"Week 5":  {"Forecast Revenue" : "$####", "Forecast Bundled Revenue" : "$#####"}, \
            "Week 6":  {"Forecast Revenue" : "$####", "Forecast Bundled Revenue" : "$#####"}, \
            "Week 7":  {"Forecast Revenue" : "$####", "Forecast Bundled Revenue" : "$#####"}, \
            "Week 8":  {"Forecast Revenue" : "$####", "Forecast Bundled Revenue" : "$#####"},}})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message, "Chart Data" : chartdata})



@app.route("/confirmPurchase", methods=['POST', 'PUT'])
def confirmPurchase():

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

            message = ("Data for App Id {} uploaded successfully." .format(app_id))

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message})


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
            value = ('%s parameter cannot be blank.'.format(parameterName))

    else:
        value = ('%s parameter not passed.'.format(parameterName))

    return flag,value
