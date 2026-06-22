# VerifyFaceAttend
## SIMPLE FACE RECOGNITION ATTENDANCE

Super simple! Just 1 Python file.

## Setup (2 minutes)

```bash
pip install -r simple_requirements.txt
```

## How to Use

### Step 1: Add Face Photos

1. Run the script first time:
```bash
python simple_face_attendance.py
```

2. It creates a `faces` folder

3. Add photos to the `faces` folder:
   - `person1.jpg`
   - `person2.jpg`
   - `person3.jpg`
   - etc...

Photos should be:
- Clear frontal face visible
- Good lighting
- JPG or PNG format

### Step 2: Run Again

```bash
python simple_face_attendance.py
```

## Using the System

- **Camera opens automatically**
- **Green border** = Face matched ✓
- **Red border** = Unknown face ✗
- **Name shown** above face
- **Attendance marked AUTOMATICALLY** when face matches
- **Press Q** = Quit

## Attendance Record

Saved automatically in `attendance.txt`:
```
2026-06-22 14:30:25 | person1 | PRESENT | detected_faces/person1_20260622_143025.jpg
2026-06-22 14:35:40 | person2 | PRESENT | detected_faces/person2_20260622_143540.jpg
2026-06-22 14:40:15 | person1 | PRESENT | detected_faces/person1_20260622_144015.jpg
```

## Folders Created

- `faces/` - Put your reference photos here
- `detected_faces/` - Auto-created, stores detected face images with timestamps
- `attendance.txt` - Auto-created, stores attendance records with image paths

## Files

- `simple_face_attendance.py` - Main script
- `simple_requirements.txt` - Dependencies
- `SIMPLE_README.md` - This file

## How It Works

1. Add 3-5 clear face photos to `faces/` folder
2. Run the script
3. Camera opens automatically
4. Look at the camera
5. When your face is recognized, attendance is **automatically marked**
6. Your face image is saved with timestamp
7. Check `attendance.txt` for records with image links

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| **Q** | Quit |

---

## Matching Settings

- **Confidence Threshold**: 80.0 (lower = stricter matching)
- **Face Size**: 100x100 pixels (for training)

To adjust strictness, edit `face_threshold` in the script:
- Higher value (e.g., 85-90) = Stricter matching (fewer false positives)
- Lower value (e.g., 70-75) = Lenient matching (fewer false negatives)

---

## Troubleshooting

### "No faces found in: person1.jpg"
- Photo doesn't have clear face
- Try different photo with better lighting
- Make sure face is frontal (looking at camera)

### Face not recognized
- Add photos with better lighting
- Get closer to camera (0.5-1.5m)
- Look directly at camera
- Check confidence value shown (higher % = better match)

### Camera not opening
- Check camera is connected
- Close other apps using camera
- Restart the script

### Images not saving
- Check `detected_faces/` folder exists
- Verify write permissions in the folder
- Check disk space

---

Done! The system is ready to use.

Done! Very simple system ready to use.
