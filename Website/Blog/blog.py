from flask import Flask, render_template, url_for, flash, redirect
from adal import AuthenticationContext
from forms import LoginForm, VoterForm
import mysql.connector
import requests
import json

AUTHORITY = 'https://login.microsoftonline.com/6d6fbafa-d99a-400e-b093-41d4a2553990'
WORKBENCH_API_URL = 'https://stallions-wfhynd-api.azurewebsites.net/'
RESOURCE = '60a51ac4-abac-41e3-ab5c-3090b749b45c'
CLIENT_APP_Id = '40abb33e-a30a-4985-80a6-3372aa605d17'
CLIENT_SECRET = 'O3U=U4mgk8CYBb?PkOI6oL.rucS_tJ?y'
auth_context = AuthenticationContext(AUTHORITY)

Username = ''
SESSION = ''
cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/CodeFundo_2019/Website/Blog/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
mycursor = cnx.cursor()
mycursor.execute('select voter_id from voter')

valid_voters = []
for i in mycursor.fetchall():
    valid_voters.append(i[0])

mycursor.execute('select off_email from official')
val = mycursor.fetchall()
official_values = []
if(val):    
    for c in val:
        official_values.append(c[0])

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()   
    if form.validate_on_submit():
        if form.Username.data in official_values and form.password.data == form.Username.data:
            global Username 
            Username = form.Username.data
            return redirect(url_for('vote'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/vote",  methods=['GET', 'POST'])
def vote():
    global Username
    form = VoterForm()
    if form.validate_on_submit():
        if form.Voter_ID_Confirm.data == form.Voter_ID.data and form.Voter_ID.data in valid_voters:
            data ={
                "workflowFunctionId":21,
                "workflowActionParameters":[
                    {
                        "name":"Voter_ID",
                        "value":form.Voter_ID.data
                    }
                ]
            }
            
            #SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/18/actions', json= (data))
            flash('You have been logged in!', 'success')
            #cnx = mysql.connector.connect(user="Stallions@stallions-test", password='qwerty12345.', host="stallions-test.mysql.database.azure.com", port=3306, database='sample', ssl_ca='C:\\Users\\Shashank\\Desktop\\Project\\codefundo\\BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)                    
            mycursor.execute('select * from login where loff_email=\'{}\''.format(Username))
            if(mycursor.fetchall()):
                mycursor.execute('UPDATE login SET cit_voterid=\'{}\' where loff_email=\'{}\''.format(form.Voter_ID.data, Username))
            else:
                sql = "INSERT INTO login (loff_email, cit_voterid) VALUES (%s, %s)"
                val = (Username, form.Voter_ID.data)
                #mycursor.execute('INSET INTO login values(\'{}\',\'{}\')'.format(Username,form.Voter_ID.data))
                mycursor.execute(sql, val)
                cnx.commit()
            #return redirect(url_for('home'))
            return render_template('finish.html', title="Voting")
        else:
            flash('Login Unsuccessful. Please check Voter_ID', 'danger')
    return render_template('vote_submit.html', title='Login', form=form)



if __name__ == '__main__':

    #SESSION = requests.Session()
    #token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    #print(token)
    #SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})

    app.run(debug=True)

"""     4479548291
        4923613555
        5000281067
        5161804634
        5648906531
        6278637227
        8287192781
        9178288458
        9401348876
        9765147850  """