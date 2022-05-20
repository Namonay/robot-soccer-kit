import rsk
import time
from math import pi
class Predict:
    def __init__(self, client, team, side):
        self.client = client
        self.team = team
        self.couleur = ['green', 'blue']
        self.numero = [1, 2]
        self.side = side
        
    def delta(self):
        '''Calcule inertie de la balle'''
        if str(self.client.ball)  ==  "None":
            return
        old = self.client.ball
        time.sleep(0.05)
        return (self.client.ball[0] - old[0], self.client.ball[1] - old[1])

    def plus_proche(self):
        '''Return tuple du robot plus proche de la balle ('team', nombre)'''
        plus_proche = 100
        robot_pp = None
        client = self.client
        for i in self.couleur:
            for j in self.numero:
                if str(client.robots[i][j].position) !=  'None' and str(client.ball) !=  'None':
                    robot = client.robots[i][j]
                    if abs(client.ball[0] - robot.position[0])+abs(client.ball[1] - robot.position[1]) < plus_proche:
                        plus_proche = abs(
                            client.ball[0] - robot.position[0])+abs(client.ball[1] - robot.position[1])
                        robot_pp = (i, j)
        return robot_pp
    
    def segment(self):
        '''Vecteur robot_plus_proche -> balle'''
        client = self.client
        return (client.ball[0] - client.robots[self.plus_proche()[0]][self.plus_proche()[1]].position[0], client.ball[1] - client.robots[self.plus_proche()[0]][self.plus_proche()[1]].position[1])
 
    def segment_nomee(self, couleur, numero):
        '''Vecteur robot_au_choix -> balle'''
        robot = client.robots[couleur][numero]
        return (client.ball[0] - robot.position[0], client.ball[1] - robot.position[1])
 
    def prolongation_seg(self, i = 1):
        '''Prolonge de vecteur robot_plus_proche -> balle jusqu'à sortir du terrain, None si sort sans finir sur l'axe des goals
        Return l'axe y de la cage correspondant au cages du goal'''
        client = self.client
        while abs(self.segment()[0]*i) < 0.8 and abs(self.segment()[1]) < 0.7:
            i +=  1
            if abs(self.segment()[1]*i) > 0.7:
                return None
        if self.segment()[0]*i < 0 and self.side  ==  'left': return client.ball[1] + self.segment()[1]*i*0.75
        if self.segment()[0]*i > 0 and self.side  ==  'right': return client.ball[1] + self.segment()[1]*i*0.75
        
    def prolongation_seg_xy(self, i = 1):
        '''Prolonge de vecteur robot_plus_proche -> balle jusqu'à sortir du terrain, None si sort sans finir sur l'axe des goals
        Return l'axe y de la cage correspondant au cages du goal'''
        client = self.client
        while abs(self.segment()[0]*i) < 0.9 and abs(self.segment()[1]) < 0.7:
            i += 1
        return (client.ball[0] + self.segment()[0]*i, client.ball[1] + self.segment()[1]*i)
        
    def print_info(self):
        '''ça print beaucoup d'info pour faire stylé'''
        if str(client.ball)  ==  "None":
            return
        print('---------------------------------')
        print("DELTA :", self.delta())
        print("PREDICT :", self.prolongation_seg())
        print('POS :', defe.defenseur.position[1])
        print('PLUS PROCHE :', self.plus_proche())
        print('BALLE :', client.ball[0], client.ball[1])
        print('PROCHE,FACE A :', defe.proche_de(), defe.face_a())
        print('#')
   
