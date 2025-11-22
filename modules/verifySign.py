# verifySign.py
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.exceptions import InvalidSignature
import base64

def xac_thuc_chu_ky(duong_dan_khoa_cong_khai, thong_diep, chu_ky_base64):
    """
    Xác thực chữ ký số RSA hoặc ECDSA.
    Trả về: tuple (bool, str_hash_message, str_hash_recovered)
    """
    gia_tri_bam_hex = ""
    gia_tri_bam_giai_ma_hex = "N/A (Verification Failed)" # Giá trị mặc định nếu thất bại

    try:
        #Đọc khóa công khai
        with open(duong_dan_khoa_cong_khai, "rb") as f:
            khoa_cong_khai = serialization.load_pem_public_key(f.read())

        #Chuyển chữ ký từ base64 về bytes
        chu_ky = base64.b64decode(chu_ky_base64)

        #Chuyển thông điệp sang bytes
        thong_diep_bytes = thong_diep.encode('utf-8')

        #TÍNH GIÁ TRỊ BĂM (HASH) CỦA THÔNG ĐIỆP GỐC (H1)
        bam = hashes.Hash(hashes.SHA256())
        bam.update(thong_diep_bytes)
        gia_tri_bam = bam.finalize()
        gia_tri_bam_hex = gia_tri_bam.hex()

        #Xác thực chữ ký
        if isinstance(khoa_cong_khai, rsa.RSAPublicKey):
            khoa_cong_khai.verify(
                chu_ky,
                thong_diep_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        elif isinstance(khoa_cong_khai, ec.EllipticCurvePublicKey):
            khoa_cong_khai.verify(
                chu_ky,
                thong_diep_bytes,
                ec.ECDSA(hashes.SHA256())
            )
        else:
            raise ValueError("Loại khóa không được hỗ trợ để xác thực")

        # Nếu không xảy ra lỗi → chữ ký hợp lệ. 
        # Hash Giải mã (H2) BẮT BUỘC phải khớp với Hash Gốc (H1).
        gia_tri_bam_giai_ma_hex = gia_tri_bam_hex 
        return (True, gia_tri_bam_hex, gia_tri_bam_giai_ma_hex)

    except InvalidSignature:
        # Nếu chữ ký không hợp lệ (H1 != H2), ta trả về H1 và H2 là thông báo lỗi
        return (False, gia_tri_bam_hex, "Hash Mismatch (Verification Failed)")

    except Exception as e:
        # Lỗi đọc khóa, lỗi base64, vv.
        print("Lỗi khi xác thực:", e)
        # Nếu lỗi khác, trả về thông báo lỗi chi tiết
        return (False, gia_tri_bam_hex, f"Error: {type(e).__name__}")