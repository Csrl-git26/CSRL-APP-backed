filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update the React import to include hooks
old_import = "import React from 'react';"
new_import = "import React, { useEffect, useRef, useCallback } from 'react';"

if old_import in content:
    content = content.replace(old_import, new_import)
    print("Updated React import!")
else:
    print("WARNING: Could not find React import")

# 2. Add the Web Audio API sound function + useEffect INSIDE the component, right after the function signature
old_component_start = """export default function CentreLeaderboard({ centreStats = [], selTest, selectedSubject, onCentreClick }) {
  if (!selTest) return <Empty message="Select a test to view rankings" />;
  if (!centreStats.length) return <Empty message={`No test data for ${selTest}`} />;"""

new_component_start = """export default function CentreLeaderboard({ centreStats = [], selTest, selectedSubject, onCentreClick }) {
  const audioCtxRef = useRef(null);

  const getAudioCtx = useCallback(() => {
    if (!audioCtxRef.current) {
      audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioCtxRef.current;
  }, []);

  // Play a sharp two-tone alert beep using Web Audio API (no external file needed)
  const playAlertSound = useCallback(() => {
    try {
      const ctx = getAudioCtx();
      const playTone = (freq, startTime, duration, vol = 0.4) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, startTime);
        gain.gain.setValueAtTime(0, startTime);
        gain.gain.linearRampToValueAtTime(vol, startTime + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
        osc.start(startTime);
        osc.stop(startTime + duration);
      };
      const now = ctx.currentTime;
      playTone(880, now, 0.12, 0.5);        // High beep
      playTone(660, now + 0.15, 0.12, 0.4); // Lower beep
      playTone(880, now + 0.30, 0.18, 0.5); // High beep again
    } catch (e) {
      // Audio not supported or blocked
    }
  }, [getAudioCtx]);

  // Play once on mount when red flags are detected
  useEffect(() => {
    if (!centreStats || !centreStats.length || !selTest) return;
    const hasRedFlag = centreStats.some(data => {
      if (selectedSubject === 'Total' || !selectedSubject) {
        return data.avg < 100 || (data.qualRate ?? 0) < 80;
      } else if (selectedSubject === 'Qualification') {
        return (data.qualRate ?? 0) < 80;
      } else {
        return data.avg <= 20;
      }
    });
    if (hasRedFlag) {
      // Small delay so the page renders first
      const t = setTimeout(() => playAlertSound(), 600);
      return () => clearTimeout(t);
    }
  }, [selTest, selectedSubject, centreStats, playAlertSound]);

  if (!selTest) return <Empty message="Select a test to view rankings" />;
  if (!centreStats.length) return <Empty message={`No test data for ${selTest}`} />;"""

if old_component_start in content:
    content = content.replace(old_component_start, new_component_start)
    print("Injected sound logic into component!")
else:
    print("WARNING: Could not find component start")

# 3. Add onMouseEnter to the bar to play sound on hover over red flag bars
# Find the BarChart Cell that uses isRedFlag color and add onMouseEnter
old_cell = """          <Cell
                key={`cell-${index}`}
                fill={isRedFlagBar ? '#ef4444' : '#1e4a9e'}
                stroke={isRedFlagBar ? '#b91c1c' : 'none'}
                strokeWidth={isRedFlagBar ? 2 : 0}
              />"""
new_cell = """          <Cell
                key={`cell-${index}`}
                fill={isRedFlagBar ? '#ef4444' : '#1e4a9e'}
                stroke={isRedFlagBar ? '#b91c1c' : 'none'}
                strokeWidth={isRedFlagBar ? 2 : 0}
                onMouseEnter={isRedFlagBar ? playAlertSound : undefined}
              />"""
if old_cell in content:
    content = content.replace(old_cell, new_cell)
    print("Added onMouseEnter sound to Cell!")
else:
    # Try alternate — find any Cell with isRedFlagBar
    import re
    # Try a simpler approach - find isRedFlagBar Cell block
    pattern = r"(fill=\{isRedFlagBar \? '#ef4444' : '#1e4a9e'\})"
    if re.search(pattern, content):
        print("Found Cell fill line, but pattern didn't match full block - skipping Cell hover (will rely on onMouseEnter on SVG g element)")
    else:
        print("WARNING: Could not find Cell block for hover sound")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! Sound effects added to CentreLeaderboard.jsx")
