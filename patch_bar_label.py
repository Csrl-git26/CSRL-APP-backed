import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    const showInside = height > 70;
    const topY = showInside ? y + 25 : y - 25;
    const textColor = showInside ? "#ffffff" : "#1e293b";
    const subTextColor = showInside ? "#93c5fd" : "#0284c7";

    return (
      <g style={{ pointerEvents: 'none' }}>
        {isRedFlag && (
          <g style={{ pointerEvents: 'none' }}>
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
          </g>
        )}
        <text x={centerX} y={topY + (isRedFlag ? 12 : 0)} fill={textColor} textAnchor="middle" fontSize={12} fontWeight={500}>
          {typeof value === 'number' ? Math.round(value) : value}{isQualSort ? '%' : ''}
        </text>

      </g>
    );"""

new_code = """    const showInside = height > 70;
    
    // Positioning logic:
    // If text is inside, put text at y+20. Put dot ABOVE the bar (y-12)
    // If text is outside, put text at y-10. Put dot ABOVE the text (y-30)
    const textY = showInside ? y + 20 : y - 10;
    const dotY = showInside ? y - 12 : y - 30;
    
    const textColor = showInside ? "#ffffff" : "#1e293b";

    return (
      <g style={{ pointerEvents: 'none' }}>
        {isRedFlag && (
          <g style={{ pointerEvents: 'none' }}>
            {/* Outermost pulsing ring - delayed */}
            <circle
              cx={centerX}
              cy={dotY}
              r={4}
              fill="none"
              stroke="#cc0000"
              strokeWidth={2}
              style={{ animation: 'csrlRingPulse 1.2s ease-out infinite 0.3s', transformOrigin: `${centerX}px ${dotY}px` }}
            />
            {/* Middle pulsing ring */}
            <circle
              cx={centerX}
              cy={dotY}
              r={4}
              fill="none"
              stroke="#ff0000"
              strokeWidth={2.5}
              style={{ animation: 'csrlRingPulse2 1.2s ease-out infinite' }}
            />
            {/* Inner bold solid dot */}
            <circle
              cx={centerX}
              cy={dotY}
              r={6}
              fill="#cc0000"
              stroke="#ffffff"
              strokeWidth={1.5}
              style={{ animation: 'csrlDotBlink 1.2s ease-in-out infinite', filter: 'drop-shadow(0 0 4px #ff0000)' }}
            />
          </g>
        )}
        <text x={centerX} y={textY} fill={textColor} textAnchor="middle" fontSize={11} fontWeight={600} letterSpacing={-0.5}>
          {typeof value === 'number' ? Math.round(value) : value}{isQualSort ? '%' : ''}
        </text>
      </g>
    );"""

content = content.replace(old_code, new_code)
with open(filepath, 'w') as f:
    f.write(content)
print("Updated label positions in CentreLeaderboard.jsx")