'''---------------------------------------- CHANGEMENT DE CLASSE WOUHOU ----------------------------------------'''
class Defense:
    def __init__(self, client, team, nbr: int,side : str):
        self.defenseur = client.robots[team][nbr]
        self.client = client
        self.team = team
        self.nbr = nbr
        self.coords = {}
        self.side = side
        self.init_coords()
    def init_coords(self):
        
        if self.side == 'right':
            self.coords['cage'] = 0.9
            self.coords['retreat_cage'] = 1.075
            self.coords['angle'] = pi
            self.coords['threshold_cage'] = 0.8
            self.coords['degagement'] =  -0.1
            self.coords['deplace_cage'] = 0.3
            self.coords['deplace_cage2'] =  -0.3
            
        if self.side == 'left':
            self.coords['cage'] =  -0.9
            self.coords['retreat_cage'] =  -1.075
            self.coords['angle'] = 0
            self.coords['threshold_cage'] =  -0.8
            self.coords['degagement'] = 0.1
            self.coords['deplace_cage'] =  -0.3
            self.coords['deplace_cage2'] = 0.3
            
    def reset_placement(self):
        '''Replace le goal à sa place de défaut'''
        self.defenseur.goto((self.defenseur.position[0], self.defenseur.position[1], pi - self.coords['angle']), True)
        self.defenseur.goto((self.coords['cage'], 0, pi - self.coords['angle']), True)
        self.defenseur.goto((self.defenseur.position[0], self.defenseur.position[1], self.coords['angle']), True)

    def kick(self):
        self.defenseur.kick(1)

    def next_to_goal(self):
        client = self.client
        if abs(client.ball[0]) > 0.75 and abs(client.ball[1]) < 0.6:
            return True

    def proche_de(self):
        client = self.client
        return abs(client.ball[0] - self.defenseur.position[0]) < 0.4

    def face_a(self):
        client = self.client
        return abs(abs(client.ball[1]) - abs(self.defenseur.position[1])) < 0.05

    def control(self, x, y, z):
        self.defenseur.control(x, y, z)

    def degagement(self):
        defe.reset_angle()
        self.defenseur.goto((client.ball[0] - self.coords['degagement'],client.ball[1], self.coords['angle']), True)
        time.sleep(0.5)
        self.defenseur.goto((client.ball[0] - self.coords['degagement'],client.ball[1], self.coords['angle']), True)
        self.defenseur.control(0.25, 0, 0)
        time.sleep(0.25)
        self.defenseur.kick()
        time.sleep(0.5)

    def reset_angle(self):
        self.defenseur.goto(
            (self.defenseur.position[0], self.defenseur.position[1], self.coords['angle']), False)

    def deplace_cage(self):
        client = self.client
        while client.ball[1] - self.defenseur.position[1] > 0.05 and abs(client.ball[1]) < 0.6:
            self.defenseur.control(0, self.coords['deplace_cage2'], 0)
        while client.ball[1] - self.defenseur.position[1] < - 0.05 and abs(client.ball[1]) < 0.6:
            self.defenseur.control(0, self.coords['deplace_cage'], 0)
        if abs(client.ball[1]) > 0.6:
            self.defenseur.control(0,0,0)

    def deplace_cage_avance(self):
        self.reset_angle()

        prolongation = predict.prolongation_seg()
        if prolongation  ==  None:    
            return

        while True:
            prolongation = predict.prolongation_seg()

            if prolongation is None or abs(prolongation) > 0.4:
                self.defenseur.control(0, 0, 0)
                break

            if prolongation - self.defenseur.position[1] > 0.05 and abs(prolongation) < 0.4:
                self.defenseur.control(0, self.coords['deplace_cage2'], 0)
            else:
                break
        while True:
            prolongation = predict.prolongation_seg()

            if prolongation is None or abs(prolongation) > 0.4:
                self.defenseur.control(0, 0, 0)
                break

            if prolongation - self.defenseur.position[1] < - 0.05 and abs(prolongation) < 0.4:
                self.defenseur.control(0, self.coords['deplace_cage'], 0)
            else:
                break

    def reset_axe_avance(self):
        if self.side == 'left':
            while self.defenseur.position[0] > - 0.85:
                self.defenseur.control( - 0.15, 0, 0)
            while self.defenseur.position[0] < - 0.95:
                self.defenseur.control(0.15, 0, 0)
        else:
            while self.defenseur.position[0] < 0.85:
                self.defenseur.control( - 0.15, 0, 0)
            while self.defenseur.position[0] > 0.95:
                self.defenseur.control(0.15, 0, 0)

    def reset_axe(self):
        self.defenseur.goto((self.coords['cage'], self.defenseur.position[1], self.coords['angle']), True)

    def threshold_cage(self):
        if self.side == 'right':
            return self.client.ball[0] > 0.8 and abs(client.ball[1]) < 0.6
        return self.client.ball[0] < - 0.8 and abs(client.ball[1]) < 0.6

    def retreat(self):
        self.defenseur.goto((self.coords['retreat_cage'], self.defenseur.position[1], self.coords['angle']), True)


team = 'blue'
nbr = 2
display = True
venere = False
with rsk.Client(host='172.19.39.223', key='') as client:
    print('Attempt to connect...')
    if client.referee["teams"][team]["x_positive"]:
        side = 'right'
    else:
        side = 'left'
    defe = Defense(client, team, nbr, side)
    predict = Predict(client, team, side)
    defe.reset_angle()
    defe.reset_placement()
    print('Connected')
    while True:
        try:
            if str(client.ball)  ==  "None":
                continue
            if display:
                predict.print_info()

            while defe.threshold_cage():
                print('STRAT : Threshold')
                defe.retreat()
                defe.defenseur.goto((defe.defenseur.position[0], client.ball[1], defe.coords['angle']), True)
                defe.defenseur.goto((defe.defenseur.position[0], client.ball[1], defe.coords['angle']), True)
                while defe.face_a():
                    defe.deplace_cage()
                    defe.reset_axe_avance()
                    time.sleep(0.7)
                    defe.degagement()
                    defe.reset_placement()

            if predict.prolongation_seg()  ==  None or abs(predict.prolongation_seg()) > 0.4 or defe.next_to_goal() or venere:
                print('STRAT : SUIVRE BALLE SIMPLE')
                defe.deplace_cage()
                defe.reset_axe_avance()
                defe.reset_angle()

                if defe.proche_de() and defe.face_a() or predict.plus_proche()  ==  (defe.team, defe.nbr) and defe.face_a() or venere:
                    print('STRAT : DEGAGEMENT')
                    defe.deplace_cage()
                    defe.reset_angle()
                    time.sleep(0.7)
                    defe.degagement()
            else:
                print('STRAT : PREDIRE BALLE')
                defe.deplace_cage_avance()
                defe.reset_axe_avance()
                defe.reset_angle()
        except Exception as e:
            print('STRAT : EXCEPTION')
            defe.control(0, 0, 0)
            defe.reset_angle()

            if "keyboard" in str(e).lower():
                break
