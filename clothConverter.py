import maya.cmds as cmds
import random

collider = cmds.polyCylinder(r=1, h=2, sx=20, sy=1, sz=1, ax=[0, 1, 0], cuv=3, ch=1, n = 'name' + 'collider')

clothmesh = cmds.polyPlane(w=1, h=1, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n='clothmesh')
cmds.move(0, 1.877564, 0, r=True, os=True, wd=True)
cmds.scale(5.716102, 5.716102, 5.716102, r=True)
clothmesh = cmds.polySmooth(mth=0, sl = 2)
outMesh = cmds.createNode('nRigid', name='name' + 'nRigid1')

cmds.connectAttr('name' + 'colliderShape.worldMesh[0]', 'name' + 'nRigid1.inputMesh')
cmds.createNode('nucleus', name='nucleus1')
cmds.connectAttr('nRigid1.currentState', 'nucleus1.inputPassive[0]')
cmds.connectAttr('nRigid1.startState', 'nucleus1.inputPassiveStart[0]')
cmds.connectAttr('nucleus1.startFrame', 'nRigid1.startFrame')


cmds.createNode('nCloth', name='nCloth1')
cmds.connectAttr('nucleus1.outputObjects[0]', 'nCloth1.nextState')
cmds.connectAttr('clothmeshShape.worldMesh[0]', 'nCloth1.inputMesh')
cmds.connectAttr('nucleus1.startFrame', 'nCloth1.startFrame')
cmds.connectAttr('nCloth1.startState', 'nucleus1.inputActiveStart[0]')
cmds.connectAttr('nCloth1.currentState', 'nucleus1.inputActive[0]')
outMesh = cmds.createNode('mesh', n = 'cloth1')
cmds.connectAttr('nCloth1.outputMesh', 'cloth1.inMesh')
time_node = cmds.createNode('time', n = 'time')
cmds.playbackOptions(minTime=1, maxTime=100, animationStartTime=1, animationEndTime=100)
cmds.currentTime( query=True )

cmds.connectAttr('time.outTime', 'nCloth1.currentTime')
cmds.connectAttr('time.outTime', 'nucleus1.currentTime')
cmds.connectAttr('time.outTime', 'nRigid1.currentTime')


cmds.expression(s=f"{time_node}.outTime = `currentTime -q`;")
name = 's'
shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
            
cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
cmds.select(outMesh)
cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)