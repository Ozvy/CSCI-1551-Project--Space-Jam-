from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from SpaceJamClasses import Missile
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task

class SpaceShip(SphereCollideObject):
    
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceShip, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1)
        self.taskMgr = taskMgr
        self.accept = accept
        self.loader = loader
        
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.render = parentNode
        # Added these because the given project3 code refused to reference it.
        
    

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.reloadTime = .25
        self.missileDistance = 4000
        self.missileBay = 1
        
        
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
    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode,Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
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
    
    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + ' has reached the end of its fire solution')
                break
        return Task.cont

    def fire(self):
        
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront
            currentMissile = Missile(self.loader, './assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
            
        else:
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            print('reload complete')
            return Task.done
        elif task.time <= self.reloadTime:
            print("Reload proceeding..")
            return Task.cont
        if self.missileBay > 1:
            self.missileBay = 1
    
