from flask import*
import pymysql
import sms


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Set a secret key for session management

# Index route
@app.route('/')  
def index():
    return render_template('index.html')  # Assuming you have an index.html template

@app.route('/about')  
def about():
    return render_template('about.html')

@app.route('/diani')  
def diani():
    return render_template('diani.html')
@app.route('/mombasa')  
def mombasa():
    return render_template('mombasa.html')
@app.route('/malindi')  
def malindi():
    return render_template('malindi.html')

@app.route('/location')  
def location():
    return render_template('location.html')
@app.route('/more')  
def  more():
    return render_template('more.html')
# root of servises
@app.route('/services') 
def services():
    connection=pymysql.connect(host='localhost',user='root',password='',database='travelingagency')
    cursor=connection.cursor()
    sql='SELECT * FROM places'
    cursor.execute(sql)
    services=cursor.fetchall()

    return render_template('services.html',services=services)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        passkey = request.form['passkey']
        passkey2 = request.form['passkey2']

        if len(passkey) < 8:
            return render_template('register.html', error='Password should be more than 8 characters')
        elif passkey != passkey2:
            return render_template('register.html', error='Passwords did not match. Please check again.')

        # Establish database connection
        connection = pymysql.connect(host='localhost', user='root', password='', database='travelingagency')
        cursor = connection.cursor()

        # Insert user data into the database
        data = (name, phone_number, email, passkey)
        sql = 'INSERT INTO agency(name, phone_number, email, passkey) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql,data)
        connection.commit()
        
        # Send SMS notification to the registered user
       
        return render_template('register.html', success='Registration successful.')
    else:
        return render_template('register.html', welcome='Kindly register to login.')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        passkey=request.form['passkey']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='travelingagency')
        cursor = connection.cursor()
        data = (name,passkey)
        sql = 'SELECT * FROM agency WHERE name=%s AND passkey=%s'
        
        cursor.execute(sql, data)
        if cursor.rowcount !=0:
            return render_template('login.html', error="Invalid Credentials")
        else:
            session['name'] = name  # Store name in session
            return redirect('/')
    else:
        return render_template('login.html', success='successful login.')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return render_template('login.html')

# this function is doing
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name= request.form['name']
        email= request.form['email']
        message= request.form['message']
        

        # Establish database connection
        connection = pymysql.connect(host='localhost', user='root', password='', database='travelingagency')
        cursor = connection.cursor()

        # Insert booking data into the database
        data = (name, email, message)
        sql = 'INSERT INTO contact(name, email, message) VALUES (%s, %s, %s)'
        cursor.execute(sql, data)
        connection.commit()

        return render_template('contact.html', success='contact successful.')
    else:
        # connection.rollback()
        return render_template('contact.html', success='contact failed.')

@app.route('/booking', methods=['POST', 'GET'])
def booking():
    if request.method == 'POST':
        name=request.form['name']
        date_in= request.form['date_in']
        date_out= request.form['date_out']
        adult_no= request.form['adult_no']
        children_no= request.form['children_no']
        room = request.form['room']
        anything_else = request.form['anything_else']

        # Establish database connection
        connection = pymysql.connect(host='localhost', user='root', password='', database='travelingagency')
        cursor = connection.cursor()

        # Insert booking data into the database
        data = (name,date_in,date_out,adult_no,children_no, room,anything_else)
        sql = 'INSERT INTO booking(name,date_in, date_out, adult_no, children_no, room, anything_else) VALUES (%s, %s, %s, %s, %s, %s,%s)'
        cursor.execute(sql, data)
        connection.commit()
        
        

        return render_template('booking.html', success='Booking successful.')
    else:
        # connection.rollback()
        return render_template('booking.html', error='Booking failed.')
    
@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method=='POST':
        place_name=request.form['place_name']
        place_decription=request.form['place_decription']
        place_price=request.form['place_price']
        place_categoriy=request.form['place_categoriy']
        place_image=request.files['place_image']
        place_image.save('static/images/'+place_image.filename)
        
        # Conaction to database
        connection=pymysql.connect (host='localhost', user='root', password='', database='travelingagency')
        cursor=connection.cursor()

        #attaching data from the form to a variable in thepython file
        data=(place_name,place_decription,place_price,place_categoriy,place_image.filename)

        # inserting to the edatabase
        sql='insert into places(place_name,place_decription,place_price,place_categoriy,place_image) values(%s,%s,%s,%s,%s)'
        cursor.execute(sql,data)
        connection.commit()
        return render_template('upload.html',message_two='place uploaded successfully')
    else:
        return render_template('upload.html', message_one='Please upload Place')
    
@app.route('/order')
def order():
    connection=pymysql.connect (host='localhost',user='root',passwd='', database='travelingagency')
    cursor=connection.cursor()
    
    sql='select* from booking'
    cursor.execute(sql)
    order=cursor.fetchall()

    return render_template('order.html',order=order)    

@app.route('/single/<place_id>')
def single(place_id):
        
        connection=pymysql.connect (host='localhost', user='root', password='', database='travelingagency')
        cursor=connection.cursor()

        sql='select *from places where place_id= %s'
        cursor.execute(sql,place_id)
        place=cursor.fetchone()
        return render_template('single.html', place=place)


if __name__ == '__main__':
    app.run(debug=True)