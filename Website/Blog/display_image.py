import mysql.connector
from flask import Flask, render_template, url_for, flash, redirect
from base64 import b64encode

app = Flask(__name__)
global image

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

@app.route("/")
def home():
    cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/codefundo/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
    mycursor = cnx.cursor()
    sql =  "select voter_name from voter where voter_name = 'puru'"
    mycursor.execute(sql)
    val = mycursor.fetchall()
    if(val):
        for row in val:
            x = row[0]
    return render_template('home_1.html', image = x)

if __name__ == '__main__':
    app.run(debug=True)
    #<img src="data:;base64,{{ image }}"/>