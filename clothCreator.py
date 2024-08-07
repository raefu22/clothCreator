import maya.cmds as cmds
import random
import math
import maya.mel as mel
import colorsys
import time

#UI window
def showTableclothOp(*args):
    cmds.checkBoxGrp(useTable, edit=True, enable=True)
    cmds.floatSliderGrp(tableScale, edit=True, enable=True)
    cmds.radioButtonGrp(clothShape, edit=True, enable=True)

def hideTableclothOp(*args):
    cmds.checkBoxGrp(useTable, edit=True, enable=False)
    cmds.floatSliderGrp(tableScale, edit=True, enable=False)
    cmds.radioButtonGrp(clothShape, edit=True, enable=False)

def hideTableOp(*args):
    showCheckbox = cmds.checkBoxGrp(useTable, q = True)
    cmds.floatSliderGrp(tableScale, edit=True, enable=False)
   
def showTableOp(*args):
    showCheckbox = cmds.checkBoxGrp(useTable, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(tableScale, edit=True, enable=True)

def showCurtainOp(*args):
    cmds.checkBoxGrp(tieBack, edit=True, enable=True)
    cmds.checkBoxGrp(curtainRod, edit=True, enable=True)
    cmds.optionMenuGrp(curtainType, edit=True, enable = True)

def hideCurtainOp(*args):
    cmds.checkBoxGrp(tieBack, edit=True, enable=False)
    cmds.checkBoxGrp(curtainRod, edit=True, enable=False)
    cmds.optionMenuGrp(curtainType, edit=True, enable = False)

def showTieOp(*args):
    showCheckbox = cmds.checkBoxGrp(tieBack, q = True, vis = False, v1 = False)
    cmds.checkBoxGrp(tieWithBow, edit=True, enable=True)
    curtainCurr = cmds.optionMenuGrp('curtainType', q = True, v = True)
    if curtainCurr == 'Single Panel':
        cmds.optionMenuGrp(singleTieLocation, edit=True, enable = True)
    else:
        cmds.optionMenuGrp(pairTieLocation, edit=True, enable = True)

def hideTieOp(*args):
    showCheckbox = cmds.checkBoxGrp(tieBack, q = True)
    cmds.checkBoxGrp(tieWithBow, edit=True, enable=False)
    cmds.optionMenuGrp(singleTieLocation, edit=True, enable = False)
    cmds.optionMenuGrp(pairTieLocation, edit=True, enable = False)

def showColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterial, q = True)
    cmds.colorSliderGrp(pickColor, edit=True, enable=True)
    cmds.optionMenuGrp(materialType, edit=True, enable=True)
   
def hideColorOp(*args):
    showCheckbox = cmds.checkBoxGrp(applyMaterial, q = True, vis = False, v1 = False)
    cmds.colorSliderGrp(pickColor, edit=True, enable=False)
    cmds.optionMenuGrp(materialType, edit=True, enable=False)
    
def showRibbonOp(*args):
    cmds.floatSliderGrp(clothwidth, edit=True, enable=False)
    cmds.floatSliderGrp(clothlength, edit=True, enable=False)
    
def hideRibbonOp(*args):
    cmds.floatSliderGrp(clothwidth, edit=True, enable=True)
    cmds.floatSliderGrp(clothlength, edit=True, enable=True)
    
def showRegularOp(*args):
    cmds.checkBoxGrp(useFolds, edit=True, enable=True)

def hideRegularOp(*args):
    cmds.checkBoxGrp(useFolds, edit=True, enable=False)
    
def showSeed(*args):
    cmds.floatSliderGrp(seed, edit=True, enable=True)
    
def hideSeed(*args):
    cmds.floatSliderGrp(seed, edit=True, enable=False)
    
def curtainTypeChange(item, *args):
    tieCurr = cmds.checkBoxGrp('tieBack', q = True, v1 = True)
    if (item =='Single Panel' and tieCurr):
        cmds.optionMenuGrp(singleTieLocation, edit=True, enable = True)
        cmds.optionMenuGrp(pairTieLocation, edit=True, enable = False)
    elif tieCurr:
        cmds.optionMenuGrp(singleTieLocation, edit=True, enable = False)
        cmds.optionMenuGrp(pairTieLocation, edit=True, enable = True)
def typeChange(item, *args):
    if (item =='Tablecloth'):
        showTableclothOp()
        hideCurtainOp()
        hideRibbonOp()
        hideRegularOp()
    elif (item == 'Curtain'):
        hideTableclothOp()
        showCurtainOp()
        hideRibbonOp()
        hideRegularOp()
    elif (item == 'Ribbon Bow'):
        hideTableclothOp()
        hideCurtainOp()
        showRibbonOp()
        hideRegularOp()
    elif (item == 'Regular'):
        hideTableclothOp()
        hideCurtainOp()
        hideRibbonOp()
        showRegularOp()
        
