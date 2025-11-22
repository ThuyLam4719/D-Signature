from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.exceptions import InvalidSignature
import os # Import os để xử lý đường dẫn file

def write_public_key(public_key, output_pub_path):
    """Trích xuất và lưu khóa công khai từ chứng chỉ vào file."""
    try:
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Sử dụng output_pub_path trực tiếp để ghi file
        with open(output_pub_path, "wb") as f:
            f.write(pem_data)
        return output_pub_path
    except Exception as e:
        print(f"[CẢNH BÁO] Lỗi khi ghi Public Key: {e}")
        return None

def verify_certificate(cert_path, ca_public_key_path, output_pub_path):
    """
    Xác thực chứng chỉ.
    Tham số output_pub_path được dùng để lưu Public Key trích xuất.
    Trả về: (status: bool, message: str)
    """
    try:
        # ===== Đọc chứng chỉ & Khóa CA =====
        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())
        with open(ca_public_key_path, "rb") as f:
            ca_pub_key = serialization.load_pem_public_key(f.read()) # Đổi tên biến CA Public Key thành ca_pub_key

        # ===== Dữ liệu cần xác thực =====
        tbs = cert.tbs_certificate_bytes
        signature = cert.signature
        hash_algo = cert.signature_hash_algorithm
        
        cert_valid_from = cert.not_valid_before_utc
        cert_expired_at = cert.not_valid_after_utc

        # ===== Xác thực chữ ký =====
        if isinstance(ca_pub_key, rsa.RSAPublicKey): # Sử dụng ca_pub_key
            ca_pub_key.verify(signature, tbs, padding.PKCS1v15(), hash_algo)
        elif isinstance(ca_pub_key, ec.EllipticCurvePublicKey): # Sử dụng ca_pub_key
            ca_pub_key.verify(signature, tbs, ec.ECDSA(hash_algo))
        else:
            return False, "**LỖI KHÔNG HỢP LỆ:** Loại public key của CA không được hỗ trợ (chỉ hỗ trợ RSA và ECC)."

        # =======================================================
        # CHỨNG CHỈ HỢP LỆ
        # =======================================================
        
        # Trích xuất Public Key từ chứng chỉ (cert)
        cert_public_key = cert.public_key() # Đổi tên biến Public Key trích xuất thành cert_public_key
        output_file = write_public_key(cert_public_key, output_pub_path)
        
        output_message = f"<h3 style='color: green;'>CHỨNG CHỈ HỢP LỆ</h3>"

        # ... (các đoạn code in thông tin khác không thay đổi) ...
        # Phần code này vẫn đúng, không cần thay đổi gì thêm
        if output_file:
            # Thay \n\n bằng <br><br>
            output_message += f"Public Key đã được trích xuất và lưu tại: <b>{output_file}</b><br><br>"

        output_message += "<h4>Thông tin Chi tiết Chứng chỉ:</h4>"
        output_message += f" - <b>Subject:</b> {cert.subject.rfc4514_string()}<br>"
        output_message += f" - <b>Issuer:</b> {cert.issuer.rfc4514_string()}<br>"
        output_message += f" - <b>Ngày hiệu lực:</b> {cert_valid_from}<br>"
        output_message += f" - <b>Ngày hết hạn:</b> {cert_expired_at}"
        
        return True, output_message

    except InvalidSignature:
        return False, "<h3 style='color: red;'>CHỮ KÝ KHÔNG HỢP LỆ</h3>Chữ ký chứng chỉ không khớp với Public Key của CA (Chứng chỉ giả mạo hoặc sai CA)."
    
    except Exception as e:
        # Xử lý các lỗi khác như lỗi đọc file, định dạng file sai, v.v.
        return False, f"<h3 style='color: red;'>LỖI HỆ THỐNG</h3>Không thể xử lý chứng chỉ/khóa: {e}"