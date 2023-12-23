import datetime, requests, sqlite3, os 

key = os.urandom(32) 
iv = os.urandom(16)

from cryptography.fernet import Fernet

key = Fernet.generate_key()

cipher = Fernet(key)

def encrypt_list(list_to_encrypt):
    encrypted_list = []
    for obj in list_to_encrypt:
        encrypted_obj = cipher.encrypt(str(obj).encode())
        encrypted_list.append(encrypted_obj)
    return encrypted_list

def decrypt_list(encrypted_list):
    decrypted_list = []
    for encrypted_obj in encrypted_list:
        decrypted_obj = cipher.decrypt(encrypted_obj)
        decrypted_list.append(decrypted_obj.decode())
    return decrypted_list

# original_list = [{ 
#           "transactor": 283424, 
#           "amount": 92734 , 
#           "hash": "sjhdsbjfhsjfdh982ye982", 
#           "time": "0.0"
#      }]

# encrypted_list = encrypt_list(original_list)
# print('Encrypted List:', encrypted_list)

# decrypted_list = decrypt_list(encrypted_list)
# print('Decrypted List:', decrypted_list)


def pay_request(Accepter_url: str,transactor_api: int, amount: float, hash, timing=datetime.datetime.now().time()): 
     # cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
     # encryptor = cipher.encryptor()
     # padder = padding.PKCS7(128).padder()
     conn = sqlite3.connect("my_acc.db")
     s = { 
          "Accepter":  Accepter_url,
          "transactor": transactor_api, 
          "amount": amount , 
          "hash": hash, 
          "time": timing
     }
     unstr = str(s)
    
     # cips = encryptor.update(crytps_) + encryptor.finalize()

     send = requests.post(Accepter_url, data=s)   
    
     try: 
          return "Transaction is Succes" 
     except Exception as e: 
          return e


     # if send.status_code == 200 and send.text == "Pay is done": 
     #      return "Pay is Succes" 
     # else: 
     #      return "Erorr"
     
def accept_request(transaction, server): 
    response = requests.get(server) 
    json_data_trasactio = response.json()
    encr = decrypt_list(json_data_trasactio) 
    pay_balance = float(encr['amount']) 

    co = sqlite3.connect('users.db')
    cur = co.cursor() 
    balance = cur.execute("SELECT balance, FROM users") 
    
    cur.execute("""UPDATE users SET balance = ?""", (balance-pay_balance))

