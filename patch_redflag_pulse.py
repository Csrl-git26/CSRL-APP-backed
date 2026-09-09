import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Replace the red flag emoji in tooltip (line 30) - "🚩 ACTION REQUIRED"
old_tooltip_flag = '{isRedFlag && <div style={{ color: \'#ef4444\', fontWeight: 800, marginBottom: 4 }}>🚩 ACTION REQUIRED</div>}'
new_tooltip_flag = (
    '{isRedFlag && ('
    '<div style={{ display: \'flex\', alignItems: \'center\', gap: 6, marginBottom: 4 }}>'
    '<span style={{ display: \'inline-block\', width: 10, height: 10, borderRadius: \'50%\', background: \'#ef4444\', animation: \'csrlPulse 1s ease-in-out infinite\', boxShadow: \'0 0 0 0 rgba(239,68,68,0.7)\', flexShrink: 0 }} />'
    '<span style={{ color: \'#ef4444\', fontWeight: 800, letterSpacing: 0.5 }}>⚠ ACTION REQUIRED</span>'
    '</div>'
    ')}'
)

if old_tooltip_flag in content:
    content = content.replace(old_tooltip_flag, new_tooltip_flag)
    print("Patched tooltip flag!")
else:
    print("WARNING: Could not find tooltip flag line")

# 2. Replace the 🚩 emoji in the SVG bar label with pulsing SVG circles
old_bar_flag = """        {isRedFlag && (
          <text x={centerX} y={topY - 4} fill=\"#ef4444\" textAnchor=\"middle\" fontSize={18} style={{ textShadow: showInside ? '0px 0px 4px rgba(255,255,255,0.8)' : 'none' }}>
            🚩
          </text>
        )}"""

new_bar_flag = """        {isRedFlag && (
          <g>
            {/* Outer pulsing ring */}
            <circle
              cx={centerX}
              cy={topY - 12}
              r={9}
              fill="none"
              stroke="#ef4444"
              strokeWidth={2}
              opacity={0.5}
              style={{ animation: 'csrlRingPulse 1s ease-in-out infinite' }}
            />
            {/* Inner solid dot */}
            <circle
              cx={centerX}
              cy={topY - 12}
              r={5}
              fill="#ef4444"
              style={{ animation: 'csrlDotBlink 1s ease-in-out infinite' }}
            />
          </g>
        )}"""

if old_bar_flag in content:
    content = content.replace(old_bar_flag, new_bar_flag)
    print("Patched bar flag!")
else:
    print("WARNING: Could not find bar flag block")

# 3. Inject the keyframe CSS animation into the component via a <style> tag inside the return div
# Find the outer container div and inject a style block before it
old_return_div = '  return (\n    <div style={{ width: \'100%\', height: 320, marginTop: 0 }}>'
new_return_div = (
    '  return (\n'
    '    <div style={{ width: \'100%\', height: 320, marginTop: 0 }}>\n'
    '      <style>{`\n'
    '        @keyframes csrlPulse {\n'
    '          0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.8); background: #ef4444; }\n'
    '          50%  { box-shadow: 0 0 0 6px rgba(239,68,68,0); background: #ff6b6b; }\n'
    '          100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); background: #ef4444; }\n'
    '        }\n'
    '        @keyframes csrlRingPulse {\n'
    '          0%   { r: 6; opacity: 0.8; }\n'
    '          50%  { r: 11; opacity: 0.1; }\n'
    '          100% { r: 6; opacity: 0.8; }\n'
    '        }\n'
    '        @keyframes csrlDotBlink {\n'
    '          0%   { opacity: 1; }\n'
    '          50%  { opacity: 0.4; }\n'
    '          100% { opacity: 1; }\n'
    '        }\n'
    '      `}</style>'
)

if old_return_div in content:
    content = content.replace(old_return_div, new_return_div)
    print("Injected CSS keyframes!")
else:
    print("WARNING: Could not find return div")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! CentreLeaderboard.jsx patched.")
