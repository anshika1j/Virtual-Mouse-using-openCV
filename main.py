import cv2

cap = cv2.VideoCapture(0)  # Try different indices like 0, 1, etc.

while True:
    ret, frame = cap.read()
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
