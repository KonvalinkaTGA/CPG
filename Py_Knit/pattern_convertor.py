


def convert_pattern(text: str) -> str:
    
    if text is None:
        return 'Nebyl zadán platný text.'

    obsah = text.replace('\r\n', '\n').replace('\r', '\n')
    if not obsah.strip():
        return 'Nebyl zadán platný text.'

    # převod bind off
    obsah = obsah.replace('bind off', 'b')

    # Text je správně
    allowed_chars = set('()0123456789kpb \t\n')
    if not all(c in allowed_chars for c in obsah):
        invalid_chars = set(obsah) - allowed_chars
        return f'Chybný formát vzoru: nepovolené znaky'

    stack = [{
        'text': [],
        'has_newline': False,
        'prefix_has_non_space': False,
    }]

    line_has_non_space = False
    i = 0
    length = len(obsah)

    while i < length:
        znak = obsah[i]
        if znak == '(':
            stack.append({
                'text': [],
                'has_newline': False,
                'prefix_has_non_space': line_has_non_space,
            })
            line_has_non_space = True
            i += 1
        elif znak == ')':
            if len(stack) == 1:
                return 'Chybný formát vzoru: neočekávaná zavírací závorka.'

            segment_context = stack.pop()
            segment = ''.join(segment_context['text'])
            if segment_context['has_newline'] and segment_context['prefix_has_non_space']:
                return 'Chybný formát vzoru: víceřádková skupina musí začínat na začátku řádku.'

            i += 1
            repeat = 0
            while i < length and obsah[i].isdigit():
                repeat = repeat * 10 + int(obsah[i])
                line_has_non_space = True
                i += 1

            if repeat == 0:
                repeat = 1

            if segment_context['has_newline'] and repeat > 1 and not segment.endswith('\n'):
                repeated = (segment + '\n') * (repeat - 1) + segment
            else:
                repeated = segment * repeat

            stack[-1]['text'].append(repeated)
            if segment_context['has_newline']:
                stack[-1]['has_newline'] = True
        elif znak == '\n':
            stack[-1]['text'].append(znak)
            stack[-1]['has_newline'] = True
            line_has_non_space = False
            i += 1
        else:
            stack[-1]['text'].append(znak)
            if znak not in (' ', '\t'):
                line_has_non_space = True
            i += 1

    if len(stack) != 1:
        return 'Chybný formát vzoru: neuzavřená otevírací závorka.'

    output = ''.join(stack[0]['text'])
    lines = output.split('\n')

    return '\n'.join(lines)

