# Kamerea konfigürason, kamera işlemleri

import cv2


class Cam:

    def __init__(self):

        self.rtsp_url = "rtsp://admin:Grundig1234@191.0.51.203:554/Streaming/Channels/2"
        # Kameranın RTSP URL'si
        # self.username = "admin"  # Kullanıcı adı
        # self.password = "Grunding1234"  # Şifre

    def read_with_ai(self, ai):

        # RTSP akışını almak için VideoCapture nesnesi oluşturun
        video_capture = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)

        # Tampon boyutunu 1 olarak ayarlayın
        video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 0)

        if not video_capture.isOpened():
            print("açılmadı.")
            exit()

        while True:
            ret, frame = video_capture.read()

            # ai frame'i gönder
            ai.model_tespit(frame)

            if not ret:
                print("Akış sonlandı.")
                break

            # Alınan çerçeveyi işleyin veya gösterin
            cv2.imshow('IP KAMERA', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Temizleme
        video_capture.release()
        cv2.destroyAllWindows()
