def check_brackets(text):
    stack = []
    lines = text.split('\n')
    for line_num, line in enumerate(lines, 1):
        for char_num, char in enumerate(line, 1):
            if char in '({[':
                stack.append((char, line_num, char_num))
            elif char in ')}]':
                if not stack:
                    return f"Unmatched {char} at line {line_num} column {char_num}"
                top, l, c = stack.pop()
                if (top == '(' and char != ')') or \
                   (top == '{' and char != '}') or \
                   (top == '[' and char != ']'):
                    return f"Mismatched {char} at line {line_num} column {char_num} (expected match for {top} from line {l})"
    if stack:
        top, l, c = stack.pop()
        return f"Unclosed {top} from line {l} column {c}"
    return "All brackets balanced!"

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx', 'r') as f:
    # Need to remove JSX tags to accurately check JS brackets? Actually JSX uses {} too.
    # It's better to just write a simple check or rely on the fact that Vercel is building it.
    pass
