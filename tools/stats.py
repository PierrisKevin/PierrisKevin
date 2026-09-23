#!/usr/bin/env python3
# ============================================================
#  CARTE « HIGH SCORES » — même style pixel que tools/gen.py
#  Lancée par le workflow (.github/workflows/snake.yml) toutes les 12 h, publiée sur la
#  branche `output` à côté du serpent. En local :
#      GITHUB_TOKEN=<jeton> python tools/stats.py dist
# ============================================================
import datetime, json, os, sys, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import THEME, TEXT, TITLE, KICK, anim, cells_d, kicker, n, segments, svg, text

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


def warn(message):
    """Annotation GitHub Actions : visible dans l'onglet Actions et via l'API publique des check runs."""
    print(f"::warning title=stats::{message}", flush=True)


def request(url, body=None):
    headers = {"Authorization": f"bearer {TOKEN}", "User-Agent": f"{LOGIN}-profile-stats", "Accept": "application/vnd.github+json"}
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"{url} -> HTTP {error.code} {error.read()[:300]!r}") from None


def graphql(query, **variables):
    """Renvoie l'utilisateur, éventuellement partiel : un champ refusé par le jeton vaut None au lieu de tout casser."""
    try:
        payload = request("https://api.github.com/graphql", {"query": query, "variables": variables})
    except RuntimeError as error:
        warn(f"GraphQL : {error}")
        return {}
    for error in payload.get("errors") or []:
        warn(f"GraphQL : {error.get('message')}")
    return (payload.get("data") or {}).get("user") or {}


def dig(data, *keys):
    for key in keys:
        if not isinstance(data, dict) or data.get(key) is None:
            return None
        data = data[key]
    return data


def rest_repos():
    repos, page = [], 1
    while True:
        batch = request(f"https://api.github.com/users/{LOGIN}/repos?type=owner&per_page=100&page={page}")
        repos += [repo for repo in batch if not repo["fork"]]
        if len(batch) < 100:
            return repos
        page += 1


def search_count(kind):
    try:
        return request(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:{kind}&per_page=1")["total_count"]
    except RuntimeError as error:
        warn(str(error))
        return None


def fetch():
    user = graphql(Q_PROFILE, login=LOGIN)
    profile = request(f"https://api.github.com/users/{LOGIN}")

    languages, stars = {}, 0
    if dig(user, "repositories", "nodes") is not None:
        repos, page = user["repositories"]["nodes"], user["repositories"]["pageInfo"]
        while page["hasNextPage"]:
            more = dig(graphql(Q_PROFILE, login=LOGIN, after=page["endCursor"]), "repositories") or {"nodes": [], "pageInfo": {"hasNextPage": False}}
            repos += more["nodes"]
            page = more["pageInfo"]
        repo_count = user["repositories"]["totalCount"]
        for repo in repos:
            stars += repo["stargazerCount"]
            for edge in repo["languages"]["edges"]:
                languages[edge["node"]["name"]] = languages.get(edge["node"]["name"], 0) + edge["size"]
    else:
        repos = rest_repos()
        repo_count = len(repos)
        for repo in repos:
            stars += repo["stargazers_count"]
            for name, size in request(repo["languages_url"]).items():
                languages[name] = languages.get(name, 0) + size

    first_year = int(profile["created_at"][:4])
    years = dig(user, "contributionsCollection", "contributionYears") or list(range(datetime.date.today().year, first_year - 1, -1))
    days, total = {}, 0
    for year in years:
        calendar = dig(graphql(Q_YEAR, login=LOGIN, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"}),
                       "contributionsCollection", "contributionCalendar")
        if not calendar:
            total = None
            break
        total += calendar["totalContributions"]
        for week in calendar["weeks"]:
            for day in week["contributionDays"]:
                days[day["date"]] = day["contributionCount"]
    current, longest = streaks(days) if total is not None else (None, None)

    pick = lambda value, fallback: value if value is not None else fallback()
    return {
        "total": total, "current": current, "longest": longest, "stars": stars,
        "commits": dig(user, "contributionsCollection", "totalCommitContributions"),
        "prs": pick(dig(user, "pullRequests", "totalCount"), lambda: search_count("pr")),
        "issues": pick(dig(user, "issues", "totalCount"), lambda: search_count("issue")),
        "contributed": dig(user, "repositoriesContributedTo", "totalCount"),
        "repos": repo_count, "followers": pick(dig(user, "followers", "totalCount"), lambda: profile["followers"]),
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
    return "—" if value is None else f"{value:,}".replace(",", " ")


def card(T, s):
    W, P = 900, 12
    fg, mfg, border, accent = T["fg"], T["mfg"], T["border"], T["accent"]
    b = []
    # compteurs : filets haut / bas et séparateurs verticaux, comme la carte profil
    counters = [(number(s["total"]), "CONTRIBUTIONS"), (number(s["current"]), "CURRENT STREAK"),
                (number(s["longest"]), "LONGEST STREAK"), (number(s["stars"]), "STARS")]
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
    try:
        stats = fetch()
    except Exception as error:   # l'erreur apparaît en annotation dans l'onglet Actions
        print(f"::error title=stats::{type(error).__name__}: {error}", flush=True)
        raise
    with open(os.path.join(out, "stats.svg"), "w", encoding="utf-8") as fh:
        fh.write(card(THEME, stats))
    print("stats:", {k: v for k, v in stats.items() if k != "languages"}, [name for name, _ in stats["languages"]])


if __name__ == "__main__":
    main()
