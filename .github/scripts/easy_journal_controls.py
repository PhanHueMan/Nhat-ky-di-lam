from pathlib import Path

p = Path('checklist-lo-hang.html')
s = p.read_text(encoding='utf-8')

start = s.index('async function editItem(item){')
end = s.index('\n\nlet state =', start)
new = '''async function editItem(item){
  const newText=prompt('Tên đầu việc:',item.text);
  if(newText===null || !newText.trim()) return;
  item.text=newText.trim();
  await saveState();
  render();
}
const JOURNAL_PRESETS = [
  {label:'Không cập nhật Nhật ký', keys:[]},
  {label:'AN', keys:['AN']}, {label:'MNF', keys:['MNF']}, {label:'EDO', keys:['EDO']},
  {label:'Khai nháp TK', keys:['Khai nháp TK']}, {label:'Tờ khai', keys:['Tờ khai']},
  {label:'Lấy TK thông quan', keys:['Lấy TK thông quan']},
  {label:'Lấy TK thông quan + Lấy MV', keys:['Lấy TK thông quan','Lấy MV']},
  {label:'SI', keys:['SI']}, {label:'VGM', keys:['VGM']}, {label:'SI + VGM', keys:['SI','VGM']},
  {label:'Bill draft', keys:['Bill draft']}, {label:'Bill final', keys:['Bill (final)']}, {label:'Bill Sur', keys:['Bill Sur']}
];
function sameKeys(a,b){ return [...(a||[])].sort().join('|') === [...(b||[])].sort().join('|'); }
async function setItemJournalPreset(item, presetIndex){
  const preset=JOURNAL_PRESETS[Number(presetIndex)] || JOURNAL_PRESETS[0];
  item.journalKeys=[...preset.keys];
  item.journalManual=true;
  await saveState();
  render();
}'''
s = s[:start] + new + s[end:]

old = """        const mark=document.createElement('small');
        mark.style.cssText='display:block;margin-top:3px;font-weight:700;';
        mark.textContent=keys.length ? '→ Nhật ký: '+keys.join(' + ') : 'Không cập nhật Nhật ký';
        info.appendChild(mark);
        row.appendChild(info);
        const edit=document.createElement('button');"""
new2 = """        const mark=document.createElement('small');
        mark.style.cssText='display:block;margin-top:3px;font-weight:700;';
        mark.textContent=keys.length ? '→ Nhật ký: '+keys.join(' + ') : 'Không cập nhật Nhật ký';
        info.appendChild(mark);
        row.appendChild(info);

        const journalSelect=document.createElement('select');
        journalSelect.title='Chọn nội dung cập nhật sang Nhật ký';
        journalSelect.style.cssText='max-width:190px;padding:6px 8px;border:1px solid #d8d2c6;border-radius:7px;background:#fff;font-size:12px;';
        JOURNAL_PRESETS.forEach((preset,idx)=>{
          const opt=document.createElement('option'); opt.value=idx; opt.textContent=preset.label;
          if(sameKeys(keys,preset.keys)) opt.selected=true;
          journalSelect.appendChild(opt);
        });
        journalSelect.onchange=()=>setItemJournalPreset(it,journalSelect.value);
        row.appendChild(journalSelect);

        const edit=document.createElement('button');"""
if old not in s:
    raise SystemExit('renderManage marker missing')
s = s.replace(old, new2, 1)
p.write_text(s, encoding='utf-8')
