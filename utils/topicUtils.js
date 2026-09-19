/**
 * utils/topicUtils.js
 */

export function getMark(marks, question) {
  let raw;
  if (marks instanceof Map) {
    raw = marks.get(question);
  } else {
    raw = marks[question];
  }
  if (raw === null || raw === undefined || raw === '') return null;
  const n = typeof raw === 'number' ? raw : parseFloat(raw);
  return isNaN(n) ? null : n;
}

export function isStudentAbsent(marks, allQuestions) {
  if (!allQuestions || allQuestions.length === 0) return true;
  return allQuestions.every(q => getMark(marks, q) === null);
}

// Full Sheet4 Curriculum Definitions
export const SHEET4_CURRICULUM = [
  // Physics
  { code: 'P1', name: 'General Physics and Experimental skills', subject: 'PHYSICS' },
  { code: 'P2', name: 'Kinematics', subject: 'PHYSICS' },
  { code: 'P3', name: 'Laws of Motion, Friction', subject: 'PHYSICS' },
  { code: 'P4', name: 'Circular motion', subject: 'PHYSICS' },
  { code: 'P5', name: 'Work, Power & Energy', subject: 'PHYSICS' },
  { code: 'P6', name: 'Center of Mass & Collisions', subject: 'PHYSICS' },
  { code: 'P7', name: 'Rotation', subject: 'PHYSICS' },
  { code: 'P8', name: 'SHM', subject: 'PHYSICS' },
  { code: 'P9', name: 'WAVES', subject: 'PHYSICS' },
  { code: 'P10', name: 'Electrostatics', subject: 'PHYSICS' },
  { code: 'P11', name: 'Gravitation', subject: 'PHYSICS' },
  { code: 'P12', name: 'Capacitors', subject: 'PHYSICS' },
  { code: 'P13', name: 'Current Electricity', subject: 'PHYSICS' },
  { code: 'P14', name: 'EM Waves', subject: 'PHYSICS' },
  { code: 'P15', name: 'Wave Optics', subject: 'PHYSICS' },
  { code: 'P16', name: 'Geometric Optics', subject: 'PHYSICS' },
  { code: 'P17', name: 'Modern Physics', subject: 'PHYSICS' },
  { code: 'P18', name: 'Semi Conductors', subject: 'PHYSICS' },
  { code: 'P19', name: 'Magnetic effect of current', subject: 'PHYSICS' },
  { code: 'P20', name: 'Magnetism', subject: 'PHYSICS' },
  { code: 'P21', name: 'EMI', subject: 'PHYSICS' },
  { code: 'P22', name: 'AC', subject: 'PHYSICS' },
  { code: 'P23', name: 'Thermal Physics', subject: 'PHYSICS' },
  { code: 'P24', name: 'Elasticity', subject: 'PHYSICS' },
  { code: 'P25', name: 'Fluid', subject: 'PHYSICS' },

  // Chemistry
  { code: 'C1', name: 'Some Basic Concepts of Chemistry', subject: 'CHEMISTRY' },
  { code: 'C2', name: 'Redox reactions', subject: 'CHEMISTRY' },
  { code: 'C3', name: 'Solutions', subject: 'CHEMISTRY' },
  { code: 'C4', name: 'Atomic Structure', subject: 'CHEMISTRY' },
  { code: 'C5', name: 'Classification of elements & periodicity in properties', subject: 'CHEMISTRY' },
  { code: 'C6', name: 'Chemical Bonding & Molecular Structure', subject: 'CHEMISTRY' },
  { code: 'C7', name: 'Coordination Compounds', subject: 'CHEMISTRY' },
  { code: 'C8', name: 'd & f Block elements', subject: 'CHEMISTRY' },
  { code: 'C9', name: 'Chemical Kinetics', subject: 'CHEMISTRY' },
  { code: 'C10', name: 'Purification & Characterisation of Organic Compounds', subject: 'CHEMISTRY' },
  { code: 'C11', name: 'Some Basic Principles of Organic Chemistry-Nomenclature, Fundamental Concepts, Reaction Intermediates, Reaction Mechanism', subject: 'CHEMISTRY' },
  { code: 'C12', name: 'Isomerism - Structural & Stereoisomerism', subject: 'CHEMISTRY' },
  { code: 'C13', name: 'Hydrocarbons-Alkanes, Alkenes, Alkynes & Aromatic Hydrocarbons', subject: 'CHEMISTRY' },
  { code: 'C14', name: 'Organic compounds containing Halogens-Haloalkanes & Haloarenes', subject: 'CHEMISTRY' },
  { code: 'C15', name: 'Organic compounds containing oxygen-Alcohols, Phenols & Ethers, Aldehydes & Ketones, Carboxylic Acids', subject: 'CHEMISTRY' },
  { code: 'C16', name: 'Organic compounds containing Nitrogen-Amines & Diazonium Salts', subject: 'CHEMISTRY' },
  { code: 'C17', name: 'Biomolecules', subject: 'CHEMISTRY' },
  { code: 'C18', name: 'Chemical Thermodynamics', subject: 'CHEMISTRY' },
  { code: 'C19', name: 'Chemical Equilibrium', subject: 'CHEMISTRY' },
  { code: 'C20', name: 'Ionic Equlibrium', subject: 'CHEMISTRY' },
  { code: 'C21', name: 'Electrochemistry', subject: 'CHEMISTRY' },
  { code: 'C22', name: 'p Block Elements', subject: 'CHEMISTRY' },
  { code: 'C23', name: 'Principles Related to Practical Chemistry-Inorganic & Organic', subject: 'CHEMISTRY' },
  { code: 'C24', name: 'States of Matter Gases & Liquids', subject: 'CHEMISTRY' },
  { code: 'C25', name: 'Solid State', subject: 'CHEMISTRY' },
  { code: 'C26', name: 'Hydrogen & s Block Elements', subject: 'CHEMISTRY' },
  { code: 'C27', name: 'Isolation of Metals', subject: 'CHEMISTRY' },
  { code: 'C28', name: 'Surface Chemistry', subject: 'CHEMISTRY' },
  { code: 'C29', name: 'Polymers', subject: 'CHEMISTRY' },
  { code: 'C30', name: 'Environmental Chemistry', subject: 'CHEMISTRY' },
  { code: 'C31', name: 'Chemistry in everyday life', subject: 'CHEMISTRY' },

  // Mathematics
  { code: 'M1', name: 'Basic Maths, Sets & Relation', subject: 'MATHEMATICS' },
  { code: 'M2', name: 'Quadratic Equations', subject: 'MATHEMATICS' },
  { code: 'M3', name: 'Sequence & Series', subject: 'MATHEMATICS' },
  { code: 'M4', name: 'Trigonometric identities, Equations & inequalities; Properties & Solutions of Triangles', subject: 'MATHEMATICS' },
  { code: 'M5', name: 'Binomial Theorem', subject: 'MATHEMATICS' },
  { code: 'M6', name: 'Matrices & Determinants', subject: 'MATHEMATICS' },
  { code: 'M7', name: 'Straight Lines and Pair of Straight Lines', subject: 'MATHEMATICS' },
  { code: 'M8', name: 'Circles', subject: 'MATHEMATICS' },
  { code: 'M9', name: 'Parabola', subject: 'MATHEMATICS' },
  { code: 'M10', name: 'Ellipse & Hyperbola', subject: 'MATHEMATICS' },
  { code: 'M11', name: 'Vectors', subject: 'MATHEMATICS' },
  { code: 'M12', name: '3-D Geometry', subject: 'MATHEMATICS' },
  { code: 'M13', name: 'Statistics', subject: 'MATHEMATICS' },
  { code: 'M14', name: 'Inverse trigonometric & Function', subject: 'MATHEMATICS' },
  { code: 'M15', name: 'Limits, Continuity & Differentiability', subject: 'MATHEMATICS' },
  { code: 'M16', name: 'MOD, Application of Derivatives', subject: 'MATHEMATICS' },
  { code: 'M17', name: 'Indefinite Integration', subject: 'MATHEMATICS' },
  { code: 'M18', name: 'Definite Integeration', subject: 'MATHEMATICS' },
  { code: 'M19', name: 'Area', subject: 'MATHEMATICS' },
  { code: 'M20', name: 'Differential Equations', subject: 'MATHEMATICS' },
  { code: 'M21', name: 'Complex Numbers', subject: 'MATHEMATICS' },
  { code: 'M22', name: 'P & C', subject: 'MATHEMATICS' },
  { code: 'M23', name: 'Probability', subject: 'MATHEMATICS' },

  // NEET PHYSICS
  { code: 'NP1', name: 'Basic Mathematics For Physics', subject: 'PHYSICS' },
  { code: 'NP2', name: 'General Physics and Experimental skills', subject: 'PHYSICS' },
  { code: 'NP3', name: 'Kinematics', subject: 'PHYSICS' },
  { code: 'NP4', name: 'Laws of Motion, Friction', subject: 'PHYSICS' },
  { code: 'NP5', name: 'Work, Power & Energy', subject: 'PHYSICS' },
  { code: 'NP6', name: 'Circular motion', subject: 'PHYSICS' },
  { code: 'NP7', name: 'Center of Mass & Collisions', subject: 'PHYSICS' },
  { code: 'NP8', name: 'Rotation', subject: 'PHYSICS' },
  { code: 'NP9', name: 'Elasticity', subject: 'PHYSICS' },
  { code: 'NP10', name: 'SHM', subject: 'PHYSICS' },
  { code: 'NP11', name: 'Waves', subject: 'PHYSICS' },
  { code: 'NP12', name: 'Wave Optics', subject: 'PHYSICS' },
  { code: 'NP13', name: 'Geometric Optics', subject: 'PHYSICS' },
  { code: 'NP14', name: 'Modern Physics', subject: 'PHYSICS' },
  { code: 'NP15', name: 'Electrostatics', subject: 'PHYSICS' },
  { code: 'NP16', name: 'Gravitation', subject: 'PHYSICS' },
  { code: 'NP17', name: 'Capacitors', subject: 'PHYSICS' },
  { code: 'NP18', name: 'Current Electricity', subject: 'PHYSICS' },
  { code: 'NP19', name: 'Semi Conductors', subject: 'PHYSICS' },
  { code: 'NP20', name: 'Magnetic effect of current', subject: 'PHYSICS' },
  { code: 'NP21', name: 'Magnetism', subject: 'PHYSICS' },
  { code: 'NP22', name: 'EMI & AC', subject: 'PHYSICS' },
  { code: 'NP23', name: 'EMW', subject: 'PHYSICS' },
  { code: 'NP24', name: 'Thermal Physics', subject: 'PHYSICS' },
  { code: 'NP25', name: 'Fluid', subject: 'PHYSICS' },

  // NEET CHEMISTRY
  { code: 'NC1', name: 'Some Basic Concepts of Chemistry', subject: 'CHEMISTRY' },
  { code: 'NC2', name: 'Redox reaction', subject: 'CHEMISTRY' },
  { code: 'NC3', name: 'Solutions', subject: 'CHEMISTRY' },
  { code: 'NC4', name: 'Atomic Structure', subject: 'CHEMISTRY' },
  { code: 'NC5', name: 'Classification of elements & Periodicity in Properties', subject: 'CHEMISTRY' },
  { code: 'NC6', name: 'Chemical Bonding & Molecular Structure', subject: 'CHEMISTRY' },
  { code: 'NC7', name: 'Coordination Compounds', subject: 'CHEMISTRY' },
  { code: 'NC8', name: 'd & f Block elements', subject: 'CHEMISTRY' },
  { code: 'NC9', name: 'Chemical Kinetics', subject: 'CHEMISTRY' },
  { code: 'NC10', name: 'Purification & Characterisation of Organic Compounds', subject: 'CHEMISTRY' },
  { code: 'NC11', name: 'Some Basic Principles of Organic Chemistry, Nomenclature, Fundamental Concepts, Reaction Intermediates, Reaction Mechanism', subject: 'CHEMISTRY' },
  { code: 'NC12', name: 'Isomerism - Structural & Stereoisomerism', subject: 'CHEMISTRY' },
  { code: 'NC13', name: 'Hydrocarbons - Alkanes, Alkenes, Alkynes & Aromatic Hydrocarbons', subject: 'CHEMISTRY' },
  { code: 'NC14', name: 'Organic compounds containing Halogens - Haloalkanes & Haloarenes', subject: 'CHEMISTRY' },
  { code: 'NC15', name: 'Organic compounds containing oxygen - Alcohols, Phenols & Ethers, Aldehydes & Ketones, Carboxylic Acids', subject: 'CHEMISTRY' },
  { code: 'NC16', name: 'Organic compounds containing Nitrogen - Amines & Diazonium Salts', subject: 'CHEMISTRY' },
  { code: 'NC17', name: 'Biomolecules', subject: 'CHEMISTRY' },
  { code: 'NC18', name: 'Chemical Thermodynamics', subject: 'CHEMISTRY' },
  { code: 'NC19', name: 'Equilibrium', subject: 'CHEMISTRY' },
  { code: 'NC20', name: 'Electrochemistry', subject: 'CHEMISTRY' },
  { code: 'NC21', name: 'Principles Related to Practical Chemistry - Inorganic & Organic', subject: 'CHEMISTRY' },
  { code: 'NC22', name: 'p Block Elements', subject: 'CHEMISTRY' },

  // NEET BOTANY
  { code: 'B1', name: 'Living World', subject: 'BOTANY' },
  { code: 'B2', name: 'Biological Classification', subject: 'BOTANY' },
  { code: 'B3', name: 'Plant Kingdom', subject: 'BOTANY' },
  { code: 'B4', name: 'The Cell', subject: 'BOTANY' },
  { code: 'B5', name: 'Cell Cycle & Cell Division', subject: 'BOTANY' },
  { code: 'B6', name: 'Principle of Inheritance', subject: 'BOTANY' },
  { code: 'B7', name: 'Molecular Basis of Inheritance', subject: 'BOTANY' },
  { code: 'B8', name: 'Photosynthesis', subject: 'BOTANY' },
  { code: 'B9', name: 'Respiration in Plants', subject: 'BOTANY' },
  { code: 'B10', name: 'Plant Growth & Development', subject: 'BOTANY' },
  { code: 'B11', name: 'Microbes in Human Welfare', subject: 'BOTANY' },
  { code: 'B12', name: 'Anatomy of Plants', subject: 'BOTANY' },
  { code: 'B13', name: 'Morphology of Plants', subject: 'BOTANY' },
  { code: 'B14', name: 'Sexual Reproduction in Flowering Plants', subject: 'BOTANY' },
  { code: 'B15', name: 'Organisms & Population', subject: 'BOTANY' },
  { code: 'B16', name: 'Ecosystem', subject: 'BOTANY' },
  { code: 'B17', name: 'Biodiversity & Conservation', subject: 'BOTANY' },

  // NEET ZOOLOGY
  { code: 'Z1', name: 'Animal Kingdom', subject: 'ZOOLOGY' },
  { code: 'Z2', name: 'Biomolecules', subject: 'ZOOLOGY' },
  { code: 'Z3', name: 'Structural Organisation', subject: 'ZOOLOGY' },
  { code: 'Z4', name: 'Breathing', subject: 'ZOOLOGY' },
  { code: 'Z5', name: 'Circulation', subject: 'ZOOLOGY' },
  { code: 'Z6', name: 'Excretion', subject: 'ZOOLOGY' },
  { code: 'Z7', name: 'Locomotion', subject: 'ZOOLOGY' },
  { code: 'Z8', name: 'Neural Control & Coordination', subject: 'ZOOLOGY' },
  { code: 'Z9', name: 'Chemical Control & Coordination', subject: 'ZOOLOGY' },
  { code: 'Z10', name: 'Evolution', subject: 'ZOOLOGY' },
  { code: 'Z11', name: 'Human Reproduction', subject: 'ZOOLOGY' },
  { code: 'Z12', name: 'Reproductive Health', subject: 'ZOOLOGY' },
  { code: 'Z13', name: 'Biotechnology Principles', subject: 'ZOOLOGY' },
  { code: 'Z14', name: 'Biotechnology Applications', subject: 'ZOOLOGY' },
  { code: 'Z15', name: 'Human Health & Disease', subject: 'ZOOLOGY' },
];

export function matchCanonicalTopic(rawTopicStr) {
  // Extract topic before the slash, if any (e.g., 'Q60/Basic Maths' -> 'Basic Maths')
  let raw = rawTopicStr;
  if (raw.includes('/')) {
    const parts = raw.split('/');
    if (parts.length >= 2) {
      // The topic is usually the second part if the first is Qxx
      raw = parts[1];
    }
  }

  // Trim and remove newline
  const clean = raw.trim().replace(/\n/g, '').replace(/\s+/g, ' ').toLowerCase();

  for (const item of SHEET4_CURRICULUM) {
    const target = item.name.toLowerCase();
    if (clean === target || clean.startsWith(target) || target.startsWith(clean)) {
      return item;
    }
  }
  // Fallback
  return { code: 'GEN', name: rawTopicStr.trim(), subject: 'PHYSICS' };
}

