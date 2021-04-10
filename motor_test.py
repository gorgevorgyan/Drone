import pigpio
import time


pi = pigpio.pi()


m = [
[13, 21],
[19, 16]
]

m = [
[21, 13],
[19, 16]]

for k in (900, 1000, 1100):
    for i in m:
        for j in i:
            pi.set_servo_pulsewidth(j, k)
    print(k)
    time.sleep(0.5)

try:
        while 1:
                a = input()
                x = a.split(" ")[0]
                y = a.split(" ")[1]
                z = a.split(" ")[2]
                pi.set_servo_pulsewidth(m[int(x)][int(y)], int(z))
                print(x, y, z)
except KeyboardInterrupt:
        print("aa")
        for i in m:
                for j in i:
                        pi.set_servo_pulsewidth(j, 800)