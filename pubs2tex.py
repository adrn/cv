from datetime import date
import json
import re
from utf8totex import utf8totex

JOURNAL_MAP = {
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
        # Skip if the publication is in the skip list:
        if any([re.match(re.compile(pattr), p['pub'])
                for pattr in JOURNAL_SKIP]):
            continue

        if p["pub"] not in [None, "ArXiv e-prints"]:
            pub = JOURNAL_MAP.get(p["pub"].strip("0123456789# "),
                                  None)

            if pub is None:
                print("Journal '{0}' not recognized for paper '{1}' - "
                      " skipping...".format(p['pub'], p['title']))
                continue

        # HACK: hard-coded
        if 'astropy problem' in p['title'].lower():
            continue

        filtered.append(p)

    return filtered


def get_paper_items(papers):
    refereeds = []
    preprints = []

    for paper in papers:
        authors = parse_authors(paper)
        entry = authors

        # Skip if the publication is in the skip list:
        if any([re.match(re.compile(pattr), paper['pub'])
                for pattr in JOURNAL_SKIP]):
            continue

        if paper["doi"] is not None:
            title = "\\doi{{{0}}}{{{1}}}".format(paper["doi"],
                                                 utf8totex(paper["title"]))
        else:
            title = "\\textit{{{0}}}".format(utf8totex(paper["title"]))
        entry += ", " + title

        if paper["pub"] not in [None, "ArXiv e-prints"]:
            pub = JOURNAL_MAP.get(paper["pub"].strip("0123456789# "), None)

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

    # Now go through and add the \item and numbers:
    for corpus in [preprints, refereeds]:
        for i, item in enumerate(corpus):
            num = len(corpus) - i
            corpus[i] = ("\\item[{\\color{deemph}\\scriptsize" +
                         str(num) + "}]" + item)

    return refereeds, preprints


if __name__ == '__main__':
    from os import path
    if not path.exists('pubs.json'):
        raise FileNotFoundError("File 'pubs.json' not found - run get_pubs.py "
                                "before running this script.")

    with open("pubs.json", "r") as f:
        pubs = json.loads(f.read())

    papers = filter_papers(pubs)
    refs, unrefs = get_paper_items(papers)

    # Compute citation stats
    nref = len(refs)
    nfirst = sum(1 for p in papers if "Price-Whelan" in p["authors"][0])
    cites = sorted((p["citations"] for p in papers), reverse=True)
    ncitations = sum(cites)
    hindex = sum(c >= i for i, c in enumerate(cites))

    summary = (("refereed: {1} --- first author: {2} --- citations: {3} --- "
               "h-index: {4} (\\textit{{{0}}})")
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
