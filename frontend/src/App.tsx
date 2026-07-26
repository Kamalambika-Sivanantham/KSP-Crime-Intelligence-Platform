import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { RootState } from "./store";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CrimeList from "./pages/CrimeList";
import CrimeForm from "./pages/CrimeForm";
import GISMap from "./pages/GISMap";
import NetworkGraph from "./pages/NetworkGraph";


function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useSelector((s: RootState) => s.auth.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="crimes" element={<CrimeList />} />
        <Route path="crimes/new" element={<CrimeForm />} />
        <Route path="map" element={<GISMap />} />
        <Route path="network" element={<NetworkGraph />} />
      </Route>
    </Routes>
  );
}
