from pathlib import Path

path = Path('site/index.html')
text = path.read_text(encoding='utf-8')
marker = 'seriesContextTitle'
if marker in text:
    print('Navigation context refinement already implemented')
    raise SystemExit(0)

header_old = '  <div id="teamContextTitle" class="team-context-title" aria-hidden="true"></div>\n  <div class="navlinks">'
header_new = '  <div id="teamContextTitle" class="team-context-title" aria-hidden="true"></div>\n  <div id="seriesContextTitle" class="series-context-title" aria-hidden="true"><span id="seriesContextA" class="series-context-badge"></span><span id="seriesContextB" class="series-context-badge"></span></div>\n  <div class="navlinks">'
if text.count(header_old) != 1:
    raise SystemExit(f'Expected header anchor once, found {text.count(header_old)}')
text = text.replace(header_old, header_new, 1)

css = r'''
/* Route-aware sticky navigation refinement. */
.series-context-title{grid-area:title;justify-self:center;max-width:100%;min-width:0;display:flex;align-items:center;justify-content:center;gap:5px;opacity:0;visibility:hidden;pointer-events:none;transform:translateY(-4px);transition:opacity .16s ease,transform .16s ease,visibility 0s linear .16s}.series-context-title.visible{opacity:1;visibility:visible;transform:translateY(0);transition-delay:0s}.series-context-badge{min-width:0;max-width:100%;border-radius:7px;padding:6px 9px;background:var(--series-context-bg,#fff);color:var(--series-context-fg,var(--nav));font-family:Graduate,"Rockwell Extra Bold",Rockwell,"Arial Black",serif;font-size:17px;line-height:1.05;letter-spacing:.02em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-shadow:inset 0 0 0 1px rgba(15,23,42,.18),0 2px 7px rgba(0,0,0,.2)}
body.nav-home .topbar-inner{display:flex;align-items:center;gap:16px}body.nav-home .brand{grid-area:auto;width:auto;white-space:nowrap;text-align:left;line-height:normal}body.nav-home .navlinks{grid-area:auto;display:flex;flex-direction:row;align-items:center;margin-left:0;margin-right:0}body.nav-home .searchbox{grid-area:auto;margin-left:auto;width:min(350px,36vw)}body.nav-home .team-context-title,body.nav-home .series-context-title{display:none}
@media(max-width:950px){body.nav-home .topbar-inner{display:flex}body.nav-home .searchbox{display:none}body.nav-home .navlinks{margin-left:auto;flex-direction:row;align-items:center}body.nav-team .topbar-inner,body.nav-series .topbar-inner{grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:"brand title nav"}}
@media(max-width:720px){body.nav-home .topbar-inner{padding:9px 10px;gap:5px}body.nav-home .brand{width:auto;white-space:nowrap;text-align:left;font-size:16px;line-height:normal;letter-spacing:.035em}body.nav-home .navlinks{gap:0;margin-left:auto;margin-right:0;flex-direction:row;align-items:center}body.nav-home .navlinks button{min-height:44px;padding:8px 7px;font-size:12px;line-height:normal}body.nav-team .brand,body.nav-series .brand{width:72px;text-align:center;white-space:normal;line-height:.95}body.nav-team .navlinks,body.nav-series .navlinks{margin-right:8px;align-items:flex-end}body.nav-team .team-context-title{max-width:100%}body.nav-series .team-context-title{display:none}.series-context-title{gap:4px}.series-context-badge{padding:5px 6px;border-radius:6px;font-size:13px;letter-spacing:.01em}}
@media(max-width:360px){body.nav-home .brand{font-size:14px}body.nav-home .navlinks button{font-size:11px;padding:7px 5px}body.nav-team .brand,body.nav-series .brand{width:66px}.series-context-badge{padding:4px 5px}}
'''
if text.count('</style>') != 1:
    raise SystemExit('Expected one style close')
text = text.replace('</style>', css + '\n</style>', 1)

start = text.find('function syncTeamContextTitle() {')
end = text.find('\nlet teamContextSyncPending = false;', start)
if start < 0 or end < 0:
    raise SystemExit('Could not locate syncTeamContextTitle block')
