# polygon falan ai da dursun

import ultralytics
import cv2
import supervision as sv
import numpy as np
import requests
from id_list import unique_ids

class Model:
    def __init__(self, path):

        self.model_1 = self.model_yukle(path)
        # initiate polygon zone
        self.polygon_1 = np.array(
            [
                [250, 220],  # [250, 300]
                [450, 220],  # [450, 300]
                [450, 400],  # [450, 450]
                [250, 400],  # [250, 450]
            ]
        )
        self.kontrol_1 = True
        self.ct_1 = 0
        self.kontrol_2 = True
        self.ct_2 = 0
        self.Bas_Mak = 0
        self.kontrol_3 = True
        self.model_2 = self.model_yukle(path)
        self.polygon_2 = np.array(
            [
                [296, 30],  # [297, 2]
                [367, 30],  # [381, 2]
                [410, 216],  # [381, 50]
                [250, 216],  # [297, 50]
            ]
        )

    def model_yukle(self, path):
        return ultralytics.YOLO(path)

    def get(self):
        return self.kontrol_1

    def model_tespit(self, frame):

        zone_1 = sv.PolygonZone(polygon=self.polygon_1, frame_resolution_wh=(640, 480))
        zone_2 = sv.PolygonZone(polygon=self.polygon_2, frame_resolution_wh=(640, 480))

        # 1. dikdörtgen
        box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=2, text_scale=2)
        zone_annotator_1 = sv.PolygonZoneAnnotator(
            zone=zone_1,
            color=sv.Color.white(),
            thickness=2,
            text_thickness=2,
            text_scale=1,
        )
        zone_annotator_2 = sv.PolygonZoneAnnotator(
            zone=zone_2,
            color=sv.Color.white(),
            thickness=1,
            text_thickness=1,
            text_scale=0,
        )
        # detect
        results_1 = self.model_1(frame, imgsz=640)[0]
        detections_1 = sv.Detections.from_ultralytics(results_1)
        alandakiler_1 = zone_1.trigger(detections=detections_1)
        sayi_1 = len(alandakiler_1[alandakiler_1 == True])

        results_2 = self.model_2(frame, imgsz=640)[0]
        detections_2 = sv.Detections.from_ultralytics(results_2)
        alandakiler_2 = zone_2.trigger(detections=detections_2)
        sayi_2 = len(alandakiler_2[alandakiler_2 == True])

        if sayi_1 == 1 and self.kontrol_1 == True:  # Makine polygona girdi
            requests.post("http://127.0.0.1:5000/add_machine")
            self.ct_1 += 1
            self.kontrol_1 = False

        elif (
                sayi_1 == 0 and self.kontrol_1 == False
        ):  # Makine 1. polygondan çıktı --> Makine 2. polygona girdi
            self.kontrol_1 = True

            payload = {"id": unique_ids[self.ct_1-1], "assembly_num": 2}
            requests.post(
                "http://127.0.0.1:5000/update_assembly", json=payload
            )  # Assembly2'yi güncelle
        else:
            pass
        # annotate

        # Kamera 1 çıkış

        # annotate
        # confidence doğruluk oranı demek makinalerın bir doğruluk değerleri vardır bu
        # değer eşik değeridir.
        box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=1)
        labels_1 = [
            f"{self.model_1.names[class_id]} {confidence:0.85f} "
            for _, _, confidence, class_id, _ in detections_1
        ]
        labels_2 = [
            f"{self.model_2.names[class_id]} {confidence:0.75f} "
            for _, _, confidence, class_id, _ in detections_2
        ]

        frame_1 = box_annotator.annotate(
            scene=frame,
            detections=detections_1[alandakiler_1],
            labels=labels_1,
            skip_label=None,
        )
        frame_2 = box_annotator.annotate(
            scene=frame,
            detections=detections_2[alandakiler_2],
            labels=labels_2,
            skip_label=None,
        )

        frame_1 = zone_annotator_1.annotate(
            scene=frame_1
        )
        frame_2 = zone_annotator_2.annotate(
            scene=frame_2
        )

        # üst köşelerdeki sayıları yazdırma
        cv2.putText(
            frame_1, str(sayi_1), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )
        cv2.putText(
            frame_2, str(sayi_2), (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )

        # %matplotlib inline
        # sv.plot_image(frame, (16, 16))

        if self.kontrol_2 == True:  # Makine polygona girdi
            self.Bas_Mak = sayi_2
            self.kontrol_2 = False
        elif (
                self.Bas_Mak < self.ct_1 and self.kontrol_2 == False and self.kontrol_1 == True
        ):  # Makine polygondan çıktı
            self.ct_2 = self.ct_1 - self.Bas_Mak
            payload = {"id": unique_ids[self.ct_2-1], "assembly_num": 3}
            requests.post(
                "http://127.0.0.1:5000/update_assembly", json=payload
            )  # Assembly3'yi güncelle
        else:
            pass
