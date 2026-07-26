import { NavLink, Outlet } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { LayoutDashboard, FileText, Map, Network, LogOut, ShieldAlert } from "lucide-react";
import { RootState } from "../store";
import { logout } from "../store/authSlice";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/crimes", label: "Crime Records", icon: FileText },
  { to: "/map", label: "GIS Crime Map", icon: Map },
  { to: "/network", label: "Network Analysis", icon: Network },
];

export default function Layout() {
  const dispatch = useDispatch();
  const user = useSelector((s: RootState) => s.auth.user);

  return (
    <div className="flex h-screen bg-ksp-surface">
      <aside className="w-64 flex-shrink-0 border-r border-ksp-steel/20 bg-ksp-navy/60 flex flex-col">
        <div className="px-5 py-6 flex items-center gap-2 border-b border-ksp-steel/20">
          <ShieldAlert className="text-ksp-accent" size={28} />
          <div>
            <div className="font-bold text-sm leading-tight">KSP Crime Intelligence</div>
            <div className="text-xs text-ksp-steel">& Analytics Platform</div>
          </div>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive ? "bg-ksp-accent text-white" : "text-ksp-steel hover:bg-ksp-blue/50 hover:text-white"
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-ksp-steel/20">
          <div className="text-sm font-medium">{user?.full_name ?? "Officer"}</div>
          <div className="text-xs text-ksp-steel mb-3">{user?.role ?? ""}</div>
          <button
            onClick={() => dispatch(logout())}
            className="flex items-center gap-2 text-sm text-red-300 hover:text-red-200"
          >
            <LogOut size={16} /> Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}
