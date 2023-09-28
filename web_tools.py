from urllib.parse import urlparse
from urllib.request import urlopen
import socket


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def findTitle(url):
    webpage = urlopen(url).read()
    title = str(webpage).split('<title>')[1].split('</title>')[0]
    return title


def ip_address(website):
    print(findTitle(website))

    if "://" in website:
        website = website.split("://")[1]
    parts = website.split("/")
    domain = parts[0]
    try:
        ip_address = socket.gethostbyname(domain)
        return (domain, ip_address)
    except socket.gaierror:
        return (domain, "Invalid domain or unable to resolve IP address")
