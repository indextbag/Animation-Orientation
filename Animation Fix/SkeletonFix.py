import pymel.core.datatypes as dt
import pymel.core as pm
import time
import maya.cmds as cmds

class skeletonFix():
    #def __init__(self):
        
    def listNodes(self, node, nodeNames):
        nodeNames.append(node)
        children = node.getChildren()
        for child in children:
            self.listNodes(child, nodeNames)
            
    def getJointNames(self):
        rootName = pm.ls(selection=True)
        rootJoint = pm.PyNode(rootName[0])
        joints = []
        self.listNodes(rootJoint, joints)
        return joints
    
    def getJointSelection(self):
        selection = pm.ls(selection=True)
        joints = []
        for i in range(len(selection)):
            joints.append(pm.PyNode(selection[i]))
        return joints    
    
    def reorient(self, mocapList, targetList, listLength):
        for i in range(listLength):
            nodesRotate = pm.getAttr(mocapList[i] + ".rotate")
            pm.rotate(targetList[i], nodesRotate, pcp=True)
            
    #def transfere(self, mocapList, targetList, listLength):
        #for i in range(listLength):
            #first = pm.findKeyframe(mocapList[i], which = "first")
            #curr = first
            #last = pm.findKeyframe(mocapList[i], which = "last")
            #pm.setCurrentTime(curr)
            #while (curr < last):
                #cmds.copyAttr(mocapList[i], targetList[i], inConnections=True, values=True, attribute=['rotate'])
                #pm.setKeyframe(targetList[i], at = "rotate")
                #pm.setKeyframe(targetList[i], at = "translate")
                #pm.setKeyframe(targetList[i], at = "scale")
                #curr = pm.findKeyframe(mocapList[i], time = curr, which = "next")
                #pm.setCurrentTime(curr)
                
    def transfere(self, mocapList, targetList, listLength):
        curr = pm.findKeyframe(mocapList[0], which = "first")
        last = pm.findKeyframe(mocapList[0], which = "last")
        pm.setCurrentTime(curr)
        while (curr < last):
            cmds.copyAttr(mocapList[0], targetList[0], inConnections=True, values=True, attribute=['translate'])
            for i in range(listLength):
                cmds.copyAttr(mocapList[i], targetList[i], inConnections=True, values=True, attribute=['rotate'])
                pm.setKeyframe(targetList[i], at = "rotate")
                pm.setKeyframe(targetList[i], at = "translate")
                pm.setKeyframe(targetList[i], at = "scale")
            curr += 1
            pm.setCurrentTime(curr)