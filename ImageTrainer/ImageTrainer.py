from tkinter import *
from ManualClassifier import *
from PIL import Image,ImageTk

"""
    This provides a user interface for manually classifying images for later training a convolutional neural network for classification.
    At the moment it simply copies the unclassified images to folders labelled with the classname, which is wasteful as if something has
    more than the one class, the image will be copied multiple times. A solution in which the input files are indexed in a database,
    with classifications pointing the index of the indexed files would be much more efficient. Still, I find it to be nicer than
    manually 
"""

class ManualClassifierWindow(ManualClassifier):
    def __init__(self, strUnclassifiedPath="Unclassified", strClassifiedPath="Classified"):
        super().__init__(strUnclassifiedPath,strClassifiedPath)
        self.IMAGE_WIDTH = 1024
        # Do some initialization with the super class
        self.IndexUnclassifiedImages()
        self.IndexClasses()

        # Create a window
        self.rootWindow = Tk()
        self.rootWindow.title("Manual Classifier for Generating Training Data")
        #self.rootWindow.geometry("1024x768")
        self.strCurrentImagePath = None
        # Create a variable to use for the image panel
        self.img = None
        self.imagePanel = None
        self.classifyButton = Button(self.rootWindow, text="Classify", command=self.ClassifyAndLoadNext)
        self.classifyButton.grid(row = 1, column = 1, padx = 2, pady = 2)
        if self.LoadFirstImage():
            self.imagePanel.grid(row = 0, column = 0, padx = 2, pady = 2)
        self.textInput = Text(self.rootWindow)
        self.textInput.grid(row = 0, column = 1, padx=1, pady = 1)
        self.StartUI()

    def ClassifyAndLoadNext(self):
        strClasses = self.textInput.get("1.0",END)
        classList = strClasses.splitlines()
        if len(self.unclassifiedImages) == 0:
            Label(self.rootWindow,text="No Images Left To Load").grid(row = 0, column = 0, padx = 2, pady = 2)
            return None
        self.Classify(self.unclassifiedImages[0],classList)
        self.LoadFirstImage()

    def LoadFirstImage(self):
        # If theres no images then we cant load them
        if len(self.unclassifiedImages) == 0:
            Label(self.rootWindow,text="No Images Left To Load").grid(row = 0, column = 0, padx = 2, pady = 2)
            return False
        
        try:
            self.strCurrentImagePath = os.path.join(self.strUnclassifiedPath,self.unclassifiedImages[0])
            image = Image.open(self.strCurrentImagePath)
            scale = self.IMAGE_WIDTH / image.width
            image = image.resize((self.IMAGE_WIDTH,int(image.height*scale)), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(image)
        except Exception as e:
            print(e)
            return False
        if self.imagePanel == None:
            self.imagePanel = Label(self.rootWindow,image=self.img)
        else:
            self.imagePanel["image"]=self.img
        return True

    def StartUI(self):
        self.rootWindow.mainloop()

classifierWindow = ManualClassifierWindow()
