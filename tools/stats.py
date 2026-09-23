#!/usr/bin/env python3
# ============================================================
#  CARTE « HIGH SCORES » — même style pixel que tools/gen.py
#  Lancée par le workflow (.github/workflows/snake.yml) toutes les 12 h, publiée sur la
#  branche `output` à côté du serpent. En local :
#      GITHUB_TOKEN=<jeton> python tools/stats.py dist
# ============================================================
import datetime, json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import THEMES, TEXT, TITLE, KICK, anim, cells_d, kicker, n, segments, svg, text

LOGIN = os.environ.get("GITHUB_REPOSITORY_OWNER", "PierrisKevin")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

Q_PROFILE = """
query($login: String!, $after: String) {
  user(login: $login) {
    followers { totalCount }
    pullRequests(first: 1) { totalCount }
    issues(first: 1) { totalCount }
    repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY]) { totalCount }
    contributionsCollection { contributionYears totalCommitContributions }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
  }
}"""

Q_YEAR = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def graphql(query, **variables):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": f"{LOGIN}-profile-stats"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(f"GitHub GraphQL : {payload['errors']}")
    return payload["data"]["user"]


def fetch():
    user = graphql(Q_PROFILE, login=LOGIN)
    repos = user["repositories"]["nodes"]
    page = user["repositories"]["pageInfo"]
    while page["hasNextPage"]:
        more = graphql(Q_PROFILE, login=LOGIN, after=page["endCursor"])["repositories"]
        repos += more["nodes"]
        page = more["pageInfo"]

    languages = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            languages[edge["node"]["name"]] = languages.get(edge["node"]["name"], 0) + edge["size"]

    days, total = {}, 0
    for year in user["contributionsCollection"]["contributionYears"]:
        calendar = graphql(Q_YEAR, login=LOGIN, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        calendar = calendar["contributionsCollection"]["contributionCalendar"]
        total += calendar["totalContributions"]
        for week in calendar["weeks"]:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]

    current, longest = streaks(days)
    return {
        "total": total, "current": current, "longest": longest,
        "stars": sum(repo["stargazerCount"] for repo in repos),
        "commits": user["contributionsCollection"]["totalCommitContributions"],
        "prs": user["pullRequests"]["totalCount"], "issues": user["issues"]["totalCount"],
        "contributed": user["repositoriesContributedTo"]["totalCount"],
        "repos": user["repositories"]["totalCount"], "followers": user["followers"]["totalCount"],
        "languages": sorted(languages.items(), key=lambda item: -item[1])[:5],
    }


def streaks(days):
    """Série en cours (un jour sans contribution aujourd'hui ne la casse pas encore) et plus longue série."""
    today = datetime.date.today().isoformat()
    dates = sorted(d for d in days if d <= today)
    longest = run = 0
    for d in dates:
        run = run + 1 if days[d] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(dates)):
        if days[d]:
            current += 1
        elif i:          # aujourd'hui peut encore être à zéro
            break
    return current, longest


# ---------------- RENDU ----------------
FLAME = ["..#..", ".##..", ".###.", "####.", "#####", "##.##", ".###."]


def number(value):
    return f"{value:,}".replace(",", " ")


def card(T, s):
    W, P = 900, 12
    fg, mfg, border, accent = T["fg"], T["mfg"], T["border"], T["accent"]
    b = []
    # compteurs : filets haut / bas et séparateurs verticaux, comme la carte profil
    counters = [(number(s["total"]), "CONTRIBUTIONS"), (str(s["current"]), "CURRENT STREAK"),
                (str(s["longest"]), "LONGEST STREAK"), (number(s["stars"]), "STARS")]
    gy, gh, gw = 1, 108, (W - 2 * P) / len(counters)
    b.append(f'<rect x="{P}" y="{gy}" width="{W - 2 * P}" height="1" fill="{border}"/>'
             f'<rect x="{P}" y="{gy + gh}" width="{W - 2 * P}" height="1" fill="{border}"/>')
    for i, (value, label) in enumerate(counters):
        x = P + i * gw + (22 if i else 0)
        if i:
            b.append(f'<rect x="{n(P + i * gw)}" y="{gy + 16}" width="1" height="{gh - 32}" fill="{border}"/>')
        b.append(text(TITLE, value, x, gy + 60, 46, fg, extra=anim("fin", .6, .2 + i * .08, "ease-out both")))
        if i == 1:   # petite flamme pixel qui vacille à côté de la série en cours
            fx = x + TITLE.width(value, 46) + 12
            cells = [(c, r) for r, row in enumerate(FLAME) for c, v in enumerate(row) if v == "#"]
            b.append(f'<path d="{cells_d(cells, 3.2, .3, fx, gy + 25)}" fill="{accent}" shape-rendering="crispEdges" '
                     f'style="animation:beat .5s steps(1) infinite"/>')
        b.append(kicker(label, x + 1, gy + 88, mfg))
    # colonne gauche : détails avec points de conduite
    col = (W - 2 * P - 64) / 2
    y0 = gy + gh + 46
    details = [("COMMITS (1 YEAR)", s["commits"]), ("PULL REQUESTS", s["prs"]), ("ISSUES", s["issues"]),
               ("CONTRIBUTED TO", s["contributed"]), ("PUBLIC REPOS", s["repos"]), ("FOLLOWERS", s["followers"])]
    for i, (label, value) in enumerate(details):
        y = y0 + i * 30
        value = number(value)
        start = P + TEXT.width(label, KICK, .1) + 10
        end = P + col - TEXT.width(value, KICK, .1) - 10
        dots = "".join(f"M{n(x)} {y - 3}h2v2h-2z" for x in range(int(start), int(end), 6))
        b.append(kicker(label, P, y, mfg) + f'<path d="{dots}" fill="{fg}" fill-opacity=".25"/>' + kicker(value, P + col, y, fg, 1, "end"))
    # colonne droite : langages en barres segmentées
    x0 = P + col + 64
    b.append(kicker("TOP LANGUAGES", x0, y0, mfg))
    total = sum(size for _, size in s["languages"]) or 1
    for i, (name, size) in enumerate(s["languages"]):
        y = y0 + 32 + i * 30
        share = size / total
        b.append(kicker(name.upper(), x0, y, fg) + kicker(f"{share * 100:.1f}%", x0 + col, y, mfg, 1, "end"))
        b.append(segments(x0, y + 8, col, 5, 32, share, fg, accent, start=.5 + i * .12, head=False))
    H = y0 + max(len(details) - 1, len(s["languages"]) + .4) * 30 + 44
    b.append(kicker(f"UPDATED {datetime.date.today().isoformat()} · ALL-TIME", W - P, H - 6, mfg, 1, "end", 12))
    label = (f"GitHub stats: {s['total']} contributions, current streak {s['current']} days, longest streak "
             f"{s['longest']} days, {s['stars']} stars")
    return svg(W, int(H), "".join(b), label)


def main():
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN manquant")
    out = sys.argv[1] if len(sys.argv) > 1 else "dist"
    os.makedirs(out, exist_ok=True)
    stats = fetch()
    for theme, T in THEMES.items():
        with open(os.path.join(out, f"stats-{theme}.svg"), "w", encoding="utf-8") as fh:
            fh.write(card(T, stats))
    print("stats:", {k: v for k, v in stats.items() if k != "languages"}, [name for name, _ in stats["languages"]])


if __name__ == "__main__":
    main()
