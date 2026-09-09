import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Add imports
old_imports = """import {
  Trophy, TrendingUp, TrendingDown, Users, AlertTriangle,
  BarChart3, Target, Award, BookOpen, Star, Flag
} from 'lucide-react';"""
new_imports = """import {
  Trophy, TrendingUp, TrendingDown, Users, AlertTriangle,
  BarChart3, Target, Award, BookOpen, Star, Flag, PieChart as PieChartIcon
} from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';"""

if old_imports in content:
    content = content.replace(old_imports, new_imports)

old_block = """      {centreBoard.length > 0 && (
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          
          {(() => {
            const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
            const topCentres = sorted.slice(0,5).map((c,i) => ({...c, rank: i+1}));
            const bottomCentres = sorted.length > 5 ? sorted.slice(-5).map((c,i) => ({...c, rank: sorted.length - 5 + i + 1})) : [];
            
            const renderCard = (c) => {
              const isAlert = c.avg < 100 || (c.qualRate??0) < 80;
              const medals = {1:'🥇',2:'🥈',3:'🥉'};
              const rankDisplay = medals[c.rank] || `#${c.rank}`;
              return (
                <div key={c.code} style={{ padding:'8px 6px', borderRadius:8, textAlign:'center',
                  background: isAlert ? '#fef2f2' : '#f8fafc',
                  border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0',
                  cursor: onViewCentre ? 'pointer' : 'default' }}
                  onClick={() => onViewCentre && onViewCentre(c.code)}>
                  <div style={{ fontSize:14 }}>{rankDisplay}</div>
                  <div style={{ fontWeight:800, fontSize:12, color:'#1e293b', marginTop:2 }}>{c.code}</div>
                  <div style={{ fontSize:16, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:2 }}>
                    {Math.round(c.avg)}
                  </div>
                  {c.qualRate !== undefined && (
                    <div style={{ marginTop:2, fontSize:10, fontWeight:700,
                      color: c.qualRate < 80 ? '#dc2626' : '#16a34a' }}>
                      {Math.round(c.qualRate)}% Qual.
                    </div>
                  )}
                </div>
              );
            };

            return (
              <>
                <SectionTitle Icon={Star} color="#f59e0b">Top 5 Centres by Average Score</SectionTitle>
                <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10, marginBottom: bottomCentres.length > 0 ? 20 : 0 }}>
                  {topCentres.map(renderCard)}
                </div>
                
                {bottomCentres.length > 0 && (
                  <>
                    <SectionTitle Icon={TrendingDown} color="#dc2626">Bottom 5 Centres</SectionTitle>
                    <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
                      {bottomCentres.map(renderCard)}
                    </div>
                  </>
                )}
              </>
            );
          })()}
        </div>
      )}"""

new_block = """      {centreBoard.length > 0 && (() => {
        const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
        const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);
        const aboveAvgCount = sorted.filter(c => (c.avg||0) >= overallAvg).length;
        const belowAvgCount = sorted.filter(c => (c.avg||0) < overallAvg).length;

        const pieData = [
          { name: 'Above Average', value: aboveAvgCount, color: '#10b981' },
          { name: 'Below Average', value: belowAvgCount, color: '#ef4444' }
        ];

        return (
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>
            {/* Left Column: Top and Bottom 5 */}
            <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
              
              {(() => {
                const topCentres = sorted.slice(0,5).map((c,i) => ({...c, rank: i+1}));
                const bottomCentres = sorted.length > 5 ? sorted.slice(-5).map((c,i) => ({...c, rank: sorted.length - 5 + i + 1})) : [];
                
                const renderCard = (c) => {
                  const isAlert = c.avg < 100 || (c.qualRate??0) < 80;
                  const medals = {1:'🥇',2:'🥈',3:'🥉'};
                  const rankDisplay = medals[c.rank] || `#${c.rank}`;
                  return (
                    <div key={c.code} style={{ padding:'8px 6px', borderRadius:8, textAlign:'center',
                      background: isAlert ? '#fef2f2' : '#f8fafc',
                      border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0',
                      cursor: onViewCentre ? 'pointer' : 'default' }}
                      onClick={() => onViewCentre && onViewCentre(c.code)}>
                      <div style={{ fontSize:14 }}>{rankDisplay}</div>
                      <div style={{ fontWeight:800, fontSize:12, color:'#1e293b', marginTop:2 }}>{c.code}</div>
                      <div style={{ fontSize:16, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:2 }}>
                        {Math.round(c.avg)}
                      </div>
                      {c.qualRate !== undefined && (
                        <div style={{ marginTop:2, fontSize:10, fontWeight:700,
                          color: c.qualRate < 80 ? '#dc2626' : '#16a34a' }}>
                          {Math.round(c.qualRate)}% Qual.
                        </div>
                      )}
                    </div>
                  );
                };

                return (
                  <>
                    <SectionTitle Icon={Star} color="#f59e0b">Top 5 Centres by Average Score</SectionTitle>
                    <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10, marginBottom: bottomCentres.length > 0 ? 20 : 0 }}>
                      {topCentres.map(renderCard)}
                    </div>
                    
                    {bottomCentres.length > 0 && (
                      <>
                        <SectionTitle Icon={TrendingDown} color="#dc2626">Bottom 5 Centres</SectionTitle>
                        <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
                          {bottomCentres.map(renderCard)}
                        </div>
                      </>
                    )}
                  </>
                );
              })()}
            </div>
            
            {/* Right Column: Pie Chart */}
            <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column' }}>
              <SectionTitle Icon={PieChartIcon} color="#3b82f6">Centre Distribution</SectionTitle>
              <div style={{ flex: 1, minHeight: 220, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={2}>
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name) => [`${value} Centres`, name]} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: 12, paddingTop: 10 }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        );
      })()}"""

if old_block in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(old_block, new_block))
    print("Patched InsightsDashboard.jsx successfully")
else:
    print("old_block not found")
