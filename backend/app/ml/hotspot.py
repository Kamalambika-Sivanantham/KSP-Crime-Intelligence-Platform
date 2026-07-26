"""
Hotspot detection using DBSCAN over crime lat/lng points.
Real, runnable implementation — not a placeholder. Extend with KDE / KMeans
as additional strategies under app/ml/.
"""
import numpy as np
from sklearn.cluster import DBSCAN


def detect_hotspots(points: list[dict], eps_km: float = 0.5, min_samples: int = 5) -> list[dict]:
    """
    points: [{"id": str, "lat": float, "lng": float}, ...]
    Returns cluster assignments and per-cluster centroid + size, sorted by size desc.
    Uses haversine-approximate degrees-to-km conversion (good enough at Karnataka's latitude).
    """
    if not points:
        return []

    coords = np.radians(np.array([[p["lat"], p["lng"]] for p in points]))
    kms_per_radian = 6371.0088
    eps = eps_km / kms_per_radian

    db = DBSCAN(eps=eps, min_samples=min_samples, algorithm="ball_tree", metric="haversine").fit(coords)
    labels = db.labels_

    clusters: dict[int, list[int]] = {}
    for idx, label in enumerate(labels):
        if label == -1:
            continue  # noise point, not part of a hotspot
        clusters.setdefault(label, []).append(idx)

    results = []
    for label, idxs in clusters.items():
        lats = [points[i]["lat"] for i in idxs]
        lngs = [points[i]["lng"] for i in idxs]
        results.append({
            "cluster_id": int(label),
            "size": len(idxs),
            "centroid_lat": float(np.mean(lats)),
            "centroid_lng": float(np.mean(lngs)),
            "point_ids": [points[i]["id"] for i in idxs],
        })

    return sorted(results, key=lambda c: c["size"], reverse=True)
