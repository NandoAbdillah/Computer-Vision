import cv2

# ============================================================
# CHAPTER 9: FACE DETECTION (HAAR CASCADE)
# ============================================================
# Haar Cascade = model deteksi klasik (bukan deep learning),
# cepat dan ringan, cocok untuk demo dan device terbatas.
#
# Alur:
# 1) Load classifier (file .xml)
# 2) Baca gambar
# 3) Convert ke grayscale (wajib untuk Haar Cascade)
# 4) detectMultiScale -> dapat bounding box wajah
# 5) Gambar rectangle di wajah
# ============================================================

# 1) Load model Haar Cascade dari file XML
# File ini berisi data model untuk mendeteksi wajah depan (frontal face)
faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

# Cek apakah file classifier berhasil diload
if faceCascade.empty():
    raise FileNotFoundError("Classifier XML tidak ditemukan / gagal diload. Cek path Resources/haarcascade_frontalface_default.xml")

# 2) Baca gambar
img = cv2.imread("Resources/minji.jpg")
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan. Cek path Resources/minji.jpg")

# 3) Convert BGR -> Grayscale
# Haar cascade bekerja pada grayscale karena fitur yang dipakai berbasis intensitas (bukan warna)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4) Deteksi wajah
# detectMultiScale(image, scaleFactor, minNeighbors)
#
# - scaleFactor = 1.1 artinya gambar diperkecil bertahap 10% tiap skala
#   (untuk mencari wajah yang ukuran berbeda-beda)
#
# - minNeighbors = 4 artinya "filter" keketatan deteksi:
#   nilai lebih tinggi -> lebih sedikit false positive (lebih ketat), tapi bisa miss wajah
#   nilai lebih rendah -> lebih sensitif, tapi bisa salah deteksi
faces = faceCascade.detectMultiScale(imgGray, scaleFactor=1.1, minNeighbors=4)

# faces berisi list of rectangles: (x, y, w, h)
# x,y = titik kiri atas wajah
# w,h = lebar dan tinggi kotak wajah
print("Jumlah wajah terdeteksi:", len(faces))

# 5) Gambar kotak di setiap wajah
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # warna (255,0,0) = biru (ingat OpenCV BGR)

# 6) Tampilkan hasil
cv2.imshow("CHAPTER 9 - Face Detection Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
