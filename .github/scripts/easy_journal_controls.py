from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""let lots = [];
let logs = [];
let reflections = {};"""
new="""let lots = [];
let logs = [];
let reflections = {};
let checklistShipments = [];"""
if old not in s: raise SystemExit('globals marker missing')
s=s.replace(old,new,1)

old="""    lots = data.lots || [];
    logs = data.entries || [];
    reflections = data.reflections || {};"""
new="""    lots = data.lots || [];
    logs = data.entries || [];
    reflections = data.reflections || {};
    const checklist = data.checklist || {};
    checklistShipments = Array.isArray(checklist.shipments) ? checklist.shipments : Object.values(checklist.shipments || {});"""
if old not in s: raise SystemExit('load marker missing')
s=s.replace(old,new,1)

old="""    lots = [];
    logs = [];
    reflections = {};"""
new="""    lots = [];
    logs = [];
    reflections = {};
    checklistShipments = [];"""
if old not in s: raise SystemExit('catch marker missing')
s=s.replace(old,new,1)

marker="""function normalizeSteps(steps){"""
helper="""function normLotText(v){ return String(v||'').trim().toLowerCase().replace(/\\s+/g,' '); }
function checklistShipmentForLot(lot){
  const customer=normLotText(lot.customer), code=normLotText(lot.code);
  const exact=checklistShipments.find(sh=>{
    const sc=normLotText(sh.customer), sd=normLotText(sh.code);
    return (customer||code) && sc===customer && sd===code;
  });
  if(exact) return exact;
  const target=normLotText(((lot.customer||'')+' '+(lot.code||'')).trim());
  return checklistShipments.find(sh=>{
    const name=normLotText(sh.name);
    return target && (name===target || (customer && code && name.includes(customer) && name.includes(code)));
  }) || null;
}
function lotLoadType(lot){
  const sh=checklistShipmentForLot(lot);
  return sh && (sh.lotType==='Hàng nhập sea' || sh.lotType==='Hàng xuất sea') ? (sh.loadType||'') : '';
}

"""+marker
if marker not in s: raise SystemExit('normalize marker missing')
s=s.replace(marker,helper,1)

old="""  const typeCounts = {}; const custCounts = {};
  [...activeLotIds].forEach(id=>{
    const l = lots.find(x=>x.id===id); if(!l) return;
    typeCounts[l.type||'Khác'] = (typeCounts[l.type||'Khác']||0)+1;
    custCounts[l.customer||'(chưa đặt tên)'] = (custCounts[l.customer||'(chưa đặt tên)']||0)+1;
  });"""
new="""  const typeCounts = {}; const custCounts = {};
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
  if(seaUnknown) typeCounts['↳ Sea chưa phân loại FCL/LCL'] = seaUnknown;"""
if old not in s: raise SystemExit('type counts marker missing')
s=s.replace(old,new,1)

old="""  renderBarBreakdown('breakdown-type-body', typeCounts, '', (label)=>{
    const arr = lots.filter(l=> activeLotIds.has(l.id) && (l.type||'Khác')===label);
    openDetail(`Loại hàng: ${label}`, lotListHTML(arr), c=>bindFeed(c));
  });"""
new="""  renderBarBreakdown('breakdown-type-body', typeCounts, '', (label)=>{
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
if old not in s: raise SystemExit('breakdown marker missing')
s=s.replace(old,new,1)

# Include load type in Excel backup too.
old="""      {header:'Loại hàng', key:'type', width:16},
      {header:'Ngày mở', key:'date', width:12},"""
new="""      {header:'Loại hàng', key:'type', width:16},
      {header:'FCL/LCL', key:'loadType', width:12},
      {header:'Ngày mở', key:'date', width:12},"""
if old not in s: raise SystemExit('excel header marker missing')
s=s.replace(old,new,1)
old="""      customer: l.customer||'', code: l.code||'', type: l.type||'', date: l.date||'',"""
new="""      customer: l.customer||'', code: l.code||'', type: l.type||'', loadType: lotLoadType(l), date: l.date||'',"""
if old not in s: raise SystemExit('excel row marker missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
