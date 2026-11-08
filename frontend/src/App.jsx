import React, {useEffect, useMemo, useState} from 'react';
import {Camera, Clapperboard, Palette, Globe, CalendarDays, Users, Wallet, CheckCircle2, Clock3, ArrowUpRight, Plus, Search, Menu, X, LayoutDashboard, BriefcaseBusiness, ClipboardList, Settings, ChevronRight, MapPin, Phone, Mail, Sparkles, Image, Video, MonitorSmartphone, CircleDollarSign, Download, Filter, Bell} from 'lucide-react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const serviceGroups = [
 {id:'videography',label:'Videography',icon:Video,desc:'Events, campaigns and brand films'},
 {id:'photography',label:'Photography',icon:Camera,desc:'Portraits, products and events'},
 {id:'branding',label:'Branding & identity',icon:Palette,desc:'Visual identity, stationery and slogans'},
 {id:'digital',label:'Digital marketing & UI',icon:MonitorSmartphone,desc:'Web mockups, social retainers and Reels'},
 {id:'photomounts',label:'Photomounts',icon:Image,desc:'Professional photo mounting and display prints in sizes A4 to A0'}
];

const packages = [
 {id:'silver',name:'Silver',tag:'Essential',desc:'A polished, professional starting point',price:'Custom quote'},
 {id:'gold',name:'Gold',tag:'Most popular',desc:'More coverage and creative flexibility',price:'Custom quote',popular:true},
 {id:'platinum',name:'Platinum',tag:'Premium',desc:'Premium production and comprehensive coverage',price:'Custom quote'},
 {id:'custom',name:'Custom / hourly',tag:'Flexible',desc:'Tailored scope and event duration',price:'Custom quote'},
 {id:'studio',name:'Indoor studio shoot',tag:'Studio',desc:'Studio photography or video session',price:'Custom quote'},
 {id:'outdoor',name:'Outdoor / location shoot',tag:'On location',desc:'Production at your chosen venue',price:'Custom quote'},
 {id:'half_day',name:'Half-day event',tag:'Events',desc:'Focused event coverage',price:'Custom quote'},
 {id:'full_day',name:'Full-day event',tag:'Events',desc:'Full-day event master coverage',price:'Custom quote'},
 {id:'identity',name:'Corporate identity kit',tag:'Branding',desc:'A consistent visual identity system',price:'Custom quote'},
 {id:'stationery',name:'Corporate stationery',tag:'Branding',desc:'Branded business stationery',price:'Custom quote'},
 {id:'typography',name:'Typography & slogan',tag:'Branding',desc:'Typography, slogan and brand expression',price:'Custom quote'},
 {id:'web_mockups',name:'Responsive web mockups',tag:'Digital',desc:'Responsive web interface design concepts',price:'Custom quote'},
 {id:'social_retainer',name:'Social media retainer',tag:'Digital',desc:'Ongoing social media strategy',price:'Custom quote'},
 {id:'reels',name:'TikTok / Instagram Reels',tag:'Digital',desc:'Short-form video and channel management',price:'Custom quote'},
 {id:'photomounts_a4_a0',name:'Photomounts (A4–A0)',tag:'Print & display',desc:'Professional photo mounting available in sizes A4, A3, A2, A1 and A0. Specify your preferred size and quantity in the project details.',price:'Custom quote'}
];

const nav = [
 {id:'overview',label:'Overview',icon:LayoutDashboard},
 {id:'bookings',label:'Bookings',icon:CalendarDays},
 {id:'projects',label:'Production board',icon:BriefcaseBusiness},
 {id:'clients',label:'Clients',icon:Users},
 {id:'payments',label:'Payments',icon:Wallet}
];
const money = n => new Intl.NumberFormat('en-KE',{style:'currency',currency:'KES',maximumFractionDigits:0}).format(Number(n||0));
function getGreeting(){
 const hour=Number(new Intl.DateTimeFormat('en-KE',{
  timeZone:'Africa/Nairobi',
  hour:'2-digit',
  hourCycle:'h23'
 }).format(new Date()));
 if(hour>=5&&hour<12)return 'Good morning';
 if(hour>=12&&hour<17)return 'Good afternoon';
 return 'Good evening';
}

