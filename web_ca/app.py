from flask import Flask, request, render_template, redirect, url_for
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os, json

app = Flask(__name__)

DATA_FILE = "requests.json"
CERT_DIR = "issued"

if not os.path.exists(CERT_DIR):
    os.makedirs(CERT_DIR)

def load_requests():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_requests(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    requests_list = load_requests()
    return render_template("index.html", requests=requests_list)

@app.route("/api/submit_request", methods=["POST"])
def api_submit():
    data = request.get_json()
    requests_list = load_requests()
    data["id"] = len(requests_list) + 1
    data["status"] = "pending"
    requests_list.append(data)
    save_requests(requests_list)
    return {"message": "Yêu cầu đã được gửi thành công"}

@app.route("/approve/<int:req_id>")
def approve(req_id):
    requests_list = load_requests()
    req = next((r for r in requests_list if r["id"] == req_id), None)
    if not req:
        return "Không tìm thấy yêu cầu", 404

    # Tạo chứng chỉ tự ký bởi CA
    ca_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, req["country"]),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, req["org"]),
        x509.NameAttribute(NameOID.COMMON_NAME, req["cn"]),
    ])

    public_key = serialization.load_pem_public_key(req["public_key"].encode())

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(ca_private_key, hashes.SHA256())
    )

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    cert_path = os.path.join(CERT_DIR, f"{req['cn']}_cert.pem")
    with open(cert_path, "wb") as f:
        f.write(cert_pem)

    req["status"] = "approved"
    req["cert_path"] = cert_path
    save_requests(requests_list)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
