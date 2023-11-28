from urllib.parse import urlparse
from urllib.request import urlopen
from urllib import parse, robotparser, request
import requests
import ipinfo
from dotenv import load_dotenv
import json
import dns.resolver
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
import socket
import os
import re


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def findTitle(url):
    try:
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with request.urlopen(req) as response:
            html_content = response.read()
            return (str(html_content).split('<title>')[1].split('</title>')[0])
    except IndexError:
        return ""


def get_favicon(domain):
    return 'https://icon.horse/icon/' + domain


def website_information(website):
    title = findTitle(website)
    parsed_url = urlparse(website)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    try:
        ip_addresses = [res[4][0] for res in socket.getaddrinfo(domain, 80)]
        # Choosing the first IP address from the list
        ip_address = ip_addresses[0]
        with urlopen(website) as response:
            website_html = response.read().decode('utf-8')
        favicon_link = get_favicon(domain)
        return (domain, ip_address, title, favicon_link)
    except (socket.gaierror, OSError):
        _, ip_address, _, favicon_link = website_information(
            get_redirects(website)[1])
        return (domain, ip_address, title, favicon_link)


def get_redirects(url, max_redirects=10):
    redirects = []
    for _ in range(max_redirects):
        try:
            response = requests.get(url, allow_redirects=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {'Error': f'Failed to fetch URL: {e}'}
        if 300 <= response.status_code < 400:
            redirects.append(url)

            url = response.headers['Location']
        else:
            break

    return {'Redirects': redirects, 'Final URL': url}


def get_cookies(domain):
    response = requests.get(domain)
    cookies = response.cookies
    cookies_dict = {cookie.name: cookie.value for cookie in cookies}
    return cookies_dict


def get_headers(domain):
    response = requests.get(domain)
    headers = response.headers
    headers_dict = {header: value for header, value in headers.items()}
    return headers_dict


load_dotenv()
ipinfo_api_key = os.getenv('IPINFO_API_KEY')


def get_ip_info(ip_address):
    try:
        handler = ipinfo.getHandler(ipinfo_api_key)

        details = handler.getDetails(ip_address)
        return (details.all)
    except ValueError as e:
        return {'Error': f'{e}'}


def get_records(domain):
    results = {}
    record_types = ['NONE', 'A', 'NS', 'MD', 'MF', 'CNAME', 'SOA', 'MB', 'MG', 'MR', 'NULL', 'WKS', 'PTR', 'HINFO', 'MINFO', 'MX', 'TXT', 'RP', 'AFSDB', 'X25', 'ISDN', 'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX', 'GPOS', 'AAAA', 'LOC', 'NXT', 'SRV', 'NAPTR', 'KX', 'CERT', 'A6',
                    'DNAME', 'OPT', 'APL', 'DS', 'SSHFP', 'IPSECKEY', 'RRSIG', 'NSEC', 'DNSKEY', 'DHCID', 'NSEC3', 'NSEC3PARAM', 'TLSA', 'HIP', 'CDS', 'CDNSKEY', 'CSYNC', 'SPF', 'UNSPEC', 'EUI48', 'EUI64', 'TKEY', 'TSIG', 'IXFR', 'AXFR', 'MAILB', 'MAILA', 'ANY', 'URI', 'CAA', 'TA', 'DLV']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = [rdata.to_text() for rdata in answers]
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except Exception as e:
            continue

    return results


def get_ssl(hostname, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(
        socket.AF_INET, socket.SOCK_STREAM), server_hostname=hostname)
    conn.connect((hostname, port))

    certs = conn.getpeercert(True)
    certificate = x509.load_der_x509_certificate(certs, default_backend())
    subject = next((attr.value for attr in certificate.subject if attr.oid ==
                   x509.NameOID.COMMON_NAME), None)
    issuer = next((attr.value for attr in certificate.issuer if attr.oid ==
                  x509.NameOID.ORGANIZATION_NAME), None)
    certificate_info = {
        "subject": subject,
        "issuer": issuer,
        "serial_number": certificate.serial_number,
        "not_valid_before": certificate.not_valid_before.isoformat(),
        "not_valid_after": certificate.not_valid_after.isoformat()
    }
    return certificate_info


def get_sitemaps(website):
    robotstxturl = parse.urljoin(website, "robots.txt")
    try:
        rp = robotparser.RobotFileParser()
        rp.set_url(robotstxturl)
        rp.read()
        sitemaps = rp.site_maps()
    except robotparser.RobotFileParserError as e:
        print(f"error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return sitemaps


def sitemap_parser(sitemap):
    try:
        r = request.urlopen(sitemap)
        xml = r.read().decode('utf8')
        elements = re.findall(r'<loc>(.*?)<\/loc>', xml, re.DOTALL)

        urls = []

        for element in elements:
            try:
                if element.endswith('.xml'):
                    # Recursively call sitemap_parser
                    urls.extend(sitemap_parser(element))
                else:
                    urls.append(element)
            except Exception as e:
                print(f"Error parsing sub-sitemap '{element}': {str(e)}")

        return urls
    except Exception as e:
        print(f"Error accessing sitemap '{sitemap}': {str(e)}")
        return []


def site_maps(url):
    sitemaps = get_sitemaps(url)
    if sitemaps is None:
        return {"Pages": []}
    all_urls = []

    for sitemap in sitemaps:
        all_urls.extend(sitemap_parser(sitemap))

    urls_dict = {"Pages": all_urls}

    return (urls_dict)


def find_open_port(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((hostname, port))
    sock.close()

    return result == 0


def check_ports(url):
    ports_to_check = [21, 22, 23, 25, 53, 80, 110,
                      143, 443, 465, 587, 993, 995, 3306, 3389, 8080]
    open_ports = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda port: (
            port, find_open_port(url, port)), ports_to_check))

    for port, is_open in results:
        if is_open:
            open_ports.append(port)
    return {"Open Ports": open_ports}


def whois_info(domain):
    d, ex = domain.split('.')
    url = f"https://webwhois.verisign.com/webwhois-ui/rest/whois?q={d}&tld={ex}&type=domain"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    text = data["message"]
    lines = text.split('\n')
    domain_data = {}

    for i in range(17):
        key, value = lines[i].split(':', 1)
        domain_data[key] = value

    return domain_data
