import time
from time import gmtime, strftime, localtime
import os
from sense_hat import SenseHat



hostname = "192.168.1.13"


Periode_Scan = 5
Scans = 0
PS4_allumee = 0

sense = SenseHat()
sense.low_light = True

dureelimite = 1800


R = [255, 0, 0]  # Rouge
O = [255, 255, 255]  # Blanc
V = [0, 255, 0]  # Vert
B = [0, 0, 255]  # Bleu
n = [0, 0, 0]  # Noir
J = [255, 191, 76]  # Jaune



eteint = [
n, n, n, n, n, n, n, n,
B, B, B, B, n, n, n, n,
n, n, B, n, n, n, n, n,
n, B, n, n, B, B, B, B,
B, B, B, B, n, n, B, n,
n, n, n, n, n, B, n, n,
n, n, n, n, B, B, B, B,
n, n, n, n, n, n, n, n
]


while True:
    
    response = os.system("ping -c 3 " + hostname)
    heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print(heure)


    #   and then check the response...
    if response == 0:
          
          if PS4_allumee == 0:
              print ('PS4 s allume!')
              PS4_allumee = 1
            
              
              C = V
              
              allumeeC = [
              n, n, C, C, C, C, n, n,
              n, C, n, n, n, n, C, n,
              C, n, C, n, n, C, n, C,
              C, n, n, n, n, n, n, C,
              C, n, C, n, n, C, n, C,
              C, n, n, C, C, n, n, C,
              n, C, n, n, n, n, C, n,
              n, n, C, C, C, C, n, n
              ]
            
              sense.set_pixels(allumeeC)
            
              heureallumage = strftime("%a, %d %b %Y %H:%M:%S", localtime())
              allumage=time.time()
              
              print('heure d allumage:',heureallumage)
                
            
          else:
              print ('PS4 toujours allumee!')
              
              
              
              print('heure d allumage:',heureallumage)
              heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
              print('heure actuelle:',heure)
              duree=time.time()-allumage
              print('duree d allumage', duree)
              
              teinte = int(min(255,255*duree/dureelimite))
              
              C =  [teinte, 255-teinte, 0]            
              
              if teinte < 255:
                  allumeeC = [
                  n, n, C, C, C, C, n, n,
                  n, C, n, n, n, n, C, n,
                  C, n, C, n, n, C, n, C,
                  C, n, n, n, n, n, n, C,
                  C, n, C, n, n, C, n, C,
                  C, n, n, C, C, n, n, C,
                  n, C, n, n, n, n, C, n,
                  n, n, C, C, C, C, n, n
                  ]
              else:
                 allumeeC = [
                 n, n, C, C, C, C, n, n,
                 n, C, n, n, n, n, C, n,
                 C, n, C, n, n, C, n, C,
                 C, n, n, n, n, n, n, C,
                 C, n, n, n, n, n, n, C,
                 C, n, C, C, C, C, n, C,
                 n, C, n, n, n, n, C, n,
                 n, n, C, C, C, C, n, n
                 ] 
                  
            
              sense.set_pixels(allumeeC)
            
              
            
    else:
          
        if PS4_allumee == 1:

           print ('extinction PS4')
        
           PS4_allumee = 0
           sense.set_pixels(eteint)
        else:                    
          print ('PS4 toujours eteinte')
          sense.set_pixels(eteint)

            

    time.sleep(Periode_Scan)

