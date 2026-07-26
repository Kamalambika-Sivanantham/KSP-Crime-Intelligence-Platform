import axios from "axios";

export const api = axios.create({
  baseURL: "https://ksp-backend-a9wz.onrender.com/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("ksp_access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const refreshToken = localStorage.getItem("ksp_refresh_token");
      if (refreshToken) {
        try {
          const { data } = await axios.post("/api/v1/auth/refresh", { refresh_token: refreshToken });
          localStorage.setItem("ksp_access_token", data.access_token);
          localStorage.setItem("ksp_refresh_token", data.refresh_token);
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return api(error.config);
        } catch {
          localStorage.removeItem("ksp_access_token");
          localStorage.removeItem("ksp_refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);
