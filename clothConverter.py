import maya.cmds as cmds
import random
import math
import maya.mel as mel

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
isCurtain = cmds.checkBoxGrp('isCurtain', numberOfCheckBoxes=1, label='Is curtain ')
cmds.separator(height = 10)
cmds.radioButtonGrp('clothShape', label='Cloth Shape ', labelArray2=['Elliptic', 'Rectangular'], numberOfRadioButtons=2)
cmds.floatSliderGrp('width', label='Width ', field = True, min = 1, max = 40, v = 5)
cmds.floatSliderGrp('length', label='Length ', field = True, min = 1, max = 40, v = 5)
useFolds = cmds.checkBoxGrp('useFolds', numberOfCheckBoxes=1, label='Use Selected as Fold(s) ')

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
    isCurtain = cmds.checkBoxGrp('isCurtain', q = True, v1=True)
    clothShape = cmds.radioButtonGrp('clothShape', q = True, sl = True)
    width = cmds.floatSliderGrp('width', q = True, v = True)
    length = cmds.floatSliderGrp('length', q = True, v = True)
    useTable = cmds.checkBoxGrp('useTable', q = True, v1=True)
    useFolds = cmds.checkBoxGrp('useFolds', q = True, v1=True)
        
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
    elif (isCurtain):
        div = width * 4
        print(div)
        cmds.polyCylinder( r=0.15, h=width, sx=20, sy=1, sz=1, ax=[0, 1, 0], rcp=0, cuv=3, ch=1, n=name + 'collider')
        cmds.rotate(0, 0, 90, r=True, os=True, fo=True)
        cmds.polySubdivideFacet(name + 'collider', duv=1, dvv=div, sbm=1, ch=1)
        cmds.select(name + 'collider')
        
    else:
        if (useFolds == True):
            curveObj = cmds.ls(selection = True)
            mergeList = []
            for curveNum in range(len(curveObj)):
                curveName = curveObj[curveNum]
                cmds.select(curveName)
                curveNumName = curveNum + 1
                sweepNode = cmds.sweepMeshFromCurve(oneNodePerCurve=1)
                cmds.rename(sweepNode, f'sweepMesh{name}_{curveNumName}')
                cmds.setAttr(f'sweepMesh{name}_{curveNumName}.scaleProfileX', 0.197368)
                connections = cmds.listConnections(f'sweepMesh{name}_{curveNumName}', source = False)
                cmds.rename(connections[0], name + f'foldsMesh{curveNumName}')
                cmds.select(name + f'foldsMesh{curveNumName}')
                cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
                mergeList.append(name + f'foldsMesh{curveNum + 1}')
            if len(curveObj)>1:
                cmds.polyUnite(mergeList, ch=1, mergeUVSets=1, centerPivot=True, name=name + 'foldsCollider')
            else:
                cmds.rename(name + 'foldsMesh1', name + 'foldsCollider')
            cmds.select(name + 'foldsCollider')
            cmds.move(0, 0.7, 0, r=True)
        #clothmesh
        clothmesh = cmds.polyPlane(w=width, h=width, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
        if(clothShape == 1):    
            clothmesh = cmds.polyCircularize(name + 'clothmesh')
        cmds.select(name + 'clothmesh')
        ratio = length/width
        clothmesh = cmds.scale(ratio, 1, 1, relative = True)
        
        #plane collider
        collider = cmds.polyPlane(w=width, h=width, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'collider')
    
    #cloth shape  
    clothmesh = cmds.polyPlane(w=width, h=width, sx=10, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'clothmesh')
    if(clothShape == 1):    
        clothmesh = cmds.polyCircularize(name + 'clothmesh')
    cmds.select(name + 'clothmesh')
    ratio = length/width
    clothmesh = cmds.scale(ratio, 1, 1, relative = True)
    if isCurtain:
        cmds.rotate(90, 0, -90, r=True, os=True, fo=True)
    
    #cloth location
    clothLocation = [0, 2, 0]
    if (useTable):
        clothLocation = cmds.objectCenter(collider)
        clothLocation[1] += 2
    elif(useFolds):
        clothLocation = cmds.objectCenter(name + 'foldsCollider')
        cmds.select(name + 'collider')
        cmds.move(clothLocation[0], 0, clothLocation[2], r=True)
        clothLocation[1] += 2
    elif(isCurtain):
        cmds.select(name + 'collider')
        moveup = length/2 + 0.2
        cmds.move(0, moveup, 0, r=True)
        clothLocation[1] = clothLocation[1]-2
    cmds.select(name + 'clothmesh')
    cmds.move(clothLocation[0], clothLocation[1], clothLocation[2], r=True)
    
    #add subdivisions to cloth mesh
    
    clothSubdivide = 2
    if (width > 7 or length >  7):
        clothSubdivide = 3
    elif (width > 15 or length > 20):
        clothSubdivide = 4
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
   
    if (useFolds == True):
        cmds.createNode('nRigid', name=name + 'nRigid2')
        cmds.connectAttr(name + 'foldsCollider' + 'Shape.worldMesh[0]', name + 'nRigid2.inputMesh')
        cmds.connectAttr(name + 'nRigid2.currentState', name + 'nucleus1.inputPassive[1]')
        cmds.connectAttr(name + 'nRigid2.startState', name + 'nucleus1.inputPassiveStart[1]')
        cmds.connectAttr(name + 'nucleus1.startFrame', name + 'nRigid2.startFrame')
        cmds.connectAttr('time.outTime', name + 'nRigid2.currentTime')
        cmds.setAttr(name + 'nRigid2.thickness', 0.0)
   
    #nCloth attribute adjustments
    cmds.setAttr(name + 'nCloth1.lift', 0)
    cmds.setAttr(name + 'nCloth1.friction', 0.5)   
    cmds.setAttr(name + 'nCloth1.stickiness', 0.2)
    cmds.setAttr(name + 'nCloth1.stretchResistance', 120)
    
    #nCloth tablecloth adjustments (loosely based on t-shirt preset)
    cmds.setAttr(name + 'nCloth1.friction', 0.3)
    cmds.setAttr(name + 'nCloth1.stickiness', 0.2)
    cmds.setAttr(name + 'nCloth1.stretchResistance', 35)
    cmds.setAttr(name + 'nCloth1.bendAngleDropoff', 0.4)
    #t-shirt is 0.6 
    cmds.setAttr(name + 'nCloth1.pointMass', 0.8)
    cmds.setAttr(name + 'nCloth1.lift', 0.05)
    #t-shirt is 0.1 
    cmds.setAttr(name + 'nCloth1.tangentialDrag', 0.04)
    #t-shirt is 0.8
    cmds.setAttr(name + 'nCloth1.damp', 0.1)
    cmds.setAttr(name + 'nCloth1.scalingRelation', 1)
    
    #avoid intersecting itself | self collide
    cmds.setAttr(name + 'nCloth1.thickness', 0.05)
    cmds.setAttr(name + 'nCloth1.selfCollideWidthScale', 2.0)
    cmds.setAttr(name + 'nCloth1.trappedCheck', 1)
    cmds.setAttr(name + 'nCloth1.selfTrappedCheck', 1)
  
    #curtain folds
    if (isCurtain):
        cmds.currentTime(10)
        cmds.select(name + 'collider')
        cmds.setKeyframe(name + 'collider', attribute='sy', v=1)
        cmds.currentTime(20)
        cmds.setKeyframe(name + 'collider', attribute='sy', v=0.4)
        vtxnums = []
        #if (clothSubdivide == 2):
        vtxnums = ['.vtx[0]', '.vtx[11]', '.vtx[22]', '.vtx[33]', '.vtx[44]', '.vtx[55]', '.vtx[66]', '.vtx[77]', '.vtx[88]', '.vtx[99]', '.vtx[110]', '.vtx[122]',
        '.vtx[143]', '.vtx[164]', '.vtx[185]', '.vtx[206]', '.vtx[227]', '.vtx[248]', '.vtx[269]', '.vtx[290]', '.vtx[311]', '.vtx[443:444]', '.vtx[485:486]', 
        '.vtx[527:528]', '.vtx[569:570]', '.vtx[611:612]', '.vtx[653:654]', '.vtx[695:696]', '.vtx[737:738]', '.vtx[779:780]', '.vtx[821:822]', '.vtx[1685:1688]', 
        '.vtx[1769:1772]', '.vtx[1853:1856]', '.vtx[1937:1940]', '.vtx[2021:2024]', '.vtx[2105:2108]', '.vtx[2189:2192]', '.vtx[2273:2276]', '.vtx[2357:2360]', 
        '.vtx[2441:2444]']
        vtxs = []
        for vtx in vtxnums:
            vtxs.append(f'{name}clothmesh{vtx}')
        cmds.select(vtxs)
        cmds.select(name + 'collider', add=True)
        mel.eval('createNConstraint pointToSurface 0;')
    #material
    shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
                
    cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
    cmds.select(outMesh)
    cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
    cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
        
