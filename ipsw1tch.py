# -*- coding: utf-8 -*-
import requests, json, sys ,os

def call_armtohex_api(code):
    url = "https://armconverter.com/convert"
    request_code = "\n".join(code)
    request_body = {
        "asm" : request_code,
        "offset" : '',
        "arch" : ["arm64"]
    }
    request_head = {
        "Host" : "armconverter.com",
        "Content-Length": str(len(json.dumps(request_body))),
        "Content-Type" : "application/json",
        "Accept" : "*/*",
        "Accept-Encofing" : "gzip, deflate, br",
        "Connection" : "keep-alive"
    }
    session = requests.Session()
    r = session.post(url=url, headers=request_head, json=request_body)
    return json.loads(r.text)["hex"]["arm64"]

if __name__ == "__main__":
    print("Welcome to IPSw1tch!")
    path= os.path.dirname(os.path.abspath(sys.argv[1]))
    file = path + "/" + os.path.basename(sys.argv[1])
    with open(file) as f:
        code = []
        com = []
        for line in f:
            try:
                int(line[0:8], 16) # Find ARM
                if "/" in line: # Include comment
                    hex = line[9: line.find("/") - 1]
                    com = line[line.find("/"):]
                else:
                    if line.find(" ") < 9:
                        hex = line[9: line.find("\n")]
                    else:
                        hex = line[9: line.rfind(" ") - 1]
                code.append(hex)
            except:
                pass
        res = call_armtohex_api(code)
        if res[0] != True: # IF ARM CODE IS WRONG
            print("ARM CODE ERROR!")
            exit(1)
        else:
            with open(path + "/" + os.path.splitext(os.path.basename(file))[0] + ".pchtxt", mode='w') as fw:
                num = 0
                code = res[1].split("\n")
                f.seek(0)
                for line in f:
                    try:
                        int(line[0:8], 16) # Find ARM
                        if "/" in line: # Include comment
                            fw.write(line[0:9] + code[num] + "\n")
                        else:
                            fw.write(line[0:9] + code[num] + "\n")
                        num += 1
                    except:
                        fw.write(line)
                fw.close()