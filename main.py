import cv2
import mediapipe as mp

# def rescaleFrame(frame, scale = 0.75):
#     width = int(frame.shape[1] * scale)
#     height = int(frame.shape[0] * scale)
#     dimensions = (width, height)
#     return cv2.resize(frame, dimensions, interpolation = cv2.INTER_AREA)

# def changeRes(width, height):
#     cap.set(3, width)
#     cap.set(4, height)


image_path = "hands.jpg"
image = cv2.imread(image_path)
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCoordinates = [(8,6), (12,10), (16,14), (20, 18)]
thumbCoordinates = (4, 2)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandMarks = results.multi_hand_landmarks
    
    
    frame_height, frame_width, _ = img.shape
    image = cv2.resize(image, (frame_width, frame_height))
    
    combined_frame = cv2.hconcat([img, image])
    
    if multiLandMarks:
        handPoints = []
        for handLms in multiLandMarks:
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idx, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                handPoints.append((cx, cy))

        # for point in handPoints:
        #     cv2.circle(img, point, 10, (255, 0, 255), cv2.FILLED)
            
        upCount = 0
        flag = 0
        for coordinate in fingerCoordinates:
            if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                upCount += 1
        if upCount == 0 and handPoints[thumbCoordinates[0]][0] > handPoints[thumbCoordinates[1]][0]:
            flag = 1
        
        if handPoints[thumbCoordinates[0]][0] > handPoints[thumbCoordinates[1]][0]:
            upCount += 1
        
        if upCount == 0:
            upCount = 10
            cv2.putText(combined_frame, str(upCount), (80, 150), cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
        elif flag == 1:
            upCount = 6
            cv2.putText(combined_frame, str(upCount), (80, 150), cv2.FONT_HERSHEY_PLAIN, 12, (0, 255, 0), 12)
        else:
            cv2.putText(combined_frame, str(upCount), (80, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

        print(upCount)

    # frameResized = rescaleFrame(img, scale = 1.25)
    cv2.imshow("Dual View", combined_frame)
    # cv2.imshow("Finger Counter", )
    cv2.waitKey(5)