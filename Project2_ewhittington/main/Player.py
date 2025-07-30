from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, CollisionHandlerEvent, CollisionTraverser, TransparencyAttrib
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
from SpaceJamClasses import Missile
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText

import re




class SpaceShip(SphereCollideObject):
    
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, traverser, base: ShowBase):
        
        super(SpaceShip, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1)
        self.taskMgr = taskMgr
        self.accept = accept
        self.loader = loader
        self.base = base
    
        self.traverser = traverser

        self.handler = CollisionHandlerEvent()
        
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.render = parentNode
        # Added these because the given project3 code refused to reference it.
        
    

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.movespeed = 5
        self.reloadTime = .25
        self.chargeTime = 2
        self.boostTime = 1
        self.missileDistance = 4000
        self.missileBay = 1
        self.shipBoosts = 1
        
        self.cntExplode = 0
        self.explodeIntervals = {}
        self.SetParticles()
        
        self.fire_sfx = self.base.loader.loadSfx("./assets/Sounds/laser.ogg")
        self.thrust_sfx = self.base.loader.loadSfx("./assets/Sounds/thrust.ogg")
        self.boost_sfx = self.base.loader.loadSfx("./assets/Sounds/boost.ogg")
        self.explode_sfx = self.base.loader.loadSfx("./assets/Sounds/explode.ogg")
        self.bigexplode_sfx = self.base.loader.loadSfx("./assets/Sounds/bigexplode.ogg")

        
        self.shotHud = OnscreenImage(image = './assets/Hud/shotchargeFULL.png', pos = Vec3(-1.1, 0, -0.15), scale = 0.2)
        self.shotHud.setTransparency(TransparencyAttrib.MAlpha)
        self.boostHud = OnscreenImage(image = './assets/Hud/boostchargeFULL.png', pos = Vec3(-1.1, 0, -0.6), scale = 0.2)
        self.boostHud.setTransparency(TransparencyAttrib.MAlpha)
        self.points = 0
        self.pointHud = OnscreenText(text = f'Score: {self.points}', pos = Vec3(0.9, 0.9, 0), fg = (1, 1, 1, 1), scale = 0.07, mayChange = True)
        
        self.setKeyBindings()

    def setKeyBindings(self):

        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])

        self.accept('a', self.leftTurn, [1])
        self.accept('a-up', self.leftTurn, [0])

        self.accept('d', self.rightTurn, [1])
        self.accept('d-up', self.rightTurn, [0])

        self.accept('w', self.lookUp, [1])
        self.accept('w-up', self.lookUp, [0])

        self.accept('s', self.lookDown, [1])
        self.accept('s-up', self.lookDown, [0])

        self.accept('arrow_left', self.rollLeft, [1])
        self.accept('arrow_left-up', self.rollLeft, [0])

        self.accept('arrow_right', self.rollRight, [1])
        self.accept('arrow_right-up', self.rollRight, [0])

        self.accept('f', self.fire)
        self.accept('b', self.Boost)
    def ApplyThrust(self, task):
        rate = self.movespeed
        trajectory = self.render.getRelativeVector(self.modelNode,Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def Thrust(self, keyDown):
        if keyDown:
            self.thrust_sfx.play()
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.thrust_sfx.stop()
            self.taskMgr.remove('forward-thrust')
            
    def leftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')
    def ApplyLeftTurn(self, task):
        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def rightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')
    def ApplyRightTurn(self, task):
        rate = 0.5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    def lookUp(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookUp, 'look-up')
        else:
            self.taskMgr.remove('look-up')
    def ApplyLookUp(self, task):
        rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def lookDown(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookDown, 'look-down')
        else:
            self.taskMgr.remove('look-down')
    def ApplyLookDown(self, task):
        rate = 0.5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    def rollLeft(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollLeft, 'roll-left')
        else:
            self.taskMgr.remove('roll-left')
    def ApplyRollLeft(self, task):
        rate = 0.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def rollRight(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollRight, 'roll-right')
        else:
            self.taskMgr.remove('roll-right')
    def ApplyRollRight(self, task):
        rate = 0.5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont

    def Boost(self):
        if self.shipBoosts:
            self.boost_sfx.play()
            self.shipBoosts = 0
            self.UpdateBoostHud()
            if not self.taskMgr.hasTaskNamed('stop-boost'):
                self.taskMgr.doMethodLater(self.boostTime, self.StopBoost, 'stop-boost')
            self.movespeed = 10
            
            # print('boosted!')
        else: 
            if not self.taskMgr.hasTaskNamed('reload-boost'):
                self.taskMgr.doMethodLater(0, self.ReloadBoost, 'reload-boost')
                return Task.cont
    def StopBoost(self, task):
        self.movespeed = 5
        self.boost_sfx.stop()
        
        # print('boost stopped')
    def ReloadBoost(self, task):
        if task.time > self.chargeTime:
            self.shipBoosts += 1
            # print("Charge done!")
            self.UpdateBoostHud()
            return Task.done
        elif task.time <= self.chargeTime:
            # print("Charge proceeding..")
            return Task.cont


    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                # print(i + ' has reached the end of its fire solution')
                break
        return Task.cont

    def fire(self):
        
        if self.missileBay:
            self.fire_sfx.play()
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            self.UpdateShotHud()
            tag = 'Missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront
            currentMissile = Missile(self.loader, './assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
            
            
        else:
            if not self.taskMgr.hasTaskNamed('reload'):
                # print('Initializing reload...')
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            print('reload complete')
            self.UpdateShotHud()
            return Task.done
        elif task.time <= self.reloadTime:
            # print("Reload proceeding..")
            return Task.cont
        if self.missileBay > 1:
            self.missileBay = 1
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        # print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        # print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        # print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        # print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        # print('TempVar1: ' + str(tempVar))
        tempVar = intoNode.split('_')
        # print('TempVar2: ' + str(tempVar))
        victim = tempVar[0]
        # print('Victim: ' + str(victim))
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "Space Station"):
            if strippedString == "Drone":
                self.points += 1
                self.explode_sfx.play()
            elif strippedString == "Planet":
                self.points += 10
                self.bigexplode_sfx.play()
            elif strippedString == "Space Station":
                self.points -= 10
                self.bigexplode_sfx.play()
            if self.points < 0:
                self.points = 0
            print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)
            print(shooter + ' is DONE.')
            self.UpdateScoreHud()
            Missile.Intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()
        self.explodeNode.setPos(hitPosition)
        # self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)
        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()
        
    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)
    def SetParticles(self):
        self.base.enableParticles()
        self.explodeEffect = ParticleEffect()
        #self.explodeEffect.loadConfig('./assets/Part-Fx/Part-Efx/basic_xpld_efx.ptf')
        #self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')

        # HUD SCRIPTS: 

        
    def UpdateShotHud(self):
        if self.missileBay:
            self.shotHud.setImage('./assets/Hud/shotchargeFULL.png')
            self.shotHud.setTransparency(TransparencyAttrib.MAlpha)
        else:
            self.shotHud.setImage('./assets/Hud/shotchargeempty.png')
            self.shotHud.setTransparency(TransparencyAttrib.MAlpha)
    def UpdateBoostHud(self):
        if self.shipBoosts:
            self.boostHud.setImage('./assets/Hud/boostchargeFULL.png')
            self.boostHud.setTransparency(TransparencyAttrib.MAlpha)
        else:
            self.boostHud.setImage('./assets/Hud/boostchargeempty.png')
            self.boostHud.setTransparency(TransparencyAttrib.MAlpha)
    def UpdateScoreHud(self):
        self.pointHud.setText(f'Score: {self.points}')
    
        
        