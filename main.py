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

imgAI = cv2.imread(f"./Assets/{5}-wobg.png", cv2.IMREAD_UNCHANGED)

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
    imgBG = cv2.imread("./Assets/bg.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]
    
    # Find Hands
    hands, img = detector.findHands(imgScaled)
    
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (608, 260), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 0), 4)
        
            if timer > 3:
                timer = 0
                stateResult = True
        
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if won == None:
                        playerMove = countFingers(fingers)
                        randomNumber = random.randint(1, 5)
                        imgAI = cv2.imread(f"./Assets/{randomNumber}-wobg.png", cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                        if headsOrTails(playerMove, randomNumber) == playerChoice:
                            won = "Player"
                        else:
                            won = "AI"
                            rand = random.randint(1, 100)
                            # print("rand: " + str(rand))
                            if rand % 2 == 0:
                                batting = "AI"
                            else:
                                batting = "Player"
                        # print("won: " + won)
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
                        imgAI = cv2.imread(f"./Assets/{randomNumber}-wobg.png", cv2.IMREAD_UNCHANGED)
                        # imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 380))    
                        
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
                                # print("elif mei hun")
                                startGame = False
                            elif lastPlayed == "AI" and scores[1] < target:
                                winner = "AI"
                                # print("elif mei hun")
                                startGame = False
                        else:
                            if batting == "Player":
                                scores[1] += playerMove
                            elif batting == "AI":
                                scores[0] += aiMove
                        
                        if lastPlayed == "AI" and (scores[1] >= target):
                            winner = "Player"
                            # print("neeche wale if mei hun")
                            startGame = False
                        elif lastPlayed == "Player" and (scores[0] >= target):
                            winner = "AI"
                            # print("neeche wale if mei hun")
                            startGame = False
                        
                        
                    if batting == None:
                            if (fingers == [0,0,0,0,0]):
                                batting = "AI"
                            elif (fingers == [1,1,1,1,1]):
                                batting = "Player"
                    # print("batting: " + batting)
                    
                    
                    
    imgBG[235:655,91:491] = imgScaled
    
    cv2.putText(imgBG, str(int(scores[1])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
    cv2.putText(imgBG, str(int(scores[0])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
    
    if not startGame:
        cv2.putText(imgBG, "Press 'H' for Heads, 'T' for Tails", (240, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 5)
    
    if won and batting == None:
        cv2.putText(imgBG, "Show 5 to bat, and 10/0 to bowl", (240, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 5)
    
    if won:
        cv2.putText(imgBG, "'SPACE' to continue", (566, 554), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
        cv2.putText(imgBG, "'Q' to quit", (566, 574), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    
    if batting:
        cv2.putText(imgBG, "Batting: " + batting, (523, 320), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 5)
    
    if stateResult:
        imgAI = cv2.resize(imgAI, (500, 500), interpolation=cv2.INTER_AREA)
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (750, 200))
        
    if winner != None:
        cv2.putText(imgBG, "Winner: " + winner, (520, 440), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
        
    if target and winner == None:
        cv2.putText(imgBG, "Target: " + str(target), (520, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 5)
    cv2.flip(img,-1)
    cv2.imshow("BG", imgBG)
    
    key = cv2.waitKey(1)
    
    if key == ord('h') or key == ord('t') or key == ord(' '):
        startGame = True
        initialTime = time.time()
        stateResult = False
        if key == ord('h') or key == ord('t'):
            playerChoice = "Heads"
            scores = [0, 0]
            batting = None
            won = None
            winner = None
            lastPlayed = None
            target = None
            
            if key == ord('h'):
                playerChoice = "Heads"
            elif key == ord('t'):
                playerChoice = "Tails"
    elif key == ord('q'):
        break