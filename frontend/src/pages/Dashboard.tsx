import { useQuery } from "@tanstack/react-query";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, CartesianGrid } from "recharts";
import { AlertTriangle, ShieldCheck, Activity, Siren } from "lucide-react";
import { api } from "../api/client";

const COLORS = ["#2E6FDB", "#8B9BB4", "#4C9F70", "#D67E3C", "#C24444", "#7B5FD1", "#3AAFA9", "#C2A83A", "#B65C9E", "#5C8AC2"];

export default function Dashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: async () => (await api.get("/dashboard/summary")).data,
  });

  if (isLoading || !data) {
    return <div className="animate-pulse text-ksp-steel">Loading dashboard...</div>;
  }

  const cards = [
    { label: "Total Crimes", value: data.total_crimes, icon: Activity, color: "text-ksp-accent" },
    { label: "Today's Incidents", value: data.todays_incidents, icon: Siren, color: "text-yellow-400" },
    { label: "Under Investigation", value: data.under_investigation, icon: AlertTriangle, color: "text-orange-400" },
    { label: "Closed Cases", value: data.closed, icon: ShieldCheck, color: "text-green-400" },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">State-Level Crime Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {cards.map((c) => (
          <div key={c.label} className="glass rounded-xl p-4 flex items-center justify-between">
            <div>
              <div className="text-xs text-ksp-steel">{c.label}</div>
              <div className="text-2xl font-bold">{c.value}</div>
            </div>
            <c.icon className={c.color} size={28} />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-xl p-4">
          <h2 className="text-sm font-semibold mb-3 text-ksp-steel">30-Day Crime Trend</h2>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={data.trend_30_days}>
              <CartesianGrid strokeDasharray="3 3" stroke="#8B9BB420" />
              <XAxis dataKey="date" tick={{ fontSize: 10, fill: "#8B9BB4" }} />
              <YAxis tick={{ fontSize: 10, fill: "#8B9BB4" }} />
              <Tooltip contentStyle={{ background: "#13315C", border: "none" }} />
              <Line type="monotone" dataKey="count" stroke="#2E6FDB" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="glass rounded-xl p-4">
          <h2 className="text-sm font-semibold mb-3 text-ksp-steel">Crimes by Category</h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={data.by_category} dataKey="count" nameKey="category" outerRadius={90} label>
                {data.by_category.map((_: unknown, i: number) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#13315C", border: "none" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="glass rounded-xl p-4 lg:col-span-2">
          <h2 className="text-sm font-semibold mb-3 text-ksp-steel">Top Districts by Crime Volume</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.top_districts}>
              <CartesianGrid strokeDasharray="3 3" stroke="#8B9BB420" />
              <XAxis dataKey="district_id" tick={{ fontSize: 9, fill: "#8B9BB4" }} hide />
              <YAxis tick={{ fontSize: 10, fill: "#8B9BB4" }} />
              <Tooltip contentStyle={{ background: "#13315C", border: "none" }} />
              <Bar dataKey="count" fill="#2E6FDB" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
