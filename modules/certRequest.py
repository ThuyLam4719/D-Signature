import requests
import json
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec

# URL CA (chạy flask app trong web_ca/app.py)
CA_SERVER = "http://127.0.0.1:5000/api/submit_csr"

def tao_csr(private_key_path, cn, org, country):
    # Load private key
    with open(private_key_path, "rb") as f:
        key_data = f.read()
    private_key = serialization.load_pem_private_key(key_data, password=None)

    # Xây subject
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])

    csr_builder = x509.CertificateSigningRequestBuilder().subject_name(subject)

    # Ký CSR bằng private key
    if isinstance(private_key, rsa.RSAPrivateKey):
        csr = csr_builder.sign(private_key, hashes.SHA256())
    elif isinstance(private_key, ec.EllipticCurvePrivateKey):
        csr = csr_builder.sign(private_key, hashes.SHA256())
    else:
        # fallback: thử sign chung
        csr = csr_builder.sign(private_key, hashes.SHA256())

    csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    return csr_pem


def gui_yeu_cau(private_key_path, cn, org, country):
    try:
        csr_pem = tao_csr(private_key_path, cn, org, country)
        data = {
            "cn": cn,
            "org": org,
            "country": country,
            "csr": csr_pem
        }

        response = requests.post(CA_SERVER, json=data)
        if response.status_code == 200:
            return "OK"
        else:
            return f"Lỗi từ CA: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Lỗi khi tạo/gửi CSR: {str(e)}"
