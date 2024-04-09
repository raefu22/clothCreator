import maya.cmds as cmds
import random
import math
import maya.mel as mel
import colorsys

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

def showColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterial, q = True)
    cmds.colorSliderGrp(pickColor, edit=True, enable=True)
    cmds.radioButtonGrp(materialType, edit=True, enable=True)
   
def hideColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterial, q = True, vis = False, v1 = False)
    cmds.colorSliderGrp(pickColor, edit=True, enable=False)
    cmds.radioButtonGrp(materialType, edit=True, enable=False)

window = cmds.window(title='Cloth Creator', menuBar = True, width=250)
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
isRibbonBow = cmds.checkBoxGrp('isRibbonBow', numberOfCheckBoxes=1, label='Is ribbon bow ')
cmds.separator(height = 10)
cmds.radioButtonGrp('clothShape', label='Cloth Shape ', labelArray2=['Elliptic', 'Rectangular'], numberOfRadioButtons=2)
cmds.floatSliderGrp('width', label='Width ', field = True, min = 1, max = 40, v = 5)
cmds.floatSliderGrp('length', label='Length ', field = True, min = 1, max = 40, v = 5)
useFolds = cmds.checkBoxGrp('useFolds', numberOfCheckBoxes=1, label='Use Selected as Fold(s) ')

useTable = cmds.checkBoxGrp('useTable', numberOfCheckBoxes=1, label='Use Selected as Table ', onc = hideTableOp, ofc = showTableOp)
tableScale = cmds.floatSliderGrp('tableScale', label='Table Scale ', field = True, min = 1, max = 40, v = 3)
cmds.checkBoxGrp(useTable, edit=True, enable=False)
cmds.floatSliderGrp(tableScale, edit=True, enable=False)



cmds.separator(height = 10)


tieBack= cmds.checkBoxGrp('tieBack', numberOfCheckBoxes=1, label='Tie back curtain ')
cmds.separator(height = 10)

applyMaterial = cmds.checkBoxGrp("applyMaterial", numberOfCheckBoxes=1, label='Apply Material ', v1=False, onc = showColorOp, ofc = hideColorOp)
cmds.separator(height = 5)
materialType = cmds.radioButtonGrp('materialType', label='Material Type ', labelArray4=['Cotton', 'Velvet', 'Satin', 'Plaid'], numberOfRadioButtons=4)
#add a fun/odd/fantastical materials section and have 'Iridescent'
funMat = cmds.checkBoxGrp('funMaterial', numberOfCheckBoxes=1, label='Fun material? ')
cmds.separator(height = 5)
pickColor = cmds.colorSliderGrp('colorpicked', label= 'Color', rgb=(0.272, 0.240, 0.237))
cmds.colorSliderGrp(pickColor, edit=True, enable=False)
cmds.radioButtonGrp(materialType, edit=True, enable=False)
cmds.separator(height = 10)

submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Create Cloth", c="createCloth()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def createCloth():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
    name = inputname
    
    isTablecloth = cmds.checkBoxGrp('isTablecloth', q = True, v1=True)
    isCurtain = cmds.checkBoxGrp('isCurtain', q = True, v1=True)
    isRibbonBow = cmds.checkBoxGrp('isRibbonBow', q = True, v1=True)
    clothShape = cmds.radioButtonGrp('clothShape', q = True, sl = True)
    width = cmds.floatSliderGrp('width', q = True, v = True)
    length = cmds.floatSliderGrp('length', q = True, v = True)
    useTable = cmds.checkBoxGrp('useTable', q = True, v1=True)
    useFolds = cmds.checkBoxGrp('useFolds', q = True, v1=True)
        
    tieBack = cmds.checkBoxGrp('tieBack', q = True, v1=True)    
        
    applyMaterial = cmds.checkBoxGrp('applyMaterial', q = True, v1=True)
    materialType = cmds.radioButtonGrp('materialType', q = True, sl = True)
    maincolor = cmds.colorSliderGrp('colorpicked', q = True, rgbValue = True)
    funMat = cmds.checkBoxGrp('funMaterial', q = True, v1=True)   
     
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
        cmds.polyCylinder( r=0.15, h=width + 4, sx=20, sy=1, sz=1, ax=[0, 1, 0], rcp=0, cuv=3, ch=1, n=name + 'collider')
        cmds.rotate(0, 0, 90, r=True, os=True, fo=True)
        cmds.polySubdivideFacet(name + 'collider', duv=1, dvv=div, sbm=1, ch=1)
        cmds.select(name + 'collider')
    elif (isRibbonBow):
        #base shape
        cmds.polyPlane(w=3, h=1, sx=10, sy=4, ax=[0, 1, 0], cuv=2, ch=1, n= name + 'bow')
        cmds.nonLinear( type='bend', curvature=0.5, n=name + 'bend1')
        cmds.setAttr( name + 'bend1Handle.rotateZ', 90)
        cmds.setAttr(name + 'bend1.curvature', -180)
        cmds.delete(name + 'bow', constructionHistory = True)
        cmds.select(name + 'bow')
        cmds.scale(2.517025, 1, 1, ws= True, r=True)
        vtxnums = ['.vtx[0]', '.vtx[10:11]', '.vtx[21:22]', '.vtx[32:33]', '.vtx[43:44]', '.vtx[54]']
        vtxs = []
        for vtx in vtxnums:
            vtxs.append(f'{name}bow{vtx}')
        cmds.polyMergeVertex(vtxs, d=0.01, am=1, ch=1)
        duplicatecircle = cmds.duplicate(name + 'bow')
        cmds.rename(duplicatecircle, name + 'bowcenter')
        cmds.rotate(0,90,0,ws=True)
        edgenums = ['.e[11]', '.e[31]', '.e[51]', '.e[71]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bow{edge}')
        cmds.select(edges)
        cmds.move(0, -0.8, 0, r=True)
        edgenums = ['.e[1]', '.e[1]', '.e[21]', '.e[41]', '.e[61]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bow{edge}')
        cmds.select(edges)
        cmds.move(0, 0.2, 0, r=True)
        edgenums = ['.e[11]', '.e[31]', '.e[51]', '.e[71]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bow{edge}')
        cmds.select(edges, add=True)
        #0.32
        cmds.scale(1, 1, 0.2, r = True, ws=True, ocp = True)
        cmds.select(name + 'bowcenter')
        cmds.move(0, -0.39, 0, r=True)
        cmds.scale(0.5, 0.5, 0.31, ws=True, r=True)
        #refine base shape
        edgenums = ['.e[66]', '.e[64]','.e[62]','.e[26]', '.e[24]', '.e[22]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bow{edge}')
        cmds.select(edges)
        cmds.move(-0.13, 0, 0, r=True)
        edgenums=['.e[72]', '.e[32]', '.e[34]', '.e[74]', '.e[76]', '.e[36]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bow{edge}')
        cmds.select(edges)
        cmds.move(0.13, 0, 0, r=True)
        
        edgenums = ['.e[72]', '.e[60]', '.e[62]', '.e[64]', '.e[66]', '.e[68]', '.e[70]', '.e[72]', '.e[74]', '.e[76]', '.e[78]', '.e[32]', '.e[20]', '.e[22]', '.e[24]', '.e[26]', '.e[28]', '.e[30]', '.e[32]', '.e[34]', '.e[36]', '.e[38]']
        edges = []
        for edge in edgenums:
            edges.append(f'{name}bowcenter{edge}')
        cmds.select(edges)
        cmds.scale(1, 1, 1.095652, ws=True, r=True, ocp=True)        
        cmds.polyPlane(w=1, h=1, sx=5, sy=10, ax=[0, 1, 0], cuv=2, ch=1, n=name + 'ribbon1')
        cmds.setAttr(name + 'ribbon1.translateX', -0.53)
        cmds.setAttr(name + 'ribbon1.translateY', 0.288)
        cmds.setAttr(name + 'ribbon1.translateZ', -0.146)
        cmds.setAttr(name + 'ribbon1.rotateX', 60)
        cmds.setAttr(name + 'ribbon1.rotateY', 2.651)
        cmds.setAttr(name + 'ribbon1.rotateZ', -90.235)
        cmds.setAttr(name + 'ribbon1.scaleX', 0.378)
        cmds.setAttr(name + 'ribbon1.scaleY', 1)
        cmds.setAttr(name + 'ribbon1.scaleZ', 1.113)
        #cmds.scale(0.473491, 1, 1, ws=True, r=True)
        cmds.select(name + 'bow', name + 'bowcenter')
        cmds.move(0, 0.667064, 0, r=True) 
        cmds.rotate(90, 0, 0, r=True)
        #cmds.move(0, 0, -0.76, name + 'bow.scalePivot', name + 'bow.rotatePivot', r=True)
        cmds.select(name + 'bow')
        cmds.move(0, -0.35, 0.428669, r=True)
        cmds.rename(name + 'bow', name + 'clothmesh')
        cmds.rename(name + 'bowcenter', name + 'collider')
        #cmds.move(0, -0.35, 0.428669, r=True)
        
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
    if not isRibbonBow:
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
    #t-shirt is 0.6 || 1st pass was 0.8, 0.05
    cmds.setAttr(name + 'nCloth1.pointMass', 1.38)
    cmds.setAttr(name + 'nCloth1.lift', 0.27)
    
    
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
    
    #ribbon bow adjustments
    cmds.setAttr(name + 'nCloth1.bendResistance', 23)
    cmds.setAttr(name + 'nCloth1.rigidity', 0.04)
    cmds.setAttr(name + 'nCloth1.pointMass', 2.7)
    
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
        if (tieBack):
            cmds.polyTorus(r=width/2+1, sr=0.1, tw=0, sx=40, sy= 20, ax=[0, 1, 0], cuv=1, ch=1, n = name + 'torusTie')
            cmds.select(name + 'torusTie')
            cmds.move(0, length/2 - length/3, 0) 
            cmds.currentTime(1)
            cmds.select(name + 'torusTie')
            if(cmds.getAttr(name + 'torusTie.sx', k=True) or cmds.getAttr(name + 'torusTie.sx', cb = True)):
                cmds.setKeyframe(name + 'torusTie.sx')
            if(cmds.getAttr(name + 'torusTie.sy', k=True) or cmds.getAttr(name + 'torusTie.sy', ch = True)):
                cmds.setKeyframe(name + 'torusTie.sy')
            if(cmds.getAttr(name + 'torusTie.sz', k=True) or cmds.getAttr(name + 'torusTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'torusTie.sz')
            cmds.currentTime(117)
            cmds.scale(0.183684, 0.183684, 0.183684, ws=True, r=True)
            if(cmds.getAttr(name + 'torusTie.sx', k=True) or cmds.getAttr(name + 'torusTie.sx', cb = True)):
                cmds.setKeyframe(name + 'torusTie.sx')
            if(cmds.getAttr(name + 'torusTie.sy', k=True) or cmds.getAttr(name + 'torusTie.sy', ch = True)):
                cmds.setKeyframe(name + 'torusTie.sy')
            if(cmds.getAttr(name + 'torusTie.sz', k=True) or cmds.getAttr(name + 'torusTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'torusTie.sz')
            cmds.polySmooth(name + 'torusTie', mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
            cmds.createNode('nRigid', name=name + 'torusTienRigid')
            cmds.connectAttr(name + 'torusTie' + 'Shape.worldMesh[0]', name + 'torusTienRigid.inputMesh')
            cmds.connectAttr(name + 'torusTienRigid.currentState', name + 'nucleus1.inputPassive[2]')
            cmds.connectAttr(name + 'torusTienRigid.startState', name + 'nucleus1.inputPassiveStart[2]')
            cmds.connectAttr(name + 'nucleus1.startFrame', name + 'torusTienRigid.startFrame')
            cmds.connectAttr('time.outTime', name + 'torusTienRigid.currentTime')
            cmds.setAttr(name + 'torusTienRigid.thickness', 0.0)
    #hide objects in the scene/visibility
    cmds.setAttr(name + 'clothmesh.visibility', 0)
    
    #material
    shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader') 
    cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
    cmds.select(outMesh)
    cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
    cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
    #get a lighter color for sheen
    hsv = colorsys.rgb_to_hsv(maincolor[0], maincolor[1], maincolor[2])
    saturation = hsv[0] - 0.2
    value = hsv[2] + 0.4
    lighterColor = colorsys.hsv_to_rgb(hsv[0], saturation, value)
    
    if applyMaterial:
        if (funMat):
            cmds.shadingNode('aiThinFilm', asTexture=True, n=name + 'aiThinFilm1')
            cmds.connectAttr(name + 'aiThinFilm1.outColor', name + 'shader.specularColor')
            cmds.setAttr(name + 'shader.baseColor', 0.51, 0.51, 0.51, type='double3')
            cmds.setAttr(name + 'shader.metalness', 0.5)
            cmds.setAttr(name + 'shader.thinFilmThickness', 419.580)
            materialType = 1
        if (materialType == 1):
            cmds.shadingNode('cloth', asTexture=True, n=name + 'clothTex1')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name + 'place2dTexture1') 
            cmds.connectAttr(name + 'place2dTexture1.outUV', name + 'clothTex1.uv')
            cmds.connectAttr(name + 'place2dTexture1.outUvFilterSize', name + 'clothTex1.uvFilterSize')
            cmds.shadingNode('aiLayerRgba', asUtility = True, n=name + 'aiLayerRgba1')
            cmds.connectAttr(name + 'clothTex1.outColor', name + 'aiLayerRgba1.input1')
            cmds.connectAttr(name + 'aiLayerRgba1.outColor', name + 'shader.baseColor')
            cmds.shadingNode('aiColorCorrect', asUtility = True, n=name + 'aiColorCorrect1')
            cmds.connectAttr(name + 'aiLayerRgba1.outColor', name + 'aiColorCorrect1.input')
            cmds.connectAttr(name + 'aiColorCorrect1.outColor', name + 'shader.sheenColor')
            cmds.shadingNode('bump2d', asUtility=True, n=name + 'bump2d1')
            cmds.connectAttr(name + 'clothTex1.outAlpha', name + 'bump2d1.bumpValue')
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'shader.normalCamera')
            #revising values
            cmds.setAttr(name + 'place2dTexture1.repeatU', 250)
            cmds.setAttr(name + 'place2dTexture1.repeatV', 250)
            cmds.setAttr(name + 'clothTex1.uColor', 0.265734, 0.265734, 0.265734, type='double3')
            cmds.setAttr(name + 'clothTex1.vColor', 0.167832, 0.167832, 0.167832, type='double3')
            cmds.setAttr(name + 'aiLayerRgba1.enable2', 1)
            cmds.setAttr(name + 'aiLayerRgba1.input2', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'aiLayerRgba1.operation2', 24)
            cmds.setAttr(name + 'aiColorCorrect1.gamma', 3.0)
            cmds.setAttr(name + 'bump2d1.bumpDepth', 2)
            cmds.setAttr(name + 'shader.specular', 0)
            cmds.setAttr(name + 'shader.sheen', 1)
            cmds.setAttr(name + 'shader.sheenRoughness', 0.35)
        elif (materialType == 2):    
            cmds.setAttr(name + 'shader.specular', 0)
            cmds.setAttr(name + 'shader.baseColor', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'shader.sheen', 1)
            cmds.setAttr(name + 'shader.sheenColor', lighterColor[0], lighterColor[1], lighterColor[2], type='double3')
            cmds.setAttr(name + 'shader.sheenRoughness', 0.2)
        elif (materialType == 3):    
            cmds.setAttr(name + 'shader.specular', 0)
            cmds.shadingNode('aiFacingRatio', asUtility = True, n=name + 'aiFacingRatio1')
            cmds.shadingNode('remapValue', asUtility = True, n=name + 'remapValue1')
            cmds.connectAttr(name + 'aiFacingRatio1.outValue', name + 'remapValue1.inputValue')
            cmds.shadingNode('aiLayerRgba', asUtility = True, n=name + 'aiLayerRgba1')
            cmds.connectAttr(name + 'remapValue1.outValue', name + 'aiLayerRgba1.mix2')
            cmds.connectAttr(name + 'aiLayerRgba1.outColor', name + 'shader.baseColor')
            
            cmds.setAttr(name + 'remapValue1.value[2].value_Position', 0.469565)
            cmds.setAttr(name + 'remapValue1.value[2].value_Interp', 3) 
            cmds.setAttr(name + 'remapValue1.value[2].value_FloatValue', 0.18)
            cmds.setAttr(name + 'remapValue1.value[0].value_Interp', 3)
            cmds.setAttr(name + 'remapValue1.value[1].value_Interp', 3)
            cmds.setAttr(name + 'remapValue1.value[1].value_FloatValue', 0.3)
            cmds.setAttr(name + 'remapValue1.value[3].value_FloatValue', 0.42)
            cmds.setAttr(name + 'remapValue1.value[3].value_Position', 0.634783)
            cmds.setAttr(name + 'remapValue1.value[3].value_Interp', 3)
            cmds.setAttr(name + 'remapValue1.value[4].value_FloatValue', 0.72)
            cmds.setAttr(name + 'remapValue1.value[4].value_Position', 0.730435)
            cmds.setAttr(name + 'remapValue1.value[4].value_Interp', 3)
            cmds.setAttr(name + 'remapValue1.value[5].value_FloatValue', 1)
            cmds.setAttr(name + 'remapValue1.value[5].value_Position', 0.86087)
            cmds.setAttr(name + 'remapValue1.value[5].value_Interp', 3)
            cmds.setAttr(name + 'remapValue1.value[6].value_FloatValue', 0.74)
            cmds.setAttr(name + 'remapValue1.value[6].value_Position', 0.947826)
            cmds.setAttr(name + 'remapValue1.value[6].value_Interp', 3)
            cmds.setAttr(name + 'aiLayerRgba1.input1', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'aiLayerRgba1.enable2', 1)
            cmds.setAttr(name + 'aiLayerRgba1.input2', lighterColor[0], lighterColor[1], lighterColor[2], type='double3')
            cmds.setAttr(name + 'aiLayerRgba1.alphaOperation1', 2)
        elif(materialType == 4):
            cmds.rename(name + 'shader', name + 'horizontalStripes')
            shader = cmds.shadingNode('aiMixShader', asShader = True, n=name + 'aiMixShader1') 
            shader = cmds.shadingNode('aiMixShader', asShader = True, n=name + 'aiMixShader2')
            shader = cmds.shadingNode('aiMixShader', asShader = True, n=name + 'aiMixShader3')  
            cmds.select(outMesh)
            cmds.connectAttr(name + 'aiMixShader3.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
            cmds.shadingNode('ramp', asTexture=True, n = name + 'rampHorizontal')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name+'place2dTexture1')
            cmds.connectAttr(name + 'place2dTexture1.outUV', name + 'rampHorizontal.uv') 
            cmds.connectAttr(name + 'place2dTexture1.outUvFilterSize', name + 'rampHorizontal.uvFilterSize')
            cmds.connectAttr(name + 'rampHorizontal.outColor', name + 'horizontalStripes.baseColor') 
            cmds.setAttr(name + 'rampHorizontal.colorEntryList[0].color', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'rampHorizontal.colorEntryList[1].position', 0.5)
            cmds.setAttr(name + 'rampHorizontal.interpolation', 0)
            hue = hsv[0] + 50
            if (hue > 360):
                hue = hue - 360
            print(hue)
            value = 1
            #complcolor = colorsys.hsv_to_rgb(hue, hsv[1], value)
            complcolor = (maincolor[0], random.uniform(0, 0.5939), random.uniform(0, 0.7131))
            cmds.setAttr(name + 'rampHorizontal.colorEntryList[1].color', complcolor[0], complcolor[1], complcolor[2], type='double3')
            #vertical stripes
            cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'verticalStripes') 
            cmds.shadingNode('ramp', asTexture=True, n = name + 'rampVertical')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name+'place2dTexture2')
            cmds.connectAttr(name + 'place2dTexture2.outUV', name + 'rampVertical.uv') 
            cmds.connectAttr(name + 'place2dTexture2.outUvFilterSize', name + 'rampVertical.uvFilterSize')
            cmds.connectAttr(name + 'rampVertical.outColor', name + 'verticalStripes.baseColor') 
            cmds.setAttr(name + 'place2dTexture2.rotateUV', 90) 
            cmds.setAttr(name + 'rampVertical.colorEntryList[1].position', 0.5)
            cmds.setAttr(name + 'rampVertical.interpolation', 0)
            hue = hsv[0] + 30
            print(hue)
            if (hue > 360):
                hue = hue - 360
            value = 1
            complcolor2 = colorsys.hsv_to_rgb(hue, hsv[1], value)
            cmds.setAttr(name + 'rampVertical.colorEntryList[0].color', complcolor2[0], complcolor2[1], complcolor2[2], type='double3')
            cmds.setAttr(name + 'rampVertical.colorEntryList[1].color', lighterColor[0], lighterColor[1], lighterColor[2], type='double3')
            cmds.setAttr(name + 'place2dTexture1.repeatU', 10)
            cmds.setAttr(name + 'place2dTexture1.repeatV', 10)
            cmds.setAttr(name + 'place2dTexture2.repeatU', 10)
            cmds.setAttr(name + 'place2dTexture2.repeatV', 10)
            #lines vertical
            cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'verticalLines') 
            cmds.shadingNode('ramp', asTexture=True, n = name + 'rampVerticalLines')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name+'place2dTexture4')
            cmds.connectAttr(name + 'place2dTexture4.outUV', name + 'rampVerticalLines.uv') 
            cmds.connectAttr(name + 'place2dTexture4.outUvFilterSize', name + 'rampVerticalLines.uvFilterSize')
            cmds.connectAttr(name + 'rampVerticalLines.outColor', name + 'verticalLines.baseColor') 
            cmds.setAttr(name + 'place2dTexture4.rotateUV', 90) 
            cmds.setAttr(name + 'rampVerticalLines.colorEntryList[1].position', 0.04)
            cmds.setAttr(name + 'rampVerticalLines.interpolation', 0)
            
            cmds.setAttr(name + 'rampVerticalLines.colorEntryList[0].color', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'rampVerticalLines.colorEntryList[1].color', 0, 0, 0, type='double3')
            cmds.setAttr(name + 'place2dTexture4.repeatU', 25)
            cmds.setAttr(name + 'place2dTexture4.repeatV', 25)
            #lines horizontal
            cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'horizontalLines') 
            cmds.shadingNode('ramp', asTexture=True, n = name + 'rampHorizontalLines')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name+'place2dTexture5')
            cmds.connectAttr(name + 'place2dTexture5.outUV', name + 'rampHorizontalLines.uv') 
            cmds.connectAttr(name + 'place2dTexture5.outUvFilterSize', name + 'rampHorizontalLines.uvFilterSize')
            cmds.connectAttr(name + 'rampHorizontalLines.outColor', name + 'horizontalLines.baseColor') 
             
            cmds.setAttr(name + 'rampHorizontalLines.colorEntryList[1].position', 0.04)
            cmds.setAttr(name + 'rampHorizontalLines.interpolation', 0)
            
            cmds.setAttr(name + 'rampHorizontalLines.colorEntryList[0].color', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'rampHorizontalLines.colorEntryList[1].color', 0, 0, 0, type='double3')
            cmds.setAttr(name + 'place2dTexture5.repeatU', 25)
            cmds.setAttr(name + 'place2dTexture5.repeatV', 25)
            #cloth normal
            cmds.shadingNode('cloth', asTexture=True, n=name + 'clothTex1')
            cmds.shadingNode('place2dTexture', asUtility = True, n=name + 'place2dTexture3') 
            cmds.connectAttr(name + 'place2dTexture3.outUV', name + 'clothTex1.uv')
            cmds.connectAttr(name + 'place2dTexture3.outUvFilterSize', name + 'clothTex1.uvFilterSize')
            cmds.shadingNode('bump2d', asUtility=True, n=name + 'bump2d1')
            cmds.connectAttr(name + 'clothTex1.outAlpha', name + 'bump2d1.bumpValue')
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'horizontalStripes.normalCamera')
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'verticalStripes.normalCamera')
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'verticalLines.normalCamera')
            cmds.connectAttr(name + 'bump2d1.outNormal', name + 'horizontalLines.normalCamera')
            cmds.setAttr(name + 'place2dTexture3.repeatU', 250)
            cmds.setAttr(name + 'place2dTexture3.repeatV', 250)
            cmds.setAttr(name + 'clothTex1.uColor', 0.265734, 0.265734, 0.265734, type='double3')
            cmds.setAttr(name + 'clothTex1.vColor', 0.167832, 0.167832, 0.167832, type='double3')
            #general
            cmds.setAttr(name + 'horizontalStripes.sheen', 0.2)
            cmds.setAttr(name + 'horizontalStripes.specularRoughness', 0.51)
            cmds.setAttr(name + 'verticalStripes.sheen', 0.2)
            cmds.setAttr(name + 'verticalStripes.specularRoughness', 0.51)
            cmds.setAttr(name + 'horizontalLines.specularRoughness', 0.6)
            cmds.setAttr(name + 'verticalLines.specularRoughness', 0.6)
            cmds.setAttr(name + 'horizontalLines.sheen', 0.2)
            cmds.setAttr(name + 'verticalLines.sheen', 0.2)
            cmds.connectAttr(name + 'horizontalStripes.outColor', name + 'aiMixShader1.shader1')
            cmds.connectAttr(name + 'verticalStripes.outColor', name + 'aiMixShader1.shader2')
            cmds.connectAttr(name + 'aiMixShader1.outColor', name + 'aiMixShader2.shader1')
            cmds.connectAttr(name + 'verticalLines.outColor', name + 'aiMixShader2.shader2')
            cmds.setAttr(name + 'aiMixShader2.mode', 1)
            cmds.setAttr(name + 'aiMixShader3.mode', 1)
            cmds.connectAttr(name + 'aiMixShader2.outColor', name + 'aiMixShader3.shader1')
            cmds.connectAttr(name + 'horizontalLines.outColor', name + 'aiMixShader3.shader2')
