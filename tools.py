import time
import requests

def link_checker(link):
    # checks link status code
    # if all good returns request file
    # if not sleeps for 10s and trys again

    try:
        req = requests.get(link)
        print(req.status_code)
        if req.status_code == 200:
            return req
        else:
            raise RuntimeError
    except:
        time.sleep(10)
        print("sleeepingg on link", link)
        link_checker(link)

