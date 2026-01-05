import cv2


# =========================
# CHAPTER 3: RESIZE & CROP
# =========================

# 1) Baca gambar (OpenCV membaca dalam format BGR)
img = cv2.imread("Resources/test_image.jpg")

# Validasi: kalau path salah, img akan None
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan. Cek path: Resources/test_image.jpg")

# 2) Cek ukuran gambar
# img.shape => (height, width, channels)
h, w, c = img.shape
print("Original shape (h, w, c):", img.shape)

# =========================
# A) RESIZE
# =========================
# Penting: cv2.resize(img, (width, height)) -> urutan param (w, h)
imgResizeSmall = cv2.resize(img, (300, 300))
imgResizeBig   = cv2.resize(img, (800, 800))

print("Resize 300x300 shape:", imgResizeSmall.shape)
print("Resize 800x800 shape:", imgResizeBig.shape)

# =========================
# B) CROP DASAR (SLICING)
# =========================
# Crop menggunakan slicing array:
# img[y1:y2, x1:x2]
#
# Kenapa y dulu?
# Karena array di Python/NumPy diakses dengan [row, col]
# - row  = baris = y (atas -> bawah)
# - col  = kolom = x (kiri -> kanan)

# Contoh crop: ambil area atas (0..199) dan agak kanan (200..w-1)
# Catatan: batas akhir slicing itu eksklusif (tidak ikut diambil)
imgCroppedBasic = img[0:200, 200:w]   # y:0-199, x:200-(w-1)

# =========================
# C) CROP TENGAH OTOMATIS (CENTER CROP)
# =========================
# Misal kita mau crop kotak 250x250 tepat di tengah gambar
crop_w, crop_h = 250, 250

# Titik tengah gambar
cx, cy = w // 2, h // 2

# Hitung koordinat crop (x1,x2,y1,y2)
# x = kiri/kanan, y = atas/bawah
x1 = cx - crop_w // 2
x2 = cx + crop_w // 2
y1 = cy - crop_h // 2
y2 = cy + crop_h // 2

# Biar aman, pastikan tidak keluar batas gambar (0..w dan 0..h)
x1 = max(0, x1)
y1 = max(0, y1)
x2 = min(w, x2)
y2 = min(h, y2)

# Lakukan crop tengah
imgCroppedCenter = img[y1:y2, x1:x2]

print("Center crop coords: x1,x2,y1,y2 =", x1, x2, y1, y2)
print("Center crop shape:", imgCroppedCenter.shape)

# =========================
# D) VISUALISASI AREA CROP (BIAR KELIHATAN)
# =========================
# Kita buat salinan gambar supaya original tidak berubah
imgShow = img.copy()


# =========================
# TAMPILKAN HASIL
# =========================
cv2.imshow("Original (with crop box)", imgShow)
cv2.imshow("Cropped Basic", imgCroppedBasic)
cv2.imshow("Cropped Center", imgCroppedCenter)

# Kalau mau lihat hasil resize, aktifkan:
# cv2.imshow("Resize 300x300", imgResizeSmall)
# cv2.imshow("Resize 800x800", imgResizeBig)

cv2.waitKey(0)
cv2.destroyAllWindows()
