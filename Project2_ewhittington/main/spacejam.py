from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
import SpaceJamClasses as spaceJamClasses
import DefensePaths as defensePaths
class SetupScene(ShowBase):
    
    def __init__(self):

        ShowBase.__init__(self)
        self.Universe = spaceJamClasses.Universe(self.loader, "./assets/Universe/Universe.x", self.render, "Universe", "./assets/Universe/Universe.jpg", (0, 0, 0), 10000)
        self.PlayerShip = spaceJamClasses.SpaceShip(self.loader, "./assets/Spaceships/Dumbledore/Dumbledore.x", self.render, "PlayerShip", "./assets/Spaceships/Dumbledore/spacejet_C.png", Vec3(1000, 1200,-50), 50)
        self.spaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./assets/Space_Station/SpaceStation1B/spaceStation.x", self.render, "Space Station", "./assets/Space_Station/SpaceStation1B/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet1", "./assets/Planets/planet1.jpg", (-6000, -3000, -800), 250)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet2", "./assets/Planets/planet2.jpg", (0, 6000, 0), 300)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet3", "./assets/Planets/planet3.jpg", (500, -5000, 200), 500)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet4", "./assets/Planets/planet4.jpg", (300, 6000, 500), 150)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet5", "./assets/Planets/planet5.jpg", (700, -2000, 100), 500)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet6", "./assets/Planets/planet6.jpg", (0, -900, -1400), 700)

        fullCycle = 60
        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            
            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.spaceStation1, nickName, j, fullCycle, 2)
    
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseBallSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./assets/DroneDefender/octotoad1_auv.png", position, 5)
    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./assets/DroneDefender/octotoad1_auv.png", position, 10)
    

        

runspacejam = SetupScene()
runspacejam.run()
