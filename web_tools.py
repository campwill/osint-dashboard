from urllib.parse import urlparse
from urllib.request import urlopen
from urllib import request
import requests
import ipinfo
from dotenv import load_dotenv
import json
import dns.resolver
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
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


findTitle("http://x.com")


def get_favicon(domain):
    return 'https://icon.horse/icon/' + domain


def website_information(website):
    title = findTitle(website)
    parsed_url = urlparse(website)
    domain = parsed_url.netloc
    try:
        ip_addresses = [res[4][0] for res in socket.getaddrinfo(domain, 80)]
        # Choosing the first IP address from the list
        ip_address = ip_addresses[0]
        with urlopen(website) as response:
            website_html = response.read().decode('utf-8')
        favicon_link = get_favicon(website_html)
        return (domain, ip_address, title, favicon_link)
    except (socket.gaierror, OSError):
        domain, ip_address, title, favicon_link = website_information(get_redirects(website)[1])
        return (domain, ip_address, title, favicon_link)


def get_redirects(url):
    try:
        response = requests.get(url, allow_redirects=True)
        redirects = response.history
        final_url = response.url
        return redirects, final_url
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return [], None


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
