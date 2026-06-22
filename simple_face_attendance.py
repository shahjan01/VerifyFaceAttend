import cv2
import numpy as np
import os
from datetime import datetime

faces_folder = "faces"
detected_folder = "detected_faces"
face_size = (100, 100)
face_threshold = 80.0
attendance_marked = set()

# Create detected faces folder
if not os.path.exists(detected_folder):
    os.makedirs(detected_folder)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("ERROR: Could not load Haar cascade classifier.")
    exit(1)

# Create folder if needed
if not os.path.exists(faces_folder):
    os.makedirs(faces_folder)
    print("Created 'faces' folder - add person1.png, person2.png, etc")
    exit()

# Load and label all face images
files = [f for f in os.listdir(faces_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print(f"\nLoading {len(files)} faces...")

label_images = []
label_ids = []
label_names = {}
next_label = 0

for fname in files:
    path = os.path.join(faces_folder, fname)
    image = cv2.imread(path)
    if image is None:
        print(f"  ✗ Cannot read {fname}, skipping")
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    name = os.path.splitext(fname)[0]

    if len(faces) == 0:
        print(f"  ✗ No face found in {fname}, skipping")
        continue

    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    face_resized = cv2.resize(face_roi, face_size)

    label_images.append(face_resized)
    label_ids.append(next_label)
    label_names[next_label] = name
    next_label += 1
    print(f"  ✓ {name}")

if not label_images:
    print("ERROR: No valid face photos in 'faces' folder!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(label_images, np.array(label_ids))

print(f"\nReady! Starting camera...\n")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit(1)

print("="*70)
print("FACE RECOGNITION ATTENDANCE - SIMPLE VERSION")
print("="*70)
print("Press Q = Quit")
print("="*70 + "\n")


def mark_attendance(name, face_image=None):
    if name in attendance_marked:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    img_filename = None
    # Save face image if provided
    if face_image is not None:
        img_filename = f"{detected_folder}/{name}_{ts_filename}.jpg"
        cv2.imwrite(img_filename, face_image)
    
    # Write to attendance file with image path
    with open("attendance.txt", "a") as f:
        if img_filename:
            f.write(f"{ts} | {name} | PRESENT | {img_filename}\n")
        else:
            f.write(f"{ts} | {name} | PRESENT\n")
    
    attendance_marked.add(name)
    print(f"✓ ATTENDANCE MARKED: {name}")
    if img_filename:
        print(f"  → Image saved: {img_filename}")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 600))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    is_matched = False
    match_name = "NO MATCH"
    match_score = 0

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_resized = cv2.resize(face_roi, face_size)
        label, confidence = recognizer.predict(face_resized)
        score = max(0, min(100, int(100 - confidence)))

        if confidence < face_threshold:
            is_matched = True
            match_name = label_names[label]
            match_score = score
            # Save the original color face region
            face_roi_color = frame[y:y+h, x:x+w]
            mark_attendance(match_name, face_roi_color)
            box_color = (0, 255, 0)
            label_text = f"{match_name} ({match_score}%)"
        else:
            box_color = (0, 0, 255)
            label_text = f"NO MATCH ({score}%)"

        cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
        cv2.rectangle(frame, (x, y-35), (x+w, y), box_color, -1)
        cv2.putText(frame, label_text, (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    border_color = (0, 255, 0) if is_matched else (0, 0, 255)
    cv2.rectangle(frame, (0, 0), (800, 600), border_color, 10)

    status_text = f"MATCH: {match_name}" if is_matched else "NO MATCH - FACE NOT RECOGNIZED"
    status_color = (0, 255, 0) if is_matched else (0, 0, 255)
    cv2.putText(frame, status_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)
    cv2.putText(frame, "Q=Quit", (10, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Face Recognition Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nSystem closed")
