from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
import os

def sinh_khoa_rsa(ten="nguoidung", bit=2048, thu_muc="data/keys"):
    if not os.path.exists(thu_muc):
        os.makedirs(thu_muc)

    khoa_rieng = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bit
    )

    with open(os.path.join(thu_muc, f"{ten}_rsa_private.pem"), "wb") as f:
        f.write(khoa_rieng.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(os.path.join(thu_muc, f"{ten}_rsa_public.pem"), "wb") as f:
        f.write(khoa_rieng.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Đã sinh khóa RSA {bit} bit trong {thu_muc}")

def sinh_khoa_ecdsa(ten="nguoidung", curve_name="P-256", thu_muc="data/keys"):
    if not os.path.exists(thu_muc):
        os.makedirs(thu_muc)

    if curve_name == "P-256":
        curve = ec.SECP256R1()
    elif curve_name == "P-384":
        curve = ec.SECP384R1()
    else:
        curve = ec.SECP521R1()

    khoa_rieng = ec.generate_private_key(curve)

    with open(os.path.join(thu_muc, f"{ten}_ecc_private.pem"), "wb") as f:
        f.write(khoa_rieng.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(os.path.join(thu_muc, f"{ten}_ecc_public.pem"), "wb") as f:
        f.write(khoa_rieng.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Đã sinh khóa ECDSA {curve_name} trong {thu_muc}")

# Test nhanh
if __name__ == "__main__":
    sinh_khoa_rsa("test", 2048, "output")
    sinh_khoa_ecdsa("test", "P-384", "output")
