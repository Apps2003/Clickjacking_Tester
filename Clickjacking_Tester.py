from urllib.request import urlopen
from sys import argv, exit
import re

def check(url):
    ''' check given URL is vulnerable or not '''
    try:
        if "http" not in url:
            url = "http://" + url

        data = urlopen(url)
        headers = data.info()

        if "X-Frame-Options" not in headers:
            return True

    except:
        return False

def sanitize_url(url):
    ''' sanitize the URL to create a valid filename '''
    return re.sub(r'[^a-zA-Z0-9]', '_', url)

def create_poc(url):
    ''' create HTML page of given URL '''
    sanitized_url = sanitize_url(url)
    code = f"""
<html>
   <head><title>Clickjack test page</title></head>
   <body>
     <p>Website is vulnerable to clickjacking!</p>
     <iframe src="{url}" width="500" height="500"></iframe>
   </body>
</html>
    """

    with open(sanitized_url + ".html", "w") as f:
        f.write(code)

def main():
    ''' Everything comes together '''
    try:
        sites = open(argv[1], 'r').readlines()
    except:
        print("[*] Usage: python(3) clickjacking_tester.py <file_name>")
        exit(0)

    for site in sites:
        site = site.strip()
        print("\n[*] Checking " + site)
        status = check(site)

        if status:
            print(" [+] Website is vulnerable!")
            create_poc(site)
            print(f" [*] Created a poc and saved to {sanitize_url(site)}.html")
        else:
            print(" [-] Website is not vulnerable!")

if __name__ == '__main__':
    main()
