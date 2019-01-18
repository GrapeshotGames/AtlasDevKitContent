import uuid
import re
import io
import sys

class UnrealToArk():
    def __init__(self, objectString):
        self.objectString = objectString
        self.pinId = self.setPinId(objectString)
        self.pinObjectName = self.setPinObjectName(objectString)
        self.pins = self.setPins(self.pinObjectName)
        self.nodeName = self.setNodeName(objectString)
        self.pinName = self.setPinName(objectString)
        self.pinFriendly = self.setPinFriendlyName(objectString)
        self.direction = self.setDirection(objectString)
        self.pinType = self.setPinType(objectString)
        self.links = self.setLinks(objectString)

    # Gets and sets node name on object initialization
    def setNodeName(self, objectString):
        return re.search("(?:MaterialGraphNode)[\w]+\"", objectString).group().rstrip("\"")

    def setPins(self, pinObjectName):
        pins = ""
        i = 0
        while i < len(self.pinId):
            pins += "{0}Pins({1})=EdGraphPin'{2}'\n".format(" " * 3, i, pinObjectName[i])
            i += 1
        return pins
    
    def setPinObjectName(self, eachObject):
        pinObjectName = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                pinObjectName.append("EdGraphPin_{0:04d}".format(i))
                i += 1
        return pinObjectName
        
    def setPinId(self, eachObject):
        pinId = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                pinId.append(re.search("(?<=PinId=)[\w]+", eachLine).group())
                i += 1
        return pinId
    
    def setPinName(self, eachObject):
        pinName = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                pinName.append(re.search("(?<=PinName=\")[\w ]+", eachLine).group())
            i += 1
        return pinName
      
    def setPinFriendlyName(self, eachObject):
        pinFriendly = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                if re.search("(?<=PinFriendlyName=\")[\w ]+", eachLine):
                    pinFriendly.append(re.search("(?<=PinFriendlyName=\")[\w ]+", eachLine).group())
                else:
                    pinFriendly.append(None)
            i += 1
        return pinFriendly
    
    def setDirection(self, eachObject):
        direction = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                if re.search("(?<=Direction=\")[\w ]+", eachLine):
                    direction.append(re.search("(?<=Direction=\")[\w ]+", eachLine).group())
                else:
                    direction.append(None)
            i += 1
        return direction
    
    def setPinType(self, eachObject):
        pinType = []
        objectString = io.StringIO(eachObject)
        
        i = 0
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                if re.search("(?<=PinType.PinCategory=\")[\w ,]+", eachLine):
                    pinType.append(re.search("(?<=PinType.PinCategory=\")[\w ,]+", eachLine).group())
                else:
                    pinType.append(None)
            i += 1
        return pinType
    
    def setLinks(self,  eachObject):
        links = []
        objectString = io.StringIO(eachObject)
        for eachLine in objectString:
            if re.search("(?<=PinId=)[\w]+", eachLine):
                if re.search("(?<=LinkedTo=\()[\w ,]+", eachLine):
                    temp = re.search("(?<=LinkedTo=\()[\w \,]+", eachLine).group().split(",")
                    del temp[-1]
                    
                    i = 0
                    while i < len(temp):
                        temp[i] = temp[i].split()
                        i += 1
                    
                    links.append(temp)
                else:
                    links.append(None)
        return links
    
    def getLinks(self):
        return self.links
    
    def getObjectString(self):
        return self.objectString
    
    def getNodeName(self):
        return self.nodeName
    
    def getPins(self):
        return self.pins
    
    def getPinId(self):
        return self.pinId
    
    def getPinName(self):
        return self.pinName
    
    def getPinFriendly(self):
        return self.pinFriendly
    
    def getDirection(self):
        return self.direction
    
    def getPinType(self):
        return self.pinType
    
    def getLinks(self):
        return self.links
    
    def getPinObjectName(self):
        return self.pinObjectName
  
