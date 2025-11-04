import WeeklyCalendar from '../components/WeeklyCalendar';
import React, {useEffect, useState} from 'react'
import axios from 'axios'
import { useParams } from 'react-router-dom'
export default function TeacherDashboard(){
  const { id } = useParams();
  const [entries,setEntries]=useState([])
  useEffect(()=>{ fetch() },[id])
  async function fetch(){ try{ const r=await axios.get(`http://localhost:8000/api/teacher/pending/${id}`); setEntries(r.data) }catch(e){console.error(e)} }
  async function respond(eid,resp){ await axios.patch(`http://localhost:8000/api/teacher/respond/${eid}`,{response:resp}); fetch(); }
  return (
    <div>
      <h1>Teacher Dashboard</h1>
      <div style={{background:'#fff',padding:16,borderRadius:8}}>
        <h3>Pending</h3>
        {entries.length===0? <div>No pending</div> : (
          <table style={{width:'100%'}}>
            <thead><tr><th>Date</th><th>Class</th><th>Subject</th><th>Action</th></tr></thead>
            <tbody>
              {entries.map(e=> (<tr key={e.id}><td>{e.date}</td><td>{e.class_name} {e.section}</td><td>{e.subject}</td><td><button onClick={()=>respond(e.id,'available')}>Available</button><button onClick={()=>respond(e.id,'unavailable')}>Unavailable</button></td></tr>))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
