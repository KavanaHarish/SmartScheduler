import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Login from './pages/Login'
import AdminDashboard from './pages/AdminDashboard'
import TeacherDashboard from './pages/TeacherDashboard'
import StudentDashboard from './pages/StudentDashboard'

export default function App(){
  return (
    <div style={{display:'flex', minHeight:'100vh'}}>
      <aside style={{width:260, background:'#fff', padding:20, boxShadow:'0 2px 8px rgba(0,0,0,0.06)'}}>
        <h2 style={{margin:0}}>HackNova</h2>
        <nav style={{marginTop:20, display:'flex', flexDirection:'column', gap:10}}>
          <Link to="/admin">Admin</Link>
          <Link to="/teacher/1">Teacher</Link>
          <Link to="/student/S001">Student</Link>
          <Link to="/login">Login</Link>
        </nav>
      </aside>
      <main style={{flex:1, padding:24}}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/teacher/:id" element={<TeacherDashboard />} />
          <Route path="/student/:id" element={<StudentDashboard />} />
          <Route path="*" element={<div>Welcome — use the side menu.</div>} />
        </Routes>
      </main>
    </div>
  )
}