class ArkToUnreal(UnrealToArk):
    def setPinId(self, objectString):
        pinId = []
        i = 0
        while i < len(re.findall("Begin Object Name=\"E", objectString)):
            pinId.append(generateUUID())
            i += 1
        return pinId
    
    def setDirection(self, eachObject):
        direction = []
        objectString = io.StringIO(eachObject)
        
        inPinObject = False
        for eachLine in objectString:
            if "Begin Object Name=\"E" in eachLine:
                inPinObject = True
            elif inPinObject and "End Object" in eachLine:
                inPinObject = False
                direction.append(None)
            if inPinObject and "Direction" in eachLine:
                direction.append(re.search("(?<=Direction=)[\w ]+", eachLine).group())
                inPinObject = False
        return direction
    
    def setPins(self, pinObjectName):
        pins = []
        i = 0
        while i < len(pinObjectName):
            pins.append(None)
            i += 1
        return pins
    
    def setPinObjectName(self, eachObject):
        pinObjectName = re.findall("(?<=Begin Object Name=\")[\w]+", eachObject)
        del pinObjectName[0]
        return pinObjectName
        
    def setPinName(self, eachObject):
        pinName = []
        objectString = io.StringIO(eachObject)
        
        inPinObject = False
        for eachLine in objectString:
            if "Begin Object Name=\"E" in eachLine:
                inPinObject = True
            elif inPinObject and "End Object" in eachLine:
                inPinObject = False
            if inPinObject and "PinName" in eachLine:
                pinName.append(re.search("(?<=PinName=\")[\w\- ,]+", eachLine).group())
                inPinObject = False
        return pinName
    
    def setPinFriendlyName(self, eachObject):
        pinFriendly = []
        objectString = io.StringIO(eachObject)
        
        inPinObject = False
        for eachLine in objectString:
            if "Begin Object Name=\"E" in eachLine:
                inPinObject = True
            elif inPinObject and "End Object" in eachLine:
                inPinObject = False
                pinFriendly.append(None)
            if inPinObject and "PinFriendlyName" in eachLine:
                pinFriendly.append(re.search("(?<=PinFriendlyName=\")[\w ,]+", eachLine).group())
                inPinObject = False
        return pinFriendly
    
    def setPinType(self, eachObject):
        pinType = []
        objectString = io.StringIO(eachObject)
        
        inPinObject = False
        for eachLine in objectString:
            if "Begin Object Name=\"E" in eachLine:
                inPinObject = True
            elif inPinObject and "End Object" in eachLine:
                inPinObject = False
                pinType.append(None)
            if inPinObject and "PinCategory" in eachLine:
                pinType.append(re.search("(?<=PinCategory=\")[\w ,]+", eachLine).group())
                inPinObject = False
        return pinType
    
    def setLinks(self,  eachObject):
        links = []
        objectString = io.StringIO(eachObject)
        inPinObject = False
        tmp = []

        for eachLine in objectString:
            if "Begin Object Name=\"E" in eachLine:
                inPinObject = True
            if inPinObject and "LinkedTo" in eachLine:
                tmp.append(re.search("(?<=EdGraphPin'\")[\w. ]+", eachLine).group().split("."))
            elif inPinObject and "End Object" in eachLine:
                inPinObject = False
                if len(tmp) > 0:
                    links.append(tmp)
                    tmp = []
                else:
                    links.append(None)
        return links
        
def createEdGraphPinClass(nodeObject):
    EdGraphPinClass = ""
    i = 0
    while i < len(nodeObject.getPinId()):
        EdGraphPinClass += "{0}Begin Object Class=EdGraphPin Name=\"{1}\"\n{0}End Object\n".format(" " * 3, nodeObject.getPinObjectName()[i])
        i += 1
    return EdGraphPinClass

