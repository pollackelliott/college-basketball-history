from pathlib import Path
import re

PATH = Path("site/index.html")
text = PATH.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    text = text.replace(old, new, 1)


def replace_regex(pattern: str, replacement: str, label: str, flags=re.S) -> None:
    global text
    text2, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 regex match, found {count}")
    text = text2


# Sticky behavior: avoid creating a horizontal overflow scroll container on html/body,
# and compute mobile sticky offsets from the actual top bar height.
replace_once(
    'html,body{max-width:100%;overflow-x:hidden}body.search-open{overflow:hidden}',
    'html,body{max-width:100%;overflow-x:clip}body.search-open{overflow:hidden}',
    'overflow/sticky base',
)
replace_once(
    '.mobile-history-season{position:sticky;top:66px;z-index:11;background:#16324a;color:#fff;padding:7px 12px;font-family:Graduate,"Arial Black",serif;font-size:11px;letter-spacing:.04em;border-bottom:1px solid rgba(255,255,255,.16)}\n.mobile-history-month-group{position:relative}\n.mobile-history-month{position:sticky;top:96px;z-index:10;background:#eaf1f7;color:#526174;padding:6px 12px;font-size:11px;font-weight:800;border-bottom:1px solid var(--line)}',
    '.mobile-history-season{position:sticky;top:var(--sticky-topbar,58px);z-index:11;background:#16324a;color:#fff;padding:7px 12px;font-family:Graduate,"Arial Black",serif;font-size:11px;letter-spacing:.04em;border-bottom:1px solid rgba(255,255,255,.16)}\n.mobile-history-month-group{position:relative}\n.mobile-history-month{position:sticky;top:calc(var(--sticky-topbar,58px) + var(--sticky-season-height,30px));z-index:10;background:#eaf1f7;color:#526174;padding:6px 12px;font-size:11px;font-weight:800;border-bottom:1px solid var(--line)}',
    'mobile sticky offsets',
)

# Additional presentation styles for desktop grouping, school-color links, controls, and series cards.
css = r'''
.filter-field.searchable-field{min-width:190px;flex:1 1 210px}
.filter-field.searchable-field input{width:100%}
.school-color-link{display:inline-block;border:0;border-radius:5px;padding:3px 6px;background:var(--opp-bg)!important;color:var(--opp-fg)!important;font-weight:800;text-decoration:underline;text-decoration-color:currentColor;text-decoration-thickness:1px;text-underline-offset:2px;box-shadow:inset 0 0 0 1px rgba(15,23,42,.15);cursor:pointer}
.school-color-link:hover{filter:brightness(.94)}
.desktop-history-group th{position:static!important;left:auto!important;text-align:left;border-bottom:1px solid var(--line)}
.desktop-history-season-row th{background:#16324a;color:#fff;padding:8px 12px;font-family:Graduate,"Arial Black",serif;font-size:12px;letter-spacing:.035em}
.desktop-history-month-row th{background:#eaf1f7;color:#526174;padding:7px 12px;font-size:11px;font-weight:800}
.opponent-breakdown-controls{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;padding:11px 14px;border-bottom:1px solid var(--line);background:#f8fafc}
.opponent-breakdown-control{display:flex;align-items:center;gap:7px;color:#526174;font-size:11px;font-weight:800}
.opponent-breakdown-control select{min-height:36px;border:1px solid var(--line);border-radius:6px;background:#fff;padding:6px 8px;color:var(--ink)}
.opponent-breakdown-control input[type="checkbox"]{width:17px;height:17px;accent-color:var(--nav)}
.ungrouped-opponent-table{width:100%}
.metric small{display:block;color:#7b8797;font-size:10px;line-height:1.3;font-weight:600;margin-top:2px}
.match-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}
.series-history-summary{text-align:center;padding:9px 12px;background:#f7fafc;border-bottom:1px solid var(--line);font-size:12px;color:#526174}
@media(max-width:720px){.opponent-breakdown-controls{align-items:stretch;justify-content:flex-start}.opponent-breakdown-control{justify-content:space-between;width:100%}.opponent-breakdown-control select{min-width:150px}.filter-field.searchable-field{min-width:0;width:100%;max-width:none}.school-color-link{padding:3px 7px}.match-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
'''.strip()
replace_once(
    'footer{max-width:1280px;margin:0 auto;padding:0 22px 35px;color:#7b8a9a;font-size:11px;text-align:center}\n@media(max-width:1080px)',
    'footer{max-width:1280px;margin:0 auto;padding:0 22px 35px;color:#7b8a9a;font-size:11px;text-align:center}\n' + css + '\n@media(max-width:1080px)',
    'insert enhancement css',
)

# Remove About completely and remove the home-page official-colors tagline.
replace_once(
    '<div class="navlinks"><button type="button" onclick="goHome()">Teams</button><button type="button" onclick="showAbout()">About</button><button type="button" class="mobile-search-toggle" onclick="toggleMobileSearch(true)" aria-label="Search programs">Search</button></div>',
    '<div class="navlinks"><button type="button" onclick="goHome()">Teams</button><button type="button" class="mobile-search-toggle" onclick="toggleMobileSearch(true)" aria-label="Search programs">Search</button></div>',
    'remove about nav',
)
replace_regex(r'function showAbout\(\) \{.*?\n\}\n\n(?=function directoryCard)', '', 'remove showAbout')
replace_once(
    '<div class="section-head"><h2>Current D-I Directory</h2><p>Every school uses its official colors. Select any published program to explore its results.</p></div>',
    '<div class="section-head"><h2>Current D-I Directory</h2></div>',
    'remove directory tagline',
)

# State for matchup filtering.
replace_once(
    'const directoryState = { query: "", conference: "all", availability: "all" };\nlet mobileSearchReturnFocus = null;',
    'const directoryState = { query: "", conference: "all", availability: "all" };\nconst matchupPageState = {};\nlet mobileSearchReturnFocus = null;',
    'matchup state',
)

