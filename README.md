# IP Kamera Nesne Takibi

Bu proje, 2 farklı IP kamerasından gelen görüntülerin YOLOv8 üzerinde eğitilmiş ağırlıklar kullanılarak gerçek zamanlı olarak nesne takibini sağlar.

## Kurulum

Projenizi çalıştırmak için aşağıdaki adımları izleyin.

1. **Gerekli Kütüphanelerin Yüklenmesi:**
   ```bash
   pip install -r requirements.txt
IP kameralardan alınan görüntülerdeki canlı olarak insan yada nesne tespiti için yoloya uygun coco ağırlığını indirmek için;
YOLOv8 Ağırlıklarının İndirilmesi: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
YOLOv8 ağırlıklarını YOLOv8 GitHub sayfasından indirin ve proje dizinine yerleştirin.
<br>
Konfigürasyon Dosyasının Ayarlanması:<br>
Kamera IP'leri ve o kameraların ID ve şifrelerini camera_1, camera_2 olarak belirtilen scriptlerin içinden ayarlayabilirsiniz. 
<br><i>Not: Daha fazla kameranız varsa eğer "camera" scriptlerini kopyalayıp çoğaltabilirsiniz bu işemi yaptıntan sonra oluiturduğunuz yeni scriptleri çağırmayı unutmayın</i>
 


bash
Copy code
python main.py
Ekran Görüntüleri
github_1
![github_1](https://github.com/necipsahamettinkucuk/IP-kameradan-nesne-takibi/assets/121046682/0d378322-cd56-44e9-bd61-f1a3ae5b837d)
