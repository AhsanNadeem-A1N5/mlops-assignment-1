from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

# Load the Iris datasetS
iris = load_iris()
X = iris.data  # Feature matrix
y = iris.target  # Target labels
target_names = iris.target_names  # ['setosa', 'versicolor', 'virginica']

# Train a K-Means model
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)


@app.route('/')
def home():
    return "Welcome to the K-Means Model Training API!"


@app.route('/train')
def train_model():
    cluster_centers = kmeans.cluster_centers_.tolist()
    return jsonify({"message": "Model trained successfully!",
                    "cluster_centers": cluster_centers})


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    iris_type = data.get("type", "").lower()

    if iris_type not in target_names:
        return jsonify({
            "error":
            "Invalid type. Choose from setosa, versicolor, or virginica."
            }), 400

    # Get the average feature values for the selected species
    species_index = list(target_names).index(iris_type)
    avg_features = np.mean(X[y == species_index], axis=0).tolist()

    response = {
        "type": iris_type,
        "average_features": {
            "sepal_length": avg_features[0],
            "sepal_width": avg_features[1],
            "petal_length": avg_features[2],
            "petal_width": avg_features[3]
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
