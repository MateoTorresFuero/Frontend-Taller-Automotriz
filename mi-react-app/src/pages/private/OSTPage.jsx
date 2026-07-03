import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { Plus, Search, Calendar, Eye } from 'lucide-react';
import './OSTPage.css';

const OSTPage = () => {
  const [osts, setOsts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Filters State
  const [filters, setFilters] = useState({
    estado: '',
    placa: '',
    fecha_desde: '',
    fecha_hasta: ''
  });

  useEffect(() => {
    fetchOsts();
  }, []);

  const fetchOsts = async (currentFilters = filters) => {
    setLoading(true);
    setError('');
    try {
      // Build clean query params
      const params = {};
      if (currentFilters.estado) params.estado = currentFilters.estado;
      if (currentFilters.placa) params.placa = currentFilters.placa;
      if (currentFilters.fecha_desde) params.fecha_desde = `${currentFilters.fecha_desde}T00:00:00`;
      if (currentFilters.fecha_hasta) params.fecha_hasta = `${currentFilters.fecha_hasta}T23:59:59`;

      const response = await api.get('/ost/', { params });
      setOsts(response.data);
      setLoading(false);
    } catch (err) {
      setError('Error al cargar las órdenes de servicio técnico.');
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleApplyFilters = (e) => {
    if (e) e.preventDefault();
    fetchOsts();
  };

  const handleResetFilters = () => {
    const defaultFilters = {
      estado: '',
      placa: '',
      fecha_desde: '',
      fecha_hasta: ''
    };
    setFilters(defaultFilters);
    fetchOsts(defaultFilters);
  };

  const formatFecha = (fechaString) => {
    if (!fechaString) return '-';
    try {
      const date = new Date(fechaString);
      return date.toLocaleDateString('es-PE', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (err) {
      return fechaString;
    }
  };

  return (
    <div className="ost-page">
      <div className="page-header">
        <div>
          <h2>Órdenes de Servicio Técnico (OST)</h2>
          <p>Consulta, filtra y registra las órdenes de servicio del taller.</p>
        </div>
        <button 
          className="btn-primary"
          onClick={() => navigate('/dashboard/ost/nuevo')}
        >
          <Plus size={20} />
          Nueva Orden (OST)
        </button>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <div className="filters-container">
        <form onSubmit={handleApplyFilters} className="filters-form">
          <div className="filter-group">
            <label htmlFor="estado">Estado</label>
            <select 
              id="estado" 
              name="estado" 
              value={filters.estado} 
              onChange={handleFilterChange}
            >
              <option value="">Todos</option>
              <option value="PENDIENTE">PENDIENTE</option>
              <option value="EN_PROCESO">EN PROCESO</option>
              <option value="COMPLETADA">COMPLETADA</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="placa">Placa</label>
            <input 
              type="text" 
              id="placa" 
              name="placa" 
              value={filters.placa} 
              onChange={handleFilterChange}
              placeholder="Ej. ABC-123"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="fecha_desde">Desde</label>
            <input 
              type="date" 
              id="fecha_desde" 
              name="fecha_desde" 
              value={filters.fecha_desde} 
              onChange={handleFilterChange}
            />
          </div>

          <div className="filter-group">
            <label htmlFor="fecha_hasta">Hasta</label>
            <input 
              type="date" 
              id="fecha_hasta" 
              name="fecha_hasta" 
              value={filters.fecha_hasta} 
              onChange={handleFilterChange}
            />
          </div>

          <div className="filter-actions-row">
            <button type="submit" className="btn-primary btn-filter">
              Filtrar
            </button>
            <button type="button" className="btn-secondary btn-reset" onClick={handleResetFilters}>
              Reestablecer
            </button>
          </div>
        </form>
      </div>

      <div className="table-container">
        {loading ? (
          <div className="loading-state">Cargando órdenes de trabajo...</div>
        ) : osts.length === 0 ? (
          <div className="empty-state">
            <p>No se encontraron órdenes de servicio técnico con los filtros seleccionados.</p>
            <button className="btn-secondary" onClick={() => navigate('/dashboard/ost/nuevo')}>
              Registrar nueva orden
            </button>
          </div>
        ) : (
          <table className="data-table clickable-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Fecha Ingreso</th>
                <th>Cliente</th>
                <th>Vehículo</th>
                <th>Falla Reportada</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {osts.map((ost) => (
                <tr key={ost.id} onClick={() => navigate(`/dashboard/ost/${ost.id}`)}>
                  <td className="font-semibold text-primary">{ost.codigo}</td>
                  <td>{formatFecha(ost.fecha_ingreso)}</td>
                  <td>
                    <div className="font-medium">
                      {ost.cliente.persona.nombres} {ost.cliente.persona.apellido_paterno}
                    </div>
                    <span className="text-muted text-small">{ost.cliente.persona.numero_documento}</span>
                  </td>
                  <td>
                    <span className="plate-badge">{ost.placa}</span>
                    <div className="text-small text-muted">{ost.marca} {ost.modelo}</div>
                  </td>
                  <td className="truncate-text" title={ost.falla_reportada}>
                    {ost.falla_reportada}
                  </td>
                  <td>
                    <span className={`status-badge ${ost.estado.toLowerCase()}`}>
                      {ost.estado}
                    </span>
                  </td>
                  <td className="actions-cell" onClick={(e) => e.stopPropagation()}>
                    <button 
                      className="btn-icon" 
                      title="Ver Detalle" 
                      onClick={() => navigate(`/dashboard/ost/${ost.id}`)}
                    >
                      <Eye size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default OSTPage;
