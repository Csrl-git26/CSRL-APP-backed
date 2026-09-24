filepath = '../CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. After the stream changes, auto-reset selectedTestKey to the first NEET test.
# Find the useEffect for adminStream changes, add a new one for globalStream.
old_effect = """  useEffect(() => {
    if (selectedTestKey) {
      if (selectedTestKey.toUpperCase().startsWith('NCT') || selectedTestKey.toUpperCase().includes('NEET')) {
        setGlobalStream('NEET');
      } else if (selectedTestKey.toUpperCase().startsWith('MT') || selectedTestKey.toUpperCase().startsWith('FMT') || selectedTestKey.toUpperCase().startsWith('CMT')) {
        setGlobalStream('JEE');
      }
    }
  }, [selectedTestKey]);"""

new_effect = """  useEffect(() => {
    if (selectedTestKey) {
      if (selectedTestKey.toUpperCase().startsWith('NCT') || selectedTestKey.toUpperCase().includes('NEET')) {
        setGlobalStream('NEET');
      } else if (selectedTestKey.toUpperCase().startsWith('MT') || selectedTestKey.toUpperCase().startsWith('FMT') || selectedTestKey.toUpperCase().startsWith('CMT')) {
        setGlobalStream('JEE');
      }
    }
  }, [selectedTestKey]);

  // When stream changes manually, auto-select the first test for that stream.
  // This prevents crashes where selectedTestKey is a JEE test but globalStream is NEET.
  useEffect(() => {
    if (!allTestOptions || allTestOptions.length === 0) return;
    const NEET_PREFIX = /^(MMT|NCT|NMT|NEET)/i;
    const isNeetTest = (k) => NEET_PREFIX.test(k);
    const testsForStream = allTestOptions.filter(k => {
      return globalStream === 'NEET' ? isNeetTest(k) : !isNeetTest(k);
    });
    if (testsForStream.length === 0) return; // No tests for this stream yet — don't reset
    const currentIsWrongStream = globalStream === 'NEET'
      ? !isNeetTest(selectedTestKey || '')
      : isNeetTest(selectedTestKey || '');
    if (currentIsWrongStream) {
      setSelectedTestKey(testsForStream[0]);
      setSelectedLeaderboardTestKeys([testsForStream[0]]);
    }
  }, [globalStream]);"""

if old_effect in content:
    content = content.replace(old_effect, new_effect)
    print("Patched: added stream-change auto-select test useEffect")
else:
    print("ERROR: could not find target block")

# 2. Also guard centreChartData fetch with stream when globalStream changes
old_chart_fetch = """        fetchCentreChart(selectedCenterCode)
          .then(res => setCentreChartData(res?.chartData || []))
          .catch(e => console.error(\"Failed to fetch centre chart:\", e));"""
new_chart_fetch = """        fetchCentreChart(selectedCenterCode, globalStream)
          .then(res => setCentreChartData(res?.chartData || []))
          .catch(e => console.error(\"Failed to fetch centre chart:\", e));"""

if old_chart_fetch in content:
    content = content.replace(old_chart_fetch, new_chart_fetch)
    print("Patched: added stream param to initial centreChart fetch")
else:
    print("WARNING: could not find chart fetch block")

# 3. Add a useEffect to re-fetch centreChartData when stream changes  
old_trend_effect = """  useEffect(() => {
    if (!selectedTrendCentre) return;
    let isMounted = true;
    setTrendChartLoading(true);
    fetchCentreChart(selectedTrendCentre)"""
new_trend_effect = """  // Re-fetch centre chart data when stream changes
  useEffect(() => {
    if (!selectedCenterCode) return;
    fetchCentreChart(selectedCenterCode, globalStream)
      .then(res => setCentreChartData(res?.chartData || []))
      .catch(e => console.error('Failed to re-fetch centre chart on stream change:', e));
  }, [globalStream, selectedCenterCode]);

  useEffect(() => {
    if (!selectedTrendCentre) return;
    let isMounted = true;
    setTrendChartLoading(true);
    fetchCentreChart(selectedTrendCentre)"""

if old_trend_effect in content:
    content = content.replace(old_trend_effect, new_trend_effect)
    print("Patched: added re-fetch chart on stream change useEffect")
else:
    print("WARNING: could not find trend chart effect block")

with open(filepath, 'w') as f:
    f.write(content)

print("Done!")
