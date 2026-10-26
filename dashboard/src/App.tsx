import { useEffect, useState } from 'react';

type Route = {route_id:string;name:string;eligible:boolean;rejection_reasons:string[];total_cost:number;contribution_margin:number;settlement_seconds:number;score:number|null;risk:number;treasury_impact:Record<string,number>};
type Eval = {decision:string;recommended_route:string|null;reasoning:string[];routes:Route[]};
type Treasury = {label:string;balances:Record<string,number>;reserved_liquidity:number;pending_settlements:number;capital_locked:number;utilization_pct:number};
const money=(n:number,currency='USD')=>new Intl.NumberFormat('en-US',{style:'currency',currency,maximumFractionDigits:0}).format(n);

export default function App(){
 const [amount,setAmount]=useState(100000); const [source,setSource]=useState('EUR'); const [destination,setDestination]=useState('BRL');
 const [result,setResult]=useState<Eval|null>(null); const [treasury,setTreasury]=useState<Treasury|null>(null); const [error,setError]=useState('');
 const evaluate=async()=>{setError('');try{const r=await fetch('/api/payment/evaluate',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({amount,source_currency:source,destination_currency:destination,deadline_seconds:1800,payment_type:'B2B_PAYOUT'})});if(!r.ok)throw new Error(await r.text());setResult(await r.json());}catch{setError('API unavailable. Start the FastAPI server on port 8000.')} };
 useEffect(()=>{fetch('/api/treasury').then(r=>r.json()).then(setTreasury).catch(()=>{});evaluate();},[]);
 const winner=result?.routes.find(r=>r.route_id===result.recommended_route);
 return <main><header><div><div className="eyebrow">SYNTHETIC REFERENCE IMPLEMENTATION</div><h1>PayFlow <span>Control Plane</span></h1><p>Payment routing economics and treasury consequence, before execution.</p></div><div className="badge">NON-PRODUCTION · NO LIVE RAILS</div></header>
 <div className="notice">Every rate, liquidity balance and route below is illustrative synthetic data. This demo does not initiate or settle payments.</div>
 <section className="grid">
  <article className="panel decision"><div className="label">1 · CAN WE SERVE THIS PAYMENT?</div><div className={`state ${result?.decision==='ROUTE'?'go':'stop'}`}>{result?.decision??'LOADING'}</div><p>{result?.reasoning[0]??'Evaluating route evidence…'}</p><div className="inputs"><label>Amount<input type="number" value={amount} onChange={e=>setAmount(Number(e.target.value))}/></label><label>From<select value={source} onChange={e=>{setSource(e.target.value);setDestination(e.target.value==='EUR'?'BRL':'BRL')}}><option>EUR</option><option>USD</option></select></label><label>To<select value={destination} onChange={e=>setDestination(e.target.value)}><option>BRL</option><option>MXN</option></select></label><button onClick={evaluate}>Evaluate routes</button></div>{error&&<p className="error">{error}</p>}</article>
  <article className="panel"><div className="label">2 · WHICH RAIL?</div><div className="winner">{winner?.name??'No route selected'}</div><p>Recommended route: <b>{winner?.route_id??'—'}</b></p><p>Settlement: <b>{winner?`${Math.round(winner.settlement_seconds/60)} min`:'—'}</b></p></article>
  <article className="panel"><div className="label">3 · WHICH CORRIDOR?</div><div className="winner">{source} → {destination}</div><p>Supported demo corridors</p><div className="chips">EUR → BRL · USD → BRL · USD → MXN</div></article>
  <article className="panel"><div className="label">4 · WHAT DOES IT COST?</div><div className="metrics"><div><small>Route cost</small><b>{winner?money(winner.total_cost):'—'}</b></div><div><small>Contribution</small><b>{winner?money(winner.contribution_margin):'—'}</b></div><div><small>Risk index</small><b>{winner?`${(winner.risk*100).toFixed(1)}%`:'—'}</b></div></div><p>Weighted routing objective changes with payment type; hard controls always apply first.</p></article>
  <article className="panel"><div className="label">5 · WHAT HAPPENS TO TREASURY?</div><div className="metrics">{treasury&&Object.entries(treasury.balances).slice(0,3).map(([k,v])=><div key={k}><small>{k} balance</small><b>{money(v,k==='USDC'?'USD':k)}</b></div>)}</div><p>Reserved: {treasury?money(treasury.reserved_liquidity):'—'} · Capital locked: {winner?money(winner.treasury_impact.capital_locked):'—'}</p></article>
 </section>
 <section className="panel table-panel"><div className="label">ROUTE COMPARISON</div><div className="overflow"><table><thead><tr><th>Route</th><th>Decision</th><th>Total cost</th><th>Settlement</th><th>Contribution</th><th>Score</th></tr></thead><tbody>{result?.routes.map(r=><tr key={r.route_id}><td><b>{r.name}</b><small>{r.route_id}</small></td><td><span className={r.eligible?'pill yes':'pill no'}>{r.eligible?'ELIGIBLE':r.rejection_reasons[0]}</span></td><td>{money(r.total_cost)}</td><td>{Math.round(r.settlement_seconds/60)} min</td><td>{money(r.contribution_margin)}</td><td>{r.score??'—'}</td></tr>)}</tbody></table></div></section>
 <footer>Lifecycle states remain separate: <b>authorized → executed → settled → reconciled → assured</b>. Decision ledger and evidence are synthetic demo artifacts.</footer>
 </main>
}
