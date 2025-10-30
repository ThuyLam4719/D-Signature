from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
import base64

def ky_du_lieu(duong_dan_khoa, thong_diep):
    try:
        # Đọc khóa bí mật
        with open(duong_dan_khoa, "rb") as f:
            khoa_bi_mat = serialization.load_pem_private_key(f.read(), password=None)

        # Băm thông điệp bằng SHA256
        thong_diep_bytes = thong_diep.encode('utf-8')
        bam = hashes.Hash(hashes.SHA256())
        bam.update(thong_diep_bytes)
        gia_tri_bam = bam.finalize()

        # Ký tùy theo loại khóa
        if isinstance(khoa_bi_mat, rsa.RSAPrivateKey):
            chu_ky = khoa_bi_mat.sign(
                gia_tri_bam,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        elif isinstance(khoa_bi_mat, ec.EllipticCurvePrivateKey):
            chu_ky = khoa_bi_mat.sign(
                gia_tri_bam,
                ec.ECDSA(hashes.SHA256())
            )
        else:
            raise ValueError("Loại khóa không được hỗ trợ")

        # Trả chữ ký dạng base64 để dễ lưu
        chu_ky_base64 = base64.b64encode(chu_ky).decode('utf-8')
        return chu_ky_base64

    except Exception as e:
        return f"Lỗi khi ký: {str(e)}"
