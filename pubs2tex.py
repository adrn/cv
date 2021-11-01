from datetime import date
import json
import re
from utf8totex import utf8totex

# To appear in CV as highlighted papers:
SELECTED_PAPERS = [
    '10.3847/1538-4357/abe1b7',   # Orbital Torus Imaging
    '10.3847/1538-4357/ab8acc',   # DR16 APOGEE binaries
    '10.3847/1538-4357/ab4bdd',   # PW1
    '10.3847/1538-4357/ab4bdd',   # Pal 5 RRL
    '10.3847/2041-8213/aad7b5',   # GD-1 DR2
    '10.3847/1538-3881/aac387',   # DR14 APOGEE binaries
    '10.21105/joss.00388',        # Gala
    '10.3847/1538-4357/aa5e50',   # The Joker
    '10.1093/mnras/stv2383',      # Chaos+Streams
    '10.1093/mnras/stv1324',      # TriAnd
    '10.1088/0004-637X/794/1/4',  # Rewinder
    '10.3847/1538-4357/aaab4d',   # Kronos & Krios
    '10.3847/1538-3881/aa6ffd',   # Comoving Pairs
    '10.3847/1538-4357/ac0b44',   # Nico LMC impact
    '10.3847/1538-3881/abbd3a',   # Nora Pal 13
    '10.3847/1538-4357/ab2873',   # Ana spur
]

_JOURNAL_MAP = {
    "ArXiv e-prints": "ArXiv",
    "The Astronomical Journal": "\\aj",
    "The Astrophysical Journal": "\\apj",
    "The Astrophysical Journal Supplement Series": "\\apjs",
    "Astronomy and Astrophysics": "\\aanda",
    "Galaxies": "MDPI: galaxies",
    "The Journal of Open Source Software": "JOSS",
    "Monthly Notices of the Royal Astronomical Society": "\\mnras",
    "Nature": "\\nature",
    "Nature Astronomy": "\\natureast",
    "Publications of the Astronomical Society of the Pacific": "\\pasp",
    "Publications of the Astronomical Society of Japan": "\\pasj",
}

JOURNAL_SKIP = [
    "VizieR Online Data Catalog",
    "^American Astronomical Society.*",
    "^AAS.*",
    "Astrophysics Source Code Library",
    "Zenodo Software Release",
    "Ph.D. Thesis",
    "Spitzer Proposal",
    "Rediscovering Our Galaxy",
    "The Astronomer's Telegram",
]
JOURNAL_SKIP = [x.lower() for x in JOURNAL_SKIP]

# Lower case journals:
JOURNAL_MAP = {}
for k, v in _JOURNAL_MAP.items():
    JOURNAL_MAP[k.lower()] = v


def format_name(name):
    try:
        last, others = name.split(', ')
        others = ['{0}.'.format(o[0]) for o in others.split()]
        name = "{last}, {first}".format(first=' '.join(others), last=last)

    except ValueError:
        print("couldn't format name '{0}'".format(name))

    return name


def parse_authors(paper_dict, max_authors=4):
    raw_authors = [utf8totex(x) for x in paper_dict['authors']]

    show_authors = raw_authors[:max_authors]

    if any(['price-whelan' in x.lower() for x in show_authors]):
        # Bold my name because it makes the cut to be shown
        names = []
        for name in show_authors:
            if 'price-whelan' in name.lower():
                name = '\\textbf{Price-Whelan,~A.~M.}'
            else:
                name = format_name(name)
            names.append(name)

        author_tex = '; '.join(names)

        if len(show_authors) < len(raw_authors): # use et al.
            author_tex = author_tex + "~\\textit{et al.}"

    else:
        # Add "incl. APW" after et al., because I'm buried in the author list
        author_tex = "{0}".format(format_name(show_authors[0]))
        author_tex += "~\\textit{et al.}~(incl. \\textbf{APW})"

    return author_tex


def filter_papers(pubs):
    filtered = []

    for p in pubs:
        if p["pub"] is None:
            continue

        # Skip if the publication is in the skip list:
        if any([re.match(re.compile(pattr), p['pub'].lower())
                for pattr in JOURNAL_SKIP]):
            continue

        if p["pub"].lower() != "arxiv e-prints":
            pub = JOURNAL_MAP.get(p["pub"].strip("0123456789# ").lower(),
                                  None)

            if pub is None:
                print("Journal '{0}' not recognized for paper '{1}' - "
                      " skipping...".format(p['pub'], p['title']))
                continue

        # HACK: hard-coded skip
        if 'astropy problem' in p['title'].lower():
            continue

        filtered.append(p)

    return filtered