# Preserve venue identity fields in the series-game projection.
replace_once(
    '      venue: game.venue,\n      location: game.location,\n      gameType: game.gameType,',
    '      venue: game.venue,\n      venueKey: game.venueKey,\n      location: game.location,\n      siteCity: game.siteCity,\n      siteState: game.siteState,\n      gameType: game.gameType,',
    'series venue identity projection',
)

helpers = r'''
function colorRgb(hex) {
  const value = String(hex || "").replace("#", "");
  if (!/^[0-9a-fA-F]{6}$/.test(value)) return null;
  return [0, 2, 4].map((index) => parseInt(value.slice(index, index + 2), 16));
}

function relativeLuminance(hex) {
  const rgb = colorRgb(hex);
  if (!rgb) return 0;
  const linear = rgb.map((channel) => {
    const value = channel / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function contrastRatio(a, b) {
  const first = relativeLuminance(a);
  const second = relativeLuminance(b);
  const light = Math.max(first, second);
  const dark = Math.min(first, second);
  return (light + 0.05) / (dark + 0.05);
}

function opponentColorPresentation(opponentKey) {
  const program = DB.programs.find((row) => row.key === opponentKey);
  if (!program) return null;
  const background = program.primary;
  let foreground = program.secondary;
  if (contrastRatio(background, foreground) < 4.5) foreground = textColor(background);
  return { background, foreground };
}

function opponentLinkMarkup(teamKey, game, extraClass = "") {
  const colors = opponentColorPresentation(game.opponentKey);
  const classes = ["opp-link", extraClass, colors ? "school-color-link" : ""].filter(Boolean).join(" ");
  const style = colors ? ` style="--opp-bg:${esc(colors.background)};--opp-fg:${esc(colors.foreground)}"` : "";
  return `<button type="button" class="${classes}"${style} onclick="event.stopPropagation();goMatch('${teamKey}','${game.opponentKey}')" aria-label="Open complete ${esc(DB.teams[teamKey].name)} versus ${esc(game.opponent)} series">${esc(game.opponent)}</button>`;
}

function venueFilterValue(game) {
  const venue = game.venue && game.venue !== "—" ? game.venue : "Unknown / unresolved venue";
  const location = game.location || "";
  const key = game.venueKey || (venue === "Unknown / unresolved venue" ? "__unknown__" : `label:${venue}@@${location}`);
  return { key, label: `${venue}${location ? ` — ${location}` : ""}` };
}

function venueOptionsForGames(games) {
  const map = new Map();
  for (const game of games || []) {
    const item = venueFilterValue(game);
    if (!map.has(item.key)) map.set(item.key, item);
  }
  return [...map.values()].sort((a, b) => a.label.localeCompare(b.label));
}

function locationFilterValue(game) {
  const label = game.location || "Unknown location";
  return { key: game.location || "__unknown__", label };
}

function locationOptionsForGames(games) {
  const map = new Map();
  for (const game of games || []) {
    const item = locationFilterValue(game);
    if (!map.has(item.key)) map.set(item.key, item);
  }
  return [...map.values()].sort((a, b) => a.label.localeCompare(b.label));
}

function optionMatchesGame(query, game, options, valueFunction) {
  const normalized = String(query || "").trim();
  if (!normalized) return true;
  const exact = options.find((option) => option.label === normalized);
  const value = valueFunction(game);
  if (exact) return value.key === exact.key;
  return value.label.toLowerCase().includes(normalized.toLowerCase());
}

function opponentRowComparator(mode) {
  if (mode === "alpha") return (a, b) => a.name.localeCompare(b.name);
  if (mode === "wins") return (a, b) => b.wins - a.wins || b.games - a.games || a.name.localeCompare(b.name);
  return (a, b) => b.games - a.games || b.wins - a.wins || a.name.localeCompare(b.name);
}

function opponentTableRows(key, rows) {
  return rows.map((row) => {
    const name = `<button type="button" class="series-link" onclick="goMatch('${key}','${row.key}')" aria-label="Open complete series against ${esc(row.name)}">${esc(row.name)}</button>`;
    return `<tr><td>${name}</td><td>${fmtRecord(row.wins, row.losses, row.ties)}</td><td>${fmtNum(row.games)}</td><td>${fmtWinPct(row.wins, row.losses, row.ties)}</td></tr>`;
  }).join("");
}
'''.strip()
replace_once(
    'function opponentBreakdown(key) {',
    helpers + '\n\nfunction opponentBreakdown(key) {',
    'insert ui helpers',
)

