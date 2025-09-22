import cv2

# Interaktive Ellipse Klasse
class InteractiveEllipse:
    def __init__(self, video_source="video.mp4"):
        self.video_source = video_source
        self.r1, self.r2, self.r3 = 100, 50, 0  # Ellipsen Parameter (r1: Horizontale Radius, r2: Vertikale Radius, r3: Neigungswinkel)
        self.cx, self.cy = 300, 300  # Zentrum der Ellipse
        self.dragging_variable = None  # Verfolgt, welche Variable gezogen wird
        self.is_fixed = False  # Sind die Ellipsen Parameter fixiert?
        self.cap = cv2.VideoCapture(self.video_source)

        # Wenn das Video nicht geöffnet werden kann
        if not self.cap.isOpened():
            print("Video konnte nicht geöffnet werden!")
            exit()

    # Ellipse auf das Bild zeichnen
    def draw_ellipse(self, image):
        height, width, _ = image.shape  # Bildgröße abfragen
        # Skaliere die Radien basierend auf der Bildgröße
        scaled_r1 = int(self.r1 * width / 640)  # 640 ist die ursprüngliche Breite des Videos
        scaled_r2 = int(self.r2 * height / 480)  # 480 ist die ursprüngliche Höhe des Videos
        axes = (scaled_r1, scaled_r2)  # Achsen (Radien)
        angle = self.r3  # Neigungswinkel der Ellipse
        # Zeichne die Ellipse auf das Bild
        cv2.ellipse(image, (self.cx, self.cy), axes, angle, 0, 360, (0, 255, 0), 2)

    # Mausereignisbehandlung
    def on_mouse(self, event, x, y, flags, param):
        if not self.is_fixed:
            if event == cv2.EVENT_LBUTTONDOWN:
                # Wenn der Mauszeiger auf den Parameter klickt, den Parameter ändern
                if 50 < x < 150 and 30 < y < 50:
                    self.dragging_variable = "r1"  # r1 ändern
                elif 50 < x < 150 and 70 < y < 90:
                    self.dragging_variable = "r2"  # r2 ändern
                elif 50 < x < 150 and 110 < y < 130:
                    self.dragging_variable = "r3"  # r3 ändern
                elif self.cx - 50 < x < self.cx + 50 and self.cy - 50 < y < self.cy + 50:
                    self.dragging_variable = "center"  # Zentrum der Ellipse ändern

            # Wenn die Mausbewegung erkannt wird, den entsprechenden Parameter ändern
            elif event == cv2.EVENT_MOUSEMOVE and self.dragging_variable:
                if self.dragging_variable == "r1":
                    self.r1 = max(10, min(x - 50, 300))  # r1 mit der x-Position ändern
                elif self.dragging_variable == "r2":
                    self.r2 = max(10, min(x - 50, 300))  # r2 mit der y-Position ändern
                elif self.dragging_variable == "r3":
                    self.r3 = x % 360  # r3 mit der x-Bewegung ändern
                elif self.dragging_variable == "center":
                    self.cx, self.cy = x, y  # Zentrum auf die Mausposition setzen

            elif event == cv2.EVENT_LBUTTONUP:
                self.dragging_variable = None  # Bewegung stoppen, wenn die Maustaste losgelassen wird

    # Hauptfunktion zum Ausführen der Anwendung
    def run(self):
        cv2.namedWindow("Interactive Ellipse")
        cv2.setMouseCallback("Interactive Ellipse", self.on_mouse)

        while True:  # Unendliche Schleife, um das Video immer wieder abzuspielen
            ret, frame = self.cap.read()

            if not ret:  # Wenn das Video zu Ende ist, gehe zum ersten Frame zurück
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # Ellipse und Parameter auf das Bild zeichnen
            if not self.is_fixed:
                self.draw_ellipse(frame)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, f"r1: {self.r1}", (50, 50), font, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, f"r2: {self.r2}", (50, 90), font, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, f"r3: {self.r3}", (50, 130), font, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, f"Center: ({self.cx}, {self.cy})", (50, 170), font, 0.7, (0, 0, 0), 2)
                cv2.putText(frame, "Drücke 'Enter', um Werte zu fixieren", (50, 210), font, 0.7, (0, 0, 0), 2)
                cv2.circle(frame, (self.cx, self.cy), 5, (0, 0, 255), -1)
            else:
                # Wenn die Parameter fixiert sind, nur die Ellipse zeichnen
                self.draw_ellipse(frame)

            cv2.imshow("Interactive Ellipse", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Beenden
                return [0, 0, 0, 0, 0]
            elif key == 13:  # Enter-Taste drücken, um die Parameter zu fixieren
                self.is_fixed = True
                self.cap.release()
                cv2.destroyAllWindows()
                return self.r1, self.r2, self.r3, self.cx, self.cy

        self.cap.release()
        cv2.destroyAllWindows()

# Anwendung starten
if __name__ == "__main__":
    ellipse_app = InteractiveEllipse(video_source=0)  # Videoquelle
    a, b, c, d, e = ellipse_app.run()
    print(f"Finale Parameter: r1={a}, r2={b}, r3={c}, cx={d}, cy={e}")

