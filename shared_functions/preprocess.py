def read_file(filename, test=False):
    """
    read file
    return format :
    [ ['EU', 'B-ORG'], ['rejects', 'O'], ['German', 'B-MISC'], ['call', 'O'], ['to', 'O'], ['boycott', 'O'], ['British', 'B-MISC'], ['lamb', 'O'], ['.', 'O'] ]
    """

    f = open(filename, encoding="utf8")
    sentences = []
    sentence = []
    for line in f:
        if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == "\n":
            if len(sentence) > 0:
                sentences.append(sentence)
                sentence = []
            continue
        splits = line.split(' ')
        true_label = splits[-1].replace('\n', '')
        if test:
            pred_label = splits[1].replace('\n', '')
            sentence.append([splits[0], pred_label, true_label])
        else:
            sentence.append([splits[0], true_label])

    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences
