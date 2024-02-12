import maya.cmds as cmds
import random

#UI window
def showTableclothOp(*args):
    showCheckbox = cmds.checkBoxGrp(isTablecloth, q = True, vis = False, v1 = False)
    cmds.checkBoxGrp(useTable, edit=True, enable=True)
    cmds.floatSliderGrp(tableScale, edit=True, enable=True)

def hideTableclothOp(*args):
    showCheckbox = cmds.checkBoxGrp(isTablecloth, q = True)
    cmds.checkBoxGrp(useTable, edit=True, enable=False)
    cmds.floatSliderGrp(tableScale, edit=True, enable=False)

def hideTableOp(*args):
    showCheckbox = cmds.checkBoxGrp(useTable, q = True)
    cmds.floatSliderGrp(tableScale, edit=True, enable=False)
   
def showTableOp(*args):
    showCheckbox = cmds.checkBoxGrp(useTable, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(tableScale, edit=True, enable=True)

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
isTablecloth = cmds.checkBoxGrp('isTablecloth', numberOfCheckBoxes=1, label='Is tablecloth ', onc = showTableclothOp, ofc = hideTableclothOp)
cmds.separator(height = 10)
cmds.radioButtonGrp('clothShape', label='Cloth Shape ', labelArray2=['Elliptic', 'Rectangular'], numberOfRadioButtons=2)
cmds.floatSliderGrp('width', label='Width ', field = True, min = 1, max = 40, v = 5)
cmds.floatSliderGrp('height', label='Height ', field = True, min = 1, max = 40, v = 5)
useCrease = cmds.checkBoxGrp('useCrease', numberOfCheckBoxes=1, label='Use Selected as Crease ')
useTable = cmds.checkBoxGrp('useTable', numberOfCheckBoxes=1, label='Use Selected as Table ', onc = hideTableOp, ofc = showTableOp)
tableScale = cmds.floatSliderGrp('tableScale', label='Table Scale ', field = True, min = 1, max = 40, v = 3)
cmds.checkBoxGrp(useTable, edit=True, enable=False)
cmds.floatSliderGrp(tableScale, edit=True, enable=False)

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
    
    clothShape = cmds.radioButtonGrp('clothShape', q = True, sl = True)
    width = cmds.floatSliderGrp('width', q = True, v = True)
    height = cmds.floatSliderGrp('height', q = True, v = True)
    if (isTablecloth):
        useTable = cmds.checkBoxGrp('useTable', q = True, v1=True)
        tableScale = cmds.floatSliderGrp('tableScale', q = True, v = True)
        
        if (useTable == True):
            table = cmds.ls(selection = True, sn=True)
            colliderName = table[0]
            
            collider = cmds.duplicate(colliderName, n = name + 'collider')
            
        else:
            collider = cmds.polyCylinder(r=0.3, h=0.2, sx=20, sy=1, sz=1, ax=[0, 1, 0], cuv=3, ch=1, n = name + 'collider')
            cmds.select(name + 'collider')
            cmds.scale(tableScale, tableScale, tableScale, relative = True)
    
        clothmesh = cmds.polyPlane(w=width, h=width, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
        if(clothShape == 1):    
            clothmesh = cmds.polyCircularize(name + 'clothmesh')
        cmds.select(name + 'clothmesh')
        ratio = height/width
        clothmesh = cmds.scale(ratio, 1, 1, relative = True)
        
        #location
        clothLocation = 0, 5, 0
        if (useTable):
            clothLocation = cmds.objectCenter(collider)
            clothLocation[1] += 5
        cmds.move(clothLocation[0], clothLocation[1], clothLocation[2], r=True)
        
        #add subdivisions to cloth mesh
        clothSubdivide = 2
        if (width > 7 or height >  7):
            clothSubdivide = 3
        print(clothSubdivide)
        clothmesh = cmds.polySmooth(name + 'clothmesh', dv = clothSubdivide, mth=0, sl = 2)
        
        #convert to nCloth
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
        cmds.setAttr(name + 'nRigid1.thickness', 0.0)
        cmds.setAttr(name + 'nCloth1.thickness', 0.02)
        
        time_node = cmds.createNode('time', n = 'time')
        cmds.playbackOptions(minTime=1, maxTime=300, animationStartTime=1, animationEndTime=300)
        cmds.currentTime( query=True )
        
        cmds.connectAttr('time.outTime', name + 'nCloth1.currentTime')
        cmds.connectAttr('time.outTime', name + 'nucleus1.currentTime')
        cmds.connectAttr('time.outTime', name + 'nRigid1.currentTime')
        
        cmds.expression(s=f"{time_node}.outTime = `currentTime -q`;")
       
        #nCloth attribute adjustments
        cmds.setAttr(name + 'nCloth1.lift', 0)
        cmds.setAttr(name + 'nCloth1.friction', 0.5)   
        cmds.setAttr(name + 'nCloth1.stickiness', 0.2)
        cmds.setAttr(name + 'nCloth1.stretchResistance', 120)
        
        shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
                    
        cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
        cmds.select(outMesh)
        cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
        cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
        
    else:
        useCrease = cmds.checkBoxGrp('useCrease', q = True, v1=True)
        
        if (useCrease == True):
            curveObj = cmds.ls(selection = True)
            curveName = curveObj[0]
            #SAYS THAT ^ INDEX IS OUT OF RANGE
            print(curveName)
            cmds.polyCube(n='creaseMesh')
            curveStart = cmds.getAttr(curveName + '.cv[0]')
            print(curveStart[0])
            print(curveStart[1])
            print(curveStart[2])
            cmds.move(curveStart[0], curveStart[1], curveStart[2])
        
        clothmesh = cmds.polyPlane(w=width, h=width, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
        if(clothShape == 1):    
            clothmesh = cmds.polyCircularize(name + 'clothmesh')
        cmds.select(name + 'clothmesh')
        ratio = height/width
        clothmesh = cmds.scale(ratio, 1, 1, relative = True)
        
        
