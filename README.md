# IP Kamera Nesne Takibi

Bu proje, 2 farklı IP kamerasından gelen görüntülerin YOLOv8 üzerinde eğitilmiş ağırlıklar kullanılarak gerçek zamanlı olarak nesne takibini sağlar.

## Kurulum

Projenizi çalıştırmak için aşağıdaki adımları izleyin.

1. **Gerekli Kütüphanelerin Yüklenmesi:**
   ```bash
   pip install -r requirements.txt
YOLOv8 Ağırlıklarının İndirilmesi: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
YOLOv8 ağırlıklarını YOLOv8 GitHub sayfasından indirin ve proje dizinine yerleştirin.

Konfigürasyon Dosyasının Ayarlanması:
config.yaml dosyasını düzenleyerek IP kameralarınızın adreslerini ve diğer ayarları yapın.

Kullanım
Projenizi başlatmak için terminalde aşağıdaki komutu kullanın:

bash
Copy code
python main.py
Ekran Görüntüleri
github_1
Kamera 1 Görüntüsü

Kamera 2 Görüntüsü
Kamera 2 Görüntüsü
