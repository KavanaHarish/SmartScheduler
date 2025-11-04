import WeeklyCalendar from '../components/WeeklyCalendar';
import React, {useEffect, useState} from 'react'
import axios from 'axios'
import { useParams } from 'react-router-dom'
export default function StudentDashboard(){
  const { id } = useParams();
  const [entries,setEntries]=useState([])
  useEffect(()=>{ fetch() },[id])
  async function fetch(){ try{ const r=await axios.get(`http://localhost:8000/api/student/${id}/timetable`); setEntries(r.data) }catch(e){console.error(e)} }
  return (
    <div>
      <h1>Student Dashboard</h1>
      <div style={{background:'#fff',padding:16,borderRadius:8}}>
        {entries.length===0? <div>No classes yet</div> : (<ul>{entries.map(e=> <li key={e.id}>{e.date} — {e.subject} — {e.room}</li>)}</ul>)}
      </div>
    </div>
  )
}
