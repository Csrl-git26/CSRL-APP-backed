import AdvancedAttemptSheet from '../models/AdvancedAttemptSheet.js';
export const isAdvanced = (stream, branch) => String(stream).toUpperCase() === 'JEE' && branch === 'ADVANCED';
export const rollKey = value => String(value ?? '').trim().replace(/\.0+$/, '').toUpperCase();
const headerKey = value => String(value ?? '').trim().toLowerCase().replace(/[^a-z0-9]/g, '');
const error = message => Object.assign(new Error(message), { status: 400 });
export function parseAdvancedAttemptRows(rows, profiles) {
  if (!Array.isArray(rows) || rows.length < 2 || rows.length > 15001) throw error('Upload a header and 1–15000 student rows.');
  if (rows.some(row => !Array.isArray(row) || row.length > 50)) throw error('Invalid sheet rows.');
  const headers = rows[0].map(headerKey);
  const required = ['name','rollnumber','stream','centre','totalquestions','notattempted','attempted','incorrect','correct'];
  const indices = Object.fromEntries(required.map(key => [key,headers.indexOf(key)]));
  const missing = required.filter(key => indices[key] < 0);
  if (missing.length) throw error('Missing columns: '+missing.join(', ')+'. Use the provided attempt-count sheet format.');
  if (required.some(key => headers.filter(h => h === key).length !== 1)) throw error('The sheet contains duplicate column headers.');
  const accIndex = headers.indexOf('acc');
  const subjectDefinitions = [['physics','Physics'],['chemistry','Chemistry'],['mathematics','Math']];
  const hasSubjects = subjectDefinitions.some(([prefix]) => headers.some(h => h.startsWith(prefix)));
  const subjectColumns = hasSubjects ? subjectDefinitions.map(([prefix, subject]) => {
    const fields = Object.fromEntries([['total','totalQuestions'],['attempted','attempted'],['notattempted','notAttempted'],['correct','correct'],['incorrect','incorrect']].map(([suffix,key]) => {
      const header = prefix + suffix;
      if (headers.filter(h => h === header).length !== 1) throw error('Missing or duplicate subject column: ' + header);
      return [key, headers.indexOf(header)];
    }));
    const start = Math.min(...Object.values(fields)), end = Math.max(...Object.values(fields));
    const acc = headers.findIndex((h,i) => i >= start && i <= end && h === 'acc');
    return { subject, fields, acc };
  }) : [];
  const profileMap = new Map();
  for (const p of profiles) { const key=rollKey(p.ROLL_KEY); const list=profileMap.get(key)||[]; list.push(p); profileMap.set(key,list); }
  const seen = new Set(), records = [], errors = [];
  for (let index=1; index<rows.length; index++) {
    const row=rows[index]; if (row.every(v => v === null || v === undefined || String(v).trim()==='')) continue;
    const prefix=`Row ${index+1}`;
    const read=key=>row[indices[key]];
    const roll=rollKey(read('rollnumber')), centre=String(read('centre')??'').trim().toUpperCase();
    const name=String(read('name')??'').trim();
    if (!roll || roll.length>80 || !name || name.length>200 || !centre) { errors.push(`${prefix}: name, roll number and centre are required.`); continue; }
    if (seen.has(roll)) { errors.push(`${prefix}: duplicate roll number ${roll}.`); continue; } seen.add(roll);
    if (String(read('stream')).trim().toUpperCase() !== 'JEE') { errors.push(`${prefix}: only JEE students are allowed.`); continue; }
    const matches=(profileMap.get(roll)||[]).filter(p => String(p.centerCode||'').trim().toUpperCase()===centre && String(p.stream||'JEE').toUpperCase()==='JEE');
    if (matches.length!==1) { errors.push(`${prefix}: roll ${roll} must match one JEE profile in centre ${centre}.`); continue; }
    const counts={}; let invalid=false;
    for (const [column,key] of [['totalquestions','totalQuestions'],['notattempted','notAttempted'],['attempted','attempted'],['incorrect','incorrect'],['correct','correct']]) {
      const value=read(column), n=Number(value);
      if (value===null || value===undefined || String(value).trim()==='' || !Number.isInteger(n) || n<0 || n>10000) { errors.push(`${prefix}: ${column} must be a non-negative whole number.`); invalid=true; break; }
      counts[key]=n;
    }
    if(invalid) continue;
    if (!counts.totalQuestions || counts.notAttempted+counts.attempted!==counts.totalQuestions || counts.incorrect+counts.correct!==counts.attempted) { errors.push(`${prefix}: attempted + not_attempted must equal total_questions, and correct + incorrect must equal attempted.`); continue; }
    const accuracy=counts.attempted ? counts.correct/counts.attempted*100 : 0;
    if (accIndex>=0 && row[accIndex]!==null && row[accIndex]!==undefined && String(row[accIndex]).trim()!=='') {
      const value=Number(String(row[accIndex]).replace(/%$/,''));
      if (!Number.isFinite(value) || Math.abs(value-accuracy)>0.051) { errors.push(`${prefix}: ACC% disagrees with correct ÷ attempted × 100.`); continue; }
    }
    const subjects = {};
    for (const {subject, fields, acc} of subjectColumns) {
      const values = Object.fromEntries(Object.entries(fields).map(([key,col]) => [key, Number(row[col])]));
      if (Object.values(fields).some(col => row[col] === null || row[col] === undefined || String(row[col]).trim() === '' || !Number.isInteger(Number(row[col])) || Number(row[col]) < 0 || Number(row[col]) > 10000)) {
        errors.push(`${prefix}: ${subject} counts must be non-negative whole numbers.`); invalid=true; break;
      }
      if (values.attempted + values.notAttempted !== values.totalQuestions || values.correct + values.incorrect !== values.attempted) {
        errors.push(`${prefix}: ${subject} counts do not reconcile.`); invalid=true; break;
      }
      const expected = values.attempted ? values.correct / values.attempted * 100 : 0;
      if (acc >= 0 && row[acc] !== null && row[acc] !== undefined && String(row[acc]).trim() !== '') {
        const actual = Number(String(row[acc]).replace(/%$/,''));
        if (!Number.isFinite(actual) || Math.abs(actual-expected) > 0.051) { errors.push(`${prefix}: ${subject} ACC% disagrees with correct ÷ attempted × 100.`); invalid=true; break; }
      }
      subjects[subject] = values;
    }
    if (invalid) continue;
    if (hasSubjects && Object.keys(counts).some(key => Object.values(subjects).reduce((sum,v) => sum + v[key],0) !== counts[key])) {
      errors.push(`${prefix}: subject counts must add up to the overall counts.`); continue;
    }
    records.push({roll,name,centre,...counts,...(hasSubjects ? {subjects} : {})});
  }
  if(errors.length) throw error(`${errors.length} row error(s). Nothing uploaded.\n`+errors.slice(0,30).join('\n')+(errors.length>30?'\n…Fix these and preview again.':''));
  if(!records.length) throw error('No student data found.');
  return records;
}
export function emptyAdvancedMetrics() {
  return Object.fromEntries(['Physics','Chemistry','Math','Mathematics','Total'].flatMap(s => ['Attempted','Accuracy','Correct','Wrong'].map(m=>[`${s}_${m}`,null])));
}
export function aggregateAttemptRecords(records) {
  const attempted=records.reduce((sum,r)=>sum+r.attempted,0), correct=records.reduce((sum,r)=>sum+r.correct,0);
  const metrics = { ...emptyAdvancedMetrics(), Total_Attempted:records.length?attempted/records.length:null, Total_Accuracy:records.length?(attempted?correct/attempted*100:0):null, records:records.length };
  for (const subject of ['Physics','Chemistry','Math']) {
    const values = records.map(r => r.subjects?.[subject]);
    // Do not present partial subject coverage as a full centre/test result.
    if (!values.length || values.some(v => !v)) continue;
    const att = values.reduce((sum,v) => sum + v.attempted,0), cor = values.reduce((sum,v) => sum + v.correct,0);
    metrics[subject+'_Attempted'] = att / values.length;
    metrics[subject+'_Accuracy'] = att ? cor / att * 100 : 0;
  }
  return metrics;
}
export function advancedMetricsFromSheets(sheets, profiles) {
  const allowed=new Set(profiles.map(p=>rollKey(p.ROLL_KEY)+'|'+String(p.centerCode||'').trim().toUpperCase()));
  const groups=Object.fromEntries(profiles.map(p=>[p.centerCode,[]])); const all=[];
  for (const sheet of sheets) for (const record of sheet.records||[]) {
    if (!allowed.has(record.roll+'|'+record.centre)) continue;
    (groups[record.centre] ||= []).push(record); all.push(record);
  }
  return { source:'advanced-attempt-sheet', centres:Object.fromEntries(Object.entries(groups).map(([code,records])=>[code,aggregateAttemptRecords(records)])), overall:aggregateAttemptRecords(all) };
}
export async function loadAdvancedMetrics(testIds, profiles) {
  const sheets=await AdvancedAttemptSheet.find({_id:{$in:testIds}}).lean();
  return advancedMetricsFromSheets(sheets,profiles);
}
export async function applyAdvancedChartMetrics(rows, {stream,branch,profiles,roll,centre}, Model=AdvancedAttemptSheet) {
  if(!isAdvanced(stream,branch)) return rows;
  // Clear first, so a database failure cannot fall back to marks-derived metrics.
  for(const row of rows) {
    for(const key of Object.keys(row)) if (/_(Attempted|Accuracy|Correct|Wrong)$/.test(key)) row[key]=null;
    Object.assign(row,emptyAdvancedMetrics(),{attemptSource:'advanced-attempt-sheet'});
  }
  const sheets=await Model.find({_id:{$in:rows.map(r=>r.name)}}).lean();
  for(const row of rows) {
    const sheet=sheets.find(s=>s._id===row.name); if(!sheet) continue;
    if(roll) {
      const record=sheet.records.find(r=>r.roll===rollKey(roll) && (!centre || r.centre===String(centre).toUpperCase()));
      if(record) {
        Object.assign(row,aggregateAttemptRecords([record]),{Total_Correct:record.correct,Total_Wrong:record.incorrect});
        for (const [subject,counts] of Object.entries(record.subjects || {})) {
          row[subject+'_Correct']=counts.correct; row[subject+'_Wrong']=counts.incorrect;
        }
      }
    } else {
      const metrics=advancedMetricsFromSheets([sheet],profiles);
      Object.assign(row,metrics.centres[centre]||emptyAdvancedMetrics());
    }
  }
  return rows;
}
