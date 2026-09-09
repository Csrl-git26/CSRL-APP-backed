filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# ── 1. Replace CSS keyframes ──────────────────────────────────────────────────
old_css = """`
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

new_css = """`
        @keyframes csrlPulse {
          0%   { box-shadow: 0 0 0 0 rgba(200,0,0,1), 0 0 8px 2px rgba(255,0,0,0.9); background: #990000; }
          35%  { box-shadow: 0 0 0 10px rgba(200,0,0,0.5), 0 0 16px 6px rgba(255,0,0,0.6); background: #ff0000; }
          70%  { box-shadow: 0 0 0 20px rgba(200,0,0,0.1), 0 0 24px 8px rgba(255,0,0,0.2); background: #cc0000; }
          100% { box-shadow: 0 0 0 0 rgba(200,0,0,0), 0 0 8px 2px rgba(255,0,0,0.9); background: #990000; }
        }
        @keyframes csrlRing1 {
          0%   { r: 9;  stroke-opacity: 1;   stroke-width: 3; }
          100% { r: 22; stroke-opacity: 0;   stroke-width: 0.5; }
        }
        @keyframes csrlRing2 {
          0%   { r: 9;  stroke-opacity: 0.8; stroke-width: 2.5; }
          100% { r: 20; stroke-opacity: 0;   stroke-width: 0.5; }
        }
        @keyframes csrlRing3 {
          0%   { r: 9;  stroke-opacity: 0.5; stroke-width: 2; }
          100% { r: 18; stroke-opacity: 0;   stroke-width: 0.5; }
        }
        @keyframes csrlDotPump {
          0%   { r: 8; }
          40%  { r: 10; }
          100% { r: 8; }
        }
      `"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("Updated CSS keyframes!")
else:
    print("WARNING: Could not find old CSS block")

# ── 2. Replace SVG circles with bigger, denser, more dramatic version ─────────
old_circles = """          <g style={{ pointerEvents: 'all', cursor: 'pointer' }} onMouseEnter={playAlertSound}>
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

new_circles = """          <g style={{ pointerEvents: 'all', cursor: 'pointer' }} onMouseEnter={playAlertSound}>
            {/* SVG defs for radial gradient */}
            <defs>
              <radialGradient id={`rdg-${index}`} cx="40%" cy="35%" r="65%">
                <stop offset="0%"   stopColor="#ff6666" />
                <stop offset="45%"  stopColor="#dd0000" />
                <stop offset="100%" stopColor="#660000" />
              </radialGradient>
              <filter id={`rglow-${index}`} x="-80%" y="-80%" width="260%" height="260%">
                <feGaussianBlur stdDeviation="3.5" result="blur" />
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>

            {/* Ring 1 — fastest, first wave */}
            <circle
              cx={centerX} cy={topY - 14} r={9}
              fill="none" stroke="#ff0000" strokeWidth={3}
              style={{ animation: 'csrlRing1 1s ease-out infinite 0s' }}
            />
            {/* Ring 2 — medium, second wave */}
            <circle
              cx={centerX} cy={topY - 14} r={9}
              fill="none" stroke="#cc0000" strokeWidth={2.5}
              style={{ animation: 'csrlRing2 1s ease-out infinite 0.25s' }}
            />
            {/* Ring 3 — slowest, third wave */}
            <circle
              cx={centerX} cy={topY - 14} r={9}
              fill="none" stroke="#990000" strokeWidth={2}
              style={{ animation: 'csrlRing3 1s ease-out infinite 0.5s' }}
            />
            {/* Dense core dot with gradient and glow */}
            <circle
              cx={centerX} cy={topY - 14} r={9}
              fill={`url(#rdg-${index})`}
              stroke="#ffffff"
              strokeWidth={2}
              filter={`url(#rglow-${index})`}
              style={{ animation: 'csrlDotPump 1s ease-in-out infinite' }}
            />
          </g>"""

if old_circles in content:
    content = content.replace(old_circles, new_circles)
    print("Updated SVG circles to dense red!")
else:
    print("WARNING: Could not find old circles block")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! Dense red alert dot upgraded.")
