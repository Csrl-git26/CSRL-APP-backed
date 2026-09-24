import os

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """function filterByStream(profiles, tests, stream) {
  if (!stream || stream === 'ALL') return { profiles, tests };
  const targetStream = stream.toUpperCase();
  
  const profileStreams = {};
  profiles.forEach(p => {
    let rawStream = p.stream || p.STREAM || p.Stream;
    if (p.ROLL_KEY && (p.ROLL_KEY.includes('JRS') || p.ROLL_KEY.includes('TEZ') || p.ROLL_KEY.includes('PUN') || p.ROLL_KEY.includes('GVM') || p.ROLL_KEY.includes('JRT'))) {
      rawStream = 'NEET';
    } else if (!rawStream) {
      rawStream = 'JEE';
    }
    profileStreams[p.ROLL_KEY] = String(rawStream).trim().toUpperCase();
  });

  const filteredProfiles = profiles.filter(p => profileStreams[p.ROLL_KEY] === targetStream);

  const filteredTests = tests.filter(t => {
    if (profileStreams[t.ROLL_KEY]) {
      return profileStreams[t.ROLL_KEY] === targetStream;
    }
    let rawStream = t.stream;
    const roll = t.ROLL_KEY || '';
    const center = t.centerCode || '';
    if (roll.includes('JRS') || roll.includes('TEZ') || roll.includes('PUN') || roll.includes('GVM') || roll.includes('JRT') || center === 'JRS' || center === 'TEZ' || center === 'PUN' || center === 'GVM' || center === 'JRT') {
       rawStream = 'NEET';
    } else if (!rawStream) {
       rawStream = 'JEE';
    }
    return String(rawStream).trim().toUpperCase() === targetStream;
  });

  return { profiles: filteredProfiles, tests: filteredTests };
}"""

new_logic = """function filterByStream(profiles, tests, stream) {
  if (!stream || stream === 'ALL') return { profiles, tests };
  const targetStream = stream.toUpperCase();
  
  const profileStreams = {};
  profiles.forEach(p => {
    let rawStream = p.stream || p.STREAM || p.Stream;
    if (p.ROLL_KEY && (p.ROLL_KEY.includes('JRS') || p.ROLL_KEY.includes('TEZ') || p.ROLL_KEY.includes('PUN') || p.ROLL_KEY.includes('GVM') || p.ROLL_KEY.includes('JRT'))) {
      rawStream = 'NEET';
    } else if (!rawStream) {
      rawStream = 'JEE';
    }
    profileStreams[p.ROLL_KEY] = String(rawStream).trim().toUpperCase();
  });

  const filteredProfiles = profiles.filter(p => profileStreams[p.ROLL_KEY] === targetStream);
  const profileKeys = new Set(filteredProfiles.map(p => p.ROLL_KEY));

  const filteredTests = tests.filter(t => {
    if (profileStreams[t.ROLL_KEY]) {
      return profileStreams[t.ROLL_KEY] === targetStream;
    }
    let rawStream = t.stream;
    const roll = t.ROLL_KEY || '';
    const center = t.centerCode || '';
    if (roll.includes('JRS') || roll.includes('TEZ') || roll.includes('PUN') || roll.includes('GVM') || roll.includes('JRT') || center === 'JRS' || center === 'TEZ' || center === 'PUN' || center === 'GVM' || center === 'JRT') {
       rawStream = 'NEET';
    } else if (!rawStream) {
       rawStream = 'JEE';
    }
    
    const isTarget = String(rawStream).trim().toUpperCase() === targetStream;
    
    if (isTarget) {
      if (!profileKeys.has(roll)) {
        filteredProfiles.push({
          ROLL_KEY: roll,
          centerCode: center,
          stream: rawStream,
          name: t.name || roll
        });
        profileKeys.add(roll);
      }
      return true;
    }
    return false;
  });

  return { profiles: filteredProfiles, tests: filteredTests };
}"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched filterByStream for dummy profiles!")
else:
    print("Could not find old_logic in server.js")
