filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Replace the old CSS keyframes with new stronger ones
old_css = """`
        @keyframes csrlPulse {
          0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.8); background: #ef4444; }
          50%  { box-shadow: 0 0 0 6px rgba(239,68,68,0); background: #ff6b6b; }
          100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); background: #ef4444; }
        }
        @keyframes csrlRingPulse {
          0%   { r: 6; opacity: 0.8; }
          50%  { r: 11; opacity: 0.1; }
          100% { r: 6; opacity: 0.8; }
        }
        @keyframes csrlDotBlink {
          0%   { opacity: 1; }
          50%  { opacity: 0.4; }
          100% { opacity: 1; }
        }
      `"""

new_css = """`
        @keyframes csrlPulse {
          0%   { box-shadow: 0 0 0 0 rgba(220,0,0,1); background: #cc0000; }
          40%  { box-shadow: 0 0 0 10px rgba(220,0,0,0.3); background: #ff0000; }
          80%  { box-shadow: 0 0 0 18px rgba(220,0,0,0); background: #cc0000; }
          100% { box-shadow: 0 0 0 0 rgba(220,0,0,0); background: #cc0000; }
        }
        @keyframes csrlRingPulse {
          0%   { r: 3; stroke-opacity: 1; stroke-width: 3; }
          60%  { r: 14; stroke-opacity: 0.1; stroke-width: 1; }
          100% { r: 16; stroke-opacity: 0; stroke-width: 0.5; }
        }
        @keyframes csrlRingPulse2 {
          0%   { r: 3; stroke-opacity: 0.7; stroke-width: 2; }
          60%  { r: 12; stroke-opacity: 0.05; stroke-width: 1; }
          100% { r: 14; stroke-opacity: 0; stroke-width: 0.5; }
        }
        @keyframes csrlDotBlink {
          0%   { opacity: 1; r: 6; }
          50%  { opacity: 0.75; r: 7; }
          100% { opacity: 1; r: 6; }
        }
      `"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("Updated CSS keyframes!")
else:
    print("WARNING: Could not find old CSS block")

# 2. Replace the SVG circles in the bar with bigger/bolder ones + two pulsing rings
old_bar_circles = """          <g>
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
          </g>"""

new_bar_circles = """          <g>
            {/* Outermost pulsing ring - delayed */}
            <circle
              cx={centerX}
              cy={topY - 14}
              r={4}
              fill="none"
              stroke="#cc0000"
              strokeWidth={2}
              style={{ animation: 'csrlRingPulse 1.2s ease-out infinite 0.3s', transformOrigin: `${centerX}px ${topY - 14}px` }}
            />
            {/* Middle pulsing ring */}
            <circle
              cx={centerX}
              cy={topY - 14}
              r={4}
              fill="none"
              stroke="#ff0000"
              strokeWidth={2.5}
              style={{ animation: 'csrlRingPulse2 1.2s ease-out infinite' }}
            />
            {/* Inner bold solid dot */}
            <circle
              cx={centerX}
              cy={topY - 14}
              r={6}
              fill="#cc0000"
              stroke="#ffffff"
              strokeWidth={1.5}
              style={{ animation: 'csrlDotBlink 1.2s ease-in-out infinite', filter: 'drop-shadow(0 0 4px #ff0000)' }}
            />
          </g>"""

if old_bar_circles in content:
    content = content.replace(old_bar_circles, new_bar_circles)
    print("Updated SVG bar circles!")
else:
    print("WARNING: Could not find old bar circles block")

# 3. Update the tooltip dot - bigger, bolder red
old_tooltip_dot = "style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#ef4444', animation: 'csrlPulse 1s ease-in-out infinite', boxShadow: '0 0 0 0 rgba(239,68,68,0.7)', flexShrink: 0 }}"
new_tooltip_dot = "style={{ display: 'inline-block', width: 14, height: 14, borderRadius: '50%', background: '#cc0000', animation: 'csrlPulse 1.2s ease-out infinite', boxShadow: '0 0 0 0 rgba(220,0,0,1)', flexShrink: 0, border: '2px solid #ff0000' }}"

if old_tooltip_dot in content:
    content = content.replace(old_tooltip_dot, new_tooltip_dot)
    print("Updated tooltip dot!")
else:
    print("WARNING: Could not find tooltip dot style")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! CentreLeaderboard.jsx fully upgraded.")
