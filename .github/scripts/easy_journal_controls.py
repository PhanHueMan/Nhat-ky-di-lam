from pathlib import Path

# PAGE 1: add FCL/LCL into existing summary and Excel backup.
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace("let reflections = {};\nlet currentLotId", "let reflections = {};\nlet checklistShipments = [];\nlet currentLotId", 1)

old="""    reflections = data.reflections || {};

  } catch(e) {"""
new="""    reflections = data.reflections || {};
    const rawChecklistShipments = data.checklist && data.checklist.shipments ? data.checklist.shipments : [];
    checklistShipments = Array.isArray(rawChecklistShipments) ? rawChecklistShipments : Object.values(rawChecklistShipments || {});

  } catch(e) {"""
if old not in s: raise SystemExit('loadAll marker missing')
s=s.replace(old,new,1)
s=s.replace("    reflections = {};\n  }", "    reflections = {};\n    checklistShipments = [];\n  }", 1)

marker="""function normalizeSteps(steps){"""
helper="""function normLotText(v){ return String(v||'').trim().toLowerCase().replace(/[–—_-]+/g,' ').replace(/\\s+/g,' '); }
function checklistShipmentForLot(lot){
  if(!lot) return null;
  const customer=normLotText(lot.customer), code=normLotText(lot.code);
  const full=normLotText([lot.customer,lot.code].filter(Boolean).join(' '));
  return checklistShipments.find(sh=>{
    const shCustomer=normLotText(sh.customer), shCode=normLotText(sh.code), shName=normLotText(sh.name);
    if(customer && code && shCustomer===customer && shCode===code) return true;
    if(full && shName===full) return true;
    if(code && shCode===code && (!customer || !shCustomer || shCustomer===customer)) return true;
    return false;
  }) || null;
}
function lotLoadType(lot){
  const sh=checklistShipmentForLot(lot);
  return sh && (sh.lotType==='Hàng nhập sea' || (!sh.lotType && sh.type==='import')) ? (sh.loadType||'') : '';
}

"""+marker
if marker not in s: raise SystemExit('normalize marker missing')
s=s.replace(marker,helper,1)

old="""  const typeCounts = {}; const custCounts = {};
  [...activeLotIds].forEach(id=>{
    const l = lots.find(x=>x.id===id); if(!l) return;
    typeCounts[l.type||'Khác'] = (typeCounts[l.type||'Khác']||0)+1;
    custCounts[l.customer||'(chưa đặt tên)'] = (custCounts[l.customer||'(chưa đặt tên)']||0)+1;
  });
  renderBarBreakdown('breakdown-type-body', typeCounts, '', (label)=>{
    const arr = lots.filter(l=> activeLotIds.has(l.id) && (l.type||'Khác')===label);
    openDetail(`Loại hàng: ${label}`, lotListHTML(arr), c=>bindFeed(c));
  });"""
new="""  const typeCounts = {}; const custCounts = {}; const seaLoadCounts = {FCL:0,LCL:0,'Chưa phân loại':0};
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
if old not in s: raise SystemExit('type breakdown marker missing')
s=s.replace(old,new,1)

old="""      {header:'Loại hàng', key:'type', width:16},
      {header:'Ngày mở', key:'date', width:12},"""
new="""      {header:'Loại hàng', key:'type', width:16},
      {header:'FCL/LCL', key:'loadType', width:12},
      {header:'Ngày mở', key:'date', width:12},"""
if old not in s: raise SystemExit('backup columns marker missing')
s=s.replace(old,new,1)
old="""      customer: l.customer||'', code: l.code||'', type: l.type||'', date: l.date||'',
      done: l.doneFlag?'Có':'Không', doneDate: l.doneDate||'', doneNote: l.doneNote||''"""
new="""      customer: l.customer||'', code: l.code||'', type: l.type||'', loadType: lotLoadType(l), date: l.date||'',
      done: l.doneFlag?'Có':'Không', doneDate: l.doneDate||'', doneNote: l.doneNote||''"""
if old not in s: raise SystemExit('backup row marker missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# PAGE 2: remove the mistakenly-added standalone statistics panel, keep FCL/LCL classification itself.
p=Path('checklist-lo-hang.html')
s=p.read_text(encoding='utf-8')
start=s.find('    <details class="manage" id="statsPanel" open>')
end=s.find('    <div class="agenda" id="agendaPanel">', start)
if start!=-1 and end!=-1: s=s[:start]+s[end:]
s=s.replace('  renderStats();\n','',1)
logic_start=s.find('function shipmentStatDate(sh){')
logic_end=s.find('function gatherMilestones(withinDays, typeFilter){',logic_start)
if logic_start!=-1 and logic_end!=-1: s=s[:logic_start]+s[logic_end:]
for line in [
"document.getElementById('statsYear').addEventListener('change',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});\n",
"document.getElementById('statsFrom').addEventListener('change',renderStats);\n",
"document.getElementById('statsTo').addEventListener('change',renderStats);\n",
"document.getElementById('statsReset').addEventListener('click',function(){document.getElementById('statsFrom').value='';document.getElementById('statsTo').value='';renderStats();});\n"]:
    s=s.replace(line,'',1)
p.write_text(s,encoding='utf-8')
