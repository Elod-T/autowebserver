"""
Code from: http://www.zedwood.com/article/python-create-self-signed-cert
With license: https://creativecommons.org/licenses/by-sa/3.0/

Modified:
cert.set_serial_number(int(rand.bytes(16).encode('hex'),16)) to cert.set_serial_number(randint(1000,1000000))
Removed:
from OpenSSL import rand
Added:
from random import randint
"""

from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate, X509, X509Name, PKey, TYPE_RSA, X509Req, dump_privatekey, X509Extension)
import re
from random import randint


def create_self_signed_cert(cert_file_path):
    private_key_path = re.sub(r".(pem|crt)$", ".key", cert_file_path, flags=re.IGNORECASE)

    # create public/private key
    key = PKey()
    key.generate_key(TYPE_RSA, 2048)

    # Self-signed cert
    cert = X509()

    # subject = X509Name(cert.get_subject())
    subject = cert.get_subject()
    subject.CN = 'localhost'
    subject.O = 'XYZ Widgets Inc'
    subject.OU = 'IT Department'
    subject.L = 'Seattle'
    subject.ST = 'Washington'
    subject.C = 'US'
    subject.emailAddress = 'e@example.com'

    cert.set_version(2)
    cert.set_issuer(subject)
    cert.set_subject(subject)
    # cert.set_serial_number(int(os.urandom(16).encode('hex'),16))
    cert.set_serial_number(randint(1000,1000000))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    with open(cert_file_path, 'wb+') as f:
        f.write(dump_certificate(FILETYPE_PEM, cert))
    with open(private_key_path, 'wb+') as f:
        f.write(dump_privatekey(FILETYPE_PEM, key))