from pathlib import Path

p = Path('checklist-lo-hang.html')
s = p.read_text(encoding='utf-8')

# Add detailed shipment mode + FCL/LCL controls to new shipment form.
old = '''        <div class="toggle-group" id="typeToggle">
          <button type="button" class="active" data-type="import">Nhập</button>
          <button type="button" data-type="export">Xuất</button>
        </div>
        <button class="btn-main" id="addShipmentBtn">+ Thêm</button>'''
new = '''        <div class="toggle-group" id="typeToggle">
          <button type="button" class="active" data-type="import">Nhập</button>
          <button type="button" data-type="export">Xuất</button>
        </div>
        <select id="newLotType" title="Loại hình" style="height:40px;padding:0 10px;border:1px solid var(--line);border-radius:7px;background:#fff;font-family:inherit;font-size:14px;">
          <option value="Hàng nhập sea">Hàng nhập sea</option>
          <option value="Hàng nhập air">Hàng nhập air</option>
          <option value="Hàng xuất sea">Hàng xuất sea</option>
          <option value="Hàng xuất air">Hàng xuất air</option>
          <option value="Khác">Khác</option>
        </select>
        <select id="newLoadType" title="FCL / LCL" style="height:40px;padding:0 10px;border:1px solid var(--line);border-radius:7px;background:#fff;font-family:inherit;font-size:14px;">
          <option value="FCL">FCL</option>
          <option value="LCL">LCL</option>
        </select>
        <button class="btn-main" id="addShipmentBtn">+ Thêm</button>'''
if old not in s:
    raise SystemExit('new shipment form marker missing')
s = s.replace(old, new, 1)

# Show FCL/LCL only for import sea and keep import/export toggle in sync with detailed mode.
old = '''document.getElementById('typeToggle').addEventListener('click', function(e){
  const btn = e.target.closest('button');
  if(!btn) return;
  selectedType = btn.dataset.type;
  document.querySelectorAll('#typeToggle button').forEach(function(b){ b.classList.toggle('active', b===btn); });
});'''
new = '''function syncNewShipmentMode(){
  const lotType=document.getElementById('newLotType');
  const loadType=document.getElementById('newLoadType');
  if(!lotType || !loadType) return;
  const v=lotType.value;
  selectedType=v.indexOf('xuất')>=0 ? 'export' : 'import';
  document.querySelectorAll('#typeToggle button').forEach(function(b){ b.classList.toggle('active', b.dataset.type===selectedType); });
  loadType.style.display = v==='Hàng nhập sea' ? '' : 'none';
}
document.getElementById('newLotType').addEventListener('change', syncNewShipmentMode);
document.getElementById('typeToggle').addEventListener('click', function(e){
  const btn = e.target.closest('button');
  if(!btn) return;
  selectedType = btn.dataset.type;
  document.querySelectorAll('#typeToggle button').forEach(function(b){ b.classList.toggle('active', b===btn); });
  const lotType=document.getElementById('newLotType');
  if(lotType){ lotType.value = selectedType==='import' ? 'Hàng nhập sea' : 'Hàng xuất sea'; syncNewShipmentMode(); }
});
syncNewShipmentMode();'''
if old not in s:
    raise SystemExit('type toggle marker missing')
s = s.replace(old, new, 1)

# Save detailed shipment mode and FCL/LCL on each new shipment.
old = '''  state.shipments.unshift({ id:newId, name:name, type:selectedType, checks:checks, dates:{} });'''
new = '''  const lotTypeEl=document.getElementById('newLotType');
  const loadTypeEl=document.getElementById('newLoadType');
  const lotType=lotTypeEl ? lotTypeEl.value : (selectedType==='export'?'Hàng xuất sea':'Hàng nhập sea');
  const loadType=(lotType==='Hàng nhập sea' && loadTypeEl) ? loadTypeEl.value : '';
  state.shipments.unshift({ id:newId, name:name, type:selectedType, lotType:lotType, loadType:loadType, checks:checks, dates:{} });'''
if old not in s:
    raise SystemExit('add shipment marker missing')
s = s.replace(old, new, 1)

# Show and allow editing detailed mode on every shipment card.
old = '''    head.appendChild(badge);

    if(shipment.archived){'''
new = '''    head.appendChild(badge);

    const modeSelect=document.createElement('select');
    modeSelect.title='Loại hình';
    modeSelect.style.cssText='height:30px;padding:0 7px;border:1px solid var(--line);border-radius:6px;background:#fff;font-size:12px;';
    ['Hàng nhập sea','Hàng nhập air','Hàng xuất sea','Hàng xuất air','Khác'].forEach(v=>{
      const o=document.createElement('option'); o.value=v; o.textContent=v;
      if(v===(shipment.lotType||(shipment.type==='export'?'Hàng xuất sea':'Hàng nhập sea'))) o.selected=true;
      modeSelect.appendChild(o);
    });
    modeSelect.onchange=()=>{
      shipment.lotType=modeSelect.value;
      if(modeSelect.value.indexOf('xuất')>=0) shipment.type='export';
      else if(modeSelect.value.indexOf('nhập')>=0) shipment.type='import';
      if(modeSelect.value!=='Hàng nhập sea') shipment.loadType='';
      saveState(); render();
    };
    head.appendChild(modeSelect);

    if((shipment.lotType||(shipment.type==='export'?'Hàng xuất sea':'Hàng nhập sea'))==='Hàng nhập sea'){
      const loadSelect=document.createElement('select');
      loadSelect.title='FCL / LCL';
      loadSelect.style.cssText='height:30px;padding:0 7px;border:1px solid var(--line);border-radius:6px;background:#fff;font-size:12px;font-weight:700;';
      ['FCL','LCL'].forEach(v=>{ const o=document.createElement('option'); o.value=v; o.textContent=v; if(v===(shipment.loadType||'FCL')) o.selected=true; loadSelect.appendChild(o); });
      loadSelect.onchange=()=>{ shipment.loadType=loadSelect.value; saveState(); };
      head.appendChild(loadSelect);
    }

    if(shipment.archived){'''
if old not in s:
    raise SystemExit('shipment card marker missing')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
