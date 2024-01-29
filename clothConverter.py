import maya.cmds as cmds
import random

window = cmds.window(title='Cloth Converter', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)

leftmar = cmds.columnLayout(p=cols)
cmds.text('       ', p =leftmar)

maincol = cmds.columnLayout('Block', p=cols)
cmds.text('            ')

cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
isTablecloth = cmds.checkBoxGrp('isTablecloth', numberOfCheckBoxes=1, label='Is tablecloth ')
cmds.separator(height = 10)
cmds.radioButtonGrp('clothShape', label='Cloth Shape ', labelArray4=['Circular', 'Square', 'Elliptic', 'Rectangular'], numberOfRadioButtons=4)
cmds.floatSliderGrp('radius', label='Radius ', field = True, min = 1, max = 40, v = 1)
cmds.floatSliderGrp('width', label='Width ', field = True, min = 1, max = 40, v = 1)
cmds.floatSliderGrp('height', label='Height ', field = True, min = 1, max = 40, v = 1)
cmds.checkBoxGrp('useTable', numberOfCheckBoxes=1, label='Use Selected as Table ')
submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Convert into Cloth", c="convertCloth()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def convertCloth():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
    name = inputname
    
    isTablecloth = cmds.checkBoxGrp('isTablecloth', q = True, v1=True)
    useTable = cmds.checkBoxGrp('useTable', q = True, v1=True)
    clothShape = cmds.radioButtonGrp('clothShape', q = True, sl = True)
    width = cmds.floatSliderGrp('width', q = True, v = True)
    height = cmds.floatSliderGrp('height', q = True, v = True)
    
    print(clothShape)
    
    if (useTable == True):
        table = cmds.ls(selection = True, sn=True)
        colliderName = table[0]
        
        cmds.duplicate(colliderName, n = name + 'collider')
        
    else:
        collider = cmds.polyCylinder(r=0.5, h=1, sx=20, sy=1, sz=1, ax=[0, 1, 0], cuv=3, ch=1, n = name + 'collider')
        #colliderName = name + 'collider'
    
    if(clothShape == 1):
        #clothmesh = cmds.polyDisc(sides=3, subdivisionMode=4, subdivisions=3, radius=1, n = name + 'clothmesh')
        clothmesh = cmds.polyPlane(w=width, h=height, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
        clothmesh = cmds.polyCircularize(name + 'clothmesh')
    elif (clothShape == 2):
        clothmesh = cmds.polyPlane(w=width, h=height, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
    elif (clothShape == 3):
        clothmesh = cmds.polyDisc(sides=3, subdivisionMode=4, subdivisions=3, radius=1, n = name + 'clothmesh')
    else:
        clothmesh = cmds.polyPlane(w=width, h=height, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
    
    cmds.move(0, 1.877564, 0, r=True, os=True, wd=True)
    #cmds.scale(5.716102, 5.716102, 5.716102, r=True)
    clothmesh = cmds.polySmooth(mth=0, sl = 2)
    outMesh = cmds.createNode('nRigid', name=name + 'nRigid1')
    
    cmds.connectAttr(name + 'collider' + 'Shape.worldMesh[0]', name + 'nRigid1.inputMesh')
    cmds.createNode('nucleus', name= name + 'nucleus1')
    cmds.connectAttr(name + 'nRigid1.currentState', name + 'nucleus1.inputPassive[0]')
    cmds.connectAttr(name + 'nRigid1.startState', name + 'nucleus1.inputPassiveStart[0]')
    cmds.connectAttr(name + 'nucleus1.startFrame', name + 'nRigid1.startFrame')
    
    cmds.createNode('nCloth', name= name + 'nCloth1')
    cmds.connectAttr(name + 'nucleus1.outputObjects[0]', name + 'nCloth1.nextState')
    cmds.connectAttr(name + 'clothmeshShape.worldMesh[0]', name + 'nCloth1.inputMesh')
    cmds.connectAttr(name + 'nucleus1.startFrame', name + 'nCloth1.startFrame')
    cmds.connectAttr(name + 'nCloth1.startState', name + 'nucleus1.inputActiveStart[0]')
    cmds.connectAttr(name + 'nCloth1.currentState', name + 'nucleus1.inputActive[0]')
    outMesh = cmds.createNode('mesh', n = name + 'cloth1')
    cmds.connectAttr(name + 'nCloth1.outputMesh', name + 'cloth1.inMesh')
    time_node = cmds.createNode('time', n = 'time')
    cmds.playbackOptions(minTime=1, maxTime=300, animationStartTime=1, animationEndTime=300)
    cmds.currentTime( query=True )
    
    cmds.connectAttr('time.outTime', name + 'nCloth1.currentTime')
    cmds.connectAttr('time.outTime', name + 'nucleus1.currentTime')
    cmds.connectAttr('time.outTime', name + 'nRigid1.currentTime')
    
    
    cmds.expression(s=f"{time_node}.outTime = `currentTime -q`;")
   
    shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
                
    cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
    cmds.select(outMesh)
    cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
    cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
