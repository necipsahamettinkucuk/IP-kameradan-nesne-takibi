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
<br>İndirdiğiniz <b>yolov8s.pt</b> ağırlığınının dosya yolunu ai'nesnesinin içine kopyalayın.
![image](https://github.com/necipsahamettinkucuk/IP-kameradan-nesne-takibi/assets/121046682/b9f6713f-9c42-40d3-94a1-2cae6c0190e6)

<br> Veri tabanı maksimum <b>5 satır</b> olacak ekilde yazılmıştır. Gerek duyulduğunda duruma göre attırabilirsiniz.

  
<br>
Konfigürasyon Dosyasının Ayarlanması:<br>
Kamera IP'leri ve o kameraların ID ve şifrelerini camera_1, camera_2 olarak belirtilen scriptlerin içinden ayarlayabilirsiniz. 
<br> Bağlanacağınız kameranın id ve şifresini belirtilen bölüme yazınız.
![image](https://github.com/necipsahamettinkucuk/IP-kameradan-nesne-takibi/assets/121046682/d291d2a3-9fd1-4f98-870e-3c4ff2f65b79)

<br><i>Not: Daha fazla kameranız varsa eğer "camera" scriptlerini kopyalayıp çoğaltabilirsiniz bu işemi yaptıntan sonra oluşturduğunuz yeni scriptleri main'den çağırmayı unutmayın çağırmayı unutmayın</i>
 
https://github.com/necipsahamettinkucuk/IP-kameradan-nesne-takibi/assets/121046682/37055a47-9453-48bc-ae66-f45f708f74d1

