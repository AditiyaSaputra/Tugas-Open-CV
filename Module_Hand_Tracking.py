import cv2 #Mengakses kamera
import mediapipe as mp #Module LindMarking

class HandDetector(): #Deklarasi class
    #Constructor
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity=modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    #Fungsi untuk menemukan  tangan
    def Find_Hands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
        
    #Fungsi untuk menemukan  posisi tangan
    def Find_Position(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            #Membuat LandMark dan LandConnection
            for hand_landmarks in self.results.multi_hand_landmarks :
                self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS,
                self.mpDraw.DrawingSpec(color=(16,31,235), thickness=4, circle_radius=3,), # Land Mark(buletan)
                self.mpDraw.DrawingSpec(color=(52,235,155), thickness=2)) # Land Connections(garis)

            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y *h)
                lmList.append([id, cx, cy])
        return lmList
