# Computer Vision with Python OpenCV  

<p>
  <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGVtMTJ1bWJpanVxcGE3NXJkeTRjbGxqdm8yeGFtaHN6am05MGlvdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FcqKy4Kj7XOK0hCW4g/giphy.gif" width="500" alt="Webcam Capture">
</p>

Repositori ini berisi rangkuman belajar **OpenCV (Python)** dari Chapter 1–9, dengan fokus pada pemahaman konsep dan alur kerja Computer Vision yang sering dipakai di robotik (deteksi warna, kontur, perspektif, face detection, dan debugging visual).

> Format folder `Resources/` berisi resource untuk Repositori ini

---

## ✅ Tech Stack

* **Python 3.x**
* **OpenCV** (`opencv-python`)
* **NumPy**


---

## ⚙️ Instalasi & Setup Cepat

### 1) Buat Virtual Environment 

**Windows**

```bash
py -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install --upgrade pip
pip install opencv-python numpy
```

### 3) Test OpenCV

```bash
python -c "import cv2; print(cv2.__version__)"
```

---

# 🧠 Ringkasan Materi per Chapter

## CHAPTER 1 — Read Image / Video / Webcam

**Tujuan:** memahami input visual (gambar, video file, webcam).

**Konsep kunci:**

* `cv2.imread(path)` baca gambar (format **BGR**)
* `cv2.imshow(name, img)` tampilkan image
* `cv2.waitKey(ms)` baca keyboard + menahan window
* `cv2.VideoCapture(source)` sumber video (file / webcam: 0)
* `cap.read()` ambil frame: `(success, frame)`
* `cap.release()` + `cv2.destroyAllWindows()` tutup resource rapi

**Catatan:** video/webcam wajib pakai loop dan cek `success`.

---

## CHAPTER 2 — Basic Image Processing (Gray, Blur, Canny, Morphology)

**Tujuan:** preprocessing agar hasil edge/mask lebih bersih.

**Pipeline umum (recommended):**

1. `cvtColor` → grayscale
2. `GaussianBlur` → kurangi noise
3. `Canny` → edge detection
4. `dilate` → menebalkan edge
5. `erode` → merapikan/mengikis noise

**Konsep morphology:**

* `dilate` = memperbesar area putih (menyambungkan garis)
* `erode` = mengikis area putih (rapikan noise)
* `dilate → erode` = **closing** (menutup celah kecil)

---

## CHAPTER 3 — Resize & Crop (ROI)

**Tujuan:** pahami image sebagai array dan konsep ROI.

**Konsep kunci:**

* `img.shape = (height, width, channels)`
* `cv2.resize(img, (width, height))` **(ingat urutan w,h)**
* Crop pakai slicing: `img[y1:y2, x1:x2]`

  * y = baris (atas→bawah)
  * x = kolom (kiri→kanan)

**Kenapa penting di robotik:** ROI mempercepat proses dan fokus pada area relevan (misal line following bagian bawah frame).

---

## CHAPTER 4 — Drawing (Line, Rectangle, Circle, Text)

**Tujuan:** overlay visual untuk debugging dan output.

**Konsep kunci:**

* Kanvas: `np.zeros((h,w,3), np.uint8)`
* `cv2.line`, `cv2.rectangle`, `cv2.circle`, `cv2.putText`
* Warna OpenCV = **BGR** (bukan RGB)

**Use case robotik:** bounding box, centroid target, arah vektor, teks FPS/mode.

---

## CHAPTER 5 — Perspective Transform (Warp / Scan Effect)

**Tujuan:** meluruskan objek miring (scan effect).

**Konsep kunci:**

* `pts1` = 4 titik sudut objek di gambar asli
* `pts2` = 4 titik tujuan output (`width x height`)
* `getPerspectiveTransform(pts1, pts2)` → matrix
* `warpPerspective(img, matrix, (width, height))` → hasil

**Kesalahan paling sering:** urutan titik salah. Pastikan urutan `pts1` sama dengan `pts2`:

* Top-Left, Top-Right, Bottom-Left, Bottom-Right

---

## CHAPTER 6 — Stack Images (Grid Debugging)

**Tujuan:** tampilkan banyak image dalam 1 window.

**Masalah:** `np.hstack/vstack` butuh ukuran & channel yang sama.

**Solusi `stackImages()`:**

* resize semua image ke ukuran patokan
* convert grayscale → BGR
* hstack per baris → vstack semua baris

**Kegunaan:** melihat `Original | Gray | Blur` dan `Canny | Dilate | Erode` sekaligus.

---

## CHAPTER 7 — Color Detection (HSV + Trackbar)

**Tujuan:** cari range warna terbaik secara interaktif (untuk deteksi bola/garis/target).

**Pipeline:**

1. BGR → HSV (`cvtColor`)
2. Ambil slider HSV (`getTrackbarPos`)
3. Mask: `cv2.inRange(hsv, lower, upper)`
4. Result: `cv2.bitwise_and(img, img, mask=mask)`

**Kenapa HSV:** lebih stabil terhadap perubahan cahaya dibanding BGR.

---

## CHAPTER 8 — Contours + Shape Detection

**Tujuan:** deteksi objek dan klasifikasi bentuk.

**Pipeline:**

1. Gray → Blur → Canny
2. `findContours` cari kontur
3. Filter noise: `contourArea`
4. Sederhanakan kontur: `approxPolyDP`
5. Klasifikasi bentuk (jumlah sudut):

   * 3 = Triangle
   * 4 = Square/Rectangle (cek aspect ratio)
   * > 4 = Circle (perkiraan)
6. Visualisasi: bounding box + label

---

## CHAPTER 9 — Face Detection (Haar Cascade)

**Tujuan:** deteksi wajah cepat dan ringan memakai file XML.

**Pipeline:**

1. Load model: `CascadeClassifier(xml)`
2. Grayscale
3. `detectMultiScale(gray, scaleFactor, minNeighbors)`
4. Gambar rectangle hasil deteksi

**Parameter penting:**

* `scaleFactor` lebih kecil → lebih teliti tapi lebih berat
* `minNeighbors` lebih besar → lebih ketat (lebih sedikit false positive)

---

# 🧪 Tips Debugging Cepat

* Path salah → `img is None` (selalu cek)
* Video habis → `success == False` (break)
* Warna OpenCV = BGR
* Draw pakai `(x,y)`, tapi crop pakai `[y, x]`

---

