import cv2
import numpy as np

# ============================================================
# CHAPTER 7: COLOR DETECTION (HSV + TRACKBAR)
# ============================================================
# Tujuan:
# - Mendeteksi area pada gambar berdasarkan RANGE warna tertentu.
# - Kita pakai HSV karena lebih mudah memfilter warna dibanding BGR/RGB:
#   Hue  = jenis warna (merah, hijau, biru, dll)
#   Sat  = kejenuhan warna (pucat vs pekat)
#   Val  = kecerahan (gelap vs terang)
#
# Output pipeline:
# BGR image -> convert HSV -> ambil range HSV (lower, upper)
# -> mask (hitam/putih) -> hasil akhir (bitwise_and)


# ---------------------------
# Callback kosong untuk trackbar
# createTrackbar butuh fungsi callback, walau kita tidak memakainya.
# ---------------------------
def empty(a=None):
    pass


# ---------------------------
# stackImages: fungsi bantu untuk menampilkan banyak gambar dalam 1 window (grid)
# (ini dari chapter 6) -> agar Original, HSV, Mask, Result bisa terlihat sekaligus
# ---------------------------
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)

    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):

                # 1) Samakan ukuran
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y],
                        (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                        None, scale, scale
                    )

                # 2) Samakan channel (grayscale -> BGR)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)

        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])

        ver = np.vstack(hor)

    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x],
                    (imgArray[0].shape[1], imgArray[0].shape[0]),
                    None, scale, scale
                )

            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)

        ver = np.hstack(imgArray)

    return ver


# ============================================================
# 1) SETUP TRACKBAR (SLIDER) UNTUK HSV
# ============================================================

path = "Resources/lambo.png"

# Buat window khusus untuk slider HSV
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)

# Trackbar Hue range:
# Hue di OpenCV itu 0..179 (bukan 0..360), karena OpenCV mengkompres rentang hue.
cv2.createTrackbar("Hue Min", "TrackBars", 0,   179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 19,  179, empty)

# Trackbar Saturation range: 0..255
cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)

# Trackbar Value (brightness) range: 0..255
cv2.createTrackbar("Val Min", "TrackBars", 153, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)


# ============================================================
# 2) LOOP: BACA GAMBAR -> CONVERT HSV -> MASK -> RESULT
# ============================================================

while True:
    # Baca gambar setiap loop (biar update hasil realtime saat slider digeser)
    img = cv2.imread(path)

    # Validasi: pastikan file ada
    if img is None:
        raise FileNotFoundError("File tidak ditemukan. Cek path Resources/lambo.png")

    # Resize agar ukuran stabil saat ditampilkan
    img = cv2.resize(img, (600, 400))

    # Convert BGR -> HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Ambil nilai slider (range HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    # Print agar kamu tahu nilai range yang pas untuk suatu warna
    print("HSV:", h_min, h_max, s_min, s_max, v_min, v_max)

    # Buat batas bawah dan atas HSV (range warna yang mau diambil)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # ============================================================
    # MASK: cv2.inRange()
    # ============================================================
    # inRange menghasilkan gambar biner:
    # - pixel putih (255) jika HSV pixel berada di dalam range lower..upper
    # - pixel hitam (0) jika di luar range
    mask = cv2.inRange(imgHSV, lower, upper)

    # ============================================================
    # RESULT: bitwise_and
    # ============================================================
    # Mengambil pixel asli img yang mask-nya putih saja.
    # Yang mask-nya hitam akan jadi hitam di hasil.
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    # Tampilkan semua tahap dalam 1 window menggunakan stackImages:
    # [Original | HSV]
    # [Mask     | Result]
    imgStack = stackImages(0.6, ([img, imgHSV],
                                 [mask, imgResult]))
    cv2.imshow("CHAPTER 7 - Stacked Images", imgStack)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
