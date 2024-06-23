from flask import Flask, render_template, flash, request, jsonify
import time
from mongo_queries import *
# from redis_queries import *
#from utils import *
import json

import pickle
# Importing the function which takes parameters as input (comment, title, ...) and predicts a score between 0 and 5.
import pred_new_sentence




app = Flask(__name__, template_folder="templates", static_folder="stylesheets")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


website_info = json.load(open('./website_info.json','rb'))

@app.route('/status', methods=["GET"])
def status():
    return jsonify(1)

@app.route('/get_website_info/<site_name>', methods=['GET'])
def get_website_info(site_name):
    if site_name in website_info:
        return website_info[site_name]
    else:
        return jsonify({"error": "Site not found"}), 404
        
        
@app.route('/predict', methods=['POST'])
def predict(): 
    # Retrieving request data in JSON
    data = request.get_json()
    # Retrieving and checking the existence of the site name in the list with the `get_website_info` function.
    site_name = data.get('site_name')  
    if site_name not in website_info:
        return jsonify({"error": "Site not found. Prediction cannot be made."}), 404

    # Extraction of other data necessary for prediction
    main_category = data.get('main_category', '')  # optional
    sub_category = data.get('sub_category', '')    # optional
    sub_sub_category = data.get('sub_sub_category', '')  # optional
    # site_name = data.get('site_name', None)          # optional
    title = data.get('title', '')                  # optional
    comment = data.get('comment', None)            # Texte obligatoire
    location = data.get('location', '')            # optional
    
    if not comment:
        return jsonify({"error": "The 'comment' field is required."}), 400

    # Using the pred_new_sentence function to predict a score between 0 and 5
    try:
        prediction = pred_new_sentence.predict(main_category, sub_category, sub_sub_category, title, comment, location)
        score = prediction.get('score') 
        return jsonify({"score": int(score)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
###############################################################################





# show databases
@app.route('/')
def home1():
    mongo_dbs = mongo_client.list_databases()
    return jsonify(mongo_dbs)
    #return render_template("index.html", mongo_dbs=mongo_dbs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
