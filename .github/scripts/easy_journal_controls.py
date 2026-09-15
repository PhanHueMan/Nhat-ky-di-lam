from pathlib import Path

p=Path('checklist-lo-hang.html')
s=p.read_text(encoding='utf-8')
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
if old not in s:
    if "customOpt.textContent='➕ Thêm nội dung khác...'" in s:
        raise SystemExit(0)
    raise SystemExit('Journal select structure changed; refusing broad edit')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
