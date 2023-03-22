from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, request
import pymongo
import os
from error import *
from bson import json_util, ObjectId
import json

load_dotenv()

app = Flask(__name__)
mongodb = os.getenv('MONGODB')
client = pymongo.MongoClient(mongodb)
db = client['ESDProject']
companyCollection = db['companies']

# insert new company
@app.route('/create', methods=['POST'])
def insert():
    data = request.json
    errMsg = handleError(data)
    if errMsg == '':
        companyCollection.insert_one(data)
        return "Created company"
    return errMsg

# read company
@app.route('/<company_id>', methods=['GET'])
def read(company_id):
    company = companyCollection.find_one({"_id": ObjectId(company_id)})
    company = json.loads(json_util.dumps(company))
    return company

# edit company
@app.route('/edit/<company_id>', methods=['PUT'])
def edit(company_id):
    data = request.json
    errMsg = handleError(data)
    if errMsg == '':
        originalQuery = companyCollection.find_one({"_id": ObjectId(company_id)})
        newValues = { "$set": data }
        companyCollection.update_one(originalQuery, newValues)
        return "Company updated"
    return errMsg

# delete company
@app.route('/delete/<company_id>', methods=['DELETE'])
def delete(company_id):
    data = request.json
    errMsg = handleError(data)
    if errMsg == '':
        companyCollection.delete_one({"_id": ObjectId(company_id)})
        return "Company deleted"
    return errMsg

if __name__ == '__main__':
    app.run(debug=True)