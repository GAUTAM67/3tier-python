import SearchForm as SearchForm
from flask import Flask, render_template, request
from flask import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '13.232.135.26u'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        name = details['name']
        address = details['name']
        phonenumber = details['phonenumber']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(name, address, phonenumber ) VALUES (%s, %s, %s)", (name, address, phonenumber))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')



@app.route('/search_results/<query>', methods = ['GET','POST'])

def search_results(query):
    cur=mysql.connection.cursor()
    likeString = "'%%" + query + "%%'"
    result = cur.execute("SELECT * FROM MyUsers WHERE %s  LIKE %s;", (query, likeString))
    if result > 0:
        data  = cur.fetchall()
    return render_template('index.html' , data = search)
    else:
        error = 'Nothing found'
        return render_template('dashboard.html' , error = error)
    return render_template('index.html')




@app.route('/dashboard')
@is_logged_in
def dashboard():
  search = SearchForm(request.form)
if request.method == 'POST':
    select = form.select.data
    search = form.search.data
    query = select + search
    return redirect((url_for('search_results', query = query)))
return render_template('dashboard.html', form = search)


if __name__ == '__main__':
    app.run()
