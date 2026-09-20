import os

frontend_dir = "/Users/surya/Desktop/CSRL-APP-frontend/src/components"

for filename in ["StudentDashboard.jsx", "StudentProfileView.jsx"]:
    filepath = os.path.join(frontend_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()
    
    # 1. Update imports
    if "sortTestRowsChronologically" not in content:
        content = content.replace("buildStudentChartData,", "buildStudentChartData, sortTestRowsChronologically,")
    
    # 2. Update chartData logic
    old_code1 = "const rawRows = chart?.chartData ?? buildStudentChartData(studentTests, testColumns);"
    new_code1 = "const rawRows = chart?.chartData ? sortTestRowsChronologically([...chart.chartData]) : buildStudentChartData(studentTests, testColumns);"
    content = content.replace(old_code1, new_code1)

    old_code2 = "const rawRows = actualChart?.chartData ?? buildStudentChartData(studentTests, testColumns);"
    new_code2 = "const rawRows = actualChart?.chartData ? sortTestRowsChronologically([...actualChart.chartData]) : buildStudentChartData(studentTests, testColumns);"
    content = content.replace(old_code2, new_code2)
    
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Patched {filename}")

