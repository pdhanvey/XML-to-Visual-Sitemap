import xml.etree.ElementTree as ET

class Node:
    def __init__(self, name, parent=""):
        self.name = name
        self.children = []
        self.parent = parent
        self.usable = True
        self.x = None
        self.y = None
        self.id = None
        self.length = 0
        if parent != "":
            assert isinstance(parent, Node)
            parent.add_child(self)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Node)
        new = True
        for child in self.children:
            if node.name == child.name:
                new = False
                break
        if new:    
            self.children.append(node)
        else:
            node.usable = False
    def setid(self, id):
        self.id = id
    def setx(self, x):
        self.x = x
    def sety(self, y):
        self.y = y

mxfile = ET.Element("mxfile")
diagram = ET.SubElement(mxfile, "diagram")
diagram.set("id", "s4HBoznF436Gjv50dPv8")
diagram.set("name", "New Map")
mxGraphModel = ET.SubElement(diagram, "mxGraphModel")
mxGraphModel.set("dx","1000")
mxGraphModel.set("dy","800")
mxGraphModel.set("grid","1")
mxGraphModel.set("gridsize","10")
mxGraphModel.set("guides","1")
mxGraphModel.set("tooltips","1")
mxGraphModel.set("connect", "1")
mxGraphModel.set("arrows","1")
mxGraphModel.set("fold", "1")
mxGraphModel.set("page", "1")
mxGraphModel.set("pageScale", "1")
mxGraphModel.set("pageWidth", "1200")
mxGraphModel.set("pageHeight","900")
mxGraphModel.set("math","0")
mxGraphModel.set("shadow","0")
root = ET.SubElement(mxGraphModel, "root")
mxCell0 = ET.SubElement(root, "mxCell")
mxCell1 = ET.SubElement(root, "mxCell")
mxCell0.set("id", "0")
mxCell1.set("id", "1")
mxCell1.set("parent", "0")

file = input("Input XML File Name: ")
outfile = file.replace(".xml", "_visual.xml")
outfile_d = file.replace(".xml", "_visual.drawio")

in_file = ET.parse(file)
urlset = in_file.getroot()

loc_count = 0

used = {}
id = 2
x = 0
parent = Node("parent")
parent.setid("1")

for url in urlset:
    for loc in url:
        if "loc" in loc.tag:
            if loc_count == 0:
                if "https://" in loc.text[:8]:
                    i = 8
                elif "http://" in loc.text[:7]:
                    i = 7
                else:
                    i = 0
                slash = loc.text[i:].find("/")
                if slash > 0:
                    tree = Node(loc.text[i:i+slash], parent)
                else:
                    tree = Node(loc.text[i:], parent)
                used[0] = [tree]
                tree.setid(str(id))
                tree.setx(str(x))
                tree.sety("0")
            else:
                slash = loc.text[i:].find("/")
                slash_count = 0
                while slash > 0:
                    slash_count += 1
                    next_slash = loc.text[i:].find("/", slash + 1, -1)
                    if next_slash == -1:
                        name = loc.text[i:][slash+1:]
                    else:
                        name = loc.text[i:][slash+1:next_slash]
                    node = Node(name, used[slash_count - 1][-1])
                    if slash_count >= len(used):
                        used[slash_count] = []
                    if node.usable:
                        id += 1
                        node.setid(str(id))
                        node.setx(str(150*slash_count))
                        used[slash_count].append(node)        
                    slash = next_slash
            loc_count += 1

def create_box(box_node):
    mxCell = ET.SubElement(root, "mxCell")
    mxCell.set("id", box_node.id)
    mxCell.set("value", box_node.name)
    mxCell.set("style","rounded=1;fillColor=#ccccff;gradientColor=none;strokeColor=none;fontColor=#000000;fontStyle=1;fontFamily=Tahoma;fontSize=8;whiteSpace=wrap;")
    mxCell.set("parent", "1")
    mxCell.set("vertex", "1")
    mxGeometry = ET.SubElement(mxCell, "mxGeometry")
    mxGeometry.set("x", box_node.x)
    mxGeometry.set("y", box_node.y)
    mxGeometry.set("width", "100")
    mxGeometry.set("height", "50")
    mxGeometry.set("as", "geometry")

def dfcreate_box(tree):
    create_box(tree)
    for child in tree.children:
        dfcreate_box(child)
        mxCell = ET.SubElement(root, "mxCell")
        mxCell.set("id", tree.id + "_" + child.id)
        mxCell.set("value", "")
        if tree.children.index(child) == 0:
            mxCell.set("style","edgeStyle=elbowEdgeStyle;elbow=vertical;strokeWidth=1;rounded=0;exitX=1;exitY=0.5;entryX=0;entryY=0.5;strokeColor=#000000;endArrow=none;endFill=0;")
        else:
            mxCell.set("style","edgeStyle=orthogonalEdgeStyle;rounded=0;jumpStyle=none;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endArrow=none;endFill=0;strokeColor=#000000;")
        mxCell.set("parent", "1")
        mxCell.set("source", tree.id)
        mxCell.set("target", child.id)
        mxCell.set("edge", "1")
        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", tree.x)
        mxGeometry.set("y", child.y)
        mxGeometry.set("width", "100")
        mxGeometry.set("height", "100")
        mxGeometry.set("as", "geometry")
        

def dffind_y(tree, y):
    tree.sety(str(y))
    for index in range(len(tree.children)):
        if index == 0:
            dffind_y(tree.children[index], int(tree.y))
        else:
            if tree.children[index-1].length == 1:
                dffind_y(tree.children[index], int(tree.children[index-1].y) + 75)
            else:
                dffind_y(tree.children[index], int(tree.children[index-1].y) + tree.children[index-1].length*75)

def df_size(tree):
    for child in tree.children:
        df_size(child)
        if tree.children.index(child) != 0:
            tree.length += child.length
        else:
            tree.length += child.length - 1
    tree.length += 1

df_size(tree)
dffind_y(tree, 0)
dfcreate_box(tree)

new_xml = ET.tostring(mxfile)

out_file = open(outfile, "wt")
out_file.write(new_xml.decode("utf-8"))
out_file_d = open(outfile_d, "wt")
out_file_d.write(new_xml.decode("utf-8"))
