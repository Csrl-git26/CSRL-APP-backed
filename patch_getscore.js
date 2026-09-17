const fs = require('fs');
let code = fs.readFileSync('services/analyticsService.js', 'utf8');
code = code.replace(
  /const rkUpper = rk\.toUpperCase\(\);\s+const subUpper = sub\.toUpperCase\(\);\s+if \(rkUpper === subUpper.+?return true;\s+return rk\.toLowerCase\(\)\.endsWith.+?;/g,
  `const rkUpper = rk.toUpperCase();
        const subUpper = sub.toUpperCase();
        if (rkUpper === subUpper || (rkUpper === "PHY" && sub === "Physics") || (rkUpper === "CHEM" && sub === "Chemistry") || (rkUpper === "BIO" && sub === "Biology") || (rkUpper === "BOT" && sub === "Botany") || (rkUpper === "ZOO" && sub === "Zoology") || (rkUpper === "MAT" && sub === "Math") || (rkUpper === "MATHS" && sub === "Math") || (rkUpper === "MATHEMATICS" && sub === "Math") || (rkUpper.includes("BOTNAY") && sub === "Botany")) return true;
        return rk.toLowerCase().endsWith("_" + sub.toLowerCase()) || rk.toLowerCase().endsWith("_botnay") && sub === "Botany" || (rkUpper.endsWith("_PHY") && sub === "Physics") || (rkUpper.endsWith("_CHEM") && sub === "Chemistry") || (rkUpper.endsWith("_BIO") && sub === "Biology") || (rkUpper.endsWith("_BOT") && sub === "Botany") || (rkUpper.endsWith("_ZOO") && sub === "Zoology") || (rkUpper.endsWith("_MAT") && sub === "Math") || (rkUpper.endsWith("_MATHS") && sub === "Math");`
);
fs.writeFileSync('services/analyticsService.js', code);
