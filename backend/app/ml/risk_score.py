"""
Risk score model: gradient-boosted classifier predicting escalation risk
for a district/police-station based on recent crime features.
Trains on whatever historical rows are passed in; ships untrained until
enough data exists (falls back to a heuristic score).
"""
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

FEATURE_NAMES = [
    "crimes_last_30d", "crimes_last_90d", "violent_crime_ratio",
    "repeat_offender_count", "population_density", "avg_response_time_min",
]


class RiskScoreModel:
    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=150, max_depth=3, learning_rate=0.05)
        self.is_trained = False

    def train(self, X: list[list[float]], y: list[float]):
        self.model.fit(np.array(X), np.array(y))
        self.is_trained = True

    def predict(self, features: dict) -> dict:
        vec = np.array([[features.get(f, 0) for f in FEATURE_NAMES]])
        if self.is_trained:
            score = float(self.model.predict(vec)[0])
            importances = dict(zip(FEATURE_NAMES, self.model.feature_importances_.tolist()))
        else:
            # Heuristic fallback until the model has enough labeled history to train on
           score = (
                features.get("crimes_last_30d", 0) * 0.8
                + features.get("crimes_last_90d", 0) * 0.2
                + features.get("violent_crime_ratio", 0) * 20
                + features.get("repeat_offender_count", 0) * 2
                + features.get("population_density", 0) * 0.2
                + features.get("avg_response_time_min", 0) * 0.5
            )

        score = max(0, min(score, 100))
        importances = {f: 1 / len(FEATURE_NAMES) for f in FEATURE_NAMES}
        return {"risk_score": round(max(0.0, min(100.0, score)), 2), "feature_importance": importances}


risk_model = RiskScoreModel()
