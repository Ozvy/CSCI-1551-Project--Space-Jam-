from direct.showbase.ShowBase import ShowBase

class SetupScene(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = self.loader.loadModel("./assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)

        self.playerShip = self.loader.loadModel("./assets/Spaceships/Dumbledore/Dumbledore.x")
        self.playerShip.reparentTo(self.render)
        self.playerShip.setPos(100,2000,0)
        self.playerShip.setScale(200)
        self.playerShip.setHpr(0,90,0)
        self.spaceStation1 = self.loader.loadModel("./assets/Space_Station/SpaceStation1B/spaceStation.x")
        self.spaceStation1.reparentTo(self.render)
        self.spaceStation1.setPos(500,2900,20)
        self.spaceStation1.setScale(50)
        
        


        self.Planet1 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150,5000,67)
        self.Planet1.setScale(350)

        self.Planet2 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(427,7000,234)
        self.Planet2.setScale(800)

        self.Planet3 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(-500,-3000,-200)
        self.Planet3.setScale(340)

        self.Planet4 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(598,-4398,-1200)
        self.Planet4.setScale(150)

        self.Planet5 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(460,-5942,455)
        self.Planet5.setScale(400)

        self.Planet6 = self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(200,400,-2000)
        self.Planet6.setScale(200)

        uniTex = self.loader.loadTexture("./main/assets/Universe/starfield-in-blue.jpg")
        plan1Tex = self.loader.loadTexture("./main/assets/Planets/planet1.jpg")
        plan2Tex = self.loader.loadTexture("./main/assets/Planets/planet2.jpg")
        plan3Tex = self.loader.loadTexture("./main/assets/Planets/planet3.jpg")
        plan4Tex = self.loader.loadTexture("./main/assets/Planets/planet4.jpg")
        plan5Tex = self.loader.loadTexture("./main/assets/Planets/planet5.jpg")
        plan6Tex = self.loader.loadTexture("./main/assets/Planets/planet6.jpg")

        self.Universe.setTexture(uniTex,1)
        self.Planet1.setTexture(plan1Tex,1)
        self.Planet2.setTexture(plan2Tex,1)
        self.Planet3.setTexture(plan3Tex,1)
        self.Planet4.setTexture(plan4Tex,1)
        self.Planet5.setTexture(plan5Tex,1)
        self.Planet6.setTexture(plan6Tex,1)
    

        

runspacejam = SetupScene()
runspacejam.run()
