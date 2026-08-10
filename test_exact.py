import re

TOPIC_SUBJECT_MAP = {
  'DEFINITE INTEGRATION': 'Mathematics',
  'BASIC MATHS, SETS & RELATION(BASIC TRIGONOMETRY, INEQUALITIES, MODULUS, LOGARITHM, FUNCTIONS & GRAPHS, GREATEST INTEGER FUNCTION, SURDS & INDICES.)': 'Mathematics',
  'TRIGONOMETRIC IDENTITIES, EQUATIONS & INEQUALITIES, PROPERTIES & SOLUTIONS OF TRIANGLES': 'Mathematics',
}

KNOWN_SUBJECTS = {'Physics', 'Chemistry', 'Mathematics'}

def inferSubject(rawTopic):
    trimmed = (rawTopic or '').strip()
    normalized = re.sub(r'\s+', ' ', rawTopic or '').strip().upper()
    
    if normalized in TOPIC_SUBJECT_MAP:
        return TOPIC_SUBJECT_MAP[normalized], trimmed

    normNoEllipsis = re.sub(r'[\.…]+$', '', normalized).strip()
    for knownTopic, knownSubject in TOPIC_SUBJECT_MAP.items():
        if knownTopic.startswith(normNoEllipsis) or normNoEllipsis.startswith(knownTopic):
            return knownSubject, trimmed
            
    return None, trimmed

def test(raw):
    subject, topic = inferSubject(raw)
    if not subject or subject not in KNOWN_SUBJECTS:
        print(f'ERROR: Question Q: topic "{topic}" does not map to a known subject')
    else:
        print(f'SUCCESS: "{topic}" -> {subject}')

test("Definite Integration")
test("Basic Maths, Sets & Relation(Basic trigonometry, Inequalities, Modulus, Logarithm, Functions & graphs, Greatest integer Function, Surds & Indices.)")
test("Trigonometric Identities, Equations & Inequalities, Properties & Solutions of Triangles")
