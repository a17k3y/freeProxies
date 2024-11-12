import requests

# Initialize required lists for holding stuffs
obtainedProxies = []
workingProxies = []
badProxies = [] 
timeout = 10000


def getProxyList(timeout):
    #Attempt to obtain proxies. If failed, throw exception.
    try:
        request = requests.get(f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout={timeout}&country=all&ssl=all&anonymity=all')
    except Exception as e:
        print(f"The following error has occured: {e}.")
        exit()
    #Adds the grabbed proxies to a list
    for line in request.iter_lines():
        proxy = (line.decode())
        obtainedProxies.append(proxy)
    #Tests proxies
    for proxy in obtainedProxies:
        proxies = {
            'http': proxy
        }
        try:
            request = requests.get('https://www.scrapethissite.com/pages/simple', proxies=proxies, timeout=1)
            if request.status_code == 200:
                workingProxies.append(proxy)
            else:
                badProxies.append(proxy)
        except:
            badProxies.append(proxy)
    #Writes all obtained proxies to file for threat intel later
    try:
        f = open("obtainedproxies.txt", "a")
    except:
        f = open("obtainedproxies.txt", "w")
    for proxy in obtainedProxies:
        f.write(f"{proxy}\n")
    f.close()
    #Writes all good proxies to another file for sharing between systems
    try:
        f = open("goodproxies.txt", "a")
    except:
        f = open("goodproxies.txt", "w")
    for proxy in workingProxies:
        f.write(f"{proxy}\n")
    f.close()

getProxyList(timeout)