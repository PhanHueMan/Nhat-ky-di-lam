from pathlib import Path
p=Path('checklist-lo-hang.html')
s=p.read_text(encoding='utf-8')

marker='''    <div class="agenda" id="agendaPanel">'''
insert='''    <details class="manage" id="statsPanel" open>
      <summary>📊 Thống kê lô hàng</summary>
      <div class="manage-body">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px;">
          <label style="font-weight:700;">Năm</label><select id="statsYear" style="height:36px;padding:0 10px;border:1px solid var(--line);border-radius:6px;background:#fff;"></select>
          <label style="font-weight:700;">Từ ngày</label><input type="date" id="statsFrom" style="height:36px;border:1px solid var(--line);border-radius:6px;padding:0 8px;">
          <label style="font-weight:700;">Đến ngày</label><input type="date" id="statsTo" style="height:36px;border:1px solid var(--line);border-radius:6px;padding:0 8px;">
          <button class="btn-ghost-sm" id="statsReset">Cả năm</button>
        </div><div id="statsBody"></div>
      </div>
    </details>

'''+marker
if marker not in s: raise SystemExit('agenda marker missing')
s=s.replace(marker,insert,1)

old='''function render(){
  renderManage();
  renderAgenda();
  renderShipments();
}'''
new='''function render(){
  renderManage();
  renderStats();
  renderAgenda();
  renderShipments();
}'''
if old not in s: raise SystemExit('render marker missing')
s=s.replace(old,new,1)

marker='''function gatherMilestones(withinDays, typeFilter){'''
logic=r'''function shipmentStatDate(sh){
  if(sh.createdAt){ const d=new Date(sh.createdAt); if(!isNaN(d)) return d; }
  const vals=Object.values(sh.dates||{}).filter(Boolean).sort();
  if(vals.length){ const d=new Date(vals[0]); if(!isNaN(d)) return d; }
  return null;
}
function renderStats(){
  const body=document.getElementById('statsBody'), yearEl=document.getElementById('statsYear');
  if(!body||!yearEl) return;
  const currentYear=new Date().getFullYear();
  if(!yearEl.options.length){
    const years=new Set([currentYear]); state.shipments.forEach(sh=>{const d=shipmentStatDate(sh);if(d)years.add(d.getFullYear());});
    [...years].sort((a,b)=>b-a).forEach(y=>{const o=document.createElement('option');o.value=y;o.textContent=y;yearEl.appendChild(o);}); yearEl.value=String(currentYear);
  }
  const y=Number(yearEl.value)||currentYear, fromEl=document.getElementById('statsFrom'), toEl=document.getElementById('statsTo');
  const from=fromEl.value?new Date(fromEl.value+'T00:00:00'):new Date(y,0,1), to=toEl.value?new Date(toEl.value+'T23:59:59'):new Date(y,11,31,23,59,59);
  const c={fcl:0,lcl:0,unknown:0,airImport:0,seaExport:0,airExport:0,other:0,total:0};
  state.shipments.forEach(sh=>{const d=shipmentStatDate(sh);if(!d||d<from||d>to)return;c.total++;const lt=sh.lotType||(sh.type==='export'?'Hàng xuất sea':'Hàng nhập sea');if(lt==='Hàng nhập sea'){if(sh.loadType==='FCL')c.fcl++;else if(sh.loadType==='LCL')c.lcl++;else c.unknown++;}else if(lt==='Hàng nhập air')c.airImport++;else if(lt==='Hàng xuất sea')c.seaExport++;else if(lt==='Hàng xuất air')c.airExport++;else c.other++;});
  const rows=[['Sea Import – FCL',c.fcl],['Sea Import – LCL',c.lcl],['Sea Import – Chưa phân loại',c.unknown],['Air Import',c.airImport],['Sea Export',c.seaExport],['Air Export',c.airExport],['Khác',c.other]];
  body.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:9px;">'+rows.map(r=>'<div style="border:1px solid var(--line);border-radius:8px;padding:10px;background:#fff;"><div style="font-size:12px;color:var(--muted);">'+r[0]+'</div><div style="font-size:24px;font-weight:800;color:var(--navy);">'+r[1]+' <span style="font-size:12px;font-weight:600;">lô</span></div></div>').join('')+'</div><div style="margin-top:10px;font-weight:800;">Tổng: '+c.total+' lô</div>';
}

'''+marker
if marker not in s: raise SystemExit('gather marker missing')
s=s.replace(marker,logic,1)

old='''state.shipments.unshift({ id:newId, name:name, type:selectedType, lotType:lotType, loadType:loadType, checks:checks, dates:{} });'''
new='''state.shipments.unshift({ id:newId, name:name, type:selectedType, lotType:lotType, loadType:loadType, checks:checks, dates:{}, createdAt:new Date().toISOString() });'''
if old not in s: raise SystemExit('shipment marker missing')
s=s.replace(old,new,1)

marker="""document.getElementById('newShipmentInput').addEventListener('keydown', function(e){"""
controls="""document.getElementById('statsYear').addEventListener('change',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});
document.getElementById('statsFrom').addEventListener('change',renderStats);
document.getElementById('statsTo').addEventListener('change',renderStats);
document.getElementById('statsReset').addEventListener('click',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});

"""+marker
if marker not in s: raise SystemExit('keydown marker missing')
s=s.replace(marker,controls,1)
p.write_text(s,encoding='utf-8')
