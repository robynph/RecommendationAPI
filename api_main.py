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
            modelID = req.data['model_id']
            flag,value = validator(req, "app_id")
            if(flag):
                app_id = value
                print("Validated ",app_id)
            else:
                return jsonify({"Status" : "F", "Message" : value})

            message = ("Data for App Id {} uploaded successfully." .format(app_id))
            ques = ({"app_id":"appID","model_id":{modelID:[{"Q1":"What will be the flat rate discount?","Type":"float","Range":"0-100","A1":"answer"},\
            {"Q2":"How many bundles to show on product page?","Type":"float","Range":"0-100","A2":"answer"},\
            {"Q3":"Which items will be exluded from any bundle?","Type":"stack, dynamic list","Key":"string (ID) - product picker","A3":"answer"}]}})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message,"Questions" : ques})


@app.route("/revData", methods=['POST', 'PUT'])
def revData():

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
            tabledata = ({"app_id":"appID","Data":{"actual":{"Week 1":{"% Revenue Increase":"##%","Order Count":"150","Original Revenue":"$####","Total Bundled Revenue":"$#####","Total Bundles Purchased":"250","Total Bundles Recommended":"1500","Revenue Lift":"$###"},\
            "Week 2":{"% Revenue Increase":"##%","Order Count":"300","Original Revenue":"$####","Total Bundled Revenue":"$#####","Total Bundles Purchased":"500","Total Bundles Recommended":"2000","Revenue Lift":"$###"},\
            "Week 3":{"% Revenue Increase":"##%","Order Count":"250","Original Revenue":"$####","Total Bundled Revenue":"$#####","Total Bundles Purchased":"500","Total Bundles Recommended":"1700","Revenue Lift":"$###"},\
            "Week 4":{"% Revenue Increase":"##%","Order Count":"300","Original Revenue":"$####","Total Bundled Revenue":"$#####","Total Bundles Purchased":"750","Total Bundles Recommended":"2500","Revenue Lift":"$###"}},\
            "forecast":{"Week 5":{"Forecast Bundled Revenue":"$#####","Forecast Revenue":"$####"},"Week 6":{"Forecast Bundled Revenue":"$#####","Forecast Revenue":"$####"},"Week 7":{"Forecast Bundled Revenue":"$#####","Forecast Revenue":"$####"},\
            "Week 8":{"Forecast Bundled Revenue":"$#####","Forecast Revenue":"$####"}}},"Message":"Data for App Id App Id1 uploaded successfully.","Status":"S"})

        except ValueError:
            return jsonify({"Status" : "F", "Message" : "Please provide the valid data for orders."})

        return jsonify({"Status" : "S","Message" : message, "Table Data" : tabledata})


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
