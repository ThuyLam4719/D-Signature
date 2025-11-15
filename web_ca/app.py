from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from datetime import datetime, timedelta
import os, json

app = Flask(__name__, template_folder="templates")

DATA_FILE = "requests.json"
CERT_DIR = "issued"
CA_KEY_FILE = "ca_private.pem"
CA_CERT_FILE = "ca_cert.pem"

if not os.path.exists(CERT_DIR):
    os.makedirs(CERT_DIR)

def load_requests():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_requests(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_ca():
    if os.path.exists(CA_KEY_FILE) and os.path.exists(CA_CERT_FILE):
        with open(CA_KEY_FILE, "rb") as f:
            ca_priv = serialization.load_pem_private_key(f.read(), password=None)
        with open(CA_CERT_FILE, "rb") as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())
        return ca_priv, ca_cert
    else:
        ca_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"VN"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Demo CA"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"Demo Root CA"),
        ])
        ca_cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(ca_priv.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow() - timedelta(days=1))
            .not_valid_after(datetime.utcnow() + timedelta(days=3650))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(ca_priv, hashes.SHA256())
        )
        with open(CA_KEY_FILE, "wb") as f:
            f.write(ca_priv.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(CA_CERT_FILE, "wb") as f:
            f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
        return ca_priv, ca_cert

CA_PRIVATE_KEY, CA_CERT = ensure_ca()

@app.route("/")
def index():
    requests_list = load_requests()
    return render_template("index.html", requests=requests_list)

@app.route("/api/submit_csr", methods=["POST"])
def api_submit_csr():
    data = request.get_json()
    if not data or "csr" not in data:
        return {"error": "Thiếu CSR"}, 400

    csr_pem = data["csr"]
    cn = data.get("cn", "")
    org = data.get("org", "")
    country = data.get("country", "")

    requests_list = load_requests()
    new_id = len(requests_list) + 1
    entry = {
        "id": new_id,
        "cn": cn,
        "org": org,
        "country": country,
        "csr": csr_pem,
        "status": "pending",
        "cert_path": ""
    }
    requests_list.append(entry)
    save_requests(requests_list)
    return {"message": "CSR đã được gửi thành công"}, 200

def verify_csr_signature(csr):
    try:
        pub = csr.public_key()
        sig = csr.signature
        tbs = csr.tbs_certrequest_bytes
        try:
            if isinstance(pub, rsa.RSAPublicKey):
                pub.verify(sig, tbs, padding.PKCS1v15(), csr.signature_hash_algorithm)
            else:
                pub.verify(sig, tbs, ec.ECDSA(csr.signature_hash_algorithm))
        except Exception as e:
            return False, str(e)
        return True, ""
    except Exception as exc:
        return False, str(exc)

@app.route("/approve/<int:req_id>")
def approve(req_id):
    requests_list = load_requests()
    req = next((r for r in requests_list if r["id"] == req_id), None)
    if not req:
        return "Không tìm thấy yêu cầu", 404

    if req["status"] != "pending":
        return redirect(url_for("index"))

    csr_pem = req.get("csr")
    try:
        csr = x509.load_pem_x509_csr(csr_pem.encode())
    except Exception as e:
        return f"CSR không hợp lệ: {str(e)}", 400

    ok, err = verify_csr_signature(csr)
    if not ok:
        return f"Xác minh chữ ký CSR thất bại: {err}", 400

    subject = csr.subject
    issuer = CA_CERT.subject

    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.public_key(csr.public_key())
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    cert_builder = cert_builder.not_valid_before(datetime.utcnow() - timedelta(minutes=1))
    cert_builder = cert_builder.not_valid_after(datetime.utcnow() + timedelta(days=365))
    try:
        for ext in csr.extensions:
            cert_builder = cert_builder.add_extension(ext.value, ext.critical)
    except Exception:
        pass

    cert = cert_builder.sign(private_key=CA_PRIVATE_KEY, algorithm=hashes.SHA256())

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    cert_filename = f"{req['cn']}_cert.pem"
    cert_path = os.path.join(CERT_DIR, cert_filename)
    with open(cert_path, "wb") as f:
        f.write(cert_pem)

    req["status"] = "approved"
    req["cert_path"] = cert_filename
    save_requests(requests_list)

    return redirect(url_for("index"))

@app.route("/issued/<path:filename>")
def issued_files(filename):
    return send_from_directory(CERT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)