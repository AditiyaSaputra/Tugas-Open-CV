import cv2 #Mengakses kamera
import time #Modul untuk pewaktuan
import Module_Hand_Tracking as htm #Memanggil Module_Hand_Tracking

#Membuat resolusi kamera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

pTime = 0 #Mengetset waktu awal 0
detector = htm.HandDetector(detectionCon=0.5)

#Perulangan untuk membuat logika pada jari-jari
while True:
    success, img = cap.read()
    img = detector.Find_Hands(img)
    lmList = detector.Find_Position(img)
    tipId = [4, 8, 12, 16, 20] #LandMark setiap ujing jari
    RLId = [3, 17] #Untuk bolak-balik tangan
    if(len(lmList)!=0):
        fingers = []
        output = []
        #Logika Ibu Jari
        if(lmList[tipId[0]][1] > lmList[tipId[0]-1][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        #Logika 4 jari lainnya
        for id in range(1, len(tipId)):
            if(lmList[tipId[id]][2] < lmList[tipId[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)

        #Pengkondisian untuk membuat angka 0 - 5
        if(lmList[RLId[0]][1] > lmList[RLId[1]][1]):
            if fingers == [0, 0, 0, 0, 0]:
                output = "0"
            elif fingers == [0, 1, 0, 0, 0]:
                output = "1"
            elif fingers == [0, 1, 1, 0, 0]:
                output = "2"
            elif fingers == [1, 1, 1, 0, 0]:
                output = "3"
            elif fingers == [0, 1, 1, 1, 1]:
                output = "4"
            elif fingers == [1, 1, 1, 1, 1]:
                output = "5"
            else:
                output = " "

        #Pengkondisian untuk membuat angka 6 - 10
        elif(lmList[RLId[0]][1] < lmList[RLId[1]][1]):
            if fingers == [1, 1, 1, 1, 0]:
                output = "6"
            elif fingers == [1, 1, 1, 0, 1]:
                output = "7"
            elif fingers == [1, 1, 0, 1, 1]:
                output = "8"
            elif fingers == [1, 0, 1, 1, 1]:
                output = "9"
            elif fingers == [0, 0, 0, 0, 0]:
                output = "10"
            else:
                output = " "
            

        #Settting posisi, ketebalan, dan warna angka
        cv2.putText(img, str(output), (45, 370), cv2.FONT_HERSHEY_COMPLEX, 4, (75, 0, 130), 10)

    #Mengatur fps
    cTime = time.time()
    fps = 1/(cTime-pTime) 
    pTime = cTime
    #Setting posisi, ketebalan, dan warna text 'fps'
    cv2.putText(img, f'fps: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 1, (10, 0, 0), 2)
    #Menampilkan gambar output pada layar
    cv2.imshow("Images", img)
    if(cv2.waitKey(1) & 0xFF==ord('q')):
        break
