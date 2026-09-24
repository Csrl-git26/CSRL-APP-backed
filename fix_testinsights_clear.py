filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Fix 1: Add setLoading(true) at start of load function
old_load_start = """  useEffect(() => {
    const load = async () => {
      try {
        const [d, ov] = await Promise.all(["""

new_load_start = """  useEffect(() => {
    setLoading(true);
    setError('');
    const load = async () => {
      try {
        const [d, ov] = await Promise.all(["""

# Fix 2: Clear testInsights when selectedTestKey changes
old_insights_fetch = """    if (activePage !== 'topbottom' || !selectedTestKey) return undefined;
    let cancelled = false;
    setTestInsightsLoading(true);
    setTestInsightsError('');"""

new_insights_fetch = """    if (activePage !== 'topbottom' || !selectedTestKey) return undefined;
    let cancelled = false;
    setTestInsights(null);
    setTestInsightsLoading(true);
    setTestInsightsError('');"""

if old_load_start in content:
    content = content.replace(old_load_start, new_load_start, 1)
    print("Fixed: Added setLoading(true) at start of load")
else:
    print("WARNING: Could not find load start")

if old_insights_fetch in content:
    content = content.replace(old_insights_fetch, new_insights_fetch, 1)
    print("Fixed: Added setTestInsights(null) before new fetch")
else:
    print("WARNING: Could not find insights fetch")

with open(filepath, 'w') as f:
    f.write(content)
print("CentreDashboard.jsx updated!")
