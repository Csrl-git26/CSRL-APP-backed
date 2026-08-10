import re

TOPIC_SUBJECT_MAP = {
  'BASIC MATHS, SETS & RELATION(BASIC TRIGONOMETRY, INEQUALITIES, MODULUS, LOGARITHM, FUNCTIONS & GRAPHS, GREATEST INTEGER FUNCTION, SURDS & INDICES.)': 'Mathematics'
}

def infer_subject(raw_topic):
  # Keep only alphanumeric chars
  norm_topic = re.sub(r'[^a-zA-Z0-9]', '', raw_topic or '').upper()
  
  for known_topic, subj in TOPIC_SUBJECT_MAP.items():
    norm_known = re.sub(r'[^a-zA-Z0-9]', '', known_topic).upper()
    if norm_known.startswith(norm_topic):
      return {'subject': subj, 'topic': raw_topic.strip()}
      
  return None

print(infer_subject("Basic Maths, Sets & Relation..."))
print(infer_subject("Basic Maths, Sets & Relation ..."))
print(infer_subject("Basic Maths, Sets & Relation(Basic Trigonometry"))
print(infer_subject("Basic Maths, Sets & Relation (Basic Trigonometry..."))
