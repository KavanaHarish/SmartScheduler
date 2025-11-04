import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';

export default function WeeklyCalendar({ userRole, userId }) {
  const [events, setEvents] = useState([]);
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    async function fetchData() {
      try {
        let res;
        if (userRole === 'teacher') {
          res = await axios.get(`${API_URL}/api/teacher/pending/${userId}`);
        } else {
          res = await axios.get(`${API_URL}/api/student/${userId}/timetable`);
        }
        // map entries to fullcalendar events (assume date field present)
        const ev = res.data.map(e => ({
          id: e.id,
          title: `${e.subject} (${e.room || ''})`,
          start: e.date,
          end: e.date, // date only entries; could be extended with timeslots
          allDay: true,
          backgroundColor: userRole === 'teacher' ? '#1976d2' : '#43a047'
        }));
        setEvents(ev);
      } catch (err) {
        console.error(err);
      }
    }
    fetchData();
  }, [userRole, userId]);

  return (
    <div>
      <FullCalendar
        plugins={[timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        headerToolbar={{ left: 'prev,next today', center: 'title', right: 'timeGridWeek,timeGridDay' }}
        events={events}
        editable={userRole === 'teacher'}
        height="auto"
      />
    </div>
  );
}
