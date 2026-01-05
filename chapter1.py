import cv2
print("Packages Imported")  # Sekadar indikator kalau OpenCV berhasil di-import

# =========================
# 1) MENAMPILKAN GAMBAR
# =========================

# cv2.imread() membaca file gambar dari path.
# Hasilnya adalah "image matrix" (array) format BGR (bukan RGB).
img = cv2.imread("Resources/minji.jpg")

# cv2.imshow(judul_window, gambar) menampilkan gambar ke window desktop
cv2.imshow("Output", img)

# cv2.waitKey(0) artinya:
# - program "nahan" di sini sampai kamu pencet tombol apa pun
# - kalau tidak ada waitKey, window bisa langsung menutup
cv2.waitKey(0)


# =========================
# 2) MENAMPILKAN VIDEO FILE
# =========================

# cv2.VideoCapture() membuka sumber video:
# - bisa path file video (mp4, avi, dll)
# - atau angka 0/1/... untuk webcam
cap = cv2.VideoCapture("Resources/test_video.mp4")

while True:
    # cap.read() mengembalikan:
    # success = True kalau frame berhasil dibaca
    # img = frame yang terbaca (gambar per frame)
    success, img = cap.read()

    # Penting:
    # kalau video sudah habis, success akan False dan img akan None
    # jadi sebaiknya kita break agar tidak error di imshow()
    if not success:
        break

    cv2.imshow("Video", img)

    # cv2.waitKey(1) menunggu 1 ms dan juga "membaca" input keyboard.
    # & 0xFF ini trik umum agar kompatibel di beberapa OS.
    # ord('q') adalah kode ASCII untuk huruf 'q'.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ini penting: release resource video setelah selesai
cap.release()
cv2.destroyAllWindows()


# =========================
# 3) MENAMPILKAN WEBCAM
# =========================

# 0 biasanya webcam utama (default)
cam = cv2.VideoCapture(0)

# cam.set(property_id, value)
# 3 = width (lebar)
# 4 = height (tinggi)
# 10 = brightness (kecerahan) -> efeknya bisa beda tiap webcam/driver
cam.set(3, 640)
cam.set(4, 480)
cam.set(10, 100)

while True:
    success, img = cam.read()

    # Jika webcam gagal ambil frame, stop loop
    if not success:
        break

    cv2.imshow("Webcam", img)  # aku ganti judul biar jelas window-nya

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
