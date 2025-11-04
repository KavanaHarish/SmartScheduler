import React, {useState} from 'react'
import axios from 'axios'
export default function Login(){
  const [u,setU]=useState('')
  const [p,setP]=useState('')
  async function s(e){
    e.preventDefault();
    try{ const r = await axios.post('http://localhost:8000/api/auth/login',{username:u,password:p}); alert(JSON.stringify(r.data)) }catch(e){ alert('Login failed') }
  }
  return (
    <div style={{maxWidth:480}}>
      <h2>Login</h2>
      <form onSubmit={s} style={{display:'flex',flexDirection:'column',gap:8}}>
        <input placeholder='username' value={u} onChange={e=>setU(e.target.value)} />
        <input placeholder='password' type='password' value={p} onChange={e=>setP(e.target.value)} />
        <button>Login</button>
      </form>
    </div>
  )
}
