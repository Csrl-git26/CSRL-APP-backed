const fs = require('fs');
const file = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx';
let content = fs.readFileSync(file, 'utf8');

const replacement = `            {chartData.length > 0 && (() => {
              const calculateSubjectStats = (subject) => {
                let sum = 0;
                let count = 0;
                let fails = 0;
                
                let threshold = 35;
                if (stream === 'NEET') {
                  threshold = (subject === 'Biology' || subject === 'Botany' || subject === 'Zoology') ? 126 : 63;
                }

                chartData.forEach(row => {
                  const val = row[subject];
                  if (val !== undefined && val !== null && val !== 'Absent' && val !== 'a' && val !== 'A' && val !== '—') {
                    const num = Number(val);
                    if (!isNaN(num)) {
                      sum += num;
                      count++;
                      if (num < threshold) fails++;
                    }
                  }
                });

                return {
                  avg: count > 0 ? Math.round(sum / count) : '—',
                  fails
                };
              };

              const totalStats = (() => {
                let sum = 0;
                let count = 0;
                let fails = 0;
                let threshold = stream === 'NEET' ? 550 : 120;
                
                chartData.forEach(row => {
                  const val = row.Total;
                  if (val !== undefined && val !== null && val !== 'Absent' && val !== 'a' && val !== 'A' && val !== '—') {
                    const num = Number(val);
                    if (!isNaN(num)) {
                      sum += num;
                      count++;
                      if (num < threshold) fails++;
                    }
                  }
                });
                
                return {
                  avg: count > 0 ? Math.round(sum / count) : '—',
                  fails
                };
              })();

              return (
                <tr style={{ background: 'var(--gray-50)', borderTop: '2px solid var(--gray-200)' }}>
                  <td style={{ fontWeight: 800, color: 'var(--gray-800)' }}>
                    <div>Overall Average</div>
                    {!isCentre && <div style={{ fontSize: 10, color: '#991b1b', marginTop: 4 }}>No. of not qual.</div>}
                  </td>
                  {subjects.map(s => {
                    const stats = calculateSubjectStats(s);
                    return (
                      <td key={s}>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                          <span style={{ fontWeight: 700, color: 'var(--csrl-blue)', fontSize: '1.1em' }}>{stats.avg}</span>
                          {!isCentre && stats.fails > 0 && (
                            <span style={{ fontSize: 11, color: '#991b1b', fontWeight: 600 }}>{stats.fails} times</span>
                          )}
                          {!isCentre && stats.fails === 0 && stats.avg !== '—' && (
                            <span style={{ fontSize: 11, color: '#166534', fontWeight: 600 }}>0 times</span>
                          )}
                        </div>
                      </td>
                    );
                  })}
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      <span style={{ fontWeight: 800, color: '#1a4fa0', fontSize: '1.1em' }}>{totalStats.avg}</span>
                      {!isCentre && totalStats.fails > 0 && (
                        <span style={{ fontSize: 11, color: '#991b1b', fontWeight: 600 }}>{totalStats.fails} times</span>
                      )}
                      {!isCentre && totalStats.fails === 0 && totalStats.avg !== '—' && (
                        <span style={{ fontSize: 11, color: '#166534', fontWeight: 600 }}>0 times</span>
                      )}
                    </div>
                  </td>
                  <td></td>
                </tr>
              );
            })()}
          </tbody>
        </table>`;

content = content.replace('          </tbody>\n        </table>', replacement);
fs.writeFileSync(file, content);
