import ExcelJS from 'exceljs';
export const SENDER = 'ajaya.kumar@csrl.in';
export const PORTAL = 'प्रगति';
export const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const label = subject => subject === 'Math' ? 'Mathematics' : subject;
export function reportColumns(report) {
  return [
    { key: 'rank', title: 'Rank', integer: true }, { key: 'code', title: 'Centre' },
    { key: 'appeared', title: 'Appeared', integer: true }, { key: 'qualified', title: report.stream === 'NEET' ? 'Expected MBBS admission' : 'Qualified', integer: true },
    ...[...report.subjects, 'Total'].flatMap(subject => (subject === 'Total' ? ['_Attempted', '_Accuracy', ''] : ['_Attempted', '_Accuracy', '', '_Rank']).map(suffix => ({
      key: subject + suffix, group: label(subject), title: suffix === '_Attempted' ? 'Attempt' : suffix === '_Accuracy' ? 'Accu %' : suffix === '_Rank' ? 'Rank' : 'Avg', integer: suffix === '_Rank',
    }))),
  ];
}
export function renderEmail(selection, report) {
  const columns = reportColumns(report);
  const date = new Date(selection.testDate + 'T00:00:00+05:30').toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'long', year: 'numeric' });
  const scope = selection.stream + (selection.stream === 'JEE' ? ` ${selection.branch}` : '');
  const subject = `${PORTAL} | ${selection.testKey} Result Released | ${scope}`;
  const e = escapeHtml;
  const heading = 'background:#b91c1c;color:#fff;padding:9px;border:1px solid #e5e7eb;';
  const groupHead = report.subjects.concat('Total').map(sub => `<th colspan="${sub === 'Total' ? 3 : 4}" style="${heading}">${e(label(sub))}</th>`).join('');
  const body = [...report.rows, report.overall].map(row => `<tr${row.code === 'OVERALL' ? ' style="background:#b91c1c;color:white;font-weight:bold"' : ''}>${columns.map(col => {
    const v = row[col.key];
    const value = v === null || v === undefined ? '—' : typeof v === 'number' && !col.integer ? v.toFixed(1) : v;
    return `<td style="padding:8px;border:1px solid #e5e7eb;text-align:${col.key === 'code' ? 'left' : 'center'}">${e(value)}</td>`;
  }).join('')}</tr>`).join('');
  const html = `<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;padding:24px;font-family:Arial,sans-serif;color:#172554;background:#f8fafc"><h1 style="font-size:26px">${PORTAL}</h1><h2 style="font-size:20px">${e(selection.testKey)} — Result Released</h2><p>Dear Team,</p><p>The results of <strong>${e(selection.testKey)}</strong> (${e(scope)}), conducted on <strong>${e(date)}</strong>, are now available on the <strong>${PORTAL}</strong> portal.</p><p>Please log in to review the results, centre-wise performance, and student-wise analysis. The centre-wise summary is provided below, and the Excel report is attached for your reference.</p><div style="overflow-x:auto"><table style="border-collapse:collapse;font-size:12px"><thead><tr>${columns.slice(0,4).map(c => `<th rowspan="2" style="${heading}">${e(c.title)}</th>`).join('')}${groupHead}</tr><tr>${columns.slice(4).map(c => `<th style="${heading}">${e(c.title)}</th>`).join('')}</tr></thead><tbody>${body}</tbody></table></div><p style="margin:24px 0"><a href="https://csrl-pragati.vercel.app/" style="display:inline-block;background:#1d4ed8;color:white;padding:12px 20px;border-radius:6px;text-decoration:none">Open ${PORTAL} Portal</a></p><p>Kindly review the performance and plan the necessary academic follow-up.</p><p>Regards,<br><strong>CSRL Team</strong><br>${PORTAL} Portal</p><hr style="border:0;border-top:1px solid #e2e8f0"><p style="font-size:12px;color:#64748b">This is an automatically generated email from the ${PORTAL} portal. Please do not reply to this email.</p></body></html>`;
  const text = `Dear Team,\n\nThe results of ${selection.testKey} (${scope}), conducted on ${date}, are now available on the ${PORTAL} portal.\n\nPlease review centre-wise performance and student-wise analysis. The centre-wise Excel report is attached.\n\nOpen portal: https://csrl-pragati.vercel.app/\n\nKindly review the performance and plan the necessary academic follow-up.\n\nRegards,\nCSRL Team\n${PORTAL} Portal\n\nThis is an automatically generated email. Please do not reply.`;
  return { subject, html, text };
}
export async function reportWorkbook(report) {
  const book = new ExcelJS.Workbook();
  book.creator = 'CSRL — प्रगति';
  const sheet = book.addWorksheet('Centre analysis', { views: [{ state: 'frozen', ySplit: 2, xSplit: 2 }], pageSetup: { orientation: 'landscape', fitToPage: true, fitToWidth: 1, fitToHeight: 0 } });
  const cols = reportColumns(report);
  sheet.addRow(cols.map(c => c.group || c.title));
  sheet.addRow(cols.map(c => c.group ? c.title : null));
  for (let c = 1; c <= 4; c++) sheet.mergeCells(1,c,2,c);
  let start = 5;
  for (const sub of [...report.subjects, 'Total']) { const count = sub === 'Total' ? 3 : 4; sheet.mergeCells(1,start,1,start+count-1); start += count; }
  for (const row of [...report.rows, report.overall]) sheet.addRow(cols.map(c => row[c.key] ?? null));
  sheet.columns.forEach((col, i) => { col.width = i === 1 ? 16 : i === 3 ? 23 : 11; });
  sheet.eachRow((row, n) => {
    row.height = n <= 2 ? 28 : 22;
    row.eachCell({ includeEmpty: true }, (cell, i) => {
      cell.alignment = { horizontal: i === 2 && n > 2 ? 'left' : 'center', vertical: 'middle', wrapText: true };
      cell.border = { bottom: { style: 'thin', color: { argb: 'FFE2E8F0' } } };
      if (n <= 2 || n === sheet.rowCount) { cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFB91C1C' } }; cell.font = { bold: true, color: { argb: 'FFFFFFFF' } }; }
      if (n > 2 && typeof cell.value === 'number') cell.numFmt = cols[i-1].integer ? '0' : '0.0';
    });
  });
  return Buffer.from(await book.xlsx.writeBuffer());
}
