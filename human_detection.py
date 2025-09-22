import cv2
import numpy as np
from ultralytics import YOLO
from dangerous_area_detection import InteractiveEllipse
from rectangle_intersect_ellipse import rectangle_intersect_ellipse

# Elips etkileşimini başlat
ellipse_app = InteractiveEllipse(0)  # 0: Web kamerası
r1, r2, angle, cx, cy = ellipse_app.run()

# Video kaynağını başlat
model = YOLO('yolov8n.pt')
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Video kaynağı açılamadı!")
    exit()


frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = camera.read()
    if not ret:
        print("Görüntü alınamadı, video sona ermiş olabilir.")
        break
    frame_height, frame_width, _ = frame.shape
    # Model tahmini
    results = model(frame, verbose=False)

    cv2.ellipse(frame, (cx, cy), (r1, r2), angle, 0, 360, (0, 255, 255), 2)
    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            coords = box.xyxy[0].tolist()  # Koordinatlar
            x1, y1, x2, y2 =map(int, coords)
            confidence = float(box.conf[0])  # Güven skoru
            cls = int(box.cls[0])  # Sınıf ID
            cls_name = model.names[cls]  # Sınıf adı
            

            if cls_name == 'person':
                # Kişinin merkezini hesapla
                person_center_x = (x1 + x2) // 2
                person_center_y = (y1 + y2) // 2
                width=x2-x1
                height=y2-y1
                # Çerçeve çiz ve etiket ekle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{cls_name} {confidence:.2f}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
              
                rectangle_params = [person_center_x, person_center_y, x2 - x1, y2 - y1]
                
                
                if rectangle_intersect_ellipse((cx,cy),(r1,r2),angle,(person_center_x, person_center_y),width,height,frame_width,frame_height):
                    cv2.putText(frame, "ALERT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    # Sonuçları görüntüle
    cv2.imshow("Tehlikeli Alan İzleme", frame)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
camera.release()
cv2.destroyAllWindows()
