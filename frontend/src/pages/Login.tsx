import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ShieldAlert } from "lucide-react";
import { api } from "../api/client";
import { setUser } from "../store/authSlice";

const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});
type FormData = z.infer<typeof schema>;

export default function Login() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [error, setError] = useState<string | null>(null);
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    setError(null);
    try {
      const { data: tokens } = await api.post("/auth/login", data);
      localStorage.setItem("ksp_access_token", tokens.access_token);
      localStorage.setItem("ksp_refresh_token", tokens.refresh_token);
      const { data: me } = await api.get("/auth/me");
      dispatch(setUser(me));
      navigate("/dashboard");
    } catch {
      setError("Invalid credentials. Please check your email and password.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-ksp-surface">
      <div className="glass rounded-2xl p-8 w-full max-w-sm">
        <div className="flex flex-col items-center mb-6">
          <ShieldAlert className="text-ksp-accent mb-2" size={40} />
          <h1 className="text-lg font-bold text-center">KSP Crime Intelligence</h1>
          <p className="text-xs text-ksp-steel">& Analytics Platform</p>
        </div>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="text-sm text-ksp-steel">Email</label>
            <input
              {...register("email")}
              className="w-full mt-1 px-3 py-2 rounded-lg bg-ksp-blue/40 border border-ksp-steel/30 outline-none focus:border-ksp-accent"
              placeholder="officer@ksp.gov.in"
            />
            {errors.email && <p className="text-red-300 text-xs mt-1">{errors.email.message}</p>}
          </div>
          <div>
            <label className="text-sm text-ksp-steel">Password</label>
            <input
              type="password"
              {...register("password")}
              className="w-full mt-1 px-3 py-2 rounded-lg bg-ksp-blue/40 border border-ksp-steel/30 outline-none focus:border-ksp-accent"
              placeholder="••••••••"
            />
            {errors.password && <p className="text-red-300 text-xs mt-1">{errors.password.message}</p>}
          </div>
          {error && <p className="text-red-300 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-ksp-accent hover:bg-ksp-accent/90 transition-colors py-2.5 rounded-lg font-medium disabled:opacity-50"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}
