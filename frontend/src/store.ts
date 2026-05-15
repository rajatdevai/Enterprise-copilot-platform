import { create } from 'zustand';

interface User {
  id: string;
  email: string;
  role: string;
  tenant_id: string;
}

interface ChatState {
  user: User | null;
  token: string | null;
  sessions: any[];
  currentSessionId: string | null;
  setUser: (user: User | null, token: string | null) => void;
  setSessions: (sessions: any[]) => void;
  setCurrentSession: (id: string | null) => void;
  logout: () => void;
}

export const useAppStore = create<ChatState>((set) => ({
  user: null,
  token: null,
  sessions: [],
  currentSessionId: null,
  setUser: (user, token) => set({ user, token }),
  setSessions: (sessions) => set({ sessions }),
  setCurrentSession: (id) => set({ currentSessionId: id }),
  logout: () => set({ user: null, token: null, sessions: [], currentSessionId: null }),
}));