opponent_breakdown = r'''function opponentBreakdown(key) {
  const ownConference = DB.teams[key]?.conference;
  const historicalConference = "Non-D1 / Historical";
  const state = teamPageState[key] || {};
  const grouped = state.breakdownGrouped !== false;
  const sortMode = state.breakdownSort || "games";
  const comparator = opponentRowComparator(sortMode);
  const allRows = [...(DB.opponents[key] || [])];

  if (!grouped) {
    const rows = allRows.sort(comparator);
    return `<div class="table-wrap"><table class="ungrouped-opponent-table"><thead><tr><th>Opponent</th><th>Record</th><th>Games</th><th>Win %</th></tr></thead><tbody>${opponentTableRows(key, rows)}</tbody></table></div>`;
  }

  const groups = new Map();
  for (const opponent of allRows) {
    if (!groups.has(opponent.conference)) groups.set(opponent.conference, []);
    groups.get(opponent.conference).push(opponent);
  }

  return [...groups.entries()]
    .map(([conference, rows]) => ({
      conference,
      rows: rows.sort(comparator),
      total: rows.reduce((sum, row) => sum + row.games, 0),
      wins: rows.reduce((sum, row) => sum + row.wins, 0),
      losses: rows.reduce((sum, row) => sum + row.losses, 0),
      ties: rows.reduce((sum, row) => sum + row.ties, 0),
    }))
    .sort((a, b) => {
      if (a.conference === ownConference && b.conference !== ownConference) return -1;
      if (b.conference === ownConference && a.conference !== ownConference) return 1;
      if (a.conference === historicalConference && b.conference !== historicalConference) return 1;
      if (b.conference === historicalConference && a.conference !== historicalConference) return -1;
      return a.conference.localeCompare(b.conference);
    })
    .map((group) => `<details class="conference-group"><summary>${esc(group.conference)}<span>${fmtNum(group.rows.length)} opponents · ${fmtNum(group.total)} games · ${fmtRecord(group.wins, group.losses, group.ties)}</span></summary><div class="table-wrap"><table><thead><tr><th>Opponent</th><th>Record</th><th>Games</th><th>Win %</th></tr></thead><tbody>${opponentTableRows(key, group.rows)}</tbody></table></div></details>`)
    .join("");
}

function updateOpponentBreakdown(key) {
  const state = teamPageState[key];
  const grouped = document.getElementById("groupByConference");
  const sort = document.getElementById("opponentSort");
  const body = document.getElementById("opponentBreakdownBody");
  if (!state || !grouped || !sort || !body) return;
  state.breakdownGrouped = grouped.checked;
  state.breakdownSort = sort.value;
  body.innerHTML = opponentBreakdown(key);
}
'''
replace_regex(r'function opponentBreakdown\(key\) \{.*?\n\}\n\n(?=function teamView\(key\))', opponent_breakdown + '\n', 'replace opponent breakdown')

team_view = r'''function teamView(key) {
  const team = DB.teams[key];
  const summary = DB.summaries[key];
  if (!team || !summary) return homeView();
  teamPageState[key] = { page: 0, q: "", selectedOpponentKeys: [], site: "all", season: "", venueQuery: "", locationQuery: "", type: "all", suggestionIndex: -1, breakdownGrouped: true, breakdownSort: "games" };
  const seasonOptions = seasonsFor(key).map((season) => `<option value="${esc(season)}">${esc(season)}</option>`).join("");
  const venueOptions = venueOptionsForGames(DB.games[key]).map((option) => `<option value="${esc(option.label)}"></option>`).join("");
  const locationOptions = locationOptionsForGames(DB.games[key]).map((option) => `<option value="${esc(option.label)}"></option>`).join("");
  return `<button type="button" class="back" onclick="goHome()">← All programs</button><section class="team-hero" style="--team:${team.primary}"><div class="team-strip"></div><div class="team-head">${teamLogo(key)}<div><h1>${esc(team.name)} ${esc(team.nickname)}</h1><div class="kicker" style="color:${team.primary}">${esc(team.conference)} • ${esc(team.location || "Location not listed")} • SINCE ${esc(formatSinceSeason(team.historyStartSeason))}</div></div></div></section><div class="metrics"><div class="metric"><b>${fmtRecord(summary.wins, summary.losses, summary.ties)}</b><span>On-Court Record</span></div><div class="metric"><b>${fmtOptionalNum(team.conferenceRegularSeasonChampionships)}</b><span>Conference Regular Season Championships</span></div><div class="metric"><b>${fmtOptionalNum(team.conferenceTournamentChampionships)}</b><span>Conference Tournament Championships</span></div><div class="metric"><b>${fmtOptionalNum(team.ncaaTournamentAppearances)}</b><span>NCAA Tournament Appearances</span></div><div class="metric"><b>${fmtOptionalNum(team.finalFourAppearances)}</b><span>Final Fours</span></div><div class="metric"><b>${fmtOptionalNum(team.nationalChampionships)}</b><span>National Championships</span></div><div class="metric${team.bestFinishKey === "NATIONAL_CHAMPION" ? " champion-finish" : ""}"><b>${esc(bestFinishLabel(team.bestFinishKey))}</b><span>Best Finish</span></div><div class="metric"><b>${fmtOptionalYear(team.bestFinishYear)}</b><span>Best Finish Year</span></div></div><div class="panel history-panel"><div class="panel-title">Complete Game History</div><button type="button" id="mobileFilterToggle" class="mobile-filter-toggle" onclick="toggleTeamFilters()" aria-controls="teamFilters" aria-expanded="false"><span>Filters</span><span id="filterToggleStatus">All games</span></button><div id="teamFilters" class="filters"><div class="filter-field"><label for="seasonFilter">Season</label><select id="seasonFilter" onchange="updateTeamGames('${key}',0,true)"><option value="">All seasons</option>${seasonOptions}</select></div><div class="filter-field opponent-field"><label for="oppFilter">Opponent</label><div class="opponent-combobox"><div class="opponent-input-wrap"><div id="opponentChips" class="filter-chips"></div><input id="oppFilter" placeholder="Type to match or select teams…" autocomplete="off" role="combobox" aria-autocomplete="list" aria-controls="oppSuggestions" aria-expanded="false" oninput="onOpponentFilterInput('${key}')" onkeydown="handleOpponentFilterKeydown(event,'${key}')"></div><div id="oppSuggestions" class="opponent-suggestions" role="listbox"></div></div></div><div class="filter-field"><label for="siteFilter">Site</label><select id="siteFilter" onchange="updateTeamGames('${key}',0,true)"><option value="all">All sites</option><option value="home">Home</option><option value="road">Road</option><option value="neutral">Neutral</option><option value="unknown">Unknown</option></select></div><div class="filter-field searchable-field"><label for="venueFilter">Venue</label><input id="venueFilter" list="venueFilterOptions" placeholder="All venues" autocomplete="off" oninput="updateTeamGames('${key}',0,true)"><datalist id="venueFilterOptions">${venueOptions}</datalist></div><div class="filter-field searchable-field"><label for="locationFilter">Location</label><input id="locationFilter" list="locationFilterOptions" placeholder="All locations" autocomplete="off" oninput="updateTeamGames('${key}',0,true)"><datalist id="locationFilterOptions">${locationOptions}</datalist></div><div class="filter-field"><label for="typeFilter">Type</label><select id="typeFilter" onchange="updateTeamGames('${key}',0,true)"><option value="all">All Types</option><option value="REGULAR_SEASON">Regular Season</option><option value="CONFERENCE_TOURNAMENT">Conference Tournament</option><option value="NCAA_TOURNAMENT">NCAA Tournament</option><option value="NIT">NIT</option><option value="POSTSEASON">Postseason</option></select></div><button type="button" class="filter-clear" onclick="clearTeamFilters('${key}')">Clear filters</button></div><div id="seasonSummary" class="season-summary"></div><div id="teamGamesTable"></div></div><div class="panel opponent-breakdown"><div class="panel-title">All Time Record by Opponent</div><div class="opponent-breakdown-controls"><label class="opponent-breakdown-control"><input id="groupByConference" type="checkbox" checked onchange="updateOpponentBreakdown('${key}')"><span>Group by conference</span></label><label class="opponent-breakdown-control"><span>Sort by</span><select id="opponentSort" onchange="updateOpponentBreakdown('${key}')"><option value="games" selected>Games played</option><option value="alpha">Alphabetical</option><option value="wins">Wins</option></select></label></div><div class="data-note" style="padding:11px 16px;border-bottom:1px solid var(--line)">Current D1 opponents use their ${esc(formatSeason(DB.referenceSeason))} conference; the team’s own conference stays first and Non-D1 / Historical stays last when grouping is on. Select any opponent to open the complete series.</div><div id="opponentBreakdownBody">${opponentBreakdown(key)}</div></div>`;
}
'''
replace_regex(r'function teamView\(key\) \{.*?\n\}\n\n(?=function toggleTeamFilters)', team_view + '\n', 'replace team view')