replacement = r'''function hideSeriesContextTitle() {
  const container = document.getElementById("seriesContextTitle");
  if (!container) return;
  container.classList.remove("visible");
  container.setAttribute("aria-hidden", "true");
  const a = document.getElementById("seriesContextA");
  const b = document.getElementById("seriesContextB");
  if (a) a.textContent = "";
  if (b) b.textContent = "";
}

function applyContextBadgeColors(element, key, profile) {
  if (!element || !profile) return;
  const colors = opponentColorPresentation(key);
  const background = colors?.background || profile.primary || "#FFFFFF";
  const foreground = colors?.foreground || textColor(background);
  element.style.setProperty("--series-context-bg", background);
  element.style.setProperty("--series-context-fg", foreground);
}

function fitSeriesContextTitle() {
  const container = document.getElementById("seriesContextTitle");
  const badges = [document.getElementById("seriesContextA"), document.getElementById("seriesContextB")].filter(Boolean);
  if (!container || badges.length !== 2 || !badges.every((badge) => badge.textContent)) return;
  let size = window.innerWidth <= 720 ? 13 : 17;
  const preferredMin = window.innerWidth <= 720 ? 9 : 11;
  const absoluteMin = 8;
  badges.forEach((badge) => {
    badge.style.fontSize = size + "px";
    badge.style.letterSpacing = window.innerWidth <= 720 ? ".01em" : ".02em";
  });
  while (container.scrollWidth > container.clientWidth + 1 && size > preferredMin) {
    size -= 1;
    badges.forEach((badge) => { badge.style.fontSize = size + "px"; });
  }
  if (container.scrollWidth > container.clientWidth + 1) {
    badges.forEach((badge) => { badge.style.letterSpacing = "0"; });
    while (container.scrollWidth > container.clientWidth + 1 && size > absoluteMin) {
      size -= 1;
      badges.forEach((badge) => { badge.style.fontSize = size + "px"; });
    }
  }
}

function syncTeamContextTitle() {
  const title = document.getElementById("teamContextTitle");
  const seriesTitle = document.getElementById("seriesContextTitle");
  if (!title || !seriesTitle) return;
  const route = (location.hash || "#home").slice(1).split("/");
  const isTeam = route[0] === "team" && ACTIVE.has(route[1]);
  const isSeries = route[0] === "matchup" && ACTIVE.has(route[1]) && seriesGamesFor(route[1], route[2]).length;
  document.body.classList.toggle("nav-team", Boolean(isTeam));
  document.body.classList.toggle("nav-series", Boolean(isSeries));
  document.body.classList.toggle("nav-home", !isTeam && !isSeries);

  if (isTeam) {
    hideSeriesContextTitle();
    const teamKey = route[1];
    const team = DB.teams[teamKey];
    const heading = document.getElementById("teamPageTitle");
    const topbar = document.querySelector(".topbar");
    if (!team || !heading || !topbar) {
      hideTeamContextTitle();
      return;
    }
    const colors = opponentColorPresentation(teamKey);
    const background = colors?.background || team.primary || "#FFFFFF";
    const foreground = colors?.foreground || textColor(background);
    title.textContent = team.name;
    title.style.setProperty("--team-context-bg", background);
    title.style.setProperty("--team-context-fg", foreground);
    fitTeamContextTitle();
    const show = heading.getBoundingClientRect().bottom <= topbar.getBoundingClientRect().bottom;
    title.classList.toggle("visible", show);
    title.setAttribute("aria-hidden", show ? "false" : "true");
    return;
  }

  hideTeamContextTitle();
  if (isSeries) {
    const teamAKey = route[1];
    const teamBKey = route[2];
    const teamA = DB.teams[teamAKey];
    const teamB = opponentProfile(teamAKey, teamBKey);
    const heading = document.querySelector(".match-head");
    const topbar = document.querySelector(".topbar");
    const badgeA = document.getElementById("seriesContextA");
    const badgeB = document.getElementById("seriesContextB");
    if (!teamA || !teamB || !heading || !topbar || !badgeA || !badgeB) {
      hideSeriesContextTitle();
      return;
    }
    badgeA.textContent = teamA.name;
    badgeB.textContent = teamB.name;
    applyContextBadgeColors(badgeA, teamAKey, teamA);
    applyContextBadgeColors(badgeB, teamBKey, teamB);
    fitSeriesContextTitle();
    const show = heading.getBoundingClientRect().bottom <= topbar.getBoundingClientRect().bottom;
    seriesTitle.classList.toggle("visible", show);
    seriesTitle.setAttribute("aria-hidden", show ? "false" : "true");
    return;
  }

  hideSeriesContextTitle();
}'''
text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')
print('Navigation context refinement applied')
