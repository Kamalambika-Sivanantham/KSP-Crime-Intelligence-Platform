import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface AuthUser {
  id: string;
  full_name: string;
  email: string;
  role: string;
  badge_number: string;
}

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: !!localStorage.getItem("ksp_access_token"),
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser(state, action: PayloadAction<AuthUser>) {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    logout(state) {
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem("ksp_access_token");
      localStorage.removeItem("ksp_refresh_token");
    },
  },
});

export const { setUser, logout } = authSlice.actions;
export default authSlice.reducer;
