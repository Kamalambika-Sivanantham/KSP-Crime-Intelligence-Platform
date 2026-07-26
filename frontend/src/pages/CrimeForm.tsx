import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";

const schema = z.object({
  fir_number: z.string().min(3, "FIR number is required"),
  category: z.string(),
  description: z.string().optional(),
  modus_operandi: z.string().optional(),
  lat: z.coerce.number(),
  lng: z.coerce.number(),
  address: z.string().optional(),
  district_id: z.string().uuid("Select a district"),
  police_station_id: z.string().uuid("Select a police station"),
  reported_at: z.string(),
});
type FormData = z.infer<typeof schema>;

const CATEGORIES = ["THEFT", "ROBBERY", "ASSAULT", "HOMICIDE", "CYBERCRIME", "NARCOTICS", "KIDNAPPING", "FRAUD", "DOMESTIC_VIOLENCE", "OTHER"];

export default function CrimeForm() {
  const [aiResult, setAiResult] = useState<any>(null);
  const navigate = useNavigate();
  const { register, handleSubmit, watch, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const districtId = watch("district_id");
  const { data: districts } = useQuery({
    queryKey: ["districts"],
    queryFn: async () => (await api.get("/districts")).data,
  });
  const { data: stations } = useQuery({
    queryKey: ["stations", districtId],
    queryFn: async () => (await api.get(`/districts/${districtId}/police-stations`)).data,
    enabled: !!districtId,
  });
  const analyzeCrime = async () => {
  try {
    const description = watch("description");

    const res = await api.post("/ai/analyze", {
      description: description || "",
    });

    setAiResult(res.data);
  } catch (err) {
    console.error(err);
    alert("AI Analysis Failed");
  }
};
  const onSubmit = async (data: FormData) => {
    await api.post("/crimes", { ...data, reported_at: new Date(data.reported_at).toISOString() });
    navigate("/crimes");
  };

  const inputCls = "w-full mt-1 px-3 py-2 rounded-lg bg-ksp-blue/40 border border-ksp-steel/30 outline-none focus:border-ksp-accent";

  return (
    <div className="max-w-2xl">
      <h1 className="text-xl font-bold mb-4">New Crime Record</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="glass rounded-xl p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm text-ksp-steel">FIR Number</label>
            <input {...register("fir_number")} className={inputCls} placeholder="FIR/BLR/2026/1001" />
            {errors.fir_number && <p className="text-red-300 text-xs mt-1">{errors.fir_number.message}</p>}
          </div>
          <div>
            <label className="text-sm text-ksp-steel">Category</label>
            <select {...register("category")} className={inputCls}>
              {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label className="text-sm text-ksp-steel">District</label>
            <select {...register("district_id")} className={inputCls}>
              <option value="">Select district</option>
              {districts?.map((d: any) => <option key={d.id} value={d.id}>{d.name}</option>)}
            </select>
            {errors.district_id && <p className="text-red-300 text-xs mt-1">{errors.district_id.message}</p>}
          </div>
          <div>
            <label className="text-sm text-ksp-steel">Police Station</label>
            <select {...register("police_station_id")} className={inputCls} disabled={!districtId}>
              <option value="">Select station</option>
              {stations?.map((s: any) => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
            {errors.police_station_id && <p className="text-red-300 text-xs mt-1">{errors.police_station_id.message}</p>}
          </div>
          <div>
            <label className="text-sm text-ksp-steel">Latitude</label>
            <input {...register("lat")} className={inputCls} placeholder="12.9716" />
          </div>
          <div>
            <label className="text-sm text-ksp-steel">Longitude</label>
            <input {...register("lng")} className={inputCls} placeholder="77.5946" />
          </div>
          <div className="col-span-2">
            <label className="text-sm text-ksp-steel">Address</label>
            <input {...register("address")} className={inputCls} />
          </div>
          <div className="col-span-2">
            <label className="text-sm text-ksp-steel">Reported At</label>
            <input type="datetime-local" {...register("reported_at")} className={inputCls} />
          </div>
          <div className="col-span-2">
            <label className="text-sm text-ksp-steel">Description</label>
            <textarea {...register("description")} className={inputCls} rows={3} />
          </div>
          <div className="col-span-2">
            <button
              type="button"
              onClick={analyzeCrime}
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-8 py-3"
            >
              🤖 AI Analyze
            </button>
            {aiResult && (
  <div className="col-span-2 p-4 rounded-lg bg-ksp-blue/40 border border-ksp-accent">
    <h3 className="font-bold mb-2">🤖 AI Analysis Result</h3>

    <p>
      <strong>Crime Type:</strong> {aiResult.crime_type}
    </p>

    <p>
      <strong>Risk Score:</strong> {aiResult.risk_score}
    </p>

    <p>
      <strong>Alert Level:</strong> {aiResult.alert}
    </p>

    <p className="mt-2 font-semibold">
      Recommended Actions:
    </p>

    <ul className="list-disc ml-5">
      {aiResult.recommended_action.map((item: string, index: number) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  </div>
)}
          </div>
          <div className="col-span-2">
            <label className="text-sm text-ksp-steel">Modus Operandi</label>
            <textarea {...register("modus_operandi")} className={inputCls} rows={2} />
          </div>
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="bg-ksp-accent hover:bg-ksp-accent/90 px-5 py-2.5 rounded-lg font-medium disabled:opacity-50"
        >
          {isSubmitting ? "Saving..." : "Save Crime Record"}
        </button>
      </form>
    </div>
  );
}