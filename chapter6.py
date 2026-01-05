import cv2
import numpy as np

# ============================================================
# CHAPTER 6: STACK IMAGES (MENYUSUN BANYAK GAMBAR DALAM 1 WINDOW)
# ============================================================
# Tujuan:
# - Biar kita bisa melihat beberapa hasil proses OpenCV sekaligus (grid)
# - Contoh: Original | Gray | Blur / Canny | Dilate | Erode
#
# Problem:
# - np.hstack / np.vstack butuh gambar dengan ukuran (height,width) sama
# - dan jumlah channel sama (BGR=3). Kalau ada grayscale (1 channel) -> harus diubah ke BGR
#
# Solusi:
# - Resize semua gambar ke ukuran patokan
# - Convert grayscale -> BGR
# - Lalu stack horizontal dan vertical


def stackImages(scale, imgArray):
    """
    scale    : skala ukuran gambar (misal 0.5 = 50% dari ukuran patokan)
    imgArray : bisa 2 bentuk:
               - 1D: [img1, img2, img3]            -> hasil 1 baris
               - 2D: [[img1, img2], [img3, img4]]  -> hasil grid
    return   : 1 gambar besar hasil gabungan
    """

    rows = len(imgArray)                  # jumlah baris
    rowsAvailable = isinstance(imgArray[0], list)  # True jika 2D list

    # Kalau 2D list, jumlah kolom diambil dari baris pertama
    cols = len(imgArray[0]) if rowsAvailable else len(imgArray)

    # Ambil ukuran patokan dari gambar pertama (paling kiri atas)
    # shape[:2] -> (height, width)
    if rowsAvailable:
        height, width = imgArray[0][0].shape[:2]
    else:
        height, width = imgArray[0].shape[:2]

    # =========================
    # KASUS A: GRID (2D LIST)
    # =========================
    if rowsAvailable:
        for r in range(rows):
            for c in range(cols):
                # 1) Samakan ukuran dulu
                if imgArray[r][c].shape[:2] == (height, width):
                    # kalau sama, cukup scale
                    imgArray[r][c] = cv2.resize(imgArray[r][c], (0, 0), None, scale, scale)
                else:
                    # kalau beda, resize ke patokan dulu, lalu scale
                    imgArray[r][c] = cv2.resize(imgArray[r][c], (width, height), None, scale, scale)

                # 2) Samakan channel
                # grayscale punya shape (h,w) -> len(shape)==2
                # convert agar jadi BGR (h,w,3), supaya bisa di-stack bareng gambar warna
                if len(imgArray[r][c].shape) == 2:
                    imgArray[r][c] = cv2.cvtColor(imgArray[r][c], cv2.COLOR_GRAY2BGR)

        # Gabungkan tiap baris secara horizontal
        hor_list = []
        for r in range(rows):
            hor_list.append(np.hstack(imgArray[r]))

        # Gabungkan semua baris secara vertical -> jadi grid utuh
        ver = np.vstack(hor_list)
        return ver

    # =========================
    # KASUS B: 1 BARIS (1D LIST)
    # =========================
    else:
        for i in range(rows):
            # 1) Samakan ukuran
            if imgArray[i].shape[:2] == (height, width):
                imgArray[i] = cv2.resize(imgArray[i], (0, 0), None, scale, scale)
            else:
                imgArray[i] = cv2.resize(imgArray[i], (width, height), None, scale, scale)

            # 2) Samakan channel
            if len(imgArray[i].shape) == 2:
                imgArray[i] = cv2.cvtColor(imgArray[i], cv2.COLOR_GRAY2BGR)

        # Gabungkan semua gambar jadi 1 baris
        return np.hstack(imgArray)


# =========================
# CONTOH PEMAKAIAN
# =========================
img = cv2.imread("Resources/minji.jpg")
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan. Cek path: Resources/minji.jpg")

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Buat grid 2 baris x 3 kolom
# Baris 1: Original | Gray | Original
# Baris 2: Original | Original | Original
imgStack = stackImages(0.5, [
    [img, imgGray, img],
    [img, img,     img]
])

cv2.imshow("CHAPTER 6 - ImageStack", imgStack)
cv2.waitKey(0)
cv2.destroyAllWindows()