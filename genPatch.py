# -*- coding: utf-8 -*-
import requests, json, sys ,os

ADDRESS = "003753AC"

def call_armtohex_api(code):
    url = "https://armconverter.com/api/convert"

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
    return json.loads(r.text)["hex"]["arm64"][1]

if __name__ == "__main__":
    try:
        path = os.getcwd()
        file = path + "/" + os.path.basename("input.pchtxt")
        
        codes = []
        # ファイルオープン
        with open(file, mode="r") as f:
            for line in f:
                line = line.split(",")
                code = {"arm": [ f'MOV X0, #0x{line[0][0:4]}0000', f'MOVK X0, #0x{line[0][4:8]}'], "wave": line[1], "desc": line[2].strip() }
                codes.append(code)
            # コード部分を抽出してくっつける
            arm = list(map(lambda code: "\n".join(code["arm"]), codes))
            # response = call_armtohex_api(arm)
            response = call_armtohex_api(arm).split("\n")
            response = list(map(lambda code: "".join(code), list(zip(*[iter(response)] * 2))))
            for idx, hexcode in enumerate(response):
                codes[idx]["hex"] = hexcode.strip()
            
            file = path + "/" + "530.pchtxt"
            with open(file, mode='w') as fw:
                for code in codes:
                        fw.write(f'// {code["wave"]} {code["desc"]}\n')
                        fw.write("@disabled\n")
                        fw.write(f'{ADDRESS} {code["hex"]}\n\n')
                fw.close()
    except FileNotFoundError:
        print("Not found input.pchtxt")