clear_filters = r'''function clearTeamFilters(key) {
  const state = teamPageState[key];
  if (!state) return;
  Object.assign(state, { page: 0, q: "", selectedOpponentKeys: [], site: "all", season: "", venueQuery: "", locationQuery: "", type: "all", suggestionIndex: -1 });
  const input = document.getElementById("oppFilter");
  const site = document.getElementById("siteFilter");
  const season = document.getElementById("seasonFilter");
  const venue = document.getElementById("venueFilter");
  const location = document.getElementById("locationFilter");
  const type = document.getElementById("typeFilter");
  if (input) input.value = "";
  if (site) site.value = "all";
  if (season) season.value = "";
  if (venue) venue.value = "";
  if (location) location.value = "";
  if (type) type.value = "all";
  updateTeamGames(key, 0, true);
}
'''
replace_regex(r'function clearTeamFilters\(key\) \{.*?\n\}\n\n(?=function siteLabel)', clear_filters + '\n', 'replace clear filters')

mobile_row = r'''function mobileTeamGameRow(game, teamKey) {
  const resultAndScore = `${game.result || "—"}${scoreText(game) !== "—" ? ` · ${scoreText(game)}` : ""}`;
  const opponent = opponentLinkMarkup(teamKey, game, "mobile-game-opponent");
  return `<details class="mobile-game-row"><summary><div class="mobile-game-line mobile-team-game-line">${opponent}<span class="mobile-game-outcome result ${esc(game.result)}">${esc(resultAndScore)}</span></div><div class="mobile-game-line"><span class="mobile-game-meta">${esc(compactGameDate(game))} · ${esc(siteLabel(game.site))} · ${esc(mobileGameTypeLabel(game, teamKey))}</span><span class="mobile-game-cue">Details</span></div></summary>${mobileGameDetails(game, teamKey)}</details>`;
}
'''
replace_regex(r'function mobileTeamGameRow\(game, teamKey\) \{.*?\n\}\n\n(?=function mobileHistoryMonth)', mobile_row + '\n', 'replace mobile game row')

desktop_rows = r'''
function desktopTeamGameRows(games, teamKey) {
  let html = "";
  let currentSeason = null;
  let currentMonth = null;
  for (const game of games) {
    if (game.season !== currentSeason) {
      currentSeason = game.season;
      currentMonth = null;
      html += `<tr class="desktop-history-group desktop-history-season-row"><th colspan="9">${esc(formatSeason(game.season))}</th></tr>`;
    }
    const month = mobileHistoryMonth(game);
    if (month.key !== currentMonth) {
      currentMonth = month.key;
      html += `<tr class="desktop-history-group desktop-history-month-row"><th colspan="9">${esc(month.label)}</th></tr>`;
    }
    const opponent = opponentLinkMarkup(teamKey, game);
    html += `<tr><td>${esc(formatGameDate(game))}</td><td>${opponent}</td><td class="result ${esc(game.result)}">${esc(game.result)}</td><td>${esc(scoreText(game))}</td><td>${esc(siteShort(game.site))}</td><td>${esc(game.venue)}</td><td>${esc(game.location || "—")}</td><td>${esc(gameTypeLabel(game, teamKey))}</td><td>${administrativeChip(game)}</td></tr>`;
  }
  return html;
}
'''.strip()
replace_once('function updateTeamGames(key, delta = 0, reset = false) {', desktop_rows + '\nfunction updateTeamGames(key, delta = 0, reset = false) {', 'insert desktop grouped rows')

