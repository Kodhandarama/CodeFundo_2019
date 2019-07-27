from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, VoterForm
import mysql.connector


Username = ''

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.Username.data == 'admin@blog.com' and form.password.data == 'password':
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
        if form.Voter_ID.data == '123456789' and form.Voter_ID_Confirm.data == form.Voter_ID.data:
            flash('You have been logged in!', 'success')
            cnx = mysql.connector.connect(user="Stallions@stallions-test", password='qwerty12345.', host="stallions-test.mysql.database.azure.com", port=3306, database='sample', ssl_ca='C:\\Users\\Shashank\\Desktop\\Project\\codefundo\\BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)                
            mycursor = cnx.cursor()    
            mycursor.execute('select * from login where ID=\'{}\''.format(Username))
            if(mycursor.fetchall()):
                mycursor.execute('UPDATE login SET Voter_ID=\'{}\' where ID=\'{}\''.format(form.Voter_ID.data, Username))
            else:
                sql = "INSERT INTO login (ID, Voter_ID) VALUES (%s, %s)"
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
