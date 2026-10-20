def huffman_codes(probs):
    if len(probs) == 1:
        return {s: "0" for s in probs}
    groups = [(p, {s: ""}) for s, p in probs.items()]
    while len(groups) > 1:
        groups.sort(key=lambda g: g[0])
        p1, codes1 = groups.pop(0)
        p2, codes2 = groups.pop(0)
        merged = {s: "0" + c for s, c in codes1.items()}
        merged.update({s: "1" + c for s, c in codes2.items()})
        groups.append((p1 + p2, merged))
    return groups[0][1]