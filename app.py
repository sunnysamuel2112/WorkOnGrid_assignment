from flask import Flask, request, jsonify
import sqlite3
import requests

# Create the SQLite database and user table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    email TEXT,
                    phone TEXT,
                    birth_date TEXT
                )''')
conn.commit()
conn.close()

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>WorkOnGrid Assignment</h1></b><h3>Use this to access API:  http://localhost:5000/api/users?first_name=Will</h3></b><h4>Submitted by:  SHAN NEHEMIAH SAMUEL MS</h4>"

@app.route('/api/users')
def get_users():
    first_name = request.args.get('first_name')

    # Search the user table for matching users
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE first_name LIKE ?", (first_name + '%',))
    matching_users = cursor.fetchall()
    conn.close()
    

    # If users are found, return them in JSON format
    if matching_users:
        users_json = []
        for user in matching_users:
            user_dict = {
                'first_name': user[1],
                'last_name': user[2],
                'age': user[3],
                'gender': user[4],
                'email': user[5],
                'phone': user[6],
                'birth_date': user[7]
            }
            users_json.append(user_dict)
        return jsonify(users_json)

    # If no users are found, call the external API and save the resulting users
    else:
        external_api_url = f"https://dummyjson.com/users/search?q={first_name}"
        response = requests.get(external_api_url)
        fetched_users = response.json()

        #Save the retrieved users to the user table
        return_json = []
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        for each_user in fetched_users['users']:
            if each_user['firstName'].startswith(first_name.capitalize()):
                cursor.execute("INSERT INTO users (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)",(each_user['firstName'], each_user['lastName'], each_user['age'], each_user['gender'], each_user['email'], each_user['phone'], each_user['birthDate']))
                user_json = {
                'first_name': each_user['firstName'],
                'last_name': each_user['lastName'],
                'age': each_user['age'],
                'gender': each_user['gender'],
                'email': each_user['email'],
                'phone': each_user['phone'],
                'birth_date': each_user['birthDate']}
                return_json.append(user_json)
        conn.commit()
        conn.close()
        
        # return the retrieved users in JSON format
        return jsonify(return_json)

if __name__ == '__main__':
    app.run(debug=True)
