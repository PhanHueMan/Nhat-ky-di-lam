from pathlib import Path

p=Path('checklist-lo-hang.html')
s=p.read_text(encoding='utf-8')

# Keep the custom free-text Journal option.
old="""        JOURNAL_PRESETS.forEach((preset,idx)=>{
          const opt=document.createElement('option'); opt.value=idx; opt.textContent=preset.label;
          if(sameKeys(keys,preset.keys)) opt.selected=true;
          journalSelect.appendChild(opt);
        });
        journalSelect.onchange=()=>setItemJournalPreset(it,journalSelect.value);
        row.appendChild(journalSelect);"""
new="""        let matchedPreset=false;
        JOURNAL_PRESETS.forEach((preset,idx)=>{
          const opt=document.createElement('option'); opt.value=idx; opt.textContent=preset.label;
          if(sameKeys(keys,preset.keys)){ opt.selected=true; matchedPreset=true; }
          journalSelect.appendChild(opt);
        });
        if(it.journalManual===true && keys.length===1 && !matchedPreset){
          const customCurrent=document.createElement('option');
          customCurrent.value='custom-current'; customCurrent.textContent='✏ '+keys[0]; customCurrent.selected=true;
          journalSelect.appendChild(customCurrent);
        }
        const customOpt=document.createElement('option'); customOpt.value='custom'; customOpt.textContent='➕ Thêm nội dung khác...'; journalSelect.appendChild(customOpt);
        journalSelect.onchange=async ()=>{
          if(journalSelect.value==='custom'){
            const text=prompt('Nhập nội dung muốn ghi vào Nhật ký:','');
            if(text!==null && text.trim()){
              it.journalKeys=[text.trim()]; it.journalManual=true;
              await saveState(); render(); return;
            }
            render(); return;
          }
          if(journalSelect.value==='custom-current') return;
          await setItemJournalPreset(it,journalSelect.value);
        };
        row.appendChild(journalSelect);"""
if old in s:
    s=s.replace(old,new,1)
elif "customOpt.textContent='➕ Thêm nội dung khác...'" not in s:
    raise SystemExit('Journal select structure changed; refusing broad edit')

# Shipment names: use the same warm orange accent as section headings instead of black.
needle="""    nameInput.className = 'shipment-name';
    nameInput.value ="""
replacement="""    nameInput.className = 'shipment-name';
    nameInput.style.color = 'var(--accent)';
    nameInput.style.fontWeight = '700';
    nameInput.value ="""
if needle in s:
    s=s.replace(needle,replacement,1)
elif "nameInput.style.color = 'var(--accent)'" not in s:
    raise SystemExit('Shipment name structure changed; refusing broad edit')

p.write_text(s,encoding='utf-8')
