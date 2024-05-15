import cv2

image_path = "hands.jpg"
image = cv2.imread(image_path)

cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Resize the webcam frame to fit the window and image
    frame_height, frame_width, _ = frame.shape
    image = cv2.resize(image, (frame_width, frame_height))

    # Combine the frame and image side by side
    combined_frame = cv2.hconcat([frame, image])

    # Show the combined frame
    cv2.imshow("Dual View", combined_frame)

    # Release the webcam when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
