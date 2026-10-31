import json, subprocess, sys, time
def post(path, body, tries=3):
    for i in range(tries):
        r=subprocess.run(["curl","-sS","-m","60","-X","POST","https://api.usaspending.gov"+path,"-H","Content-Type: application/json","-d",json.dumps(body)],capture_output=True,text=True)
        try:
            return json.loads(r.stdout)
        except Exception as e:
            time.sleep(2)
    return {"error":r.stdout[:300],"stderr":r.stderr[:200]}
def get(path):
    r=subprocess.run(["curl","-sS","-m","60","https://api.usaspending.gov"+path],capture_output=True,text=True)
    try: return json.loads(r.stdout)
    except: return {"error":r.stdout[:300]}