async function authenticatedFetch(url, options={}) {
 const send = token => fetch(url, {...options, headers:{...(options.headers||{}), Authorization:`Bearer ${token||''}`}});
 let response = await send(sessionStorage.getItem('charis_access'));
 if (response.status === 401) {
  const refresh = sessionStorage.getItem('charis_refresh');
  if (!refresh) return response;
  try {
   const renewed = await fetch(`${API}/auth/refresh/`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh})});
   if (!renewed.ok) return response;
   const tokens = await renewed.json();
   sessionStorage.setItem('charis_access', tokens.access);
   response = await send(tokens.access);
  } catch { return response; }
 }
 return response;
}
function Workspace(){
 const [greeting,setGreeting]=useState(getGreeting),[page,setPage]=useState('overview'),[mode,setMode]=useState('admin'),[mobileNav,setMobileNav]=useState(false),[showBooking,setShowBooking]=useState(false),[bookings,setBookings]=useState([]),[stats,setStats]=useState(null),[loading,setLoading]=useState(true),[notice,setNotice]=useState(''),[search,setSearch]=useState(''),[filter,setFilter]=useState('all'),[selected,setSelected]=useState(null);
 const refresh=async()=>{try{const [b,s]=await Promise.all([authenticatedFetch(`${API}/bookings/`),authenticatedFetch(`${API}/dashboard/`)]);if(b.ok)setBookings(await b.json());if(s.ok)setStats(await s.json());}catch(e){}finally{setLoading(false)}};
 useEffect(()=>{refresh()},[]);
 useEffect(()=>{
  const updateGreeting=()=>setGreeting(getGreeting());
  updateGreeting();
  const timer=setInterval(updateGreeting,60000);
  return ()=>clearInterval(timer);
 },[]);
 const flash=(msg)=>{setNotice(msg);setTimeout(()=>setNotice(''),3800)};
 const filtered=useMemo(()=>bookings.filter(b=>(`${b.full_name} ${b.company_name} ${b.email} ${b.venue}`.toLowerCase().includes(search.toLowerCase()))&&(filter==='all'||b.status===filter)),[bookings,search,filter]);
 const updateBooking=async(id,patch)=>{try{const r=await authenticatedFetch(`${API}/bookings/${id}/`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(patch)});if(!r.ok)throw Error();await refresh();flash('Booking updated successfully.')}catch{flash('Could not update the booking. Check your connection and account permissions, then try again.')}};
 const exportCsv=()=>{const rows=[['ID','Client','Email','Phone','Date','Venue','Services','Status','Quote KES','Deposit paid','Balance paid'],...filtered.map(b=>[b.id,b.full_name,b.email,b.phone,b.event_date||'',b.venue,(b.services||[]).join('; '),b.status,b.quote_amount,b.deposit_paid?'Yes':'No',b.balance_paid?'Yes':'No'])];const csv=rows.map(r=>r.map(v=>`"${String(v??'').replaceAll('"','""')}"`).join(',')).join('\n');const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='charis-bookings.csv';a.click();URL.revokeObjectURL(a.href)};
 return <div className="app-shell">
  <aside className={`sidebar ${mobileNav?'mobile-open':''}`}><div className="brand"><img src="/charis-logo.png" alt="Charis Digital Crafts Media House" className="charis-logo charis-logo-sidebar"/><button className="icon-btn close-nav" onClick={()=>setMobileNav(false)}><X/></button></div><div className="workspace-label">WORKSPACE</div><nav>{nav.map(n=><button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>{setPage(n.id);setMobileNav(false)}}><n.icon size={18}/><span>{n.label}</span>{n.id==='bookings'&&bookings.length>0&&<small>{bookings.length}</small>}</button>)}</nav><div className="side-divider"/><div className="workspace-label">TOOLS</div><button className={`nav-item ${page==='services'?'active':''}`} onClick={()=>setPage('services')}><Palette size={18}/><span>Service catalogue</span></button><button className={`nav-item ${page==='settings'?'active':''}`} onClick={()=>setPage('settings')}><Settings size={18}/><span>Settings & help</span></button><div className="sidebar-bottom"><div className="help-card"><div className="help-icon"><Clapperboard size={19}/></div><b>Make something memorable.</b><p>Your next great story starts with a booking.</p><button onClick={()=>setShowBooking(true)}>Create booking <ArrowUpRight size={15}/></button></div><div className="profile-row"><div className="avatar">CD</div><div className="profile-copy"><b>Charis Media</b><span>Workspace admin</span></div><Settings size={16} className="muted"/></div></div></aside>
  {mobileNav&&<div className="scrim" onClick={()=>setMobileNav(false)}/>}
  <main className="main"><header className="topbar"><div className="top-left"><button className="icon-btn mobile-menu" onClick={()=>setMobileNav(true)}><Menu/></button><div className="breadcrumb">Workspace <ChevronRight size={14}/><b>{nav.find(n=>n.id===page)?.label||({services:'Service catalogue',settings:'Settings & help'}[page]||'Overview')}</b></div></div><div className="top-actions"><div className="mode-switch"><button className={mode==='admin'?'chosen':''} onClick={()=>setMode('admin')}>Admin</button><button className={mode==='client'?'chosen':''} onClick={()=>setMode('client')}>Client view</button></div><button className="icon-btn notification" title="Notifications"><Bell size={18}/><i/></button><div className="avatar top-avatar">CD</div></div></header>
  {mode==='client'?<ClientView onBook={()=>setShowBooking(true)} onAdmin={()=>setMode('admin')} bookings={bookings}/>:<div className="page-content">
   {page==='overview'&&<><div className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-dot"/> YOUR CREATIVE BUSINESS, IN ONE PLACE</div><h1>{greeting}<span className="gold-dot">.</span></h1><p className="subheading">Here’s what’s happening across your studio today.</p></div><button className="primary-btn" onClick={()=>setShowBooking(true)}><Plus size={17}/> New booking</button></div>
    <section className="hero-banner"><div className="hero-content"><div className="hero-chip"><Sparkles size={13}/> CHARIS DIGITAL CRAFTS MEDIA HOUSE</div><h2>Capturing stories.<br/><em>Building brands.</em></h2><p>Every project, every client, every detail — beautifully organised.</p><button className="hero-btn" onClick={()=>setPage('services')}>Explore services <ArrowUpRight size={16}/></button></div><div className="hero-art"><div className="art-orbit orbit-one"/><div className="art-orbit orbit-two"/><div className="art-circle"><Camera size={51} strokeWidth={1.2}/></div><div className="floating-card card-one"><Video size={17}/><span>Video production</span></div><div className="floating-card card-two"><Palette size={17}/><span>Brand identity</span></div><div className="floating-card card-three"><Image size={17}/><span>Photography</span></div></div><div className="hero-number">01 <span>/ CREATIVE STUDIO</span></div></section>
    <div className="section-heading"><div><h3>Studio at a glance</h3><p>Performance overview across your projects</p></div><span className="period-label"><CalendarDays size={14}/> All time</span></div>
    <div className="stat-grid"><Stat icon={CalendarDays} label="Total bookings" value={stats?.total_bookings??bookings.length} foot="All client enquiries" tone="gold"/><Stat icon={Clock3} label="New enquiries" value={stats?.new_enquiries??bookings.filter(b=>b.status==='new').length} foot="Awaiting review" tone="blue"/><Stat icon={Clapperboard} label="Active projects" value={stats?.active_projects??bookings.filter(b=>['confirmed','in_production','editing'].includes(b.status)).length} foot="In production or editing" tone="purple"/><Stat icon={CircleDollarSign} label="Quoted revenue" value={money(stats?.quoted_revenue??bookings.reduce((s,b)=>s+Number(b.quote_amount||0),0))} foot="Across all quotations" tone="green"/></div>
    <div className="dashboard-grid"><section className="panel recent-panel"><div className="panel-head"><div><h3>Recent bookings</h3><p>Keep every project moving forward</p></div><button className="text-btn" onClick={()=>setPage('bookings')}>View all <ChevronRight size={15}/></button></div>{loading?<Empty text="Connecting to your workspace…"/>:bookings.length===0?<div className="empty-state"><div className="empty-icon"><CalendarDays size={24}/></div><b>Your next project starts here</b><p>New client requests will appear here when submitted.</p><button className="secondary-btn" onClick={()=>setShowBooking(true)}><Plus size={15}/> Create first booking</button></div>:<div className="table-wrap"><table><thead><tr><th>CLIENT</th><th>SERVICE</th><th>EVENT DATE</th><th>STATUS</th><th/></tr></thead><tbody>{bookings.slice(0,5).map(b=><tr key={b.id} onClick={()=>{setSelected(b);setPage('bookings')}}><td><div className="client-cell"><div className="mini-avatar">{initials(b.full_name)}</div><div><b>{b.full_name}</b><span>{b.company_name||b.email}</span></div></div></td><td>{(b.services||[]).map(s=>serviceGroups.find(x=>x.id===s)?.label||s).join(', ')||'Creative services'}</td><td>{dateLabel(b.event_date)}</td><td><Status status={b.status}/></td><td><ChevronRight size={15} className="muted"/></td></tr>)}</tbody></table></div>}</section>
    <section className="panel workflow-panel"><div className="panel-head"><div><h3>Project workflow</h3><p>From first enquiry to final delivery</p></div><div className="workflow-icon"><ClipboardList size={18}/></div></div><div className="workflow-list">{[['01','Enquiry received','Capture client requirements','new'],['02','Quote & confirmation','Agree scope and budget','quoted'],['03','Production','Crew, shoot and editing','in_production'],['04','Final delivery','Settle balance and share files','ready']].map((w,i)=><div className="workflow-step" key={w[0]}><div className={`step-number step-${i}`}>{w[0]}</div><div className="step-copy"><b>{w[1]}</b><span>{w[2]}</span></div><span className="step-count">{bookings.filter(b=>i===2?['confirmed','in_production','editing'].includes(b.status):b.status===w[3]).length}</span></div>)}</div><button className="workflow-link" onClick={()=>setPage('projects')}>Open production board <ArrowUpRight size={15}/></button></section></div>
    <div className="bottom-strip"><div className="bottom-icon"><Wallet size={19}/></div><div><b>Payment milestones</b><p>Keep deposit and final balance visible for every project.</p></div><div className="payment-mini"><span>Deposits pending</span><b>{stats?.pending_deposits??bookings.filter(b=>!b.deposit_paid).length}</b></div><div className="payment-mini"><span>Balances pending</span><b>{stats?.pending_balances??bookings.filter(b=>!b.balance_paid).length}</b></div><button className="text-btn" onClick={()=>setPage('payments')}>Review <ChevronRight size={15}/></button></div>
   </>}
   {page==='bookings'&&<><PageTitle eyebrow="CLIENT RELATIONSHIPS" title="Bookings & enquiries" subtitle="Every request, from first contact to confirmed project." action={<button className="primary-btn" onClick={()=>setShowBooking(true)}><Plus size={17}/> New booking</button>}/><div className="toolbar"><div className="search-box"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search clients, email or venue…"/></div><div className="filter-box"><Filter size={16}/><select value={filter} onChange={e=>setFilter(e.target.value)}><option value="all">All statuses</option>{['new','quoted','confirmed','in_production','editing','ready','completed','cancelled'].map(s=><option key={s} value={s}>{pretty(s)}</option>)}</select></div><button className="secondary-btn" onClick={exportCsv}><Download size={15}/> Export CSV</button></div><section className="panel list-panel">{filtered.length===0?<Empty text={loading?'Loading bookings…':'No bookings match this view yet.'}/>:<div className="table-wrap"><table className="wide-table"><thead><tr><th>CLIENT</th><th>SERVICE</th><th>EVENT DATE</th><th>VENUE</th><th>QUOTE</th><th>STATUS</th><th/></tr></thead><tbody>{filtered.map(b=><tr key={b.id} onClick={()=>setSelected(b)}><td><div className="client-cell"><div className="mini-avatar">{initials(b.full_name)}</div><div><b>{b.full_name}</b><span>{b.email}</span></div></div></td><td>{(b.services||[]).map(s=>serviceGroups.find(x=>x.id===s)?.label||s).join(', ')||'—'}</td><td>{dateLabel(b.event_date)}</td><td>{b.venue||'Not set'}</td><td>{money(b.quote_amount)}</td><td><Status status={b.status}/></td><td><button className="row-action" onClick={e=>{e.stopPropagation();setSelected(b)}}><ChevronRight size={16}/></button></td></tr>)}</tbody></table></div>}</section></>}
   {page==='projects'&&<><PageTitle eyebrow="PRODUCTION MANAGEMENT" title="Production board" subtitle="Move each project through its production milestones." action={<button className="primary-btn" onClick={()=>setShowBooking(true)}><Plus size={17}/> New project</button>}/><div className="kanban">{[['new','New enquiries'],['confirmed','Confirmed'],['in_production','In production'],['editing','Editing'],['ready','Ready to deliver']].map(([status,label])=><div className="kanban-col" key={status}><div className="kanban-head"><span className={`kanban-dot dot-${status}`}/><b>{label}</b><span>{bookings.filter(b=>b.status===status).length}</span></div>{bookings.filter(b=>b.status===status).map(b=><div className="project-card" key={b.id} onClick={()=>setSelected(b)}><div className="project-card-top"><span>CH-{String(b.id).padStart(4,'0')}</span><Status status={b.status}/></div><b>{b.company_name||b.full_name}</b><p>{(b.services||[]).map(s=>serviceGroups.find(x=>x.id===s)?.label||s).join(', ')||'Creative project'}</p><div className="project-meta"><span><CalendarDays size={13}/>{dateLabel(b.event_date)}</span><span><MapPin size={13}/>{b.venue||'Venue TBD'}</span></div><div className="project-card-foot"><div className="mini-avatar">{initials(b.full_name)}</div><select aria-label="Update project status" value={b.status} onClick={e=>e.stopPropagation()} onChange={e=>updateBooking(b.id,{status:e.target.value})}>{['new','quoted','confirmed','in_production','editing','ready','completed','cancelled'].map(s=><option value={s} key={s}>{pretty(s)}</option>)}</select></div></div>)}</div>)}</div></>}
   {page==='clients'&&<><PageTitle eyebrow="YOUR CLIENT NETWORK" title="Client directory" subtitle="A simple view of everyone who has reached out to your studio."/><section className="panel list-panel"><div className="toolbar inline-toolbar"><div className="search-box"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search clients…"/></div><span className="result-count">{new Set(filtered.map(b=>b.email)).size} unique clients</span></div>{[...new Map(filtered.map(b=>[b.email,b])).values()].length===0?<Empty text="Your client directory will populate when enquiries arrive."/>:<div className="client-directory">{[...new Map(filtered.map(b=>[b.email,b])).values()].map(b=><div className="directory-card" key={b.email}><div className="directory-top"><div className="large-avatar">{initials(b.full_name)}</div><Status status={b.status}/></div><h4>{b.full_name}</h4><p>{b.company_name||'Individual client'}</p><div className="directory-contact"><span><Mail size={14}/>{b.email}</span><span><Phone size={14}/>{b.phone}</span></div><button className="text-btn" onClick={()=>setSelected(b)}>View booking <ArrowUpRight size={14}/></button></div>)}</div>}</section></>}