update_team_games = r'''function updateTeamGames(key, delta = 0, reset = false) {
  const state = teamPageState[key] || { page: 0, q: "", selectedOpponentKeys: [], site: "all", season: "", venueQuery: "", locationQuery: "", type: "all", suggestionIndex: -1, breakdownGrouped: true, breakdownSort: "games" };
  const opponentFilter = document.getElementById("oppFilter");
  if (opponentFilter) {
    state.q = opponentFilter.value;
    state.site = document.getElementById("siteFilter").value;
    state.season = document.getElementById("seasonFilter").value;
    state.venueQuery = document.getElementById("venueFilter")?.value || "";
    state.locationQuery = document.getElementById("locationFilter")?.value || "";
    state.type = document.getElementById("typeFilter").value;
  }
  state.page = reset ? 0 : Math.max(0, (state.page || 0) + delta);
  teamPageState[key] = state;

  const allGames = DB.games[key] || [];
  const venueOptions = venueOptionsForGames(allGames);
  const locationOptions = locationOptionsForGames(allGames);
  let games = [...allGames].sort((a, b) => gameSortValue(b).localeCompare(gameSortValue(a)));
  const selectedOpponents = new Set(state.selectedOpponentKeys || []);
  const partialQuery = state.q.toLowerCase().trim();
  games = games.filter((game) => {
    if (selectedOpponents.size || partialQuery) {
      const exactSelected = selectedOpponents.has(game.opponentKey);
      const partialMatch = partialQuery && `${game.opponent} ${game.opponentKey}`.toLowerCase().includes(partialQuery);
      if (!exactSelected && !partialMatch) return false;
    }
    if (state.season && game.season !== state.season) return false;
    if (state.type !== "all" && game.gameType !== state.type) return false;
    if (!optionMatchesGame(state.venueQuery, game, venueOptions, venueFilterValue)) return false;
    if (!optionMatchesGame(state.locationQuery, game, locationOptions, locationFilterValue)) return false;
    const short = siteShort(game.site);
    if (state.site === "home" && short !== "H") return false;
    if (state.site === "road" && short !== "A") return false;
    if (state.site === "neutral" && short !== "N") return false;
    if (state.site === "unknown" && short !== "?") return false;
    return true;
  });

  const maxPage = Math.max(0, Math.ceil(games.length / PAGE_SIZE) - 1);
  state.page = Math.min(state.page, maxPage);
  const record = { W: 0, L: 0, T: 0 };
  for (const game of games) if (record[game.result] != null) record[game.result] += 1;

  const selectedNames = (state.selectedOpponentKeys || []).map((opponentKey) => opponentProfile(key, opponentKey).name);
  const opponentSummary = selectedNames.length ? `<b>${esc(selectedNames.join(" or "))}</b> · ` : partialQuery ? `<b>Matching “${esc(state.q.trim())}”</b> · ` : "";
  document.getElementById("seasonSummary").innerHTML = `${state.season ? `<b>${esc(formatSeason(state.season))}</b> · ` : ""}${opponentSummary}${fmtRecord(record.W, record.L, record.T)} · ${fmtNum(games.length)} games shown`;
  const slice = games.slice(state.page * PAGE_SIZE, (state.page + 1) * PAGE_SIZE);
  const rows = desktopTeamGameRows(slice, key);
  const mobileRows = mobileTeamGameRows(slice, key);
  document.getElementById("teamGamesTable").innerHTML = `<div class="desktop-history"><div class="table-wrap"><table class="history-table"><thead><tr><th>Date</th><th>Opponent</th><th>Result</th><th>Score</th><th>Site</th><th>Venue</th><th>Location</th><th>Type</th><th>Administrative</th></tr></thead><tbody>${rows || '<tr><td colspan="9" class="empty">No games match these filters.</td></tr>'}</tbody></table></div></div><div class="mobile-history">${mobileRows || '<div class="empty">No games match these filters.</div>'}</div><div class="pager"><span>${fmtNum(games.length)} games · page ${fmtNum(state.page + 1)} of ${fmtNum(maxPage + 1)}</span><span><button type="button" onclick="updateTeamGames('${key}',-1)" ${state.page === 0 ? "disabled" : ""}>Previous</button> <button type="button" onclick="updateTeamGames('${key}',1)" ${state.page >= maxPage ? "disabled" : ""}>Next</button></span></div>`;
  renderOpponentAssist(key);
  syncStickyOffsets();
  const activeFilterCount = (state.selectedOpponentKeys || []).length + (partialQuery ? 1 : 0) + (state.site !== "all" ? 1 : 0) + (state.season ? 1 : 0) + (state.venueQuery ? 1 : 0) + (state.locationQuery ? 1 : 0) + (state.type !== "all" ? 1 : 0);
  const toggleStatus = document.getElementById("filterToggleStatus");
  if (toggleStatus) toggleStatus.textContent = activeFilterCount ? `${activeFilterCount} active` : "All games";
}
'''
replace_regex(r'function updateTeamGames\(key, delta = 0, reset = false\) \{.*?\n\}\n\n(?=function streakText)', update_team_games + '\n', 'replace update team games')

