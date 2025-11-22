from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from datetime import datetime, timedelta
import os, json

app = Flask(__name__, template_folder="templates")
app.secret_key = "super-secret-key"   # đổi key tùy ý

DATA_FILE = "requests.json"
ISSUED_FILE = "issued.json"
REVOKED_FILE = "revoked.json"

CERT_DIR = "issued"
CA_KEY_FILE = "ca_private.pem"
CA_CERT_FILE = "ca_cert.pem"

ADMIN_USER = "admin"
ADMIN_PASS = "123456"

if not os.path.exists(CERT_DIR):
    os.makedirs(CERT_DIR)


# ----------- Utility load/save JSON -------------

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- MỚI: Template Filter để trích xuất Public Key từ CSR ---
@app.template_filter('extract_pubkey')
def extract_pubkey_filter(csr_pem):
    try:
        if not csr_pem: return ""
        req = x509.load_pem_x509_csr(csr_pem.encode())
        pub = req.public_key()
        pem = pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()
    except Exception as e:
        return f"Error extracting key: {str(e)}"

# ----------- Ensure CA exists -----------
# (Giữ nguyên đoạn này như cũ)
def ensure_ca():
    if os.path.exists(CA_KEY_FILE) and os.path.exists(CA_CERT_FILE):
        with open(CA_KEY_FILE, "rb") as f:
            ca_priv = serialization.load_pem_private_key(f.read(), password=None)
        with open(CA_CERT_FILE, "rb") as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())
        return ca_priv, ca_cert

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


# ---------------------- USER PUBLIC ROUTES ------------------------

@app.route("/")
def home():
    return redirect(url_for("public_certs"))

@app.route("/certs")
def public_certs():
    issued = load_json(ISSUED_FILE)
    return render_template("public_certs.html", issued=issued)

@app.route("/revoked")
def public_revoked():
    revoked = load_json(REVOKED_FILE)
    return render_template("public_revoked.html", revoked=revoked)


# ---------------------- ADMIN AUTH ------------------------

def require_admin():
    if "admin" not in session:
        return False
    return True

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user == ADMIN_USER and pw == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
        return "Sai tài khoản hoặc mật khẩu"
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")


# ---------------------- ADMIN PANEL ------------------------

@app.route("/admin")
def admin_panel():
    if not require_admin():
        return redirect("/admin/login")

    pending = load_json(DATA_FILE)
    issued = load_json(ISSUED_FILE)
    revoked = load_json(REVOKED_FILE)

    return render_template(
        "admin_dashboard.html",
        pending=pending,
        issued=issued,
        revoked=revoked
    )


# ---------------------- API: Client submit CSR ------------------------

@app.route("/api/submit_csr", methods=["POST"])
def submit_csr():
    data = request.get_json()
    if not data or "csr" not in data:
        return {"error": "Thiếu CSR"}, 400

    csr_pem = data["csr"]
    cn = data.get("cn", "")
    org = data.get("org", "")
    country = data.get("country", "")

    pending = load_json(DATA_FILE)
    new_id = len(pending) + 1

    entry = {
        "id": new_id,
        "cn": cn,
        "org": org,
        "country": country,
        "csr": csr_pem,
        "status": "pending",
    }

    pending.append(entry)
    save_json(DATA_FILE, pending)

    return {"message": "Đã gửi CSR thành công"}, 200


# ---------------------- CSR Verification ------------------------

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


# ---------------------- ADMIN: Approve CSR ------------------------

@app.route("/admin/approve/<int:req_id>")
def approve(req_id):
    if not require_admin():
        return redirect("/admin/login")

    pending = load_json(DATA_FILE)
    req = next((x for x in pending if x["id"] == req_id), None)
    if not req:
        return "Không tìm thấy yêu cầu", 404

    csr = x509.load_pem_x509_csr(req["csr"].encode())

    ok, err = verify_csr_signature(csr)
    if not ok:
        return "CSR không hợp lệ: " + err

    subject = csr.subject
    issuer = CA_CERT.subject

    cert_builder = x509.CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.public_key(csr.public_key())
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    # Dùng utcnow cho chuẩn X.509 (bắt buộc), nhưng hiển thị ở web ta sẽ dùng giờ local nếu muốn
    cert_builder = cert_builder.not_valid_before(datetime.utcnow() - timedelta(minutes=1))
    cert_builder = cert_builder.not_valid_after(datetime.utcnow() + timedelta(days=365))

    try:
        for ext in csr.extensions:
            cert_builder = cert_builder.add_extension(ext.value, ext.critical)
    except:
        pass

    cert = cert_builder.sign(CA_PRIVATE_KEY, hashes.SHA256())
    cert_pem = cert.public_bytes(serialization.Encoding.PEM)

    # lưu file .pem
    filename = f"{req['cn']}_cert.pem"
    cert_path = os.path.join(CERT_DIR, filename)
    with open(cert_path, "wb") as f:
        f.write(cert_pem)

    # đưa vào danh sách issued
    issued = load_json(ISSUED_FILE)
    
    # --- THAY ĐỔI: Lưu thêm Org và Country ---
    issued.append({
        "id": req["id"],
        "cn": req["cn"],
        "org": req["org"],           # Lưu lại org
        "country": req["country"],   # Lưu lại country
        "cert_file": filename,
        "status": "valid"
    })
    save_json(ISSUED_FILE, issued)

    # xóa khỏi pending
    pending = [x for x in pending if x["id"] != req_id]
    save_json(DATA_FILE, pending)

    return redirect("/admin")


# ---------------------- ADMIN: Revoke Cert ------------------------

@app.route("/admin/revoke/<int:cert_id>")
def revoke(cert_id):
    if not require_admin():
        return redirect("/admin/login")

    issued = load_json(ISSUED_FILE)
    cert = next((x for x in issued if x["id"] == cert_id), None)
    if not cert:
        return "Không tìm thấy chứng chỉ", 404

    # remove from issued
    issued = [x for x in issued if x["id"] != cert_id]
    save_json(ISSUED_FILE, issued)

    # add to revoked
    revoked = load_json(REVOKED_FILE)
    cert["status"] = "revoked"
    
    # --- THAY ĐỔI: Dùng giờ hệ thống (Local time) ---
    cert["revoked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    revoked.append(cert)
    save_json(REVOKED_FILE, revoked)

    return redirect("/admin")


# ---------------------- Serve issued files ------------------------

@app.route("/issued/<path:filename>")
def issued_files(filename):
    return send_from_directory(CERT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)