import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Users, FileText, Settings, Activity } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts';
import './DashboardHome.css';

const dataServiciosMes = [
  { name: 'Ene', servicios: 45 },
  { name: 'Feb', servicios: 52 },
  { name: 'Mar', servicios: 38 },
  { name: 'Abr', servicios: 65 },
  { name: 'May', servicios: 48 },
  { name: 'Jun', servicios: 70 },
];

const dataIngresos = [
  { name: 'Ene', ingresos: 12500 },
  { name: 'Feb', ingresos: 15200 },
  { name: 'Mar', ingresos: 13800 },
  { name: 'Abr', ingresos: 18500 },
  { name: 'May', ingresos: 17200 },
  { name: 'Jun', ingresos: 22000 },
];

const dataTopServicios = [
  { name: 'Afinación', cantidad: 45 },
  { name: 'Frenos', cantidad: 38 },
  { name: 'Aceite', cantidad: 60 },
  { name: 'Suspensión', cantidad: 25 },
];

const dataEstadoOSTDefault = [
  { name: 'En Espera', value: 12 },
  { name: 'En Proceso', value: 25 },
  { name: 'Terminado', value: 15 },
  { name: 'Entregado', value: 45 },
];

const COLORS = ['#f59e0b', '#3b82f6', '#10b981', '#6b7280'];

const DashboardHome = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/ost/dashboard/stats');
        setStats(response.data);
      } catch (error) {
        console.error('Error al cargar estadísticas reales:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  // Map database states to human readable names for the Pie Chart
  const chartDataEstado = stats && stats.osts_por_estado && stats.osts_por_estado.length > 0
    ? stats.osts_por_estado.map(item => {
        let displayName = item.estado;
        if (item.estado === 'PENDIENTE') displayName = 'Pendiente';
        if (item.estado === 'EN_PROCESO') displayName = 'En Proceso';
        if (item.estado === 'COMPLETADA') displayName = 'Completada';
        return { name: displayName, value: item.cantidad };
      })
    : dataEstadoOSTDefault;

  return (
    <div className="dashboard-home">
      <h2>Bienvenido al Panel de Administración</h2>
      <p className="welcome-text">Desde aquí puedes gestionar los clientes, órdenes de trabajo y configurar el sistema.</p>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon clients">
            <Users size={24} />
          </div>
          <div className="stat-info">
            <h3>Clientes Totales</h3>
            <p className="stat-value">{loading ? '...' : (stats?.resumen?.total_clientes ?? 0)}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon orders">
            <FileText size={24} />
          </div>
          <div className="stat-info">
            <h3>Órdenes Totales</h3>
            <p className="stat-value">{loading ? '...' : (stats?.resumen?.total_osts ?? 0)}</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon activity">
            <Activity size={24} />
          </div>
          <div className="stat-info">
            <h3>Servicios del Mes</h3>
            <p className="stat-value">45</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon settings">
            <Settings size={24} />
          </div>
          <div className="stat-info">
            <h3>Alertas de Inventario</h3>
            <p className="stat-value">3</p>
          </div>
        </div>
      </div>
      <div className="charts-section">
        <div className="chart-card full-width">
          <h3>Ingresos Brutos (Últimos 6 Meses)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dataIngresos} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorIngresos" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} tickFormatter={(value) => `$${value}`} />
              <Tooltip formatter={(value) => [`$${value}`, 'Ingresos']} cursor={{ fill: 'transparent' }} />
              <Area type="monotone" dataKey="ingresos" stroke="#10b981" fillOpacity={1} fill="url(#colorIngresos)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="charts-grid three-cols">
          <div className="chart-card">
            <h3>Top Servicios</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dataTopServicios} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" axisLine={false} tickLine={false} />
                <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: '#f3f4f6'}} />
                <Bar dataKey="cantidad" fill="#f59e0b" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Servicios por Mes</h3>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dataServiciosMes}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: '#f3f4f6'}} />
                <Bar dataKey="servicios" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="chart-card">
            <h3>Estado de Órdenes</h3>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartDataEstado}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  label
                >
                  {chartDataEstado.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>


      <div className="recent-activity">
        <h3>Actividad Reciente</h3>
        <div className="empty-state">
          <p>El sistema está listo para registrar nueva actividad.</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
