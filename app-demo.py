# coding=utf-8

from flask import Flask, jsonify
from flask import abort
import time
app = Flask(__name__)
@app.route('/istio/<string:testname>', methods=['GET'])
def hello_world(testname):
    if len(testname) == 0:
        abort(404)
    if  testname == '500':
        abort(500)
    if testname == '5s':
        time.sleep(5)
    return testname
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
