from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, CollisionTraverser, CollisionHandlerPusher
import SpaceJamClasses as spaceJamClasses
import DefensePaths as defensePaths
import Player as playerClasses
class SetupScene(ShowBase):
    
    def __init__(self):

        ShowBase.__init__(self)
        self.Universe = spaceJamClasses.Universe(self.loader, "./assets/Universe/Universe.x", self.render, "Universe", "./assets/Universe/Universe.jpg", (0, 0, 0), 10000)
        self.PlayerShip = playerClasses.SpaceShip(self.loader, self.taskMgr, self.accept, "./assets/Spaceships/Dumbledore/Dumbledore.x", self.render, "PlayerShip", "./assets/Spaceships/Dumbledore/spacejet_C.png", Vec3(1000, 1200,-50), 50)
        self.spaceStation1 = spaceJamClasses.SpaceStation(self.loader, "./assets/Space_Station/SpaceStation1B/spaceStation.x", self.render, "Space Station", "./assets/Space_Station/SpaceStation1B/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet1", "./assets/Planets/planet1.jpg", (-6000, -3000, -800), 250)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet2", "./assets/Planets/planet2.jpg", (0, 6000, 0), 300)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet3", "./assets/Planets/planet3.jpg", (500, -5000, 200), 500)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet4", "./assets/Planets/planet4.jpg", (300, 6000, 500), 150)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet5", "./assets/Planets/planet5.jpg", (700, -2000, 100), 500)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./assets/Planets/protoPlanet.x", self.render, "Planet6", "./assets/Planets/planet6.jpg", (0, -900, -1400), 700)
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
    
        self.pusher.addCollider(self.PlayerShip.collisionNode, self.PlayerShip.modelNode)
        self.cTrav.addCollider(self.PlayerShip.collisionNode, self.pusher)
        
        self.cTrav.showCollisions(self.render)
        fullCycle = 60
        self.SetCamera()
        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            
            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.spaceStation1, nickName, j, fullCycle, 2)

            self.DrawCircleX(self.Planet2, nickName, (0.64*j))
            self.DrawCircleY(self.Planet3, nickName, (0.32*j))
            self.DrawCircleZ(self.Planet4, nickName, (0.32*j))

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
    
    def DrawCircleX(self, centralObject, droneName, countUp):
        unitVec = defensePaths.CircleX(countUp)
        unitVec.normalize()
        position = unitVec * 350 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./assets/DroneDefender/octotoad1_auv.png", position, 5)
    
    def DrawCircleY(self, centralObject, droneName, countUp):
        unitVec = defensePaths.CircleY(countUp)
        unitVec.normalize()
        position = unitVec * 600 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCircleZ(self, centralObject, droneName, countUp):
        unitVec = defensePaths.CircleZ(countUp)
        unitVec.normalize()
        position = unitVec * 200 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./assets/DroneDefender/octotoad1_auv.png", position, 5)
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.PlayerShip.modelNode)
        self.camera.setFluidPos(0, 1, 0)
        

    

        

runspacejam = SetupScene()
runspacejam.run()