streak_helpers = r'''function streakText(games, teamA, teamB) {
  if (!games.length) return "—";
  const newest = [...games].sort((a, b) => gameSortValue(b).localeCompare(gameSortValue(a)));
  const first = canonicalWinnerKey(newest[0], teamA, teamB);
  if (!first || first === "tie") return first === "tie" ? "Tie" : "—";
  let length = 0;
  for (const game of newest) {
    if (canonicalWinnerKey(game, teamA, teamB) === first) length += 1;
    else break;
  }
  const winner = first === teamA ? DB.teams[teamA] : opponentProfile(teamA, teamB);
  return `${winner.name} · ${fmtNum(length)} win${length === 1 ? "" : "s"}`;
}

function streakRuns(games, teamA, teamB) {
  const runs = [];
  let current = null;
  for (const game of [...games].sort((a, b) => gameSortValue(a).localeCompare(gameSortValue(b)))) {
    const winner = canonicalWinnerKey(game, teamA, teamB);
    if (!winner || winner === "tie") {
      if (current) runs.push(current);
      current = null;
      continue;
    }
    if (current && current.winner === winner) current.games.push(game);
    else {
      if (current) runs.push(current);
      current = { winner, games: [game] };
    }
  }
  if (current) runs.push(current);
  return runs;
}

function gameYearLabel(game) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(game.date || "")) return game.date.slice(0, 4);
  return game.season ? formatSeason(game.season) : "Year unknown";
}

function streakSpan(run) {
  const first = gameYearLabel(run.games[0]);
  const last = gameYearLabel(run.games[run.games.length - 1]);
  return first === last ? first : `${first}–${last}`;
}

function longestStreakFor(games, teamKey, teamA, teamB) {
  const runs = streakRuns(games, teamA, teamB).filter((run) => run.winner === teamKey);
  const best = Math.max(0, ...runs.map((run) => run.games.length));
  if (!best) return { length: 0, spans: [] };
  const spans = runs.filter((run) => run.games.length === best).map(streakSpan);
  return { length: best, spans };
}

function longestStreakSpanText(streak) {
  if (!streak.spans.length) return "—";
  const shown = streak.spans.slice(0, 3).join(", ");
  return streak.spans.length > 3 ? `${shown} +${streak.spans.length - 3} more` : shown;
}

function largestVictoryFor(games, teamKey, teamA, teamB) {
  return [...games]
    .filter((game) => game.scoreKnown && canonicalWinnerKey(game, teamA, teamB) === teamKey)
    .map((game) => ({ game, margin: Math.abs(game.scores[teamA] - game.scores[teamB]) }))
    .sort((a, b) => b.margin - a.margin || gameSortValue(b.game).localeCompare(gameSortValue(a.game)))[0]?.game || null;
}

function victoryScore(game, winnerKey, loserKey) {
  if (!game || game.scores?.[winnerKey] == null || game.scores?.[loserKey] == null) return "—";
  return `${fmtNum(game.scores[winnerKey])}–${fmtNum(game.scores[loserKey])}`;
}
'''
replace_regex(r'function streakText\(games, teamA, teamB\) \{.*?\n\}\n\nfunction longestStreak\(games, teamA, teamB\) \{.*?\n\}\n', streak_helpers + '\n', 'replace streak helpers')

matchup_name = r'''function matchupTeamName(program) {
  const label = [program.name, program.nickname].filter(Boolean).join(" ");
  const name = esc(label);
  if (!ACTIVE.has(program.key)) return name;
  return `<button type="button" class="team-title-link" onclick="goTeam('${program.key}')" aria-label="Open ${esc(program.name)} team history">${name}</button>`;
}
'''
replace_regex(r'function matchupTeamName\(program\) \{.*?\n\}\n', matchup_name + '\n', 'replace matchup team name')

