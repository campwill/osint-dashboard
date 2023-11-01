from urllib.parse import urlparse
from urllib.request import urlopen
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
    webpage = urlopen(url).read().decode('utf-8')
    pattern = re.compile(r'<title>(.*?)</title>')
    title_search = pattern.search(webpage)
    if title_search:
        title = title_search.group(1)
        return title
    else:
        return ""


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
    handler = ipinfo.getHandler(ipinfo_api_key)

    details = handler.getDetails(ip_address)
    print(type(details.all))
    return (details.all)


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
