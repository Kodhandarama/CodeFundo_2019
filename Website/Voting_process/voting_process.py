from flask import Flask, render_template, url_for, flash, redirect, request
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
    cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/codefundo/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
    mycursor = cnx.cursor()    
    mycursor.execute('select off_email from official')
    val = mycursor.fetchall()
    official_values = []
    if(val):    
        for c in val:
            official_values.append(c[0])         
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
    poll_data = []
    cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/codefundo/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
    mycursor = cnx.cursor()
    mycursor.execute('select cit_voterid from login where loff_email=\'{}\''.format(Username))
    temp = mycursor.fetchall()
    if(not temp):
        return render_template('process.html', title="Voting")
    val = temp[0][0]
    flash("Welcome {}".format(val), 'success') 
    mycursor.execute('select voter_const_id from voter where voter_id=\'{}\''.format(val))
    val2 = mycursor.fetchall()[0][0]
    mycursor.execute('select Const_Name from constituency where const_id={}'.format(int(val2)))
    val4 = mycursor.fetchall()[0][0]
    flash("Your constituency is {}".format(val4), 'success') 
    mycursor.execute('select candidate_name from candidates where candi_const_id=\'{}\''.format(val2))
    val3 = mycursor.fetchall()
    if(val3):    
        flash("Candidates for your constituency", 'success') 
        for c in val3:
            #flash("{}".format(c[0]), 'success') 
            poll_data.append(c[0])
        return render_template('Voter_info.html',data = poll_data)
    

@app.route('/poll')
def poll():
    global Username
    vote = request.args.get('field')
    flash("you voted for {}".format(vote), 'success')
    cnx = mysql.connector.connect(user="stallions@stallions", password='Qwerty12345.', host="stallions.mysql.database.azure.com", port=3306, database='sample', ssl_ca='/home/hp/Desktop/Projects/CodeFundo/codefundo/BaltimoreCyberTrustRoot.pem', ssl_verify_cert=True)
    mycursor = cnx.cursor()
    mycursor.execute('delete from login where loff_email=\'{}\''.format(Username))
    cnx.commit()
    return render_template('finish.html', title="Voting")


if __name__ == '__main__':
    app.run(debug=True)