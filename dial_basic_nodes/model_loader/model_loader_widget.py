
import os
import PySide2
import dependency_injector.providers as providers

current_dir = os.path.dirname(os.path.abspath(__file__))
from PySide2.QtUiTools import loadUiType
Form, Base = loadUiType(os.path.join(current_dir, "./modelLoader.ui"))

class ModelLoaderWidget(Form, Base):
    def __init__(self, parent: PySide2.QtWidgets.QWidget = None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        

        self.loadModelButton.clicked.connect(self.onLoadModelClick)

        self.loadWeightsButton.setEnabled(False)
        self.loadWeightsButton.clicked.connect(self.onLoadWeightsClick)

        self.loadWeightsInput.setEnabled(False)

        self.model = None
        return

    def send_model(self):
        
        return self.model

    def onLoadModelClick(self,event):
        self.loadWeightsButton.setEnabled(False)
        self.loadWeightsInput.setEnabled(False)
        self.loadModelInput.clear()
        self.loadWeightsInput.clear()
        #options = PySide2.QtWidgets.QFileDialog.Options()
        
        modelPath, _ = PySide2.QtWidgets.QFileDialog.getOpenFileName(self,"Open Model file", "", "Keras Model Files(*.h5 *.json)", options=PySide2.QtWidgets.QFileDialog.Options())
        if modelPath != '':
            from pathlib import Path 
            modelPath = Path(modelPath)
            try:
                if modelPath.suffix == ".json": #Solo la arquitectura
                    from tensorflow.keras.models import model_from_json
                    with open(modelPath) as json_file:
                        self.model = model_from_json(json_file.read())
                else: #modelPath.suffix == ".h5" #La arquitectura y los pesos
                    from tensorflow.keras.models import load_model
                    self.model = load_model(modelPath)
                self.loadModelInput.insert(str(modelPath))
                self.loadWeightsButton.setEnabled(True)
                self.loadWeightsInput.setEnabled(True)
            except ValueError:
                msgBox = PySide2.QtWidgets.QMessageBox();
                msgBox.setText("El fichero esta corrupto o corresponde a los pesos del modelo");
                msgBox.exec();
        return

    def onLoadWeightsClick(self,event):
        self.loadWeightsInput.clear()
        weightPath, _ = PySide2.QtWidgets.QFileDialog.getOpenFileName(self,"Open Weights file", "", "Keras Weights Files(*.h5)", options=PySide2.QtWidgets.QFileDialog.Options())
        if weightPath != '':
            try:
                self.model.load_weights(weightPath)
                self.loadWeightsInput.insert(weightPath)
            except Exception as e:
                msgBox = PySide2.QtWidgets.QMessageBox();
                msgBox.setText("Error.{}".format(e));
                msgBox.exec();

        return



ModelLoaderWidgetFactory = providers.Factory(ModelLoaderWidget)