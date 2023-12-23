import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('bank.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS accounts
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, passwrod TEXT, balance REAL)''')
conn.commit()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    password  = data['password']
    initial_balance = data['initial_balance']
    cur.execute("""SELECT * FROM accounts WHERE name = ? AND password = ?""", (name, password))
    if cur.fetchall():  
        return "USER already registered"
    else: 
         cur.execute("INSERT INTO accounts (name, password, balance) VALUES (?, ?)", (name, password, initial_balance)) 
         conn.commit()
         return "User registered successfully"


    
@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    sender = data['sender']
    recipient = data['recipient']
    amount = data['amount']
    cur.execute("SELECT balance FROM accounts WHERE name=?", (sender,))
    sender_balance = cur.fetchone()[0]
    if sender_balance < amount:
        return "Insufficient funds"
    else:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, sender))
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, recipient))
        conn.commit()
        return "Transfer completed successfully"


@app.route('/balance', methods=['GET'])
def get_balance():
    name = request.args.get("name")
    cur.execute("SELECT balance FROM accounts WHERE name=?", (name,))
    balance = cur.fetchone()
    if balance:
        return jsonify({"balance": balance[0]})
    else:
        return "User not found"

if __name__ == '__main__':
    app.run()
