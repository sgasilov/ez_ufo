def enquote(string, escape=False):
    addition = '\\"' if escape else '"'

    return addition + string + addition
