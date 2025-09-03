from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [
    "What is the difference between supervised and unsupervised learning?",
    "Explain overfitting and how to prevent it.",
    "What is the purpose of cross-validation?",
    "Describe precision, recall, and F1-score.",
    "What are the assumptions of linear regression?",
    "Explain PCA and its use in dimensionality reduction.",
    "What is the difference between bagging and boosting?",
    "What are the different types of bias in a dataset?",
    "How does a decision tree work?",
    "What is the difference between classification and regression?"
]

ideal_answers = [
    "Supervised learning uses labeled data, unsupervised does not. Supervised involves classification or regression.",
    "Overfitting happens when a model learns training data too well. It can be prevented using regularization and cross-validation.",
    "Cross-validation splits the data into folds to better estimate model performance.",
    "Precision, recall and F1-score are metrics for classification based on true/false positives/negatives.",
    "Linear regression assumes linearity, no multicollinearity, homoscedasticity, and normality of errors.",
    "PCA reduces dimensions by extracting principal components that capture variance.",
    "Bagging reduces variance using ensemble of weak learners. Boosting improves bias sequentially.",
    "Bias types include selection bias, sampling bias, measurement bias, etc.",
    "Decision trees split data based on features to reduce impurity using entropy or Gini index.",
    "Classification predicts discrete labels; regression predicts continuous values."
]

@app.route("/")
def index():
    return render_template("index.html", questions=questions)

@app.route("/score", methods=["POST"])
def score_answer():
    data = request.json
    user_answer = data.get("answer", "")
    q_index = data.get("question_index", 0)

    if not user_answer.strip():
        return jsonify({"score": 0.0, "similarity": 0.0, "message": "Empty answer"})

    user_emb = model.encode(user_answer, convert_to_tensor=True)
    ideal_emb = model.encode(ideal_answers[q_index], convert_to_tensor=True)

    similarity = util.cos_sim(user_emb, ideal_emb).item()
    score = round(similarity * 10, 2)

    return jsonify({
        "score": score,
        "similarity": round(similarity, 3),
        "ideal": ideal_answers[q_index]
    })

if __name__ == "__main__":
    app.run(debug=True)
