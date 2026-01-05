import cv2
import numpy as np

# =========================
# CHAPTER 4: DRAWING SHAPES & TEXT
# =========================

# (Opsional) Kalau bikin 2D saja (1 channel), ini jadi "grayscale image"
# img = np.ones((512, 512))  # default float64, bukan ideal untuk OpenCV

# 1) Membuat "kanvas" kosong ukuran 512x512 dengan 3 channel (BGR)
# np.zeros(...) berarti semua pixel = 0 (hitam)
# np.uint8 artinya nilai pixel 0..255 (format standar image)
img = np.zeros((512, 512, 3), np.uint8)

# Catatan:
# img.shape = (height, width, channels)
# jadi img.shape[0] = height, img.shape[1] = width


# =========================
# 2) Mengubah warna pixel manual (ARRAY SLICING)
# =========================
# img[200:300, 100:300] = 255, 0, 0
# artinya: warnai blok pixel:
# - y dari 200..299 (baris)
# - x dari 100..299 (kolom)
# jadi kotak kecil di area itu menjadi warna (B=255, G=0, R=0) = biru
#
# img[:] = 255, 0, 0
# artinya: warnai SELURUH gambar jadi biru
#
# (Ini dikomentari di kode kamu, tapi konsepnya penting)


# =========================
# 3) GAMBAR GARIS (LINE)
# =========================
# cv2.line(image, start_point, end_point, color(BGR), thickness)
#
# Start point (0,0) = pojok kiri atas
# End point (img.shape[1], img.shape[0]) = (width, height)
# Ini bikin garis diagonal dari kiri atas menuju kanan bawah.
cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
# warna (0,255,0) = hijau, ketebalan 3 pixel


# =========================
# 4) GAMBAR KOTAK (RECTANGLE)
# =========================
# cv2.rectangle(image, top_left, bottom_right, color(BGR), thickness)
#
# thickness:
# - angka (misal 2) = garis tepi setebal 2 pixel
# - cv2.FILLED = kotak diisi penuh (solid)
#
# Kotak merah filled dari (0,0) ke (250,350)
cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), cv2.FILLED)
# warna (0,0,255) = merah

# Kotak biru hanya border (tidak filled)
# dari (0,350) ke (250,450), thickness 2
cv2.rectangle(img, (0, 350), (250, 450), (255, 0, 0), 2)
# warna (255,0,0) = biru


# =========================
# 5) GAMBAR LINGKARAN (CIRCLE)
# =========================
# cv2.circle(image, center, radius, color(BGR), thickness)
#
# Lingkaran di center (400,50), radius 30
# thickness 5 -> hanya border tebal 5 pixel
cv2.circle(img, (400, 50), 30, (255, 255, 0), 5)
# warna (255,255,0) = cyan/kuning kehijauan (B=255, G=255, R=0)


# =========================
# 6) TULIS TEKS (PUTTEXT)
# =========================
# cv2.putText(image, text, org, font, fontScale, color, thickness)
#
# org = posisi titik awal teks (x,y) - biasanya kiri bawah dari teks
# fontScale = ukuran teks
cv2.putText(
    img,
    "OPENCV",
    (300, 100),                 # posisi teks
    cv2.FONT_HERSHEY_COMPLEX,    # jenis font bawaan OpenCV
    1,                           # skala ukuran font
    (0, 150, 0),                 # warna teks (hijau gelap)
    1                            # ketebalan teks
)

# =========================
# 7) TAMPILKAN HASIL
# =========================
cv2.imshow("Image", img)
cv2.waitKey(0)  # tahan sampai ada tombol ditekan
cv2.destroyAllWindows()
