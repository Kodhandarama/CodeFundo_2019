from flask import Flask, render_template, url_for, flash, redirect,request
from adal import AuthenticationContext
from forms import LoginForm, VoterForm
import mysql.connector
import requests
import json
"""
AUTHORITY = 'https://login.microsoftonline.com/6d6fbafa-d99a-400e-b093-41d4a2553990'
WORKBENCH_API_URL = 'https://stallions-wfhynd-api.azurewebsites.net/'
RESOURCE = '60a51ac4-abac-41e3-ab5c-3090b749b45c'
CLIENT_APP_Id = '40abb33e-a30a-4985-80a6-3372aa605d17'
CLIENT_SECRET = 'O3U=U4mgk8CYBb?PkOI6oL.rucS_tJ?y'
auth_context = AuthenticationContext(AUTHORITY)
"""
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
    mycursor.execute('select cit_voterid from login where loff_email=\'{}\''.format(Username))
    temp = mycursor.fetchall()
    if(not temp):
        return render_template('process.html', title="Voting")
    val = temp[0][0]
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
    vote = request.args.get('field')
    mycursor.execute('select unique_id from candidates where candidate_name=\'{}\''.format(vote))
    num = mycursor.fetchall()[0][0]
    flash("you voted for {}".format(vote), 'success')
    mycursor.execute('delete from login where loff_email=\'{}\''.format(Username))
    cnx.commit()
    return render_template('finish.html', title="Voting")


if __name__ == '__main__':
    #SESSION = requests.Session()
    #token = auth_context.acquire_token_with_client_credentials(RESOURCE, CLIENT_APP_Id, CLIENT_SECRET)
    #SESSION.headers.update({'Authorization': 'Bearer ' + token['accessToken']})
    app.run(debug=True)