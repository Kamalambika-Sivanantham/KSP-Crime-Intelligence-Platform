import { useQuery } from "@tanstack/react-query";
import { MapContainer, TileLayer, CircleMarker, Popup, Circle } from "react-leaflet";
import { api } from "../api/client";

const KARNATAKA_CENTER: [number, number] = [15.3173, 75.7139];

export default function GISMap() {
  const { data: crimeData } = useQuery({
    queryKey: ["crimes-map"],
    queryFn: async () => (await api.get("/crimes", { params: { page_size: 100 } })).data,
  });

  const { data: hotspots } = useQuery({
    queryKey: ["hotspots"],
    queryFn: async () => (await api.get("/ai/hotspots", { params: { eps_km: 2, min_samples: 3 } })).data,
  });

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">GIS Crime Map — Karnataka</h1>
      <div className="glass rounded-xl overflow-hidden" style={{ height: "70vh" }}>
        <MapContainer center={KARNATAKA_CENTER} zoom={7} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {crimeData?.items?.map((c: any) => (
            <CircleMarker key={c.id} center={[c.lat, c.lng]} radius={5} pathOptions={{ color: "#2E6FDB", fillOpacity: 0.7 }}>
              <Popup>
                <div className="text-xs">
                  <strong>{c.fir_number}</strong><br />
                  {c.category} — {c.status}
                </div>
              </Popup>
            </CircleMarker>
          ))}
          {hotspots?.hotspots?.map((h: any) => (
            <Circle
              key={h.cluster_id}
              center={[h.centroid_lat, h.centroid_lng]}
              radius={h.size * 300}
              pathOptions={{ color: "#C24444", fillOpacity: 0.15, weight: 1 }}
            >
              <Popup>Hotspot cluster #{h.cluster_id} — {h.size} incidents</Popup>
            </Circle>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
