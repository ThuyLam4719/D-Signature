from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
import base64

def ky_du_lieu(duong_dan_khoa, thong_diep):
    """
    Ký dữ liệu (string) bằng khóa bí mật. Thư viện sẽ tự động băm SHA256.
    Lưu ý: Thong_diep đã được làm sạch (.strip()) ở lớp UI.
    """
    try:
        # Đọc khóa bí mật
        with open(duong_dan_khoa, "rb") as f:
            khoa_bi_mat = serialization.load_pem_private_key(f.read(), password=None)

        # 1️⃣ Chuyển thông điệp (string đã clean) sang bytes
        thong_diep_bytes = thong_diep.encode('utf-8')

        # 2️⃣ Ký tùy theo loại khóa (Truyền thông điệp gốc, thư viện tự băm SHA256)
        if isinstance(khoa_bi_mat, rsa.RSAPrivateKey):
            chu_ky = khoa_bi_mat.sign(
                thong_diep_bytes, 
                padding.PKCS1v15(), 
                hashes.SHA256()
            )
        elif isinstance(khoa_bi_mat, ec.EllipticCurvePrivateKey):
            chu_ky = khoa_bi_mat.sign(
                thong_diep_bytes, 
                ec.ECDSA(hashes.SHA256())
            )
        else:
            raise ValueError("Loại khóa không được hỗ trợ")

        # Trả chữ ký dạng base64
        chu_ky_base64 = base64.b64encode(chu_ky).decode('utf-8')
        return chu_ky_base64

    except Exception as e:
        return f"Lỗi khi ký: {str(e)}"