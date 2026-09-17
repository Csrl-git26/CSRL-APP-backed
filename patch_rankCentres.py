import re

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'r') as f:
    content = f.read()

old_init = """    if (!centreAgg[code]) centreAgg[code] = { sum: 0, count: 0, max: -Infinity, min: Infinity, studentCount: 0, phySum: 0, cheSum: 0, mathSum: 0, phyCount: 0, cheCount: 0, mathCount: 0 };"""
new_init = """    if (!centreAgg[code]) centreAgg[code] = { sum: 0, count: 0, max: -Infinity, min: Infinity, studentCount: 0, phySum: 0, cheSum: 0, mathSum: 0, phyCount: 0, cheCount: 0, mathCount: 0, bioSum: 0, bioCount: 0, botSum: 0, botCount: 0, zooSum: 0, zooCount: 0 };"""
content = content.replace(old_init, new_init)

old_getscore = """    const rKeys = Object.keys(doc);
    const getScore = (sub) => {
       let k = null;
       for (const key of testKeys) {
          k = rKeys.find(rk => rk === `${key}_${sub}` || rk === `${key}_${sub.toUpperCase()}` || rk === `${key}_${sub.toLowerCase()}`);
          if (k) break;
       }
       if (!k) k = rKeys.find(rk => rk === sub || rk.toLowerCase().endsWith('_' + sub.toLowerCase()));
       if (k && !isNaN(Number(doc[k]))) {
           let val = Number(doc[k]);
           return val > 0 ? val : 0;
       }
       return null;
    };"""
new_getscore = """    const rKeys = Object.keys(doc);
    const getScore = (sub) => {
       let k = null;
       for (const key of testKeys) {
          k = rKeys.find(rk => rk === `${key}_${sub}` || rk === `${key}_${sub.toUpperCase()}` || rk === `${key}_${sub.toLowerCase()}`);
          if (k) break;
       }
       if (!k) {
         k = rKeys.find(rk => {
            const rkUpper = rk.toUpperCase();
            const subUpper = sub.toUpperCase();
            if (rkUpper === subUpper || (rkUpper === "PHY" && sub === "Physics") || (rkUpper === "CHEM" && sub === "Chemistry") || (rkUpper === "BIO" && sub === "Biology") || (rkUpper === "BOT" && sub === "Botany") || (rkUpper === "ZOO" && sub === "Zoology") || (rkUpper === "MAT" && sub === "Math") || (rkUpper === "MATHS" && sub === "Math") || (rkUpper === "MATHEMATICS" && sub === "Math")) return true;
            return rk.toLowerCase().endsWith("_" + sub.toLowerCase()) || (rkUpper.endsWith("_PHY") && sub === "Physics") || (rkUpper.endsWith("_CHEM") && sub === "Chemistry") || (rkUpper.endsWith("_BIO") && sub === "Biology") || (rkUpper.endsWith("_BOT") && sub === "Botany") || (rkUpper.endsWith("_ZOO") && sub === "Zoology") || (rkUpper.endsWith("_MAT") && sub === "Math") || (rkUpper.endsWith("_MATHS") && sub === "Math");
         });
       }
       if (k && !isNaN(Number(doc[k]))) {
           let val = Number(doc[k]);
           return val > 0 ? val : 0;
       }
       return null;
    };"""
content = content.replace(old_getscore, new_getscore)

old_add = """    const m1 = getScore('Math'), m2 = getScore('Mathematics');
    const math = Math.max(m1||0, m2||0);
    if (m1 !== null || m2 !== null) { 
         centreAgg[code].mathSum += math; 
         centreAgg[code].mathCount++; 
    }"""
new_add = """    const m1 = getScore('Math'), m2 = getScore('Mathematics');
    const math = Math.max(m1||0, m2||0);
    if (m1 !== null || m2 !== null) { 
         centreAgg[code].mathSum += math; 
         centreAgg[code].mathCount++; 
    }
    const bio = getScore('Biology');
    if (bio !== null) { centreAgg[code].bioSum += bio; centreAgg[code].bioCount++; }
    const bot = getScore('Botany');
    if (bot !== null) { centreAgg[code].botSum += bot; centreAgg[code].botCount++; }
    const zoo = getScore('Zoology');
    if (zoo !== null) { centreAgg[code].zooSum += zoo; centreAgg[code].zooCount++; }"""
content = content.replace(old_add, new_add)

old_return = """         Physics: s.phyCount ? Math.round(s.phySum / s.phyCount) : 0,
         Chemistry: s.cheCount ? Math.round(s.cheSum / s.cheCount) : 0,
         Math: s.mathCount ? Math.round(s.mathSum / s.mathCount) : 0
      };"""
new_return = """         Physics: s.phyCount ? Math.round(s.phySum / s.phyCount) : 0,
         Chemistry: s.cheCount ? Math.round(s.cheSum / s.cheCount) : 0,
         Math: s.mathCount ? Math.round(s.mathSum / s.mathCount) : 0,
         Biology: s.bioCount ? Math.round(s.bioSum / s.bioCount) : 0,
         Botany: s.botCount ? Math.round(s.botSum / s.botCount) : 0,
         Zoology: s.zooCount ? Math.round(s.zooSum / s.zooCount) : 0
      };"""
content = content.replace(old_return, new_return)

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'w') as f:
    f.write(content)
print("Done rankCentresByTest")
