from flask import Flask, render_template, url_for, flash, redirect, session, escape
from adal import AuthenticationContext
from forms import LoginForm, VoterForm
from time import sleep
import mysql.connector
import requests
import json

app = Flask(__name__)
app.secret_key =  '5791628bb0b13ce0c676dfde280ba245'

AUTHORITY = 'https://login.microsoftonline.com/8fb1f5b2-a2b4-409c-bcd6-21a3f3aad0d6'
WORKBENCH_API_URL = 'https://blockchain-voiqlc-api.azurewebsites.net/'
RESOURCE = '27c00335-188f-4c3f-a47c-4c825bf4f12c'
CLIENT_APP_Id = '2a525ae3-8712-4273-9ee9-9318d92028b6' # service ID
CLIENT_SECRET = 'tZ:FVbBdsHoasBoPay4*[C+Avw7eRy11'# KEY

auth_context = AuthenticationContext(AUTHORITY)

SESSION = requests.Session()
token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})
contracts = {}

x = SESSION.get(WORKBENCH_API_URL+ 'api/v2/contracts?workflowId=5').json()
for i in x['contracts']:
    for value in i["contractActions"]:
        if value["workflowFunctionId"] == 15:
            contracts.__setitem__(value["parameters"][0]["value"], i['id'])

cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
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

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()   
    if form.validate_on_submit():
        if(form.Username.data == 'admin@admin.com' and form.password.data == form.Username.data):
            return redirect(url_for('result'))
        if form.password.data == form.Username.data and form.Username.data in official_values:
            return redirect(url_for('vote'))
        else:
            flash('Login Unsuccessful. Please check Username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/vote",  methods=['GET', 'POST'])
def vote():
    dict1={}
    #user= session['Username']
    form = VoterForm()
    if form.validate_on_submit():
        if (form.Voter_ID_Confirm.data == form.Voter_ID.data and form.Voter_ID.data in valid_voters):
            Voter_ID = form.Voter_ID.data
            x = SESSION.get(WORKBENCH_API_URL+ 'api/v2/contracts?workflowId=6')
            if x.status_code == 200:
                x=x.json()
                for i in x['contracts']:
                        dict1.__setitem__(i['contractProperties'][1]['value'], dict())
                        dict1[str(i['contractProperties'][1]['value'])].__setitem__('state',i['contractProperties'][0]['value'])
                        dict1[str(i['contractProperties'][1]['value'])].__setitem__('const',i['contractProperties'][2]['value'])
                if form.Voter_ID.data in dict1.keys():
                    flash('Login Unsuccessful. Please check Voter_ID', 'danger')
                    return redirect(url_for('vote'))
            
           
            data ={
                "workflowFunctionId":19,
                "workflowActionParameters":[
                    {
                        "name":"Voter_ID",
                        "value":Voter_ID
                    }
                ]
            }
            mycursor.execute('select voter_const_id from voter where voter_id=\'{}\''.format(form.Voter_ID.data))
            val2 = mycursor.fetchall()[0][0]
            #SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/{}/actions'.format(contracts[val2]), json= (data))
            
            sql = "INSERT INTO login (loff_email, cit_voterid) VALUES (%s, %s)"
            val = ('adam@login.com' , Voter_ID)
            mycursor.execute(sql, val)
            cnx.commit()
            flash('Voter Registered!', 'success')
            flash('Voter can Vote Now!', 'success')
            return redirect(url_for('vote'))
        else:
            flash('Login Unsuccessful. Please check Voter_ID', 'danger')
            
    return render_template('vote_submit.html', title='Login', form=form)

@app.route("/result",  methods=['GET', 'POST'])
def result():
    result_data = {}
    data ={
                "workflowFunctionId":18,
                "workflowActionParameters":[]
            }
    for i in contracts.values():
        SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/{}/actions'.format(i), json= (data))
    sleep(10)
    x = SESSION.get(WORKBENCH_API_URL+ 'api/v2/contracts?workflowId=5').json()
    for i in x['contracts']:
        mycursor.execute('select const_name from constituency where const_id='+str(i['contractProperties'][1]['value']))
        const_name = mycursor.fetchall()[0][0]
        mycursor.execute('select candidate_name from candidates where unique_id='+str(i['contractProperties'][2]['value']))
        candi_name = mycursor.fetchall()[0][0]
        mycursor.execute('select candi_party from candidates where unique_id='+str(i['contractProperties'][2]['value']))
        candi_party = mycursor.fetchall()[0][0]
        result_data[candi_name] = [const_name, candi_party]
    return render_template('result.html', data=result_data)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