matchup_helpers_and_view = r'''function matchupStateKey(teamA, teamB) {
  return `${teamA}--${teamB}`;
}

function matchupHistoryMarkup(teamA, teamB, games) {
  const teamAProgram = DB.teams[teamA];
  const teamBProgram = opponentProfile(teamA, teamB);
  const sorted = [...games].sort((a, b) => gameSortValue(b).localeCompare(gameSortValue(a)));
  const rows = sorted.map((game) => {
    const scoreA = game.scoreKnown && game.scores[teamA] != null ? game.scores[teamA] : "—";
    const scoreB = game.scoreKnown && game.scores[teamB] != null ? game.scores[teamB] : "—";
    const winner = canonicalWinnerKey(game, teamA, teamB);
    return `<tr><td>${esc(formatGameDate(game))}</td><td>${seriesScoreMarkup(scoreA, teamAProgram, winner, teamA)}</td><td>${seriesScoreMarkup(scoreB, teamBProgram, winner, teamB)}</td><td>${esc(game.site || "Unknown")}</td><td>${esc(game.venue || "—")}</td><td>${esc(game.location || "—")}</td><td>${esc(gameTypeLabel(game, teamA))}</td><td>${administrativeChip(game)}</td></tr>`;
  }).join("");
  const mobileRows = sorted.map((game) => {
    const scoreA = game.scoreKnown && game.scores[teamA] != null ? game.scores[teamA] : "—";
    const scoreB = game.scoreKnown && game.scores[teamB] != null ? game.scores[teamB] : "—";
    const outcome = game.results?.[teamA] || "—";
    const winner = canonicalWinnerKey(game, teamA, teamB);
    const scoreAMarkup = seriesScoreMarkup(scoreA, teamAProgram, winner, teamA);
    const scoreBMarkup = seriesScoreMarkup(scoreB, teamBProgram, winner, teamB);
    return `<details class="mobile-game-row"><summary><div class="mobile-game-line"><span class="mobile-game-date">${esc(compactGameDate(game))}</span><span class="mobile-game-outcome series-mobile-outcome"><span class="result ${esc(outcome)}">${esc(outcome)}</span><span aria-hidden="true">·</span><span class="series-score-pair">${scoreAMarkup}<span aria-hidden="true">–</span>${scoreBMarkup}</span></span></div><div class="mobile-game-line"><span class="mobile-game-meta">${esc(game.site || "Unknown")} · ${esc(gameTypeLabel(game, teamA))}</span><span class="mobile-game-cue">Details</span></div></summary>${mobileGameDetails(game, teamA)}</details>`;
  }).join("");
  return `<div class="desktop-history"><div class="table-wrap"><table class="matchup-history-table"><thead><tr><th>Date</th><th>${esc(teamAProgram.name)}</th><th>${esc(teamBProgram.name)}</th><th>Site</th><th>Venue</th><th>Location</th><th>Type</th><th>Administrative</th></tr></thead><tbody>${rows || '<tr><td colspan="8" class="empty">No games match these filters.</td></tr>'}</tbody></table></div></div><div class="mobile-history">${mobileRows || '<div class="empty">No games match these filters.</div>'}</div>`;
}

function updateMatchupHistory(teamA, teamB) {
  const key = matchupStateKey(teamA, teamB);
  const state = matchupPageState[key];
  const allGames = seriesGamesFor(teamA, teamB);
  const results = document.getElementById("matchupHistoryResults");
  if (!state || !results) return;
  state.site = document.getElementById("matchupSiteFilter")?.value || "all";
  state.venueQuery = document.getElementById("matchupVenueFilter")?.value || "";
  state.locationQuery = document.getElementById("matchupLocationFilter")?.value || "";
  state.type = document.getElementById("matchupTypeFilter")?.value || "all";
  const venueOptions = venueOptionsForGames(allGames);
  const locationOptions = locationOptionsForGames(allGames);
  const games = allGames.filter((game) => {
    if (state.site !== "all" && game.site !== state.site) return false;
    if (state.type !== "all" && game.gameType !== state.type) return false;
    if (!optionMatchesGame(state.venueQuery, game, venueOptions, venueFilterValue)) return false;
    if (!optionMatchesGame(state.locationQuery, game, locationOptions, locationFilterValue)) return false;
    return true;
  });
  results.innerHTML = matchupHistoryMarkup(teamA, teamB, games);
  const summary = document.getElementById("matchupHistorySummary");
  if (summary) summary.textContent = `${fmtNum(games.length)} of ${fmtNum(allGames.length)} meetings shown`;
}

function clearMatchupFilters(teamA, teamB) {
  const state = matchupPageState[matchupStateKey(teamA, teamB)];
  if (!state) return;
  Object.assign(state, { site: "all", venueQuery: "", locationQuery: "", type: "all" });
  const site = document.getElementById("matchupSiteFilter");
  const venue = document.getElementById("matchupVenueFilter");
  const location = document.getElementById("matchupLocationFilter");
  const type = document.getElementById("matchupTypeFilter");
  if (site) site.value = "all";
  if (venue) venue.value = "";
  if (location) location.value = "";
  if (type) type.value = "all";
  updateMatchupHistory(teamA, teamB);
}

function matchupView(teamA, teamB) {
  const teamAProgram = DB.teams[teamA];
  const teamBProgram = opponentProfile(teamA, teamB);
  const games = seriesGamesFor(teamA, teamB);
  if (!teamAProgram || !games.length) return '<div class="empty">Series not available.</div>';
  matchupPageState[matchupStateKey(teamA, teamB)] = { site: "all", venueQuery: "", locationQuery: "", type: "all" };
  let teamAWins = 0;
  let teamBWins = 0;
  let ties = 0;
  for (const game of games) {
    const winner = canonicalWinnerKey(game, teamA, teamB);
    if (winner === teamA) teamAWins += 1;
    else if (winner === teamB) teamBWins += 1;
    else if (winner === "tie") ties += 1;
  }

  const administrativeCount = games.filter((game) => game.administrativeStatus).length;
  const sites = bucket(games, teamA, teamB, (game) => game.site).sort((a, b) => b.games - a.games);
  const decades = bucket(games, teamA, teamB, (game) => {
    const year = Number((game.date || game.season || "").slice(0, 4));
    return year ? `${Math.floor(year / 10) * 10}s` : "";
  }).sort((a, b) => b.label.localeCompare(a.label)).slice(0, 8);
  const venues = bucket(games, teamA, teamB, (game) => game.venue || game.location || "Venue not resolved").sort((a, b) => b.games - a.games).slice(0, 8);

  const teamAStreak = longestStreakFor(games, teamA, teamA, teamB);
  const teamBStreak = longestStreakFor(games, teamB, teamA, teamB);
  const teamALargest = largestVictoryFor(games, teamA, teamA, teamB);
  const teamBLargest = largestVictoryFor(games, teamB, teamA, teamB);
  const ncaaGames = games.filter((game) => game.gameType === "NCAA_TOURNAMENT");
  let ncaaAWins = 0;
  let ncaaBWins = 0;
  let ncaaTies = 0;
  for (const game of ncaaGames) {
    const winner = canonicalWinnerKey(game, teamA, teamB);
    if (winner === teamA) ncaaAWins += 1;
    else if (winner === teamB) ncaaBWins += 1;
    else if (winner === "tie") ncaaTies += 1;
  }

  const venueOptions = venueOptionsForGames(games).map((option) => `<option value="${esc(option.label)}"></option>`).join("");
  const locationOptions = locationOptionsForGames(games).map((option) => `<option value="${esc(option.label)}"></option>`).join("");
  const teamASite = `at ${teamAProgram.name}`;
  const teamBSite = `at ${teamBProgram.name}`;
  const history = matchupHistoryMarkup(teamA, teamB, games);
  const teamALargestText = victoryScore(teamALargest, teamA, teamB);
  const teamBLargestText = victoryScore(teamBLargest, teamB, teamA);

  return `<button type="button" class="back" onclick="goTeam('${teamA}')">← ${esc(teamAProgram.name)} history</button><div class="match-head"><div class="side-team">${teamLogo(teamAProgram)}<div><h2>${matchupTeamName(teamAProgram)}</h2><div class="kicker" style="color:${teamAProgram.primary}">${esc(teamAProgram.conference)}</div></div></div><div class="vs">VS.</div><div class="side-team right">${teamLogo(teamBProgram)}<div><h2>${matchupTeamName(teamBProgram)}</h2><div class="kicker" style="color:${teamBProgram.primary}">${esc(teamBProgram.conference)}</div></div></div></div><div class="series-score">${fmtRecord(teamAWins, teamBWins, ties)}</div><div class="series-caption">${esc(teamAProgram.name)} record vs. ${esc(teamBProgram.name)} · ${fmtNum(games.length)} meetings</div>${administrativeCount ? `<div class="notice">${fmtNum(administrativeCount)} game${administrativeCount === 1 ? "" : "s"} carries administrative metadata. Records shown use on-court results.</div>` : ""}<div class="match-metrics"><div class="metric"><b>${streakText(games, teamA, teamB)}</b><span>Current Streak</span></div><div class="metric"><b>${teamAStreak.length ? `${fmtNum(teamAStreak.length)} wins` : "—"}</b><span>Longest ${esc(teamAProgram.name)} Streak<small>${esc(longestStreakSpanText(teamAStreak))}</small></span></div><div class="metric"><b>${teamBStreak.length ? `${fmtNum(teamBStreak.length)} wins` : "—"}</b><span>Longest ${esc(teamBProgram.name)} Streak<small>${esc(longestStreakSpanText(teamBStreak))}</small></span></div><div class="metric"><b>${esc(teamALargestText)}</b><span>${esc(teamAProgram.name)} Largest Victory<small>${teamALargest ? esc(formatGameDate(teamALargest)) : "—"}</small></span></div><div class="metric"><b>${esc(teamBLargestText)}</b><span>${esc(teamBProgram.name)} Largest Victory<small>${teamBLargest ? esc(formatGameDate(teamBLargest)) : "—"}</small></span></div><div class="metric"><b>${fmtRecord(ncaaAWins, ncaaBWins, ncaaTies)}</b><span>NCAA Tournament Series<small>${esc(teamAProgram.name)} record vs. ${esc(teamBProgram.name)}</small></span></div></div><div class="subgrid">${miniPanel("Record by Site", sites, teamA)}${miniPanel("Record by Decade", decades, teamA)}${miniPanel("Most-Used Venues", venues, teamA)}</div><div class="panel history-panel" style="margin-top:14px"><div class="panel-title">Complete Series History</div><div class="filters"><div class="filter-field"><label for="matchupSiteFilter">Site</label><select id="matchupSiteFilter" onchange="updateMatchupHistory('${teamA}','${teamB}')"><option value="all">All sites</option><option value="${esc(teamASite)}">${esc(teamASite)}</option><option value="${esc(teamBSite)}">${esc(teamBSite)}</option><option value="Neutral">Neutral</option><option value="Unknown">Unknown</option></select></div><div class="filter-field searchable-field"><label for="matchupVenueFilter">Venue</label><input id="matchupVenueFilter" list="matchupVenueOptions" placeholder="All venues" autocomplete="off" oninput="updateMatchupHistory('${teamA}','${teamB}')"><datalist id="matchupVenueOptions">${venueOptions}</datalist></div><div class="filter-field searchable-field"><label for="matchupLocationFilter">Location</label><input id="matchupLocationFilter" list="matchupLocationOptions" placeholder="All locations" autocomplete="off" oninput="updateMatchupHistory('${teamA}','${teamB}')"><datalist id="matchupLocationOptions">${locationOptions}</datalist></div><div class="filter-field"><label for="matchupTypeFilter">Type</label><select id="matchupTypeFilter" onchange="updateMatchupHistory('${teamA}','${teamB}')"><option value="all">All Types</option><option value="REGULAR_SEASON">Regular Season</option><option value="CONFERENCE_TOURNAMENT">Conference Tournament</option><option value="NCAA_TOURNAMENT">NCAA Tournament</option><option value="NIT">NIT</option><option value="POSTSEASON">Postseason</option></select></div><button type="button" class="filter-clear" onclick="clearMatchupFilters('${teamA}','${teamB}')">Clear filters</button></div><div id="matchupHistorySummary" class="series-history-summary">${fmtNum(games.length)} of ${fmtNum(games.length)} meetings shown</div><div id="matchupHistoryResults">${history}</div></div>`;
}
'''
replace_regex(r'function matchupView\(teamA, teamB\) \{.*?\n\}\n\n(?=function aboutView)', matchup_helpers_and_view + '\n', 'replace matchup view')

