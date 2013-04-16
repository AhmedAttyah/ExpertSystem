from PyQt4.QtCore  import *
from PyQt4.QtGui import *
from frontend import Ui_Dialog
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.dom.minidom import Document
from xml.dom.minidom import *
import sys
class FrontEND (Ui_Dialog,QMainWindow):
     def __init__(self):
            Ui_Dialog.__init__(self)
            QMainWindow.__init__(self)
            self.ui=Ui_Dialog()
            self.ui.setupUi(self)
            xmlFile = parse("Atrophy.xml")
            root = xmlFile.documentElement
            self.aDiseases = []
            self.aConcepts=[]
            self.aProperties=[]
            self.aValues=[]
            self.allRules=root.getElementsByTagName("Rule")
            for rule in self.allRules :
                self.aDiseases.append(rule.getAttribute("name"))
                allTuples= rule.getElementsByTagName('Tuple')
                for tuple in allTuples:
                    concept= tuple.getAttribute('Cpt')
                    if (concept in self.aConcepts):
                        continue
                    else:
                        self.aConcepts.append(concept)
            self.allDiseases= self.aDiseases
            self.ui.disease_list.addItems(self.aDiseases)
            self.ui.concept_list.addItems(self.aConcepts)
            self.ui.concept_list.item(0).setSelected(True)
            self.connect(self.ui.concept_list,SIGNAL("itemSelectionChanged()"), self.conceptSelected)
            self.connect(self.ui.property_list,SIGNAL("itemSelectionChanged()"),self.propertySelected)
            self.connect(self.ui.linkButton,SIGNAL("clicked()"),self.buttonClick)
            self.connect(self.ui.clearmemory,SIGNAL("clicked()"),self.memoryClear)

     def conceptSelected (self):
        self.aProperties=[]
        self.ui.property_list.clear()
        self.conceptSelected = self.ui.concept_list.selectedItems()
        self.conceptSelected= self.conceptSelected[0].text()
        for rule in self.allRules:
            allTuples= rule.getElementsByTagName('Tuple')
            for tuple in allTuples:
                    if (tuple.getAttribute('Cpt')== self.conceptSelected):
                            if tuple.getAttribute('Prop') in self.aProperties:
                                continue
                            else :
                                self.aProperties.append(tuple.getAttribute('Prop'))
                    else:
                        continue
        self.ui.property_list.addItems(self.aProperties)
        self.ui.property_list.item(0).setSelected(True)
     def propertySelected (self):
        self.aValues=[]
        self.ui.value_list.clear()
        self.conceptChanged = self.ui.concept_list.selectedItems()
        self.conceptChanged= self.conceptChanged[0].text()
        self.propertyChanged = self.ui.property_list.selectedItems()
        self.propertyChanged= self.propertyChanged[0].text()
        for rule in self.allRules:
            allTuples= rule.getElementsByTagName('Tuple')
            for tuple in allTuples:
                    if (tuple.getAttribute('Cpt')==self.conceptChanged and tuple.getAttribute('Prop')== self.propertyChanged):
                        if tuple.getAttribute('Val') in self.aValues:
                            continue
                        else:
                            self.aValues.append(tuple.getAttribute('Val'))
                            
                    else:
                        continue
        self.ui.value_list.addItems(self.aValues)
        self.ui.value_list.item(0).setSelected(True)

     def buttonClick(self):
        self.memoryConcept=[]
        memoryConcept= self.ui.concept_list.selectedItems()
        concept=memoryConcept[0].text()
        self.memoryConcept.append(memoryConcept[0].text())

        self.memoryProperty=[]
        memoryProperty = self.ui.property_list.selectedItems()
        property=memoryProperty[0].text()
        self.memoryProperty.append(memoryProperty[0].text())

        self.memoryValue=[]
        memoryValue = self.ui.value_list.selectedItems()
        value=memoryValue[0].text()
        self.memoryValue.append(memoryValue[0].text())

        self.memoryItems=[]
        memory=concept + "-->" +property + "-->"+value
        self.memoryItems.append(memory)
        print (concept+property+value)
        self.ui.memory_list.addItems(self.memoryItems)
        count=0
        self.temp=[]
        for rule in self.allRules:
            if rule.getAttribute('name') in self.aDiseases:
                tuples= rule.getElementsByTagName("Tuple")
                for tuple in tuples :
                    if tuple.getAttribute('Cpt')== concept and tuple.getAttribute('Prop')== property and tuple.getAttribute('Val')==value:
                                    self.temp.append(rule.getAttribute('name'))
            else:
                continue
        self.aDiseases=self.temp;
        self.ui.disease_list.clear()
        self.ui.disease_list.addItems(self.aDiseases)



     def memoryClear(self):
        self.memoryItems=[]
        self.ui.memory_list.clear()
        self.aDiseases=self.allDiseases
        self.ui.disease_list.clear()
        self.ui.disease_list.addItems(self.aDiseases)
app = QApplication(sys.argv)
FrontEND = FrontEND()
FrontEND.show()
app.exec_()
