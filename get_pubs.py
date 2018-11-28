import json
import ads


def get_all_papers(author):
    papers = ads.SearchQuery(author=author,
                             sort="date",
                             max_pages=128,
                             fl=["id", "title", "author", "doi", "year",
                                 "pubdate", "pub", "volume", "page",
                                 "identifier", "doctype", "citation_count",
                                 "bibcode"])

    all_dicts = []
    for paper in papers:
        # Get arxiv ID
        aid = [":".join(t.split(":")[1:]) for t in paper.identifier
               if t.startswith("arXiv:")]

        try:
            page = int(paper.page[0])
        except (ValueError, TypeError):
            page = None
            if paper.page is not None and paper.page[0].startswith("arXiv:"):
                aid.append(":".join(paper.page[0].split(":")[1:]))

        all_dicts.append(dict(
            doctype=paper.doctype,
            authors=paper.author,
            year=paper.year,
            pubdate=paper.pubdate,
            doi=paper.doi[0] if paper.doi is not None else None,
            title=paper.title[0],
            pub=paper.pub,
            volume=paper.volume,
            page=page,
            arxiv=aid[0] if len(aid) else None,
            citations=(paper.citation_count
                       if paper.citation_count is not None else 0),
            url="http://adsabs.harvard.edu/abs/" + paper.bibcode,
        ))

    return sorted(all_dicts, key=lambda x: x['pubdate'], reverse=True)


if __name__ == '__main__':
    papers = get_all_papers("price-whelan, a")

    with open("pubs.json", "w") as f:
        json.dump(papers, f, sort_keys=True,
                  indent=4, separators=(",", ": "))
