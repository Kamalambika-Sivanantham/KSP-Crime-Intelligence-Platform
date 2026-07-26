from app.ml.hotspot import detect_hotspots


def test_detect_hotspots_finds_dense_cluster():
    # A tight cluster of 6 points plus one far-away noise point
    points = [{"id": str(i), "lat": 12.9716 + i * 0.0005, "lng": 77.5946 + i * 0.0005} for i in range(6)]
    points.append({"id": "noise", "lat": 20.0, "lng": 85.0})

    hotspots = detect_hotspots(points, eps_km=0.5, min_samples=4)

    assert len(hotspots) == 1
    assert hotspots[0]["size"] == 6
    assert "noise" not in hotspots[0]["point_ids"]


def test_detect_hotspots_empty_input():
    assert detect_hotspots([]) == []
