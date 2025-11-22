import time
import os
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
from modules.keyGenerate import sinh_khoa_rsa, sinh_khoa_ecdsa # Giả sử keyGenerate.py nằm trong modules/pki
from modules.signData import ky_du_lieu
from modules.verifySign import xac_thuc_chu_ky

# --- Cấu hình ---
THU_MUC_TEST = "data/benchmark"
SO_LAN_LAP = 100  # Số lần lặp lại để lấy kết quả trung bình

# --- Khởi tạo Khóa và Dữ liệu Test ---

# 1. Tạo file dữ liệu mẫu
THONG_DIEP_GOC = "Đây là thông điệp test hiệu năng của RSA và ECDSA." * 5
DUONG_DAN_THONG_DIEP = os.path.join(THU_MUC_TEST, "test_message.txt")
if not os.path.exists(THU_MUC_TEST):
    os.makedirs(THU_MUC_TEST)
with open(DUONG_DAN_THONG_DIEP, "w", encoding="utf-8") as f:
    f.write(THONG_DIEP_GOC)

# 2. Tạo Khóa Test (RSA 2048 bit và ECDSA P-256)
# Giả định các hàm sinh khóa đã có sẵn
RSA_PRI_KEY = os.path.join(THU_MUC_TEST, "benchmark_rsa_private.pem")
RSA_PUB_KEY = os.path.join(THU_MUC_TEST, "benchmark_rsa_public.pem")
ECC_PRI_KEY = os.path.join(THU_MUC_TEST, "benchmark_ecc_private.pem")
ECC_PUB_KEY = os.path.join(THU_MUC_TEST, "benchmark_ecc_public.pem")

# Sinh khóa nếu chưa tồn tại (Dùng hàm của bạn)
if not os.path.exists(RSA_PRI_KEY):
    print("Đang sinh khóa RSA...")
    sinh_khoa_rsa("benchmark", 2048, THU_MUC_TEST) 
    os.rename(os.path.join(THU_MUC_TEST, "benchmark_rsa_private.pem"), RSA_PRI_KEY)
    os.rename(os.path.join(THU_MUC_TEST, "benchmark_rsa_public.pem"), RSA_PUB_KEY)

if not os.path.exists(ECC_PRI_KEY):
    print("Đang sinh khóa ECDSA...")
    sinh_khoa_ecdsa("benchmark", "P-256", THU_MUC_TEST)
    os.rename(os.path.join(THU_MUC_TEST, "benchmark_ecc_private.pem"), ECC_PRI_KEY)
    os.rename(os.path.join(THU_MUC_TEST, "benchmark_ecc_public.pem"), ECC_PUB_KEY)

# --- Các Hàm Đo Lường ---

def do_luong_ky(ten_thuat_toan, duong_dan_khoa_rieng):
    thoi_gian_bat_dau = time.perf_counter()
    chu_ky = ""
    for _ in range(SO_LAN_LAP):
        chu_ky = ky_du_lieu(duong_dan_khoa_rieng, THONG_DIEP_GOC)
    thoi_gian_ket_thuc = time.perf_counter()
    tong_thoi_gian = thoi_gian_ket_thuc - thoi_gian_bat_dau
    print(f"| {ten_thuat_toan} | Ký ({SO_LAN_LAP} lần) | {tong_thoi_gian:.4f} giây |")
    return chu_ky, tong_thoi_gian

def do_luong_xac_thuc(ten_thuat_toan, duong_dan_khoa_cong_khai, chu_ky_test):
    thoi_gian_bat_dau = time.perf_counter()
    for _ in range(SO_LAN_LAP):
        xac_thuc_chu_ky(duong_dan_khoa_cong_khai, THONG_DIEP_GOC, chu_ky_test)
    thoi_gian_ket_thuc = time.perf_counter()
    tong_thoi_gian = thoi_gian_ket_thuc - thoi_gian_bat_dau
    print(f"| {ten_thuat_toan} | Xác thực ({SO_LAN_LAP} lần) | {tong_thoi_gian:.4f} giây |")
    return tong_thoi_gian

# --- Thực hiện Benchmarking ---

print("\n" + "="*70)
print(f"BÀI TEST HIỆU NĂNG PKI: RSA 2048 vs ECDSA P-256 (Lặp lại {SO_LAN_LAP} lần)")
print("="*70)
print("| Thuật toán | Hoạt động | Tổng thời gian |")
print("|---|---|---|")

# 1. Đo lường RSA
print("\n--- Đo lường RSA ---")
chu_ky_rsa, t_ky_rsa = do_luong_ky("RSA 2048", RSA_PRI_KEY)
t_xac_thuc_rsa = do_luong_xac_thuc("RSA 2048", RSA_PUB_KEY, chu_ky_rsa)

# 2. Đo lường ECDSA
print("\n--- Đo lường ECDSA ---")
chu_ky_ecc, t_ky_ecc = do_luong_ky("ECDSA P-256", ECC_PRI_KEY)
t_xac_thuc_ecc = do_luong_xac_thuc("ECDSA P-256", ECC_PUB_KEY, chu_ky_ecc)

print("\n" + "="*70)

# 3. So sánh kết quả
print("KẾT QUẢ TỔNG HỢP:")
print("Tốc độ Ký: ECDSA nhanh hơn RSA {:.2f} lần.".format(t_ky_rsa / t_ky_ecc))
print("Tốc độ Xác thực: RSA nhanh hơn ECDSA {:.2f} lần.".format(t_xac_thuc_ecc / t_xac_thuc_rsa))

# 4. Kiểm tra kích thước chữ ký
print("\nKích thước chữ ký:")
print(f"Kích thước RSA: {len(chu_ky_rsa)} bytes")
print(f"Kích thước ECDSA: {len(chu_ky_ecc)} bytes (Rất nhỏ!)")

print("="*70)