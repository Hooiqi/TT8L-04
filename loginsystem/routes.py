from flask import Flask, request, url_for, redirect

DBupdate = dbupdate() 

app = Flask(__name__)

@app.route('/success')
def deploy_success():
    return render_template("success.html")

def deploy_script(sql):
    res = DBupdate.dbvalues_get(sql)
    return res

@app.route('/', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['admin'] = request.form['username']
            return redirect(url_for('form_example'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def form_example():
    if 'admin' not in session:
        return redirect(url_for('login_page'))
    else:

