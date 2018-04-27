import os,time
from shutil import *
class ManualClassifier:
    def __init__(self,strUnclassifiedPath, strClassifiedPath):
        self.strUnclassifiedPath = strUnclassifiedPath
        self.strClassifiedPath = strClassifiedPath
        self.unclassifiedImages = []
        self.classes = []
    
    def IndexUnclassifiedImages(self):
        for root, dirs, files in os.walk(self.strUnclassifiedPath):
            for file in files:
                self.unclassifiedImages.append(file)

    # Assumes that the classified path contains only directories containing classified images
    # We don't really care what's in the directories at this point
    def IndexClasses(self):
        for root,dirs,files in os.walk(self.strClassifiedPath):
            for dir in dirs:
                self.classes.append(dir)

    def AddClass(self,strClass):
        # Check if the class is already in the classes
        if strClass in self.classes:
            return True

        # Make a directory for the class
        try:
            os.makedirs(os.path.join(self.strClassifiedPath,strClass))
        except Exception as e:
            print(e)
            return False
        
        # If all went well, add the class to the class list
        self.classes.append(strClass)
        return True

    def Classify(self,strImageFile,classes):
        strOriginPath = os.path.join(self.strUnclassifiedPath,strImageFile)
        for strClass in classes:
            # Create the class if it didn't exist, return false if this fails, clearly there's something wrong
            if strClass not in self.classes:
                if not self.AddClass(strClass):
                    print("Failed to add class")
                    return False
            # Check if file already in class folder. If it is, append the current epoch to the filename to prevent collisions
            strDestinationPath = os.path.join(self.strClassifiedPath,strClass,strImageFile)
            if os.path.exists(strDestinationPath):
                strDestinationPath = "{}.{}".format(strDestinationPath,time.time())
            try:
                copy(strOriginPath,strDestinationPath)
            except Exception as e:
                return False
            
        try:
            pass
            #os.remove(strOriginPath)
        except Exception as e:
            print(e)
            return False
        self.unclassifiedImages.remove(strImageFile)
        return True
            