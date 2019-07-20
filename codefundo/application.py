from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, VoterForm


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
            return redirect(url_for('vote'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/vote",  methods=['GET', 'POST'])
def vote():
    form = VoterForm()
    if form.validate_on_submit():
        if form.Voter_ID.data == '123456789' and form.Voter_ID_Confirm.data == form.Voter_ID.data:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Voter_ID', 'danger')
    return render_template('vote_submit.html', title='Login', form=form)



if __name__ == '__main__':
    app.run(debug=True)
