from urllib.parse import urlparse
from urllib.request import urlopen
import socket
import re


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


def find_favicon_link(html):
    favicon_pattern = r'<link\s+rel=["\']shortcut icon["\']\s+href=["\']([^"\']+)["\']'
    match = re.search(favicon_pattern, html, re.IGNORECASE)

    if match:
        return match.group(1)
    else:
        return None


def website_information(website):
    title = findTitle(website)
    parsed_url = urlparse(website)
    domain = parsed_url.netloc
    try:
        ip_address = socket.gethostbyname(domain)
        with urlopen(website) as response:
            website_html = response.read().decode('utf-8')
        favicon_link = find_favicon_link(website_html)
        return (domain, ip_address, title, favicon_link)
    except (socket.gaierror, OSError):
        return (domain, "Invalid domain or unable to resolve IP address")
