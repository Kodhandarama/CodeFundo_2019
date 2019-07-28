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
    cnx = mysql.connector.connect(user="Stallions@stallions-test", password='qwerty12345.', host="stallions-test.mysql.database.azure.com", port=3306, database='sample', ssl_ca='C:\\Users\\Shashank\\Desktop\\Project\\codefundo\\BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)                
    mycursor = cnx.cursor()    
    mycursor.execute('select * from login where ID=\'{}\''.format(Username))
    val = mycursor.fetchall()
    if(val):    
        for c in val:
            flash("Welcome {}".format(c[1]), 'success') 
        return render_template('Voter_info.html', title="Voting")
    return render_template('process.html', title="Voting")

if __name__ == '__main__':
    app.run(debug=True)
