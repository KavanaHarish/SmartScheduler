import HolidayCalendar from '../components/HolidayCalendar';
import WeeklyCalendar from '../components/WeeklyCalendar';
import React, {useState} from 'react'
import axios from 'axios'
export default function AdminDashboard(){
  const [name,setName]=useState('')
  async function createDept(){ await axios.post('http://localhost:8000/api/admin/department',{name}); alert('Created'); }
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
        <div style={{background:'#fff',padding:16,borderRadius:8}}>
          <h3>Create Department</h3>
          <input value={name} onChange={e=>setName(e.target.value)} placeholder='Department name' />
          <button onClick={createDept}>Create</button>
        </div>
        <div style={{background:'#fff',padding:16,borderRadius:8}}>
          <h3>Generate Timetable (demo)</h3>
          <button onClick={async()=>{ await axios.post('http://localhost:8000/api/admin/generate-intelligent',{year:new Date().getFullYear(), month:new Date().getMonth()+1, classes:[{class_name:'CSE 1', subjects:[{name:'DS'},{name:'Algo'}]}]}); alert('Generated'); }}>Generate</button>
        </div>
      </div>
      <div style={{marginTop:20}}>
        <HolidayCalendar />
      </div>
    </div>
  )
}