def get_ref_unref(papers):
    refereeds = []
    preprints = []

    for paper in papers:
        # Skip if the publication is in the skip list:
        if any([re.match(re.compile(pattr), paper['pub'].lower())
                for pattr in JOURNAL_SKIP]):
            continue

        if paper["pub"] not in [None, "ArXiv e-prints", "arXiv e-prints"]:
            refereeds.append(paper)
        else:
            preprints.append(paper)

    return refereeds, preprints


def get_paper_items(papers):
    refereeds = []
    preprints = []
    first_authors = []
    selected = []  # appears in CV

    for paper in papers:
        authors = parse_authors(paper)
        entry = authors

        # Skip if the publication is in the skip list:
        if any([re.match(re.compile(pattr), paper['pub'].lower())
                for pattr in JOURNAL_SKIP]):
            continue

        if paper["doi"] is not None:
            title = "\\doi{{{0}}}{{{1}}}".format(paper["doi"],
                                                 utf8totex(paper["title"]))
        else:
            title = "\\textit{{{0}}}".format(utf8totex(paper["title"]))
        entry += ", " + title

        if paper["pub"] not in [None, "ArXiv e-prints", "arXiv e-prints"]: # HACK
            pub = JOURNAL_MAP.get(paper["pub"].strip("0123456789# ").lower(),
                                  None)

            if pub is None:
                print("Journal '{0}' not recognized for paper '{1}' - "
                      " skipping...".format(paper['pub'], paper['title']))
                continue

            entry += ", " + pub
            is_preprint = False

        else:
            is_preprint = True

        if paper["volume"] is not None:
            entry += ", \\textbf{{{0}}}".format(paper["volume"])

        if paper["page"] is not None:
            entry += ", {0}".format(paper["page"])

        if paper['pubdate'] is not None:
            entry += ", {0}".format(paper['pubdate'].split('-')[0])

        if paper["arxiv"] is not None:
            entry += " (\\arxiv{{{0}}})".format(paper["arxiv"])

        if paper["citations"] > 1:
            entry += (" [\\href{{{0}}}{{{1} citations}}]"
                      .format(paper["url"], paper["citations"]))

        if is_preprint:
            preprints.append(entry)

        else:
            refereeds.append(entry)

        if "price-whelan" in paper["authors"][0].lower():
            first_authors.append(entry)

        if (paper['arxiv'] in SELECTED_PAPERS
                or paper['doi'] in SELECTED_PAPERS):
            selected.append(entry)

    # Now go through and add the \item and numbers:
    for corpus in [preprints, refereeds, first_authors, selected]:
        for i, item in enumerate(corpus):
            num = len(corpus) - i
            corpus[i] = ("\\item[{\\color{deemph}\\scriptsize" +
                         str(num) + "}]" + item)

    return refereeds, preprints, first_authors, selected


if __name__ == '__main__':
    from os import path
    if not path.exists('pubs.json'):
        raise FileNotFoundError("File 'pubs.json' not found - run get_pubs.py "
                                "before running this script.")

    with open("pubs.json", "r") as f:
        pubs = json.loads(f.read())

    papers = filter_papers(pubs)
    refs, unrefs, first, selected = get_paper_items(papers)

    # Compute citation stats
    nref = len(refs)
    nfirst = sum(1 for p in papers if "Price-Whelan" in p["authors"][0])
    cites = sorted((p["citations"] for p in papers), reverse=True)
    ncitations = sum(cites)
    hindex = sum(c >= i for i, c in enumerate(cites))

    summary = (("Refereed: {1} --- First author: {2} --- Citations: {3} --- "
               "h-index: {4}  (\\textit{{{0}}})")
               .format(date.today(), nref, nfirst, ncitations, hindex))

    print("-"*32)
    print("Summary:")
    print(summary)

    with open("summary.tex", "w") as f:
        f.write(summary)

    with open("pubs_ref.tex", "w") as f:
        f.write("\n\n".join(refs))

    with open("pubs_unref.tex", "w") as f:
        f.write("\n\n".join(unrefs))

    with open("pubs_firstauthor.tex", "w") as f:
        f.write("\n\n".join(first))

    with open("pubs_selected.tex", "w") as f:
        f.write("\n\n".join(selected))

    # # Now get highlighted papers
    # with open("highlighted.json", "r") as f:
    #     highlight = json.loads(f.read())
    # refs, unrefs, first = get_paper_items(papers)
