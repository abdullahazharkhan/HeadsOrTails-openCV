import cv2
import cvzone 
import time
import random
from cvzone.HandTrackingModule import HandDetector

def countFingers(arr):
    fingers = 0
    for i in arr:
        if i == 1:
            fingers += 1
    return fingers

def headsOrTails(a, b):
    if ((a+b) % 2) == 0:
        return "Tails"
    else: 
        return "Heads"

cap = cv2.VideoCapture(0)
cap.set(3, 640) # to change width
cap.set(4, 480) # to change height

detector = HandDetector(maxHands = 1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] # [AI, Player]
playerChoice = None
batting = None
won = None
winner = None
lastPlayed = None
target = None

while True:
    imgBG = cv2.imread("./Assets/HTBG.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]
    
    # Find Hands
    hands, img = detector.findHands(imgScaled)
    
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 400), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 0), 4)
        
            if timer > 3:
                timer = 0
                stateResult = True
        
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if won == None:
                        playerMove = countFingers(fingers)
                        randomNumber = random.randint(1, 5)
                        imgAI = cv2.imread(f"./Assets/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                        if headsOrTails(playerMove, randomNumber) == playerChoice:
                            won = "Player"
                        else:
                            won = "AI"
                            rand = random.randint(1, 100)
                            print("rand: " + str(rand))
                            if rand % 2 == 0:
                                batting = "AI"
                            else:
                                batting = "Player"
                        print("won: " + won)
                        continue
                    else:
                        if(fingers == [1, 0, 0, 0, 0]):
                            playerMove = 6
                        elif (fingers == [0, 0, 0, 0, 0]):
                            playerMove = 10
                        else:
                            playerMove = countFingers(fingers)
                            
                        randomNumber = random.randint(1, 7)
                        if(randomNumber == 7):
                            aiMove = 10
                        else:
                            aiMove = randomNumber
                        imgAI = cv2.imread(f"./Assets/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))    
                        
                        if(playerMove == aiMove):
                            if lastPlayed == None:
                                if batting == "Player":
                                    target = scores[1] + 1
                                    batting = "AI"
                                    lastPlayed = "Player"
                                elif batting == "AI":
                                    target = scores[0] + 1
                                    batting = "Player"
                                    lastPlayed = "AI"
                                    
                            elif lastPlayed == "Player" and scores[0] < target:
                                winner = "Player"
                                print("elif mei hun")
                                startGame = False
                            elif lastPlayed == "AI" and scores[1] < target:
                                winner = "AI"
                                print("elif mei hun")
                                startGame = False
                        else:
                            if batting == "Player":
                                scores[1] += playerMove
                            elif batting == "AI":
                                scores[0] += aiMove
                        
                        if lastPlayed == "AI" and (scores[1] >= target):
                            winner = "Player"
                            print("neeche wale if mei hun")
                            startGame = False
                        elif lastPlayed == "Player" and (scores[0] >= target):
                            winner = "AI"
                            print("neeche wale if mei hun")
                            startGame = False
                        
                        
                    if batting == None:
                            if (fingers == [0,0,0,0,0]):
                                batting = "AI"
                            elif (fingers == [1,1,1,1,1]):
                                batting = "Player"
                    print("batting: " + batting)
                    
                    
                    
    imgBG[234:654,795:1195] = imgScaled
    
    cv2.putText(imgBG, str(int(scores[0])), (410, 215-40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
    cv2.putText(imgBG, str(int(scores[1])), (1112, 215-40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
    
    if not startGame:
        cv2.putText(imgBG, "Press 'H' for Heads", (200, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 5)
        cv2.putText(imgBG, "Press 'T' for Tails", (200, 500), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 5)
    
    if won and batting == None:
        cv2.putText(imgBG, "Show paper to bat, and rock to bowl", (200, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 5)
    
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
        
    if winner != None:
        cv2.putText(imgBG, "Winner: " + winner, (600, 600), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
        
    cv2.flip(img,-1)
    cv2.imshow("BG", imgBG)
    
    key = cv2.waitKey(1)
    if key == ord('h'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        playerChoice = "Heads"
        scores = [0, 0]
        batting = None
        won = None
        winner = None
        lastPlayed = None
        target = None
    elif key == ord('t'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        playerChoice = "Tails"
        scores = [0, 0]
        batting = None
        won = None
        winner = None
        lastPlayed = None
        target = None
    elif key == ord(' '):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):
        break