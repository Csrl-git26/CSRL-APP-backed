import os

filepath_api = '/Users/surya/Desktop/CSRL-APP-frontend/src/services/dataService.js'
with open(filepath_api, 'r') as f:
    api_content = f.read()

old_api = """export async function fetchCentreChart(centerCode) {
  const params = new URLSearchParams({ centerCode, t: Date.now() });
  return apiFetch(`/api/analytics/centre-chart?${params}`);
}"""

new_api = """export async function fetchCentreChart(centerCode, stream) {
  const params = new URLSearchParams({ centerCode, t: Date.now() });
  if (stream && stream !== 'ALL') params.append('stream', stream);
  return apiFetch(`/api/analytics/centre-chart?${params}`);
}"""

api_content = api_content.replace(old_api, new_api)
with open(filepath_api, 'w') as f:
    f.write(api_content)


filepath_dash = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath_dash, 'r') as f:
    dash_content = f.read()

old_dash = """  useEffect(() => {
    if (!selectedTrendCentre) return;
    let isMounted = true;
    setTrendChartLoading(true);
    fetchCentreChart(selectedTrendCentre)
      .then(res => {"""

new_dash = """  useEffect(() => {
    if (!selectedTrendCentre) return;
    let isMounted = true;
    setTrendChartLoading(true);
    fetchCentreChart(selectedTrendCentre, globalStream)
      .then(res => {"""

dash_content = dash_content.replace(old_dash, new_dash)

# Note: The dependency array for this useEffect needs to include globalStream
# Wait, I can't just replace the top, I should replace the dependency array too.
old_dep = """    return () => { isMounted = false; };
  }, [selectedTrendCentre]);"""

new_dep = """    return () => { isMounted = false; };
  }, [selectedTrendCentre, globalStream]);"""

dash_content = dash_content.replace(old_dep, new_dep)

with open(filepath_dash, 'w') as f:
    f.write(dash_content)

print("Frontend patched for fetchCentreChart.")

# Fix hardcoded JEE in PerformanceChart
old_chart_render1 = "<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig('JEE')} noCard={true} height={240} />"
new_chart_render1 = "<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig(globalStream)} noCard={true} height={240} />"

old_chart_render2 = '<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig(\'JEE\')} noCard={true} height="100%" />'
new_chart_render2 = '<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig(globalStream)} noCard={true} height="100%" />'

dash_content = dash_content.replace(old_chart_render1, new_chart_render1)
dash_content = dash_content.replace(old_chart_render2, new_chart_render2)

with open(filepath_dash, 'w') as f:
    f.write(dash_content)

print("Frontend PerformanceChart patched.")
