import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function HolidayCalendar() {
  const [holidays, setHolidays] = useState([]);

  async function fetchHolidays() {
    try {
      const res = await axios.get(`${API_URL}/api/admin/holidays`);
      const ev = res.data.map(h => ({
        id: h.id,
        title: h.description || 'Holiday',
        date: h.date,
        color: '#e53935'
      }));
      setHolidays(ev);
    } catch (e) { console.error(e); }
  }

  useEffect(()=>{ fetchHolidays(); }, []);

  async function handleDateClick(info) {
    const date = info.dateStr;
    const exists = holidays.find(h => h.date === date);
    if (exists) {
      await axios.delete(`${API_URL}/api/admin/remove-holiday/${date}`);
      fetchHolidays();
      alert('Holiday removed');
    } else {
      const desc = prompt('Holiday name (optional):', 'Holiday');
      await axios.post(`${API_URL}/api/admin/add-holiday`, { date, description: desc });
      fetchHolidays();
      alert('Holiday added');
    }
  }

  return (
    <div>
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={holidays}
        dateClick={handleDateClick}
        height="70vh"
        headerToolbar={{ left:'prev,next today', center:'title', right:'' }}
      />
    </div>
  );
}