def materialTypeChange(item, *args):
    if (item =='Plaid'):
        showSeed()
    else:
        hideSeed()

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
clothType = cmds.optionMenuGrp('clothType', label='Type of Cloth ', cc=typeChange)
cmds.menuItem(label = 'Tablecloth')
cmds.menuItem(label = 'Curtain')
cmds.menuItem(label = 'Ribbon Bow')
cmds.menuItem(label = 'Regular')

cmds.separator(height = 10)
clothShape = cmds.radioButtonGrp('clothShape', label='Cloth Shape ', labelArray2=['Elliptic', 'Rectangular'], numberOfRadioButtons=2)
clothwidth = cmds.floatSliderGrp('width', label='Width ', field = True, min = 1, max = 40, v = 5)
clothlength = cmds.floatSliderGrp('length', label='Length ', field = True, min = 1, max = 40, v = 5)

cmds.separator(height = 10)
useFolds = cmds.checkBoxGrp('useFolds', numberOfCheckBoxes=1, label='Use Selected as Fold(s) ')
cmds.checkBoxGrp(useFolds, edit=True, enable=False)
cmds.separator(height = 10)
useTable = cmds.checkBoxGrp('useTable', numberOfCheckBoxes=1, label='Use Selected as Table ', onc = hideTableOp, ofc = showTableOp)
tableScale = cmds.floatSliderGrp('tableScale', label='Table Scale ', field = True, min = 1, max = 40, v = 3)

cmds.separator(height = 10)

curtainType = cmds.optionMenuGrp('curtainType', label='Curtain Type ', cc = curtainTypeChange)
cmds.menuItem(label = 'Single Panel')
cmds.menuItem(label = 'Panel Pair')
cmds.menuItem(label = 'Complete Set')
cmds.optionMenuGrp(curtainType, edit=True, enable=False)

tieBack = cmds.checkBoxGrp('tieBack', numberOfCheckBoxes=1, label='Tie Back Curtain ', onc = showTieOp, ofc = hideTieOp)
singleTieLocation = cmds.optionMenuGrp('singleTieLocation', label='Single Curtain Tie Location ')
cmds.menuItem(label = 'Center')
cmds.menuItem(label = 'Left')
cmds.menuItem(label = 'Right')
pairTieLocation = cmds.optionMenuGrp('pairTieLocation', label='Pair Curtains Tie Location ')
cmds.menuItem(label = 'Center')
cmds.menuItem(label = 'Side')
cmds.optionMenuGrp(singleTieLocation, edit=True, enable=False)
cmds.optionMenuGrp(pairTieLocation, edit=True, enable=False)

tieWithBow = cmds.checkBoxGrp('tieWithBow', numberOfCheckBoxes=1, label='Tie with Bow ')

curtainRod = cmds.checkBoxGrp('curtainRod', numberOfCheckBoxes=1, label='Create a Curtain Rod ')
cmds.checkBoxGrp(tieBack, edit=True, enable=False)
cmds.checkBoxGrp(tieWithBow, edit=True, enable=False)
cmds.checkBoxGrp(curtainRod, edit=True, enable=False)
cmds.separator(height = 10)

applyMaterial = cmds.checkBoxGrp("applyMaterial", numberOfCheckBoxes=1, label='Apply Material ', v1=False, onc = showColorOp, ofc = hideColorOp)
cmds.separator(height = 5)
materialType = cmds.optionMenuGrp('materialType', label='Material Type ', cc = materialTypeChange)
cmds.menuItem(label = 'Cotton')
cmds.menuItem(label = 'Velvet')
cmds.menuItem(label = 'Satin')
cmds.menuItem(label = 'Plaid')
cmds.optionMenuGrp('materialType', edit=True, enable=False)
#materialType = cmds.radioButtonGrp('materialType', label='Material Type ', labelArray4=['Cotton', 'Velvet', 'Satin', 'Plaid'], numberOfRadioButtons=4)
#add a fun/odd/fantastical materials section and have 'Iridescent'
funMat = cmds.checkBoxGrp('funMaterial', numberOfCheckBoxes=1, label='Fun material? ')
cmds.separator(height = 5)
pickColor = cmds.colorSliderGrp('colorpicked', label= 'Color', rgb=(0.272, 0.240, 0.237))
cmds.colorSliderGrp(pickColor, edit=True, enable=False)
seed = cmds.floatSliderGrp('seed', label='Seed For Other Color ', field = True, min = 0, max = 40, v = 3)
cmds.floatSliderGrp('seed', edit=True, enable=False)
#cmds.radioButtonGrp(materialType, edit=True, enable=False)
cmds.separator(height = 10)

submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Create Cloth", c="clothmain()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def createCloth(name, isCurtainBow, typeOfCurtain):
    clothType = cmds.optionMenuGrp('clothType', q = True, v = True)
    isTablecloth = False
    isCurtain = False
    isRibbonBow = False
    if (clothType == 'Tablecloth'):
        isTablecloth = True
    elif (clothType == 'Curtain'):
        isCurtain = True
    elif (clothType == 'Ribbon Bow'):
        isRibbonBow = True
        
    clothShape = cmds.radioButtonGrp('clothShape', q = True, sl = True)
    width = cmds.floatSliderGrp('width', q = True, v = True)
    length = cmds.floatSliderGrp('length', q = True, v = True)
    useTable = cmds.checkBoxGrp('useTable', q = True, v1=True)
    useFolds = cmds.checkBoxGrp('useFolds', q = True, v1=True)
        
    tieBack = cmds.checkBoxGrp('tieBack', q = True, v1=True)
    curtainRod = cmds.checkBoxGrp('curtainRod', q = True, v1=True)    
    if ('pair2' in typeOfCurtain):
        curtainRod = False    
    if ('top' in typeOfCurtain):
        tieBack = False    
        width = width * 2.25
        length = length/6
        curtainRod = False
    applyMaterial = cmds.checkBoxGrp('applyMaterial', q = True, v1=True)
    materialType = cmds.optionMenuGrp('materialType', q = True, v = True)
    #= cmds.radioButtonGrp('materialType', q = True, sl = True)
    maincolor = cmds.colorSliderGrp('colorpicked', q = True, rgbValue = True)
    funMat = cmds.checkBoxGrp('funMaterial', q = True, v1=True)   
    seed =  cmds.floatSliderGrp('seed', q = True, v = True)
     
    #creates cloth assets 
    if (isCurtainBow):
        isCurtain = False
        isRibbonBow = True
        curtainRod = False
     
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
        if ('right' in typeOfCurtain):
            cmds.rotate(180, 0, 0, r=True, os=True, fo=True)
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
        cmds.softSelect(sse = 0)
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
        cmds.select(name + 'bow', name + 'bowcenter')
        cmds.move(0, 0.667064, 0, r=True) 
        cmds.rotate(90, 0, 0, r=True)
        cmds.select(name + 'bow')
        cmds.move(0, -0.35, 0.428669, r=True)
        cmds.rename(name + 'bow', name + 'clothmesh')
        bowcentercollider = cmds.rename(name + 'bowcenter', name + 'collider')
        cmds.select(name + 'ribbon1')
        cmds.scale(0.258665, 1, 1.733546, ws=True, r=True)
        cmds.scale(0.5, 1, 1, ws=True, r=True)
        cmds.move(0, -0.08, 0, r=True)
        cmds.rotate(0, -90, 0, r=True, os=True, fo=True)
        cmds.move(-0.8, 0, -0.242509, r=True)
        #ribbon2
        cmds.duplicate(name + 'ribbon1', n=name + 'ribbon2')
        cmds.select(name + 'ribbon2')
        cmds.rotate(0, 180, 0, r=True, os=True, fo=True)
        cmds.move(1.61, 0, 0, r=True)
        cmds.rotate(35.685583, 0, 0, r=True, os=True, fo=True)
        cmds.move(0, -0.36, 0, r=True)
        
        cmds.select(name + 'ribbon1')
        cmds.rotate(35.685583, 0, 0, r=True, os=True, fo=True)
        cmds.move(0, -0.36, 0, r=True)
        bowCenterMesh = cmds.polyTorus(r=width/2+1, sr=1.2, tw=0, sx=20, sy=20, ax=[0, 1, 0], cuv=1, ch=1, n=name + 'bowCenter')
        cmds.rotate(0,0,-90, r=True, os=True, fo=True)
        cmds.scale(0.24, 0.06, 0.06, r=True, ws=True)
        cmds.move(0, 0.27, -0.243, r=True) 
        
        if (isCurtainBow):
            cmds.select([name + 'clothmesh', name + 'collider', name + 'ribbon1', name + 'ribbon2', name + 'bowCenter'])
            
            cmds.move(0, length/2 - length/3 -0.25, 0.8, r=True)
            cmds.group( name + 'clothmesh', name + 'collider', name + 'ribbon1', name + 'ribbon2', name + 'bowCenter', n=name+'theCurtainBow')
            cmds.select(name + 'theCurtainBow')
            cmds.scale(0.5, 0.5, 0.5, relative = True)
            cmds.select(name + 'ribbon1')
            cmds.move(0, 0, 0, r=True)
            cmds.select(name + 'ribbon2')
            cmds.move(0, 0.03, 0, r=True)
            cmds.select(name + 'theCurtainBow')
            if ('single' in typeOfCurtain and 'left' in typeOfCurtain):
                cmds.move(-width/5, 0, 0, r=True, os=True, wd=True)
            elif ('single' in typeOfCurtain and 'right' in typeOfCurtain):
                cmds.move(width/5, 0, 0, r=True, os=True, wd=True)    
            elif 'pair1' in typeOfCurtain:
                if 'left' in typeOfCurtain:
                    cmds.move(-width/5, 0, 0, r=True, os=True, wd=True)
                    cmds.move(-width/3 + 0.2, 0, 0, r=True, os=True, wd=True) 
                else:
                    cmds.move(-width/4, 0, 0, r=True, os=True, wd=True) 
            elif 'pair2' in typeOfCurtain:
                if 'right' in typeOfCurtain:
                    cmds.move(width/5, 0, 0, r=True, os=True, wd=True)
                    cmds.move(width/3 - 0.2, 0, 0, r=True, os=True, wd=True)
                else:
                    cmds.move(width/4, 0, 0, r=True, os=True, wd=True) 
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
    
    #uvs
    cmds.u3dUnfold(name + 'clothmesh', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
    cmds.u3dLayout(name + 'clothmesh', res=256, scl=1, box=[0, 1, 0, 1])

    #convert to nCloth
    cmds.createNode('nRigid', name=name + 'nRigid1')
    
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
    if (isRibbonBow):
        cmds.setAttr(name + 'nCloth1.bendResistance', 23)
        cmds.setAttr(name + 'nCloth1.rigidity', 0.04)
        cmds.setAttr(name + 'nCloth1.pointMass', 2.7)
    
        #connect bow to center
        vtxnums = ['.vtx[121]', '.vtx[322]', '.vtx[5]', '.vtx[15]', '.vtx[25]', '.vtx[35]', '.vtx[45]', '.vtx[61]', '.vtx[81]', '.vtx[101]', '.vtx[121]', '.vtx[202:203]', '.vtx[242:243]', '.vtx[282:283]', '.vtx[322:323]',
        '.vtx[302]', '.vtx[30]', '.vtx[0]', '.vtx[10]', '.vtx[20]', '.vtx[30]', '.vtx[40]', '.vtx[51]', '.vtx[71]', '.vtx[91]', '.vtx[111]', '.vtx[182:183]', '.vtx[222:223]', '.vtx[262:263]', '.vtx[302:303]']
        vtxs = []
        for vtx in vtxnums:
            vtxs.append(f'{name}clothmesh{vtx}')
        cmds.select(vtxs)
        cmds.select(name + 'collider', add=True)
        mel.eval('createNConstraint pointToSurface 0;')
        
        #squeeze center
        if (isCurtainBow):
            cmds.currentTime(117)
        else:
            cmds.currentTime(0)
        cmds.select(name + 'collider')
        cmds.setKeyframe(name + 'collider', attribute='sx', v=1)
        if (isCurtainBow):
            cmds.currentTime(142)
        else:
            cmds.currentTime(25)
        cmds.setKeyframe(name + 'collider', attribute='sx', v=0.6)
        
        #ribbon
        cmds.createNode('nCloth', name= name + 'nCloth2')
        cmds.connectAttr(name + 'nucleus1.outputObjects[1]', name + 'nCloth2.nextState')
        cmds.connectAttr(name + 'ribbon1Shape.worldMesh[0]', name + 'nCloth2.inputMesh')
        cmds.connectAttr(name + 'nucleus1.startFrame', name + 'nCloth2.startFrame')
        cmds.connectAttr(name + 'nCloth2.startState', name + 'nucleus1.inputActiveStart[1]')
        cmds.connectAttr(name + 'nCloth2.currentState', name + 'nucleus1.inputActive[1]')
        outRibbon1 = cmds.createNode('mesh', n = name + 'cloth2')
        cmds.connectAttr(name + 'nCloth2.outputMesh', name + 'cloth2.inMesh')
        cmds.connectAttr('time.outTime', name + 'nCloth2.currentTime')
        
        vtxnums = ['.vtx[60]', '.vtx[61]', '.vtx[62]', '.vtx[63]', '.vtx[64]', '.vtx[65]']
        vtxs = []
        for vtx in vtxnums:
            vtxs.append(f'{name}ribbon1{vtx}')
        cmds.select(vtxs)
        cmds.select(name + 'collider', add=True)
        mel.eval('createNConstraint pointToSurface 0;')
        
        #ribbon2
        cmds.createNode('nCloth', name= name + 'nCloth3')
        cmds.connectAttr(name + 'nucleus1.outputObjects[2]', name + 'nCloth3.nextState')
        cmds.connectAttr(name + 'ribbon2Shape.worldMesh[0]', name + 'nCloth3.inputMesh')
        cmds.connectAttr(name + 'nucleus1.startFrame', name + 'nCloth3.startFrame')
        cmds.connectAttr(name + 'nCloth3.startState', name + 'nucleus1.inputActiveStart[2]')
        cmds.connectAttr(name + 'nCloth3.currentState', name + 'nucleus1.inputActive[2]')
        outRibbon2 = cmds.createNode('mesh', n = name + 'cloth3')
        cmds.connectAttr(name + 'nCloth3.outputMesh', name + 'cloth3.inMesh')
        cmds.connectAttr('time.outTime', name + 'nCloth3.currentTime')
        
        vtxnums = ['.vtx[60]', '.vtx[61]', '.vtx[62]', '.vtx[63]', '.vtx[64]', '.vtx[65]']
        vtxs = []
        for vtx in vtxnums:
            vtxs.append(f'{name}ribbon2{vtx}')
        cmds.select(vtxs)
        cmds.select(name + 'collider', add=True)
        mel.eval('createNConstraint pointToSurface 0;')
        
        #ncloth attributes for ribbons
        cmds.setAttr(name + 'nCloth2.thickness', 0.05)
        cmds.setAttr(name + 'nCloth3.thickness', 0.05)
        cmds.setAttr(name + 'nCloth2.pointMass', 0.61)
        cmds.setAttr(name + 'nCloth3.pointMass', 0.61)
        
        if (isCurtainBow):
            cmds.setAttr(name + 'nucleus1.startFrame', 117)
            '''
            #cmds.select(outRibbon1, outRibbon2, outMesh)
            
            cmds.dgdirty(allPlugs=True)
            cmds.refresh(force=True)
            cmds.currentTime(131)
            cmds.delete(outRibbon1, constructionHistory = True)
            cmds.delete(outRibbon2, constructionHistory = True)
            cmds.delete(outMesh, constructionHistory = True)
            cmds.currentTime(0)
            '''
    #curtain folds
    if (isCurtain):
        cmds.currentTime(10)
        cmds.select(name + 'collider')
        cmds.setKeyframe(name + 'collider', attribute='sy', v=1)
        if ('top' in typeOfCurtain):
            cmds.currentTime(90)
            if 'side' in typeOfCurtain:
                cmds.setKeyframe(name + 'collider', attribute='sy', v=0.6)
            else:
                cmds.setKeyframe(name + 'collider', attribute='sy', v=0.45)
        else:
            cmds.currentTime(20)
            cmds.setKeyframe(name + 'collider', attribute='sy', v=0.4)    
        vtxnums = []
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
        constraint1Name = mel.eval('createNConstraint pointToSurface 0;')
        if 'center' not in typeOfCurtain:
            cmds.setAttr(constraint1Name[0] + '.connectionUpdate', 1)
            cmds.setAttr(name + 'nucleus1.maxCollisionIterations', 9)
        if (tieBack):
            cmds.polyTorus(r=width/2+1, sr=0.1, tw=0, sx=40, sy= 20, ax=[0, 1, 0], cuv=1, ch=1, n = name + 'torusTie')
            clothliketie = cmds.polyPipe(r=width/2+1, h=2, t=0.1, sa=20, sh=1, sc=4, ax=[0, 1, 0], cuv=1, rcp=0, ch=1, n= name + 'flatTie')
            cmds.move(0, length/2 - length/3, 0) 
            cmds.rotate(19, 0, 0, r=True, os=True, fo=True) 
            cmds.currentTime(1)
            cmds.select(name + 'flatTie')
            if(cmds.getAttr(name + 'flatTie.sx', k=True) or cmds.getAttr(name + 'flatTie.sx', cb = True)):
                cmds.setKeyframe(name + 'flatTie.sx')
            if(cmds.getAttr(name + 'flatTie.sy', k=True) or cmds.getAttr(name + 'flatTie.sy', ch = True)):
                cmds.setKeyframe(name + 'flatTie.sy')
            if(cmds.getAttr(name + 'flatTie.sz', k=True) or cmds.getAttr(name + 'flatTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'flatTie.sz')
            if 'center' not in typeOfCurtain:
                cmds.currentTime(85)
                if(cmds.getAttr(name + 'flatTie.tx', k=True) or cmds.getAttr(name + 'flatTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'flatTie.tx')
            cmds.currentTime(117)
            cmds.scale(0.183684, 0.183684, 0.183684, ws=True, r=True)
            if(cmds.getAttr(name + 'flatTie.sx', k=True) or cmds.getAttr(name + 'flatTie.sx', cb = True)):
                cmds.setKeyframe(name + 'flatTie.sx')
            if(cmds.getAttr(name + 'flatTie.sy', k=True) or cmds.getAttr(name + 'flatTie.sy', ch = True)):
                cmds.setKeyframe(name + 'flatTie.sy')
            if(cmds.getAttr(name + 'flatTie.sz', k=True) or cmds.getAttr(name + 'flatTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'flatTie.sz')
            if 'left' in typeOfCurtain:
                cmds.currentTime(125)
                #-1.028
                cmds.setAttr(name + 'flatTie.translateX', -width/5)
                if(cmds.getAttr(name + 'flatTie.tx', k=True) or cmds.getAttr(name + 'flatTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'flatTie.tx')
            if 'right' in typeOfCurtain:
                cmds.currentTime(125)
                cmds.setAttr(name + 'flatTie.translateX', width/5)
                if(cmds.getAttr(name + 'flatTie.tx', k=True) or cmds.getAttr(name + 'flatTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'flatTie.tx')
            #uvs
            edgenums = []
            edgenums = ['.e[203]', '.e[223]', '.e[243]', '.e[263]', '.e[283]', '.e[303]', '.e[323]', '.e[343]', '.e[363]', '.e[383]']
            edges = []
            for edge in edgenums:
                edges.append(f'{name}flatTie{edge}')
            cmds.polyMapCut(edges, ch=1)
            
            cmds.u3dUnfold(name + 'flatTie', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
            mel.eval('texOrientShells;')
            cmds.u3dLayout(name + 'flatTie', res=256, scl=1, box=[0, 1, 0, 1])
            cmds.polySmooth(name + 'flatTie', mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
            cmds.select(name + 'torusTie')
            cmds.move(0, length/2 - length/3, 0) 
            cmds.rotate(19, 0, 0, r=True, os=True, fo=True) 
            cmds.currentTime(1)
            cmds.select(name + 'torusTie')
            if(cmds.getAttr(name + 'torusTie.sx', k=True) or cmds.getAttr(name + 'torusTie.sx', cb = True)):
                cmds.setKeyframe(name + 'torusTie.sx')
            if(cmds.getAttr(name + 'torusTie.sy', k=True) or cmds.getAttr(name + 'torusTie.sy', ch = True)):
                cmds.setKeyframe(name + 'torusTie.sy')
            if(cmds.getAttr(name + 'torusTie.sz', k=True) or cmds.getAttr(name + 'torusTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'torusTie.sz')
            if 'center' not in typeOfCurtain:
                cmds.currentTime(85)
                if(cmds.getAttr(name + 'torusTie.tx', k=True) or cmds.getAttr(name + 'torusTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'torusTie.tx')
            cmds.currentTime(117)
            cmds.scale(0.183684, 0.183684, 0.183684, ws=True, r=True)
            if(cmds.getAttr(name + 'torusTie.sx', k=True) or cmds.getAttr(name + 'torusTie.sx', cb = True)):
                cmds.setKeyframe(name + 'torusTie.sx')
            if(cmds.getAttr(name + 'torusTie.sy', k=True) or cmds.getAttr(name + 'torusTie.sy', ch = True)):
                cmds.setKeyframe(name + 'torusTie.sy')
            if(cmds.getAttr(name + 'torusTie.sz', k=True) or cmds.getAttr(name + 'torusTie.sz', ch=True) ):
                cmds.setKeyframe(name + 'torusTie.sz')
            if 'left' in typeOfCurtain:
                cmds.currentTime(125)
                cmds.setAttr(name + 'torusTie.translateX', -width/5)
                if(cmds.getAttr(name + 'torusTie.tx', k=True) or cmds.getAttr(name + 'torusTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'torusTie.tx')
            if 'right' in typeOfCurtain:
                cmds.currentTime(125)
                cmds.setAttr(name + 'torusTie.translateX', width/5)
                if(cmds.getAttr(name + 'torusTie.tx', k=True) or cmds.getAttr(name + 'torusTie.tx', ch=True) ):
                    cmds.setKeyframe(name + 'torusTie.tx')
            cmds.polySmooth(name + 'torusTie', mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
            cmds.createNode('nRigid', name=name + 'torusTienRigid')
            cmds.connectAttr(name + 'torusTie' + 'Shape.worldMesh[0]', name + 'torusTienRigid.inputMesh')
            cmds.connectAttr(name + 'torusTienRigid.currentState', name + 'nucleus1.inputPassive[2]')
            cmds.connectAttr(name + 'torusTienRigid.startState', name + 'nucleus1.inputPassiveStart[2]')
            cmds.connectAttr(name + 'nucleus1.startFrame', name + 'torusTienRigid.startFrame')
            cmds.connectAttr('time.outTime', name + 'torusTienRigid.currentTime')
            cmds.setAttr(name + 'torusTienRigid.thickness', 0.0)
        if ('top' in typeOfCurtain):
             cmds.setAttr(constraint1Name[0] + '.connectionUpdate', 0)
        #curtain rod
        if(curtainRod):
            rodWidth = width + 0.4
            if 'single' in typeOfCurtain:
                rodWidth = width/3 * 2 - 0.2
            else:
                rodWidth = width * 2.25 * 0.6
                if 'left' in typeOfCurtain:
                    rodWidth = width/2 * 3
                    #* 2.25 * 0.45
            rod = cmds.polyCube(w=rodWidth, h=1, d=1, sx=3, sy=1, sz=1, ax=[0, 1, 0], cuv=4, ch=1, n= name + 'rod')
            cmds.scale(1, 0.5, 0.5, r=True)
            edgenums = ['.e[18]', '.e[14]', '.e[22]', '.e[26]']
            edges = []
            for edge in edgenums:
                edges.append(f'{name}rod{edge}')
            cmds.select(edges)
            cmds.move(1.8, 0, 0, r=True)
            edgenums = ['.e[17]', '.e[13]', '.e[21]', '.e[25]']
            edges = []
            for edge in edgenums:
                edges.append(f'{name}rod{edge}')
            cmds.select(edges)
            cmds.move(-1.8, 0, 0, r=True)
            cmds.select(name + 'rod')
            cmds.scale(1, 0.43, 0.4328024, ws=True, r=True) 
            cmds.move(0, length/2 - 0.2, -0.4, r=True)
            cmds.select(name + 'rod.f[13]')
            cmds.polyExtrudeFacet(name + 'rod.f[13]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.03)
            cmds.polyExtrudeFacet(name + 'rod.f[13]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.03)
            cmds.scale(1.35, 1.35, 1.35, cs=True, r=True) 
            cmds.polyExtrudeFacet(name + 'rod.f[13]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.05)
            cmds.scale(1.35, 1.35, 1.35, cs=True, r=True) 
            cmds.polyExtrudeFacet(name + 'rod.f[13]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.15)
            cmds.polyExtrudeFacet(name + 'rod.f[13]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.11)
            cmds.scale(0.6, 0.6, 0.6, cs=True, r=True) 
            cmds.select(name + 'rod.f[12]')
            cmds.polyExtrudeFacet(name + 'rod.f[12]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.03)
            cmds.polyExtrudeFacet(name + 'rod.f[12]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.03)
            cmds.scale(1.35, 1.35, 1.35, cs=True, r=True) 
            cmds.polyExtrudeFacet(name + 'rod.f[12]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.05)
            cmds.scale(1.35, 1.35, 1.35, cs=True, r=True) 
            cmds.polyExtrudeFacet(name + 'rod.f[12]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.15)
            cmds.polyExtrudeFacet(name + 'rod.f[12]', constructionHistory=1, keepFacesTogether=1, pvx=-2.700000048, pvy=5.1, pvz=-0.39, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, ltz = 0.11)
            cmds.scale(0.6, 0.6, 0.6, cs=True, r=True) 
            cmds.polySmooth(name + 'rod', mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=1, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
           
            if rodWidth < 5:
                edgenums = ['.e[216]', '.e[219]', '.e[224]', '.e[227:228]', '.e[231]', '.e[236]', '.e[239:240]', '.e[243]', '.e[248]', '.e[251:252]', '.e[255]', '.e[260]', '.e[263]']
                edges = []
                for edge in edgenums:
                    edges.append(f'{name}rod{edge}')
                cmds.select(edges)
                cmds.polyDelEdge(cv=True, ch=1)
            
            cmds.move(0, 0, -0.22, r=True, os=True, wd=True)
          
    #hide objects in the scene/visibility
    cmds.setAttr(name + 'clothmesh.visibility', 0)
    if (isCurtain):
        cmds.setAttr(name + 'collider.visibility', 0)
        if (tieBack):
            cmds.setAttr(name + 'torusTie.visibility', 0)
    if (isRibbonBow):
        cmds.setAttr(name + 'ribbon1.visibility', 0)
        cmds.setAttr(name + 'ribbon2.visibility', 0)
        cmds.setAttr(name + 'collider.visibility', 0)
    cmds.setAttr(name + 'nCloth1.collisionLayer', 1)
    
    if (isCurtain):
    #if panel pair curtain -> group
    #if 'pair' in typeOfCurtain:
        if tieBack:
            cmds.group(name + 'collider', name + 'clothmesh', outMesh, name + 'flatTie', name + 'torusTie', n = name + 'panelcurtain')
        else:
            cmds.group(name + 'collider', name + 'clothmesh', outMesh, n = name + 'panelcurtain')
        cmds.select(name + 'panelcurtain')
        if 'pair1' in typeOfCurtain:
            if 'left' in typeOfCurtain:
                cmds.move(-width/3 + 0.2, 0, 0, r=True, os=True, wd=True) 
            else:
                cmds.move(-width/4, 0, 0, r=True, os=True, wd=True) 
        elif 'pair2' in typeOfCurtain:
            if 'right' in typeOfCurtain:
                cmds.move(width/3 - 0.2, 0, 0, r=True, os=True, wd=True)
            else:
                cmds.move(width/4, 0, 0, r=True, os=True, wd=True) 
        elif 'top' in typeOfCurtain:
            cmds.move(0, 0, 1*width/11.25, r=True, os=True, wd=True) 
            cmds.move(0, length*3 - (length*0.5), 0, r=True, os=True, wd=True) 
    
    #prevent curtain cutting through other colliders    
    cmds.setAttr(name + 'nRigid1.trappedCheck', 1)
    
    #material
    if (curtainRod):
        shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'rodshader') 
        cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'rodaiSurfaceShader' + name + 'SG')
        cmds.select(rod)
        cmds.hyperShade(assign = 'rodaiSurfaceShader' + name + 'SG')
        cmds.connectAttr(name + 'rodshader.outColor', 'rodaiSurfaceShader' + name +'SG.surfaceShader', f=True)
        cmds.setAttr(name + 'rodshader.baseColor', 0.5, 0.5, 0.5, type='double3')
        cmds.setAttr(name + 'rodshader.metalness', 1)
        cmds.setAttr(name + 'rodshader.diffuseRoughness', 0.1)
        
    shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader') 
    cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
    cmds.select(outMesh)
    if (isRibbonBow):
        cmds.select(outRibbon1, outRibbon2, bowcentercollider, bowCenterMesh, add=True)
        
    if (isCurtain and tieBack):
        cmds.select(clothliketie, add=True)
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
            materialType = 'Cotton'
        if (materialType == 'Cotton'):
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
        elif (materialType == 'Velvet'):    
            cmds.setAttr(name + 'shader.specular', 0)
            cmds.setAttr(name + 'shader.baseColor', maincolor[0], maincolor[1], maincolor[2], type='double3')
            cmds.setAttr(name + 'shader.sheen', 1)
            cmds.setAttr(name + 'shader.sheenColor', lighterColor[0], lighterColor[1], lighterColor[2], type='double3')
            cmds.setAttr(name + 'shader.sheenRoughness', 0.2)
        elif (materialType == 'Satin'):    
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
        elif(materialType == 'Plaid'):
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
            random.seed(seed)
            rand1 = random.uniform(0, 0.5939)
            random.seed(seed)
            rand2 = random.uniform(0, 0.7131)
            complcolor = (maincolor[0], rand1, rand2)
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
            
def clothmain():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
    name = inputname
    tieWithBow = cmds.checkBoxGrp('tieWithBow', q = True, v1=True)
    clothType = cmds.optionMenuGrp('clothType', q = True, v = True)
    if (clothType == 'Curtain'):
        curtainType = cmds.optionMenuGrp('curtainType', q = True, v = True)
        if (curtainType == 'Single Panel'):
            singleTieLocation = cmds.optionMenuGrp('singleTieLocation', q = True, v = True)
            if (singleTieLocation == 'Center'):
                if (tieWithBow):
                    newname = name + 'curtainBow'
                    createCloth(newname, True, 'singlecenter')
                createCloth(name, False, 'singlecenter')
            elif (singleTieLocation == 'Left'):
                if (tieWithBow):
                    newname = name + 'curtainBow'
                    createCloth(newname, True, 'singleleft')
                createCloth(name, False, 'singleleft')
            elif (singleTieLocation == 'Right'):
                if (tieWithBow):
                    newname = name + 'curtainBow'
                    createCloth(newname, True, 'singleright')
                createCloth(name, False, 'singleright')     
        elif (curtainType == 'Panel Pair'):
            pairTieLocation = cmds.optionMenuGrp('pairTieLocation', q = True, v = True)
            if (pairTieLocation == 'Center'):
                if (tieWithBow):
                    newname = name + 'curtainBow1'
                    createCloth(newname, True, 'pair1center')
                    newname = name + 'curtainBow2'
                    createCloth(newname, True, 'pair2center')
                newname = name + '1'
                createCloth(newname, False, 'pair1center')
                newname = name + '2'
                createCloth(newname, False, 'pair2center')
            else:
                if (tieWithBow):
                    newname = name + 'curtainBow1'
                    createCloth(newname, True, 'pair1left')
                    newname = name + 'curtainBow2'
                    createCloth(newname, True, 'pair2right')
                newname = name + '1'
                createCloth(newname, False, 'pair1left')
                newname = name + '2'
                createCloth(newname, False, 'pair2right')
        elif (curtainType == 'Complete Set'):
            pairTieLocation = cmds.optionMenuGrp('pairTieLocation', q = True, v = True)
            if (pairTieLocation == 'Center'):
                if (tieWithBow):
                    newname = name + 'curtainBow1'
                    createCloth(newname, True, 'pair1center')
                    newname = name + 'curtainBow2'
                    createCloth(newname, True, 'pair2center')
                newname = name + '1'
                createCloth(newname, False, 'pair1center')
                newname = name + '2'
                createCloth(newname, False, 'pair2center')
                newname = name + 'top'
                createCloth(newname, False, 'singletop')
            else:
                if (tieWithBow):
                    newname = name + 'curtainBow1'
                    createCloth(newname, True, 'pair1left')
                    newname = name + 'curtainBow2'
                    createCloth(newname, True, 'pair2right')
                newname = name + '1'
                createCloth(newname, False, 'pair1left')
                newname = name + '2'
                createCloth(newname, False, 'pair2right')
                newname = name + 'top'
                createCloth(newname, False, 'singletop_side')
    else:
        createCloth(name, False, 'n/a')
