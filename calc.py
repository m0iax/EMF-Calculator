
import math

def calculateEMF(txpower, frequency):

    freq=frequency
    eirp=txpower

    if freq<10:
        return -10
    if freq>300000:
        return -300000

    if freq>=10 and freq<=400: 
        fri=1
    elif freq>400 and freq<=2000:
        fri=2
    elif freq>2000 and freq<=300000:
        fri=3    
    else: 
        fri=0

    refden=freq/200
    rnfz=(3*(10)**8)/(freq*(10**6)*2*math.pi)
    
    if fri == 1:
        refden=2
    elif fri==2:
        refden=freq/200
    elif fri==3:
        refden=10

    dist=max(math.sqrt((eirp*(1+0.6)**2)/(refden*4*math.pi)),rnfz)
            
    separationDIstance = round(dist,2)
   
    return separationDIstance

if __name__=="__main__":
    dist=calculateEMF(50, 145)

    print(dist)

    