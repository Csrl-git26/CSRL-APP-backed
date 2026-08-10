import json

weakMap = {
  "FMT04": {
    "attempted": 43,
    "correct": 31,
    "wrong": 12,
    "subjectMetrics": {
      "Physics": { "attempted": 9, "correct": 5, "wrong": 4, "totalQuestions": 25 },
      "Chemistry": { "attempted": 21, "correct": 16, "wrong": 5, "totalQuestions": 25 },
      "Mathematics": { "attempted": 13, "correct": 10, "wrong": 3, "totalQuestions": 25 }
    }
  }
}

chartData = [
  {"name":"FMT01","Total":95,"Chemistry":42,"Math":11,"Physics":42},
  {"name":"FMT04","Total":112,"Chemistry":59,"Math":37,"Physics":16}
]

finalChartData = []
for row in chartData:
    new_row = row.copy()
    normRowName = row.get("name", "").upper()
    wt = weakMap.get(normRowName)
    if wt:
        for sub in ['Physics', 'Chemistry', 'Mathematics', 'Biology']:
            outSub = 'Math' if sub == 'Mathematics' else sub
            metrics = wt.get("subjectMetrics", {}).get(sub)
            if metrics and metrics.get("attempted", 0) > 0:
                new_row[f"{outSub}_Attempted"] = metrics["attempted"]
                new_row[f"{outSub}_Correct"] = metrics["correct"]
                new_row[f"{outSub}_Accuracy"] = round((metrics["correct"] / metrics["attempted"]) * 100)
        
        if wt.get("attempted", 0) > 0:
            new_row["Total_Attempted"] = wt["attempted"]
            new_row["Total_Correct"] = wt["correct"]
            new_row["Total_Accuracy"] = round((wt["correct"] / wt["attempted"]) * 100)
    
    finalChartData.append(new_row)

print(json.dumps(finalChartData, indent=2))