replace_regex(r'function aboutView\(\) \{.*?\n\}\n\n(?=function render\(\))', '', 'remove about view')

render = r'''function render() {
  const route = (location.hash || "#home").slice(1).split("/");
  const app = document.getElementById("app");
  if (route[0] === "team" && ACTIVE.has(route[1])) {
    app.innerHTML = teamView(route[1]);
    setTimeout(() => updateTeamGames(route[1]), 0);
  } else if (route[0] === "matchup" && ACTIVE.has(route[1]) && seriesGamesFor(route[1], route[2]).length) {
    app.innerHTML = matchupView(route[1], route[2]);
  } else {
    app.innerHTML = homeView();
  }
  syncStickyOffsets();
  window.scrollTo(0, 0);
}
'''
replace_regex(r'function render\(\) \{.*?\n\}\n\n(?=function openProgramFromSearch)', render + '\n', 'replace render router')

sticky_fn = r'''function syncStickyOffsets() {
  const topbar = document.querySelector(".topbar");
  const topbarHeight = topbar ? Math.ceil(topbar.getBoundingClientRect().height) : 58;
  document.documentElement.style.setProperty("--sticky-topbar", `${topbarHeight}px`);
  const seasonHeader = document.querySelector(".mobile-history-season");
  const seasonHeight = seasonHeader ? Math.ceil(seasonHeader.getBoundingClientRect().height) : 30;
  document.documentElement.style.setProperty("--sticky-season-height", `${seasonHeight}px`);
}

'''
replace_once('async function boot() {', sticky_fn + 'async function boot() {', 'insert sticky offset sync')
replace_once(
    '    updateChrome();\n    bindSearch();\n    window.addEventListener("hashchange", render);\n    render();',
    '    updateChrome();\n    bindSearch();\n    syncStickyOffsets();\n    window.addEventListener("resize", syncStickyOffsets);\n    window.addEventListener("hashchange", render);\n    render();',
    'boot sticky listener',
)

PATH.write_text(text, encoding="utf-8")
print("Applied history UI enhancement patch")
