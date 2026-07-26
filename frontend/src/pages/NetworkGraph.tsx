import { useQuery } from "@tanstack/react-query";
import CytoscapeComponent from "react-cytoscapejs";
import { api } from "../api/client";

export default function NetworkGraph() {
  const { data, isLoading } = useQuery({
    queryKey: ["network"],
    queryFn: async () => (await api.get("/ai/network")).data,
  });

  if (isLoading || !data) return <div className="text-ksp-steel">Loading network...</div>;

  const elements = [
    ...data.nodes.map((n: any) => ({
      data: { id: n.id, label: n.id.split(":")[1], type: n.type, size: 20 + n.degree * 4 },
    })),
    ...data.edges.map((e: any, i: number) => ({
      data: { id: `e${i}`, source: e.source, target: e.target, label: e.relationship },
    })),
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Crime Network Analysis</h1>
      <p className="text-sm text-ksp-steel">
        {data.communities.length} communities detected across {data.nodes.length} entities.
      </p>
      <div className="glass rounded-xl overflow-hidden" style={{ height: "70vh" }}>
        <CytoscapeComponent
          elements={elements}
          style={{ width: "100%", height: "100%" }}
          layout={{ name: "cose", animate: false }}
          stylesheet={[
            {
              selector: "node",
              style: {
                "background-color": "#2E6FDB",
                label: "data(label)",
                color: "#fff",
                "font-size": 8,
                width: "data(size)",
                height: "data(size)",
              },
            },
            {
              selector: "edge",
              style: {
                width: 1.5,
                "line-color": "#8B9BB4",
                "curve-style": "bezier",
                label: "data(label)",
                "font-size": 6,
                color: "#8B9BB4",
              },
            },
          ]}
        />
      </div>
    </div>
  );
}
