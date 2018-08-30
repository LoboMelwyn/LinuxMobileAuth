import sqlite3, sys
sys.path.append('/home/melwyn/.local/lib/python3.6/site-packages')
from flask import Flask, request, jsonify
from sqlite3 import Error
app = Flask(__name__)

# root
@app.route("/")
def index():
    """
    this is a root dir of my server
    :return: str
    """
    return "Website to authenticate via android app"

# POST
@app.route('/api/authenticate', methods=['POST'])
def get_text_prediction():
    """
    predicts requested text whether it is ham or spam
    :return: json
    """
    json = request.get_json()
    if json["text"] == 'Melwyn':
        conn = sqlite3.connect("/home/melwyn/Documents/PythonWebAPI/auth.db")
        cur = conn.cursor()
        cur.execute("update authenticate set toauth = 1 where toauth = 0")
        conn.commit()
        conn.close()
        return jsonify({'Message': 'AuthOK'})
    return jsonify({'Message': 'AuthFailure'})

# running web app in local machine
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=80)