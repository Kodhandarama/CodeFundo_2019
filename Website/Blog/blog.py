from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, VoterForm
import mysql.connector


Username = ''
cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/codefundo/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
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
cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/Website/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
mycursor = cnx.cursor()
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
        if form.Voter_ID_Confirm.data == form.Voter_ID.data and if form.Voter_ID.data in valid_voters:
            
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
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Voter_ID', 'danger')
    return render_template('vote_submit.html', title='Login', form=form)



if __name__ == '__main__':
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