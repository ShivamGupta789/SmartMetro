import { create } from 'zustand';

const useStore = create((set) => ({
  user: null, // Initial state should be null for real authentication flow
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
  
  liveCrowds: {}, // Station mapping: "Andheri" -> "HIGH"
  updateCrowd: (stationId, level) => set((state) => ({
    liveCrowds: { ...state.liveCrowds, [stationId]: level }
  })),
  
  booking: { lineId: "L3", from: "", to: "", passengers: 1, cls: "AC" },
  setBooking: (update) => set((state) => ({ booking: { ...state.booking, ...update } })),
  
  bookedTickets: [],
  addBookedTickets: (tickets) => set((state) => ({ bookedTickets: [...state.bookedTickets, ...tickets] })),
}));

export default useStore;
