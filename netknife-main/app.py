from flask import Flask,render_template
import json
netknife=Flask(__name__)

@netknife.route('/')
def index():
    return render_template('index.html')

@netknife.route('/get')
def get_test():
    return json.dumps({'a':100})

if __name__ == '__main__':
    netknife.run('0.0.0.0',port=3000,debug=True)