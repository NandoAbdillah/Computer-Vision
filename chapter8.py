import cv2
import numpy as np

# ============================================================
# CHAPTER 8: CONTOUR DETECTION + SHAPE CLASSIFICATION
# ============================================================
# Tujuan:
# - Mendeteksi objek dari gambar (berdasarkan tepi / edge)
# - Menghitung kontur (garis batas objek)
# - Mengklasifikasikan bentuk (Triangle, Square, Rectangle, Circle)
# - Menggambar bounding box dan label bentuk pada objek
#
# Pipeline:
# Image -> Gray -> Blur -> Canny -> findContours -> approxPolyDP -> classify -> draw
# ============================================================


# ============================================================
# Fungsi stackImages (dari chapter 6)
# Dipakai untuk menampilkan beberapa tahap proses dalam 1 window (grid)
# ============================================================
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)

    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):

                # Samakan ukuran semua gambar
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y],
                        (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                        None, scale, scale
                    )

                # Kalau ada grayscale, convert ke BGR supaya bisa di-stack bareng gambar warna
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)

        # Gabungkan tiap baris secara horizontal
        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])

        # Gabungkan semua baris secara vertical
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
# Fungsi utama: mencari kontur dan klasifikasi bentuk
# ============================================================
def getContours(img):
    """
    img = input image yang dipakai untuk mencari kontur.
          Idealnya gambar biner/edge (hasil Canny atau threshold)
    """

    # findContours mencari garis batas objek putih pada background hitam (atau edge map)
    # cv2.RETR_EXTERNAL -> hanya mengambil kontur paling luar (tidak ambil kontur di dalam)
    # cv2.CHAIN_APPROX_NONE -> menyimpan semua titik kontur (lebih detail, lebih berat)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Loop semua kontur yang ditemukan
    for cnt in contours:
        # Hitung luas area kontur (seberapa besar objeknya)
        area = cv2.contourArea(cnt)
        print("Area:", area)

        # Gambar semua kontur (warna biru) untuk debugging
        # imgContour adalah variabel global (copy dari img original)
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)

        # Filter kontur kecil (noise)
        # Kalau area terlalu kecil biasanya cuma bintik / noise dari canny
        if area > 500:

            # Gambar kontur yang lolos filter (warna merah)
            cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 3)

            # Perimeter (keliling) kontur
            # True artinya bentuknya tertutup
            peri = cv2.arcLength(cnt, True)

            # approxPolyDP: menyederhanakan kontur menjadi titik-titik sudut penting
            # 0.02*peri adalah tingkat "ketelitian":
            # - makin kecil -> makin detail -> titik sudut bisa lebih banyak
            # - makin besar -> makin sederhana -> titik sudut bisa lebih sedikit
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # Jumlah "corner" (sudut) dari bentuk
            objCor = len(approx)
            print("Corners:", objCor)

            # boundingRect: ambil kotak pembungkus (x,y,w,h) dari bentuk approx
            # x,y = titik kiri atas kotak
            # w,h = lebar & tinggi kotak
            x, y, w, h = cv2.boundingRect(approx)

            # ============================================================
            # KLASIFIKASI BENTUK BERDASARKAN JUMLAH SUDUT
            # ============================================================
            # 3 sudut -> segitiga
            if objCor == 3:
                objectType = "Tri"

            # 4 sudut -> bisa Square atau Rectangle
            elif objCor == 4:
                aspRatio = w / float(h)  # aspect ratio = lebar / tinggi

                # kalau aspect ratio ~ 1 -> mendekati kotak (square)
                if 0.95 < aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"

            # lebih dari 4 sudut -> biasanya lingkaran atau bentuk mendekati circle
            elif objCor > 4:
                objectType = "Circle"

            else:
                objectType = "None"

            # ============================================================
            # VISUALISASI: gambar kotak & label
            # ============================================================

            # gambar bounding box hijau
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # tulis nama bentuk di tengah kotak
            # (x + w//2 - 10, y + h//2 - 10) = posisi mendekati tengah
            cv2.putText(
                imgContour,
                objectType,
                (x + (w // 2) - 10, y + (h // 2) - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0, 0, 0),
                2
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

path = "Resources/shapes.png"
img = cv2.imread(path)

if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan. Cek path: Resources/shapes.png")

# Salinan untuk menggambar kontur tanpa merusak gambar original
imgContour = img.copy()

# 1) Grayscale: biar lebih mudah diproses
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2) Blur: kurangi noise agar edge lebih bersih
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)

# 3) Canny: ubah gambar jadi edge map (hitam-putih)
imgCanny = cv2.Canny(imgBlur, 50, 50)

# Gambar kosong sebagai placeholder (opsional)
imgBlank = np.zeros_like(img)

# 4) Cari kontur dari hasil Canny (edge)
getContours(imgCanny)

# 5) Tampilkan semua tahap dalam 1 window menggunakan stack
imgStack = stackImages(0.6, ([img, imgGray, imgBlur],
                             [imgCanny, imgContour, imgBlank]))

cv2.imshow("CHAPTER 8 - Stacked Images", imgStack)
cv2.waitKey(0)
cv2.destroyAllWindows()
