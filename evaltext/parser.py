import re

def parse_llm_result(text: str, expected: str):
    """Parse the result of the LLM task."""
    print(text)

    # replace this format {var#format} to regex
    re.sub(r'{(\w+)#(\w+)}', r'(?P<\1>\w+)', expected)


    return text

def _replace_format_to_regex(text: str) -> str:
    """Replace the format {var#format} to regex."""
    index = 0
    pattern = r'{(?P<var>\w+)#(?P<format>\w+)}'
    pattern_everywhere = f'.*{pattern}.*'
    all = re.findall(pattern, text)
    replacements = []
    for var in range(len(all)):
        m = re.match(pattern_everywhere, text)
        replacements.append({'var': m['var'], 'format': m['format']})
        text = re.sub(pattern, f'___REPLACEMENT_IDX_{index}___', text, 1)
        index += 1
        # text = re.sub(pattern, r'(?P<\1>.+)', text, 1)
    text = re.escape(text)
    for i, m in enumerate(replacements):
        var = m['var']
        fmt = m['format']
        formatRegex = ''
        if fmt == 'line':
            formatRegex = r'.+'
        text = text.replace(f'___REPLACEMENT_IDX_{i}___', f'(?P<{m["var"]}>{formatRegex})')
    return text

def test_replace_format_to_regex():
    """Test the replace_format_to_regex function."""
    text = "{name#line} eats {food#line}"
    expected = "{?P<name>.+} eats {?P<food>.+}"
    assert _replace_format_to_regex(text) == expected

def test_parse_llm_result():
    """Test the parse_llm_result function."""
    text = "John eats apple"
    expected = "{name#line} eats {food#line}"
    regex = _replace_format_to_regex(expected)
    result = re.compile(regex).match("John eats apple")
    assert result['name'] == 'John'
    assert result['food'] == 'apple'