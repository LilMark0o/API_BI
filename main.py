from fastapi import FastAPI
from pydantic import BaseModel
import random
from typing import List
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

class Modelo:
    def __init__(self, archivo_modelo='initial.joblib'):
        # Carga el modelo desde el archivo proporcionado
        self.modelo = self.cargar_modelo(archivo_modelo)
    
    def cargar_modelo(self, archivo_modelo):
        """Carga el modelo desde un archivo .joblib"""
        try:
            modelo_cargado = joblib.load(archivo_modelo)
            print(f"Modelo cargado correctamente desde {archivo_modelo}")
            return modelo_cargado
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return None
    
    def predecir(self, df):
        df["u_log2"] = np.log2(df["u"])
        df["class"] = df["class_object"].replace({"QUASAR": "QSO", "S": "STAR", "G": "GALAXY"})
        df['class_QSO'] = df['class'] == 'QSO'
        df['class_STAR'] = df['class'] == 'STAR'
        df_encoded = df[["u_log2", "g", "r", "i", "z", "rowv", "colv", "class_QSO", "class_STAR"]]
        """Hace una predicción utilizando el modelo cargado"""
        if self.modelo:
            return self.modelo.predict(df_encoded)
        else:
            print("El modelo no está cargado correctamente.")
            return -1
            
class PredictionInput(BaseModel):
    objid: int
    ra: float
    dec: float
    u: float
    g: float
    r: float
    i: float
    z: float
    run: int
    camcol: int
    field: int
    score: float
    clean: int
    class_object: str  # 'class' is a reserved keyword, so we use 'class_object' instead
    mjd: int
    rowv: float
    colv: float

# Example data structure to represent the incoming objects for re-training
class TrainingInput(BaseModel):
    objid: int
    ra: float
    dec: float
    u: float
    g: float
    r: float
    i: float
    z: float
    run: int
    camcol: int
    field: int
    score: float
    clean: int
    class_object: str  # 'class' is a reserved keyword, so we use 'class_object' instead
    redshift: float
    mjd: int
    rowv: float
    colv: float

# In-memory model (simple random prediction for demo purposes)
MODEL = Modelo()

@app.post("/predict")
async def predict(data: List[PredictionInput]):
    """
    Predicts a number between 1 and 10 based on the input features.
    """
    predictions = []
    for object_to_predict in data:
        # Here we use random for the demo; replace with an actual model prediction
        dict_object = object_to_predict.dict()  # Use .dict() instead of dict(object_to_predict)
        
        df = pd.DataFrame([dict_object]) 

        prediction_result = MODEL.predecir(df)
        predictions.append({"prediction": prediction_result.tolist() if isinstance(prediction_result, np.ndarray) else prediction_result})

    return {"predictions": predictions}

@app.post("/retrain")
async def retrain(data: List[TrainingInput]):
    """
    A placeholder for retraining the model (for now it just generates a number).
    """
    # Dummy retraining logic: for now, just return the count of the training samples
    if len(data) < 10:
        return {"message": "Not enough data to retrain the model."}
    
    # Randomly retrain the model (you would replace this with actual logic)
    retrained_value = random.randint(1, 10)
    return {"message": f"Model retrained. New value: {retrained_value}"}

 # uvicorn main:app --reload