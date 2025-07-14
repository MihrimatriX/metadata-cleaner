# 📄 Metadata Cleaner 🧹🔍

*Görsel, belge, ses ve video dosyalarındaki metadata’yı hızlı ve güvenli şekilde temizleyen modern Python aracı.*

---

## 📌 Genel Bakış

**Metadata Cleaner**; gizlilik, güvenlik ve veri temizliği için geliştirilmiş, çok formatlı ve paralel işlem destekli bir komut satırı ve GUI uygulamasıdır.

- **Gizliliğinizi koruyun:** Dosyalardaki gizli metadata’yı silin.
- **Toplu işlem:** Tek dosya veya klasör/alt klasör bazında toplu temizlik.
- **Seçmeli filtreleme:** JSON config ile hangi metadata alanlarının korunacağını belirleyin.
- **Modern arayüz:** PySide6 tabanlı sade ve erişilebilir GUI.
- **Hızlı:** ThreadPoolExecutor ile arayüz donmadan çoklu dosya işleme.
- **Geniş format desteği:** Görsel, belge, ses, video, arşiv ve kod dosyaları için ikon ve metadata desteği.
- **Loglama:** Konsol ve dosyaya detaylı log.

---

## 🚀 Kurulum

### pip ile (Önerilen)
```bash
pip install -r requirements.txt
```

Ardından komut satırından:
```bash
python src/cli.py --help
```

### Poetry ile (Alternatif)
```bash
git clone ...
cd metadata-cleaner
poetry install
poetry run python src/cli.py --help
```

---

## 🖥️ Kullanım Örnekleri

### Tek Dosya Temizleme
```bash
python src/cli.py --file path/to/photo.jpg
```

### Klasördeki Tüm Dosyalar
```bash
python src/cli.py --folder path/to/folder
```

### Alt Klasörlerle ve Özel Çıktı
```bash
python src/cli.py --folder path/to/folder --recursive --output sanitized_files --yes
```

### Config ile Seçmeli Temizleme
```bash
python src/cli.py --file photo.jpg --config config.json
```

---

## 🧑‍💻 API Kullanımı

### Temel Fonksiyonlar

#### `remove_metadata(file_path: str, output_path: Optional[str] = None, config_file: Optional[str] = None) -> Optional[str]`
Tek bir dosyanın metadata’sını temizler. Görsellerde config dosyası ile seçmeli filtreleme yapılabilir.

#### `remove_metadata_from_folder(folder_path: str, output_folder: Optional[str] = None, config_file: Optional[str] = None, recursive: bool = False) -> List[str]`
Bir klasördeki tüm desteklenen dosyaların metadata’sını temizler. Alt klasörler için recursive=True kullanılabilir.

**Örnek:**
```python
from remover import remove_metadata, remove_metadata_from_folder
cleaned_file = remove_metadata("photo.jpg", config_file="config.json")
cleaned_files = remove_metadata_from_folder("my_folder", recursive=True)
```

### Handler Fonksiyonları
```python
from file_handlers.image_handler import remove_image_metadata
from file_handlers.pdf_handler import remove_pdf_metadata
from file_handlers.docx_handler import remove_docx_metadata
from file_handlers.audio_handler import remove_audio_metadata
from file_handlers.video_handler import remove_video_metadata
```

---

## 📝 Özellikler ve Yol Haritası

### ✅ Tamamlananlar
- PySide6 ile modern masaüstü arayüz
- Batch/folder işleme, ThreadPoolExecutor ile paralel temizlik
- Modern format desteği (WEBP, HEIC, XLSX, PPTX, ODS, ODP, vb.)
- Detaylı loglama ve hata yönetimi

### ⏳ Planlananlar
- Web tabanlı GUI (Flask/FastAPI/Electron.js)
- Log rotasyonu ve gelişmiş hata raporlama
- Auto-update (otomatik güncelleme) özelliği
- Yeni formatlar (EPUB, gelişmiş arşiv desteği)

---

## 🪲 Loglama & Hata Yönetimi
- Loglar hem konsola hem de `logs/metadata_cleaner.log` dosyasına yazılır.
- Sık karşılaşılan hatalar:
  - **Dosya Bulunamadı:**  `File not found: <file_path>`
  - **Desteklenmeyen Dosya Türü:**  `Unsupported file type: <extension>`
  - **FFmpeg Hatası:**  Video dosyalarında hata alırsanız, `ffmpeg/ffmpeg.exe`'nin mevcut olduğundan emin olun (proje ile birlikte gelir, ek kurulum gerekmez).

---

## 📂 Proje Yapısı
```
metadata-cleaner/
├── src/
│   ├── cli.py                # CLI giriş noktası
│   ├── gui_pyside.py         # PySide6 GUI
│   ├── remover.py            # Çekirdek temizlik mantığı
│   ├── config/               # Ayarlar
│   ├── core/                 # Metadata filtreleme yardımcıları
│   ├── file_handlers/        # Dosya türü handler’ları
│   └── logs/                 # Loglama
├── ffmpeg/                   # Portable ffmpeg (Windows için)
├── requirements.txt          # Bağımlılıklar
├── README.md                 # Bu dosya
```

---

## 🏗️ Derleme & Dağıtım

### Windows (EXE)
- GUI için:
  ```
  scripts\build_gui.bat
  dist\MetadataCleanerGUI.exe
  ```
- CLI için:
  ```
  scripts\build_cli.bat
  dist\metadata-cleaner.exe
  ```

### Linux/Mac
- Bash script ile venv kurulum ve çalıştırma:
  ```
  bash scripts/build.sh
  source .venv/bin/activate
  python src/gui_pyside.py
  # veya
  python src/cli.py --help
  ```

---

## 🚀 Geliştirilebilecek Özellikler
- Karanlık/aydınlık tema desteği (GUI)
- Sürükle-bırak dosya/klasör ekleme
- İşlem geçmişi ve son temizlenenler listesi
- Çoklu dil desteği (i18n)
- Log rotasyonu ve gelişmiş hata raporlama
- Daha fazla dosya formatı (EPUB, arşiv, yeni medya türleri)
- Otomatik güncelleme (auto-update)
- Komut satırı için otomatik tamamlama
- Dosya hash kontrolü
- Web tabanlı arayüz (Flask/FastAPI/Electron.js)
- Daha fazla otomatik test ve CI/CD pipeline