import dill
import os

class DummyModel:
    def predict(self, x):
        return [0]

class DummyTFIDF:
    def transform(self, x):
        class DummyArray:
            def toarray(self):
                return [[0.0]]
        return DummyArray()

class DummyScaler:
    def transform(self, x):
        return x

class DummyEncoder:
    def inverse_transform(self, x):
        return ["Migraine"]

pipeline = {
    'model': DummyModel(),
    'tfidf': DummyTFIDF(),
    'scaler': DummyScaler(),
    'pca': DummyScaler(),
    'angle_scaler': DummyScaler(),
    'label_encoder': DummyEncoder()
}

os.makedirs('models', exist_ok=True)
with open('models/q_medai_pipeline.dill', 'wb') as f:
    dill.dump(pipeline, f)

print("Dummy pipeline created successfully at models/q_medai_pipeline.dill")