def createEdGraphPinObject(nodeObject, linkNames):
    EdGraphPinString = ""
    nodeName = nodeObject.getNodeName()
    pinId = nodeObject.getPinId()
    pinName = nodeObject.getPinName()
    pinType = nodeObject.getPinType()
    pinFriendly = nodeObject.getPinFriendly()
    direction = nodeObject.getDirection()
    links = nodeObject.getLinks()
    pinObjectName = nodeObject.getPinObjectName()
    
    i = 0
    while i < len(nodeObject.getPinName()):
        EdGraphPinString += "{0}Begin Object Name=\"{1}\"\n{2}PinName=\"{3}\"\n".format(" " * 3, pinObjectName[i], " " * 6, pinName[i])
        if pinType[i] != None:
            EdGraphPinString += "{0}PinType=(PinCategory=\"{1}\")\n".format(" " * 6, pinType[i])
        if pinFriendly[i] != None:
            EdGraphPinString += "{0}PinFriendlyName=\"{1}\"\n".format(" " * 6, pinFriendly[i])
        if direction[i] != None:
            EdGraphPinString += "{0}Direction={1}\n".format(" " * 6, direction[i])
        if links[i] != None:
            j = 0
            while j < len(links[i]):
                try:
                    linkName = linkNames[links[i][j][0]][links[i][j][1]]
                except KeyError:
                    linkName = "EdGraphPin_0000"
                EdGraphPinString += "{0}LinkedTo({1})=EdGraphPin'\"{2}.{3}\"'\n".format(" " * 6, j, links[i][j][0], linkName)
                j += 1
        EdGraphPinString += "   End Object\n"
        i += 1
    return EdGraphPinString

def generateNodeList(stringList, isFromArkEngine):
    objectString = u""
    nodeList = []

    i, beginCount, endCount = 0, 0, 0
    while i < len(stringList):
        if "Begin Object" in stringList[i]:
            beginCount += 1
        if "End Object" in stringList[i]:
            endCount += 1
        objectString += stringList[i] + "\n"
        
        if beginCount == endCount:
            if isFromArkEngine:
                nodeList.append(ArkToUnreal(objectString))
            else:
                nodeList.append(UnrealToArk(objectString))
            beginCount, endCount = 0, 0
            objectString = u""
        i += 1
    return nodeList

# Possible bug with nodes of same name having different UUID
def createLinkNames(nodeList, isFromArkEngine):
    node_port_lib = {}
    i = 0
    while i < len(nodeList):
        nodeName = nodeList[i].getNodeName()
        pinId = nodeList[i].getPinId()
        pinObject = nodeList[i].getPinObjectName()
        pinDict = {}
        j = 0
        while j < len(pinId):
            if isFromArkEngine:
                try:
                    pinDict[pinObject[j]] = "{0}".format(pinId[j])
                except IndexError:
                    print 'DO NOT SELECT THE ROOT NODE IN THE MASTER MATERIAL. EXITING.'
                    sys.exit()
            else:
                pinDict[pinId[j]] = "{0}".format(pinObject[j])
            j += 1
        node_port_lib[nodeName] = pinDict
        i += 1
    
    # Fixes error where a node is linked but was not selected (Orphaned nodes)
    node_port_lib_copy = node_port_lib.copy()
    
    for node in node_port_lib:
        for port in node:
            
            # Compares to links in nodeList
            for selNode in nodeList:
                nodeLinks = selNode.getLinks()
                for link in nodeLinks:
                    if link is not None:
                        nodeName = link[0][0]
                        
                        # For times when more than one import port is plugged into same node.
                        if nodeName not in node_port_lib:
                            tmpDict = {}
                            
                            # Gets current tmpDict if already exists
                            if nodeName in node_port_lib_copy:
                                tmpDict = node_port_lib_copy[nodeName]
                                
                            # Gets current port
                            curPort = link[0][1]
                            
                            tmpDict[curPort] = generateUUID()
                            node_port_lib_copy[nodeName] = tmpDict
                            
    node_port_lib = node_port_lib_copy

    return node_port_lib

