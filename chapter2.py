import cv2
import numpy as np

# =========================
# CHAPTER 2: Morfologi Dasar (Dilate & Erode)
# =========================

# 1) Baca gambar dari file (format default OpenCV = BGR)
img = cv2.imread("Resources/minji.jpg")

# 2) Kernel (structuring element) untuk operasi morfologi (dilate/erode).
# np.ones((5,5)) membuat matriks 5x5 berisi 1.
# np.uint8 artinya tipe datanya 0-255 (cocok untuk image processing).
kernel = np.ones((5, 5), np.uint8)

# 3) Grayscale: mengubah gambar warna (BGR) menjadi 1 channel (abu-abu).
# Kenapa? Banyak algoritma lebih mudah/cepat diolah jika 1 channel.
# Ini juga mengurangi kompleksitas (dari 3 channel jadi 1).
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4) Blur (Gaussian): "melembutkan" gambar untuk mengurangi noise.
# (15,15) = ukuran kernel blur (semakin besar, semakin blur).
# 0 = sigma otomatis dihitung.
# Kenapa penting? Noise kecil bisa bikin deteksi tepi (edge) jadi berantakan.
imgBlur = cv2.GaussianBlur(imgGray, (15, 15), 0)

# 5) Canny Edge Detection: mencari tepi (edge) pada gambar.
# Outputnya bukan gambar normal, tapi gambar biner: tepi berwarna putih, sisanya hitam.
# 150 dan 200 itu threshold (semakin tinggi -> tepi yang terdeteksi makin "ketat"/sedikit).
# Biasanya canny dilakukan pada gambar yang sudah di-blur agar edge lebih bersih.
imgCanny = cv2.Canny(imgBlur, 150, 200)

# 6) Dilation: "menebalkan" garis/edge putih.
# Cocok kalau hasil Canny garisnya putus-putus atau tipis.
# iterations=1 artinya proses dilakukan 1 kali (bisa ditambah kalau mau makin tebal).
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)

# 7) Erosion: kebalikan dilate -> "menipiskan/mengikis" bagian putih.
# Biasanya dipakai untuk:
# - mengurangi noise putih kecil
# - mengembalikan ketebalan setelah dilate (dilate lalu erode = closing) untuk menutup celah kecil
imgEroded = cv2.erode(imgDilation, kernel, iterations=1)


cv2.imshow("Original", img)
# cv2.imshow("Gray Image", imgGray)
# cv2.imshow("Blur Image", imgBlur)
# cv2.imshow("Canny Image", imgCanny)
# cv2.imshow("Dilation Image", imgDilation)

# Yang ditampilkan sekarang:
cv2.imshow("Eroded Image", imgEroded)
cv2.waitKey(0)
