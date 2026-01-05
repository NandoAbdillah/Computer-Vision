import cv2
import numpy as np

# =========================
# CHAPTER 5: PERSPECTIVE WARP (SCAN EFFECT)
# =========================

# 1) Baca gambar kartu (format BGR)
img = cv2.imread("Resources/cards.jpg")

# Cek apakah gambar berhasil dibaca
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan. Cek path: Resources/cards.jpg")

# 2) Lihat ukuran gambar
# img.shape -> (height, width, channels)
# Jadi kalau print keluar (640, 960, 3):
# - tinggi = 640 (sumbu y)
# - lebar  = 960 (sumbu x)
# - channel = 3 (BGR)
print(img.shape)  # contoh: (640, 960, 3)

# Catatan koordinat OpenCV:
# - titik (x, y)
# - (0,0) di kiri atas
# - x ke kanan, y ke bawah


# =========================
# 3) Tentukan ukuran output (hasil "scan")
# =========================
# width dan height adalah ukuran hasil akhir yang kamu mau.
# Misal kartu mau jadi portrait 250x350.
width, height = 250, 350


# =========================
# 4) Tentukan 4 titik dari gambar asli (SOURCE points)
# =========================
# pts1 berisi 4 titik sudut objek (kartu) yang ingin kamu "ambil" dari gambar asli.
# Format titik: [x, y]
#
# PENTING BANGET:
# Urutan 4 titik harus sesuai dengan pts2 (destination points).
# Karena pts2 kamu urutannya:
#   [0,0]         -> Top-Left
#   [width,0]     -> Top-Right
#   [0,height]    -> Bottom-Left
#   [width,height]-> Bottom-Right
#
# Maka pts1 juga harus:
#   [Top-Left, Top-Right, Bottom-Left, Bottom-Right]
pts1 = np.float32([
    [111, 219],  # (seharusnya) Top-Left kartu di gambar asli
    [287, 188],  # (seharusnya) Top-Right
    [154, 482],  # (seharusnya) Bottom-Left
    [352, 440]   # (seharusnya) Bottom-Right
])

# =========================
# 5) Tentukan 4 titik tujuan (DESTINATION points)
# =========================
# Ini adalah "kanvas" output yang rapi (persegi panjang).
# Jadi kita memetakan sudut-sudut kartu ke:
# - kiri atas  = (0,0)
# - kanan atas = (width,0)
# - kiri bawah = (0,height)
# - kanan bawah= (width,height)
pts2 = np.float32([
    [0, 0],
    [width, 0],
    [0, height],
    [width, height]
])


# =========================
# 6) Hitung matriks transformasi perspektif
# =========================
# Fungsi ini mencari matriks 3x3 (homography) yang mengubah pts1 -> pts2.
# Anggap ini seperti "rumus" untuk meluruskan kartu yang miring.
matrix = cv2.getPerspectiveTransform(pts1, pts2)


# =========================
# 7) Terapkan transformasi ke gambar
# =========================
# warpPerspective akan menghasilkan gambar baru (output) dengan ukuran (width,height).
# Jadi bagian kartu yang kamu tentukan di pts1 akan "di-scan" menjadi kotak rapi.
imgOutput = cv2.warpPerspective(img, matrix, (width, height))


# =========================
# 8) Tampilkan hasil
# =========================
cv2.imshow("Image", img)         # gambar asli
cv2.imshow("Output", imgOutput)  # hasil warp (kartu jadi lurus)
cv2.waitKey(0)
cv2.destroyAllWindows()
