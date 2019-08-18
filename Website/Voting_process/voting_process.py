from flask import Flask, render_template, url_for, flash, redirect,request
from adal import AuthenticationContext
from forms import LoginForm, VoterForm
import mysql.connector
import requests
import json
AUTHORITY = 'https://login.microsoftonline.com/8fb1f5b2-a2b4-409c-bcd6-21a3f3aad0d6'
WORKBENCH_API_URL = 'https://blockchain-voiqlc-api.azurewebsites.net/'
RESOURCE = '27c00335-188f-4c3f-a47c-4c825bf4f12c'
CLIENT_APP_Id = '2a525ae3-8712-4273-9ee9-9318d92028b6' # service ID
CLIENT_SECRET = 'tZ:FVbBdsHoasBoPay4*[C+Avw7eRy11'# KEY
Voter_ID_hash=''
auth_context = AuthenticationContext(AUTHORITY)
contracts={}
Username = ''
SESSION = ''
cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/CodeFundo_2019/Website/Blog/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
mycursor = cnx.cursor()
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
            return redirect(url_for('process'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/contact_admin", methods=['GET', 'POST'])
def contact_admin():
    global Username
    return render_template('Contact_admin.html', title="Voting")

@app.route("/process", methods=['GET', 'POST'])
def process():
    global Username
    global Voter_ID_hash
    mycursor.execute('select cit_voterid from login where loff_email=\'{}\''.format(Username))
    temp = mycursor.fetchall()
    if(not temp):
        return render_template('process.html', title="Voting")
    val = temp[0][0]
    Voter_ID_hash = val
    mycursor.execute('select voter_name from voter where voter_id=\'{}\''.format(val))
    val5 = mycursor.fetchall()[0][0]
    mycursor.execute('select voter_const_id from voter where voter_id=\'{}\''.format(val))
    val2 = mycursor.fetchall()[0][0]
    mycursor.execute('select Const_Name from constituency where const_id={}'.format(int(val2)))
    val4 = mycursor.fetchall()[0][0]
    return render_template('Voter_info2.html', vid=val5, const=val4)

@app.route("/Voter_info", methods=['GET', 'POST'])
def Voter_info():
    global Username
    global Voter_ID_hash
    poll_data = {}
    mycursor.execute('select cit_voterid from login where loff_email=\'{}\''.format(Username))
    temp = mycursor.fetchall()
    if(not temp):
        return render_template('process.html', title="Voting")
    val = temp[0][0]
    mycursor.execute('select voter_const_id from voter where voter_id=\'{}\''.format(val))
    val2 = mycursor.fetchall()[0][0]
    mycursor.execute('select candidate_name from candidates where candi_const_id=\'{}\''.format(val2))
    val3 = mycursor.fetchall()
    if(val3):    
        for c in val3:
            mycursor.execute('select candi_party from candidates where candidate_name=\'{}\''.format(c[0]))
            val6 = mycursor.fetchall()[0][0]
            val6 = val6 + '.png'
            poll_data.__setitem__(c[0], val6)
        return render_template('Voter_info.html',data = poll_data)

@app.route('/poll')
def poll():
    global Username
    global Voter_ID_hash
    vote = request.args.get('field')
    mycursor.execute('select unique_id from candidates where candidate_name=\'{}\''.format(vote))
    num = mycursor.fetchall()[0][0]
    data ={
                "workflowFunctionId":21,
                "workflowActionParameters":[
                    {
                        "name":"Candidate_ID",
                        "value":num
                    }
                ]
            }
    SESSION.post(WORKBENCH_API_URL+ 'api/v2/contracts/{}/actions'.format(contracts[Voter_ID_hash]), json= (data))
    flash("you voted for {}".format(vote), 'success')
    mycursor.execute('delete from login where loff_email=\'{}\''.format(Username))
    cnx.commit()
    return render_template('finish.html', title="Voting")


if __name__ == '__main__':
    SESSION = requests.Session()
    token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})
    x = SESSION.get(WORKBENCH_API_URL+ 'api/v2/contracts?workflowId=6').json()
    for i in x['contracts']:
        for value in i["contractProperties"]:
            if value["workflowPropertyId"] == 17:
                #print(value["parameters"][0]["value"])
                contracts.__setitem__(value["value"], i['id'])
    app.run(debug=True)