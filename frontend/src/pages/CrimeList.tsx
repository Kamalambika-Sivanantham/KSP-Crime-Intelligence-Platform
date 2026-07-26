import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { Plus, Search } from "lucide-react";
import { api } from "../api/client";

export default function CrimeList() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["crimes", page],
    queryFn: async () => (await api.get("/crimes", { params: { page, page_size: 15 } })).data,
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">Crime Records</h1>
        <Link
          to="/crimes/new"
          className="flex items-center gap-2 bg-ksp-accent px-4 py-2 rounded-lg text-sm font-medium hover:bg-ksp-accent/90"
        >
          <Plus size={16} /> New Crime Record
        </Link>
      </div>

      <div className="glass rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-ksp-blue/50 text-ksp-steel text-left">
            <tr>
              <th className="px-4 py-3">FIR Number</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Reported At</th>
              <th className="px-4 py-3">Risk Score</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr><td colSpan={5} className="px-4 py-6 text-center text-ksp-steel">Loading...</td></tr>
            )}
            {data?.items?.map((c: any) => (
              <tr key={c.id} className="border-t border-ksp-steel/10 hover:bg-ksp-blue/30">
                <td className="px-4 py-3 font-mono text-xs">{c.fir_number}</td>
                <td className="px-4 py-3">{c.category}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded-full text-xs bg-ksp-accent/20 text-ksp-accent">{c.status}</span>
                </td>
                <td className="px-4 py-3">{new Date(c.reported_at).toLocaleDateString()}</td>
                <td className="px-4 py-3">{c.risk_score ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {data && (
        <div className="flex justify-between items-center text-sm text-ksp-steel">
          <span>Page {data.page} — {data.total} total records</span>
          <div className="space-x-2">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)} className="px-3 py-1 rounded bg-ksp-blue/40 disabled:opacity-30">Prev</button>
            <button disabled={page * data.page_size >= data.total} onClick={() => setPage((p) => p + 1)} className="px-3 py-1 rounded bg-ksp-blue/40 disabled:opacity-30">Next</button>
          </div>
        </div>
      )}
    </div>
  );
}
