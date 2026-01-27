# ml/model.py

class ScriptAnomalyModel:
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        # Load your trained ML model here (e.g., XGBoost, joblib, etc.)
        pass

    def predict(self, features):
        # Return 1 for suspicious, 0 for normal
        if self.model:
            return self.model.predict([features])[0]
        return 0
