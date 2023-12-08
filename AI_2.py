# polygon falan ai da dursun
import requests
import ultralytics
import cv2
import supervision as sv
import numpy as np
from id_list import unique_ids

class Model:

    # import torch
    # # Rastgele bir tensör oluştur
    # x = torch.rand(5, 3)
    # # Bir model oluştur
    # model = torch.nn.Linear(3, 2)
    # if torch.cuda.is_available():
    #     device = torch.device("cuda")  # GPU cihazını belirle
    #     model = model.to(device)  # Modeli GPU'ya taşı
    #     print("Tensör ve model GPU'da")
    # else:
    #     print("Tensör ve model CPU'da")
    # # Modeli tensör üzerinde çalıştır
    # y = model(x)
    # # GPU işlemlerinin tamamlanmasını bekleyin
    # torch.cuda.synchronize()

    def __init__(self, path):

        self.model = self.model_yukle(path)
        # initiate polygon zone
        self.polygon = np.array([
            [180, 300],
            [380, 300],
            [410, 479],
            [155, 479]
        ])  # 30
        self.a = True
        self.ct =1
        self.assembly_status = False
    def model_yukle(self, path):

        return ultralytics.YOLO(path)

    def model_al(self):

        return self.model

    def model_tespit(self, frame):

        zone = sv.PolygonZone(polygon=self.polygon, frame_resolution_wh=(640, 480))

        # initiate annotators
        box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=2, text_scale=2)
        zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.white(), thickness=2, text_thickness=2,
                                                 text_scale=1)

        # detect
        results = self.model(frame, imgsz=640)[0]
        detections = sv.Detections.from_ultralytics(results)
        alandakiler = zone.trigger(detections=detections)
        sayi = len(alandakiler[alandakiler == True])

        payload = {'id': unique_ids[0], 'assembly_num': 1}
        response = requests.get('http://127.0.0.1:5000/assembly_control', json=payload)
        assembly_num = payload['assembly_num']
        assembly_status_1 = response.json()[f'assembly{assembly_num}_status']

        if assembly_status_1 == True:

            payload = {'id': unique_ids[self.ct-1], 'assembly_num': 3}
            response = requests.get('http://127.0.0.1:5000/assembly_control', json=payload)
            assembly_num = payload['assembly_num']
            self.assembly_status = response.json()[f'assembly{assembly_num}_status']

            if sayi == 1 and self.assembly_status == True and self.a == True :
                payload = {"id": unique_ids[self.ct-1], "assembly_num": 3}
                requests.post(
                    "http://127.0.0.1:5000/update_assembly", json=payload
                )  # Assembly2'yi güncelle
                self.ct +=1
                self.a= False
            elif sayi == 0 and self.a == False:
                self.a = True
                self.ct -=1
                payload = {"id": unique_ids[self.ct-1], "assembly_num": 4}
                requests.post(
                    "http://127.0.0.1:5000/update_assembly", json=payload
                )  # Assembly4'ü güncelle
                self.ct += 1
            else:
                pass

        box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=1)
        labels = [f"{self.model.names[class_id]} {confidence:0.85f} " for _, _, confidence, class_id, _ in detections]

        frame = box_annotator.annotate(scene=frame, detections=detections[alandakiler], labels=labels, skip_label=None)
        frame = zone_annotator.annotate(scene=frame)  # Sadece bu kısmı yorum satına alarakta yapabiliriz

        # sayısını yazdırma
        cv2.putText(frame, str(self.ct), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

