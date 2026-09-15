from pathlib import Path

# Surgical/idempotent patch only: keep page 1 structure intact.
p = Path('index.html')
s = p.read_text(encoding='utf-8')

# FCL/LCL applies only to Hàng nhập sea.
s = s.replace(
"return sh && (sh.lotType==='Hàng nhập sea' || sh.lotType==='Hàng xuất sea') ? (sh.loadType||'') : '';",
"return sh && (sh.lotType==='Hàng nhập sea' || (!sh.lotType && sh.type==='import')) ? (sh.loadType||'') : '';",
1)

old = """  const typeCounts = {}; const custCounts = {};
  let seaFCL=0, seaLCL=0, seaUnknown=0;
  [...activeLotIds].forEach(id=>{
    const l = lots.find(x=>x.id===id); if(!l) return;
    typeCounts[l.type||'Khác'] = (typeCounts[l.type||'Khác']||0)+1;
    custCounts[l.customer||'(chưa đặt tên)'] = (custCounts[l.customer||'(chưa đặt tên)']||0)+1;
    if((l.type||'').toLowerCase().includes('sea')){
      const load=lotLoadType(l);
      if(load==='FCL') seaFCL++;
      else if(load==='LCL') seaLCL++;
      else seaUnknown++;
    }
  });
  if(seaFCL) typeCounts['↳ FCL'] = seaFCL;
  if(seaLCL) typeCounts['↳ LCL'] = seaLCL;
  if(seaUnknown) typeCounts['↳ Sea chưa phân loại FCL/LCL'] = seaUnknown;
  renderBarBreakdown('breakdown-type-body', typeCounts, '', (label)=>{
    let arr;
    if(label==='↳ FCL' || label==='↳ LCL'){
      const load=label.replace('↳ ','');
      arr=lots.filter(l=>activeLotIds.has(l.id) && (l.type||'').toLowerCase().includes('sea') && lotLoadType(l)===load);
    } else if(label==='↳ Sea chưa phân loại FCL/LCL'){
      arr=lots.filter(l=>activeLotIds.has(l.id) && (l.type||'').toLowerCase().includes('sea') && !lotLoadType(l));
    } else {
      arr=lots.filter(l=> activeLotIds.has(l.id) && (l.type||'Khác')===label);
    }
    openDetail(`Loại hàng: ${label}`, lotListHTML(arr), c=>bindFeed(c));
  });"""
new = """  const typeCounts = {}; const custCounts = {}; const seaLoadCounts = {FCL:0,LCL:0,'Chưa phân loại':0};
  [...activeLotIds].forEach(id=>{
    const l = lots.find(x=>x.id===id); if(!l) return;
    typeCounts[l.type||'Khác'] = (typeCounts[l.type||'Khác']||0)+1;
    if((l.type||'')==='Hàng nhập sea'){
      const load=lotLoadType(l);
      if(load==='FCL' || load==='LCL') seaLoadCounts[load]++;
      else seaLoadCounts['Chưa phân loại']++;
    }
    custCounts[l.customer||'(chưa đặt tên)'] = (custCounts[l.customer||'(chưa đặt tên)']||0)+1;
  });
  if(typeCounts['Hàng nhập sea']){
    typeCounts['↳ FCL'] = seaLoadCounts.FCL;
    typeCounts['↳ LCL'] = seaLoadCounts.LCL;
    if(seaLoadCounts['Chưa phân loại']>0) typeCounts['↳ Chưa phân loại'] = seaLoadCounts['Chưa phân loại'];
  }
  renderBarBreakdown('breakdown-type-body', typeCounts, '', (label)=>{
    let arr;
    if(label==='↳ FCL' || label==='↳ LCL'){
      const load=label.replace('↳ ','');
      arr=lots.filter(l=>activeLotIds.has(l.id) && (l.type||'')==='Hàng nhập sea' && lotLoadType(l)===load);
    } else if(label==='↳ Chưa phân loại'){
      arr=lots.filter(l=>activeLotIds.has(l.id) && (l.type||'')==='Hàng nhập sea' && !lotLoadType(l));
    } else {
      arr=lots.filter(l=> activeLotIds.has(l.id) && (l.type||'Khác')===label);
    }
    openDetail(`Loại hàng: ${label}`, lotListHTML(arr), c=>bindFeed(c));
  });"""
if old in s:
    s = s.replace(old, new, 1)
elif "const seaLoadCounts = {FCL:0,LCL:0,'Chưa phân loại':0};" not in s:
    raise SystemExit('Unexpected page-1 summary structure; refusing to modify')

p.write_text(s, encoding='utf-8')

# Page 2: remove only the mistakenly-added stats panel/code. Keep shipment controls.
p = Path('checklist-lo-hang.html')
s = p.read_text(encoding='utf-8')
start = s.find('    <details class="manage" id="statsPanel" open>')
end = s.find('    <div class="agenda" id="agendaPanel">', start)
if start != -1 and end != -1:
    s = s[:start] + s[end:]
s = s.replace('  renderStats();\n', '', 1)
logic_start = s.find('function shipmentStatDate(sh){')
logic_end = s.find('function gatherMilestones(withinDays, typeFilter){', logic_start)
if logic_start != -1 and logic_end != -1:
    s = s[:logic_start] + s[logic_end:]
for line in [
"document.getElementById('statsYear').addEventListener('change',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});\n",
"document.getElementById('statsFrom').addEventListener('change',renderStats);\n",
"document.getElementById('statsTo').addEventListener('change',renderStats);\n",
"document.getElementById('statsReset').addEventListener('click',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});\n"]:
    s = s.replace(line, '', 1)

# Historical import-sea shipments with no loadType must stay visibly unclassified.
old_load = """  ['FCL','LCL'].forEach(v=>{ const o=document.createElement('option'); o.value=v; o.textContent=v; if(v===(shipment.loadType||'FCL')) o.selected=true; loadSelect.appendChild(o); });"""
new_load = """  const blank=document.createElement('option'); blank.value=''; blank.textContent='Chọn FCL/LCL'; loadSelect.appendChild(blank);
  ['FCL','LCL'].forEach(v=>{ const o=document.createElement('option'); o.value=v; o.textContent=v; if(v===shipment.loadType) o.selected=true; loadSelect.appendChild(o); });
  loadSelect.value=shipment.loadType||'';"""
if old_load in s:
    s = s.replace(old_load, new_load, 1)

p.write_text(s, encoding='utf-8')
