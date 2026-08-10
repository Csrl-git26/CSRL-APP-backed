const TOPIC_SUBJECT_MAP = {
  'BASIC MATHS, SETS & RELATION(BASIC TRIGONOMETRY, INEQUALITIES, MODULUS, LOGARITHM, FUNCTIONS & GRAPHS, GREATEST INTEGER FUNCTION, SURDS & INDICES.)': 'Mathematics'
};

function inferSubject(rawTopic) {
  const normalized = (rawTopic || '').replace(/\s+/g, ' ').trim().toUpperCase();
  const normNoEllipsis = normalized.replace(/[\.…]+$/, '').trim();
  console.log("normNoEllipsis:", normNoEllipsis);
  for (const [knownTopic, subj] of Object.entries(TOPIC_SUBJECT_MAP)) {
    if (knownTopic.startsWith(normNoEllipsis)) {
      return { subject: subj, topic: rawTopic.trim() };
    }
  }
  return null;
}

console.log(inferSubject("Basic Maths, Sets & Relation..."));
console.log(inferSubject("Basic Maths, Sets & Relation…"));
console.log(inferSubject("Basic Maths, Sets & Relation …"));
console.log(inferSubject("Basic Maths, Sets & Relation.\\."));
