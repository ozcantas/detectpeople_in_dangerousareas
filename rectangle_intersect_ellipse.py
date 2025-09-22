import cv2
import numpy as np

def rectangle_intersect_ellipse(ellipse_center, ellipse_axes, angle, rect_center, rect_width, rect_height, frame_width, frame_height):
    # Elips parametreleri
    ellipse_center = tuple(ellipse_center)
    ellipse_axes = tuple(ellipse_axes)
    
    # Dikdörtgen parametreleri
    rect_center = tuple(rect_center)

    # Görüntü boyutlarını kullanarak boş bir resim oluştur
    img = np.zeros((frame_height, frame_width), dtype=np.uint8)
    
    # Elipsin maskesini oluştur
    cv2.ellipse(img, ellipse_center, ellipse_axes, angle, 0, 360, 255, -1)
    ellipse_mask = img.copy()
   
    # Boş bir resim ile dikdörtgenin maskesini oluştur
    img.fill(0)
    cv2.rectangle(img, 
                  (int(rect_center[0] - rect_width / 2), int(rect_center[1] - rect_height / 2)),
                  (int(rect_center[0] + rect_width / 2), int(rect_center[1] + rect_height / 2)),
                  255, -1)
    rect_mask = img.copy()
   
    # Maskelerin çarpımını al
    intersection_mask = cv2.bitwise_and(ellipse_mask, rect_mask)
    
    # Kesişen piksellerin toplamını hesapla
    intersection = np.sum(intersection_mask)

    # Eğer kesişim varsa toplam > 0 olur
    
    return intersection > 0


if __name__ == "__main__":
    print(rectangle_intersect_ellipse((100,100),(100,100),100,(150,125),200,100, 640,480))