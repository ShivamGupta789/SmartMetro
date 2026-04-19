import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Popup, LayersControl } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { LINES, projectToSVG } from '../lib/MetroData';
import { ChevronDown, Map as MapIcon, Layers, Info, Search } from 'lucide-react';

// FIX for default marker icon in Leaflet + React
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Custom Metro Icon builder
const createMetroIcon = (color) => L.divIcon({
  className: 'custom-metro-icon',
  html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; display: flex; items-center; justify-content: center; color: white; font-weight: bold; font-size: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.3)">M</div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10]
});

export default function LiveMap() {
  const [activeLines, setActiveLines] = useState(LINES.map(l => l.id));
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [expandedSection, setExpandedSection] = useState('lines');

  const toggleLine = (id) => {
    setActiveLines(prev => prev.includes(id) ? prev.filter(l => l !== id) : [...prev, id]);
  };

  const center = [19.1208, 72.8481]; // Andheri center

  return (
    <div className="flex bg-[#07090F] h-[calc(100vh-80px)] overflow-hidden border border-white/10 rounded-3xl m-2 relative">
      
      {/* SIDEBAR */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'w-80' : 'w-0'} bg-[#0B0F1A] border-r border-white/10 flex flex-col z-20`}>
        {sidebarOpen && (
          <>
            <div className="p-6 border-b border-white/5 bg-gradient-to-br from-brand-primary/10 to-transparent">
              <div className="flex items-center gap-3 mb-4">
                 <div className="p-2 bg-brand-primary rounded-lg shadow-lg">
                    <MapIcon size={18} className="text-white" />
                 </div>
                 <div>
                    <h2 className="text-sm font-bold text-white tracking-widest uppercase">Live Network</h2>
                    <p className="text-[10px] text-gray-500 font-mono tracking-tighter">MUMBAI METRO SPATIAL VIEW</p>
                 </div>
              </div>
              
              <div className="relative">
                <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <input 
                  type="text" 
                  placeholder="Find stations..." 
                  className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-9 pr-4 text-xs text-gray-300 focus:outline-none focus:border-brand-primary/50"
                />
              </div>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-2">
              
              {/* OPERATIONAL LINES SECTION */}
              <div className="bg-white/[0.02] rounded-xl border border-white/5 overflow-hidden">
                 <button 
                  onClick={() => setExpandedSection(expandedSection === 'lines' ? null : 'lines')}
                  className="w-full h-10 px-4 flex items-center justify-between text-[11px] font-bold text-gray-400 group hover:text-white transition"
                 >
                   <div className="flex items-center gap-2 uppercase tracking-[0.15em]">
                     <Layers size={14} className={expandedSection === 'lines' ? 'text-brand-primary' : ''} />
                     Operational Lines
                   </div>
                   <ChevronDown size={14} className={`transition ${expandedSection === 'lines' ? 'rotate-180' : ''}`} />
                 </button>
                 
                 {expandedSection === 'lines' && (
                   <div className="px-2 pb-3 space-y-1 animate-slideDown">
                     {LINES.map(line => (
                        <label key={line.id} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition">
                           <input 
                             type="checkbox" 
                             checked={activeLines.includes(line.id)}
                             onChange={() => toggleLine(line.id)}
                             className="rounded border-white/20 bg-transparent text-brand-primary focus:ring-brand-primary/20"
                           />
                           <div className="flex items-center gap-2 flex-1">
                              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: line.color }} />
                              <div className="flex flex-col">
                                 <span className="text-[11px] font-semibold text-gray-200">{line.name}</span>
                                 <span className="text-[9px] text-gray-500">{line.label} · {line.lengthKm} km</span>
                              </div>
                           </div>
                        </label>
                     ))}
                   </div>
                 )}
              </div>

              {/* STATIONS SECTION */}
              <div className="bg-white/[0.02] rounded-xl border border-white/5 overflow-hidden">
                 <button 
                  onClick={() => setExpandedSection(expandedSection === 'stations' ? null : 'stations')}
                  className="w-full h-10 px-4 flex items-center justify-between text-[11px] font-bold text-gray-400 group hover:text-white transition"
                 >
                   <div className="flex items-center gap-2 uppercase tracking-[0.15em]">
                     <MapIcon size={14} className={expandedSection === 'stations' ? 'text-emerald-400' : ''} />
                     Stations & Depots
                   </div>
                   <ChevronDown size={14} className={`transition ${expandedSection === 'stations' ? 'rotate-180' : ''}`} />
                 </button>
                 
                 {expandedSection === 'stations' && (
                   <div className="px-2 pb-3 space-y-1 max-h-[40vh] overflow-y-auto custom-scrollbar animate-slideDown">
                      {LINES.filter(l => activeLines.includes(l.id)).map(line => (
                        <div key={line.id} className="mb-4">
                           <div className="px-2 py-1 text-[9px] font-bold text-gray-500 uppercase tracking-widest">{line.name} Stations</div>
                           {line.stations.map(st => (
                             <div key={st.id} className="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5 transition cursor-default">
                                <div className="w-4 h-4 rounded-full flex items-center justify-center text-[7px] text-white font-black" style={{ backgroundColor: line.color }}>M</div>
                                <span className="text-[11px] text-gray-300">{st.name}</span>
                             </div>
                           ))}
                        </div>
                      ))}
                   </div>
                 )}
              </div>

              <div className="p-4 bg-white/[0.02] rounded-xl border border-white/5">
                 <div className="flex items-center gap-2 text-brand-cyan mb-2">
                    <Info size={14} />
                    <span className="text-[10px] font-bold uppercase tracking-widest">Network Info</span>
                 </div>
                 <p className="text-[10px] text-gray-500 leading-relaxed italic">
                    Map data represents real-time operational status for all lines. 
                    Red indicators suggest high crowd density currently detected.
                 </p>
              </div>

            </div>
          </>
        )}
      </div>

      {/* MAP TOGGLE BUTTON */}
      <button 
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="absolute left-0 top-1/2 -translate-y-1/2 z-30 bg-[#0B0F1A] border border-white/10 p-1 rounded-r-lg text-gray-400 hover:text-white transition shadow-xl"
        style={{ left: sidebarOpen ? '320px' : '0' }}
      >
        <div className={`transition-transform duration-300 ${sidebarOpen ? 'rotate-180' : ''}`}>
           <ChevronDown size={20} className="-rotate-90" />
        </div>
      </button>

      {/* MAP AREA */}
      <div className="flex-1 relative">
        <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%', background: '#07090F' }} zoomControl={false}>
          <LayersControl position="topright">
            <LayersControl.BaseLayer checked name="Dark Modern">
              <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Satellite">
              <TileLayer
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              />
            </LayersControl.BaseLayer>
          </LayersControl>

          {/* DRAW LINES AND STATIONS */}
          {LINES.filter(line => activeLines.includes(line.id)).map(line => {
            const positions = line.stations.map(st => [st.lat, st.lng]);
            return (
              <div key={line.id}>
                {/* Visual glow line */}
                <Polyline 
                  positions={positions} 
                  pathOptions={{ color: line.color, weight: 12, opacity: 0.1, lineJoin: 'round' }} 
                />
                {/* Main line */}
                <Polyline 
                  positions={positions} 
                  pathOptions={{ color: line.color, weight: 6, opacity: 0.8, lineJoin: 'round', dashArray: line.type === 'Underground' ? '10, 10' : '' }} 
                />
                
                {/* Stations */}
                {line.stations.map(st => (
                  <Marker 
                    key={st.id} 
                    position={[st.lat, st.lng]} 
                    icon={createMetroIcon(line.color)}
                  >
                    <Popup className="custom-popup">
                      <div className="p-1">
                        <h3 className="font-bold text-brand-primary mb-1">{st.name}</h3>
                        <div className="text-[10px] text-gray-600 mb-2">{line.label} · {line.type}</div>
                        <div className="flex items-center gap-2 text-[10px]">
                           <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-700 font-bold uppercase tracking-tighter">Status: Normal</span>
                        </div>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </div>
            );
          })}
        </MapContainer>

        {/* FLOATING ZOOM CONTROLS */}
        <div className="absolute top-4 left-4 z-[1000] flex flex-col gap-2">
            <div className="glass-panel p-2 flex flex-col gap-1 items-center bg-white/5 border-white/10">
               <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
               <span className="text-[8px] font-bold text-gray-500 uppercase tracking-widest vertical-text">Live</span>
            </div>
        </div>

        {/* MAP OVERLAY STATS */}
        <div className="absolute bottom-6 right-6 z-[1000] flex gap-4 pointer-events-none">
           <div className="glass-panel py-3 px-5 flex items-center gap-4 border-white/10 backdrop-blur-3xl animate-slideUp">
              <div>
                <div className="text-[8px] text-gray-500 font-bold uppercase tracking-widest mb-1">Total Length</div>
                <div className="text-lg font-black text-white">80.4 KM</div>
              </div>
              <div className="w-px h-8 bg-white/10" />
              <div>
                <div className="text-[8px] text-gray-500 font-bold uppercase tracking-widest mb-1">Active Trains</div>
                <div className="text-lg font-black text-emerald-400">124</div>
              </div>
           </div>
        </div>
      </div>

      <style>{`
        .custom-popup .leaflet-popup-content-wrapper {
          background: #0B0F1A;
          color: white;
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 12px;
        }
        .custom-popup .leaflet-popup-tip {
          background: #0B0F1A;
        }
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255,255,255,0.1);
          border-radius: 2px;
        }
        .animate-slideDown {
          animation: slideDown 0.3s ease-out forwards;
        }
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .vertical-text {
          writing-mode: vertical-rl;
          text-orientation: mixed;
        }
        .leaflet-container {
          cursor: crosshair !important;
        }
        /* Style adjustments for map visuals in the user screenshot */
        .leaflet-layer {
          filter: contrast(1.1) brightness(0.9);
        }
      `}</style>
    </div>
  );
}
