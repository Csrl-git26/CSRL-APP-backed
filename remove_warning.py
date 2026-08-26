import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

warning_block = """      <div
        className="card"
        style={{
          background: 'var(--yellow-bg)',
          border: '1px solid #fde68a',
          fontSize: 13,
          color: '#92400e',
          lineHeight: 1.6,
        }}
      >
        <strong>How this compares to your memo</strong>
        <p style={{ marginTop: 8, marginBottom: 0 }}>
          {insights.note}
        </p>
        {cut?.JEE && cut?.NEET && (
          <p style={{ marginTop: 8, marginBottom: 0, lineHeight: 1.5 }}>
            Default qualification — <strong>JEE</strong>: Category-based cutoff applied. 
            <br />
            <span style={{ fontSize: 11, color: 'var(--gray-600)' }}>
              Total marks criteria: GEN ≥ 110 | EWS ≥ 90 | OBC ≥ 85 | SC ≥ 65 | ST ≥ 60 | PWD ≥ 30.
            </span>
            <br />
            <strong>NEET</strong>: total ≥ {cut.NEET.overallMin} / {cut.NEET.maxTotal}; Biology max {cut.NEET.maxBySubject.Biology}, others{' '}
            {cut.NEET.maxBySubject.Physics} / {cut.NEET.maxBySubject.Chemistry}.
          </p>
        )}
      </div>"""

if warning_block in content:
    content = content.replace(warning_block, "")
    with open(filepath, 'w') as f:
        f.write(content)
    print("Warning block removed successfully!")
else:
    print("Warning block not found.")