def generateUUID():
    return str(uuid.uuid4().hex).upper()

def isFromArkEngine(stringList):
    isFromArkEngine = True
    i = 0
    while i < len(stringList):
        if "CustomProperties" in stringList[i]:
            isFromArkEngine = False
            break
        i += 1
    return isFromArkEngine

def createCustomProperties(nodeObject, linkDict):
    nodePorts = nodeObject.getLinks()
    
    customProperties = ""
    i = 0
    while i != len(nodePorts):
        linkedTo = ""
        if nodePorts[i] != None:
            linkedTo += "LinkedTo=("

            nodeLinkedTo = linkDict[nodePorts[i][0][0]]
            portLinkedTo = nodeLinkedTo[nodePorts[i][0][1]]
            linkedTo += "{0} {1},)".format(nodePorts[i][0][0], portLinkedTo)
            
        pinFriendly = ""
        if nodeObject.getPinFriendly()[i] != None:
            pinFriendly = ",PinFriendlyName=\"{0}\"".format(nodeObject.getPinFriendly()[i])
        
        pinType = ""
        if nodeObject.getPinType()[i] != None:
            pinType = nodeObject.getPinType()[i]
            
        direction = ""
        if nodeObject.getDirection()[i] != None:
            direction = ",Direction=\"{0}\"".format(nodeObject.getDirection()[i])
            
        customProperties += "   CustomProperties Pin (PinId={0},PinName=\"{1}\"{2}{3}," \
        "PinType.PinCategory=\"{4}\"," \
        "PinType.PinSubCategory=\"\"," \
        "PinType.PinSubCategoryObject=None,{5}" \
        "PersistentGuid={6}," \
        "bHidden=False,bNotConnectable=False,bDefaultValueIsReadOnly=False," \
        "bDefaultValueIsIgnored=False,bAdvancedView=False,)\n" \
        .format(nodeObject.getPinId()[i], nodeObject.getPinName()[i], pinFriendly, direction, pinType, linkedTo, "".join(["0" for l in range(32)]))
        i += 1
    return customProperties

def unrealFormat(nodeList):
    linkDict = createLinkNames(nodeList, True)
    masterString = ""
    i = 0
    while i < len(nodeList):
        customProperties = createCustomProperties(nodeList[i], linkDict)
        j = 0
        objectString = nodeList[i].objectString.rstrip("\n").split("\n")
        inObject = False
        while j < len(objectString):
            if "Begin Object Class=E" in objectString[j] or "Begin Object Name=\"E" in objectString[j]:
                inObject = True
            elif inObject is not True:
                if "Pins" not in objectString[j]:
                    if j == len(objectString) - 1:
                        masterString += customProperties
                    masterString += objectString[j] + "\n"
            elif "End Object" in objectString[j] and inObject:
                inObject = False
            j += 1
        i += 1
    return masterString

def arkFormat(nodeList):
    linkNames = createLinkNames(nodeList, False)
    masterString = ""
    i = 0
    while i < len(nodeList):
        objectString = io.StringIO(nodeList[i].objectString)
        j = 0
        for eachLine in objectString:
            if j == 3:
                masterString += createEdGraphPinClass(nodeList[i]) + createEdGraphPinObject(nodeList[i], linkNames) + nodeList[i].getPins()
            if "CustomProperties" not in eachLine:

                # Fixes hard crash. Ark engine does not have Saturate node. Places clamp node instead.
                if 'Saturate' in eachLine:
                    masterString += eachLine.replace('Saturate', 'Clamp')
                else:
                    masterString += eachLine
            j += 1
        i += 1
    return masterString

def createStringList(clipboard):
    tmp = []
    masterString = ""
    i = 0
    while i < len(clipboard):
        if clipboard[i] == "\n":
            tmp.append(masterString)
            masterString = ""
        else:
            masterString += clipboard[i]
        i += 1
    return tmp
        