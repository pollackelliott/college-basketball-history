from pathlib import Path

path = Path('site/index.html')
text = path.read_text(encoding='utf-8')


def once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    text = text.replace(old, new, 1)


once(
    '.opp-link{border:0;background:transparent;padding:2px;font-weight:700;color:#174f82;cursor:pointer;text-decoration:underline;text-decoration-color:#aac3da;text-underline-offset:2px}.opp-plain{font-weight:600}.series-link{border:0;background:transparent;padding:2px;color:#174f82;font-weight:750;text-decoration:underline;text-decoration-color:#aac3da;text-underline-offset:2px;cursor:pointer}',
    '.opp-link{border:0;background:transparent;padding:2px;font-weight:700;color:#174f82;cursor:pointer;text-align:left;text-decoration:underline;text-decoration-color:#aac3da;text-underline-offset:2px}.opp-plain{font-weight:600}.series-link{display:inline-block;border:0;background:transparent;padding:2px;color:#174f82;font-weight:750;text-align:left;white-space:normal;overflow-wrap:anywhere;text-decoration:underline;text-decoration-color:#aac3da;text-underline-offset:2px;cursor:pointer}',
    'link alignment styles',
)

once(
    '.team-title-link{border:0;background:transparent;padding:2px;color:inherit;font:inherit;text-transform:inherit;cursor:pointer;text-decoration:underline;text-decoration-color:#b5c4d3;text-decoration-thickness:2px;text-underline-offset:5px}.team-title-link:hover{color:#174f82;text-decoration-color:currentColor}.vs{font-family:Graduate,"Arial Black",serif;font-size:22px;color:#8090a2}',
    '.matchup-team-name{display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.08}.matchup-school-name{display:inline-block}.matchup-nickname{display:block;margin-top:5px;font-size:.74em;line-height:1.08;font-weight:700}.team-title-link{border:0;background:transparent;padding:2px;color:inherit;font:inherit;text-transform:inherit;cursor:pointer;text-decoration:underline;text-decoration-color:#b5c4d3;text-decoration-thickness:2px;text-underline-offset:5px}.team-title-link:hover{color:#174f82;text-decoration-color:currentColor}.vs{font-family:Graduate,"Arial Black",serif;font-size:22px;color:#8090a2}',
    'matchup title styles',
)

once(
    '.filter-field.searchable-field{min-width:190px;flex:1 1 210px}\n.filter-field.searchable-field input{width:100%}',
    '.filter-field.searchable-field{min-width:190px;flex:1 1 210px}\n.filter-field.searchable-field input{width:100%}.searchable-filter-shell{position:relative}.searchable-filter-shell input{padding-right:38px}.search-filter-clear{position:absolute;right:5px;top:50%;transform:translateY(-50%);width:30px;height:30px;border:0;border-radius:50%;background:#e8eef4;color:#43556a;font-size:19px;line-height:1;cursor:pointer}.search-filter-clear:hover{background:#dce6ef}.search-filter-clear[hidden]{display:none}',
    'searchable filter clear styles',
)

once(
    '.opponent-breakdown-controls{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;padding:11px 14px;border-bottom:1px solid var(--line);background:#f8fafc}\n.opponent-breakdown-control{display:flex;align-items:center;gap:7px;color:#526174;font-size:11px;font-weight:800}\n.opponent-breakdown-control select{min-height:36px;border:1px solid var(--line);border-radius:6px;background:#fff;padding:6px 8px;color:var(--ink)}\n.opponent-breakdown-control input[type="checkbox"]{width:17px;height:17px;accent-color:var(--nav)}',
    '.opponent-breakdown-controls{display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;padding:11px 14px;border-bottom:1px solid var(--line);background:#f8fafc}\n.opponent-breakdown-control{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#526174;font-size:11px;font-weight:800}\n.opponent-breakdown-control select{min-height:36px;border:1px solid var(--line);border-radius:6px;background:#fff;padding:6px 8px;color:var(--ink)}\n.toggle-switch{position:relative;display:inline-flex;width:42px;height:24px;flex:0 0 42px}.toggle-switch input{position:absolute;opacity:0;width:1px;height:1px}.toggle-slider{position:absolute;inset:0;border-radius:999px;background:#b8c4d0;box-shadow:inset 0 0 0 1px rgba(15,23,42,.12);transition:background .18s ease}.toggle-slider::after{content:"";position:absolute;width:18px;height:18px;left:3px;top:3px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(15,23,42,.28);transition:transform .18s ease}.toggle-switch input:checked+.toggle-slider{background:var(--nav)}.toggle-switch input:checked+.toggle-slider::after{transform:translateX(18px)}.toggle-switch input:focus-visible+.toggle-slider{outline:3px solid #2b76b9;outline-offset:2px}',
    'opponent controls toggle styles',
)

once(
    '@media(max-width:720px){.opponent-breakdown-controls{align-items:stretch;justify-content:flex-start}.opponent-breakdown-control{justify-content:space-between;width:100%}.opponent-breakdown-control select{min-width:150px}.filter-field.searchable-field{min-width:0;width:100%;max-width:none}.school-color-link{padding:3px 7px}.match-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}',
    '@media(max-width:720px){.opponent-breakdown-controls{display:grid;grid-template-columns:1fr;align-items:stretch;justify-content:stretch;gap:12px;padding:13px 14px}.opponent-breakdown-control{justify-content:space-between;width:100%;gap:16px;text-align:left}.opponent-breakdown-control select{min-width:150px}.filter-field.searchable-field{min-width:0;width:100%;max-width:none}.school-color-link{padding:3px 7px}.match-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}',
    'mobile opponent controls styles',
)

once(
    '.mobile-team-game-line .mobile-game-opponent{width:auto;max-width:none;margin:0;flex:0 1 auto}',
    '.mobile-team-game-line .mobile-game-opponent{width:auto;max-width:none;margin:0;flex:0 1 auto;text-align:left}',
    'mobile wrapped opponent alignment',
)

old = '''function opponentLinkMarkup(teamKey, game, extraClass = "") {
  const colors = opponentColorPresentation(game.opponentKey);
  const classes = ["opp-link", extraClass, colors ? "school-color-link" : ""].filter(Boolean).join(" ");
  const style = colors ? ` style="--opp-bg:${esc(colors.background)};--opp-fg:${esc(colors.foreground)}"` : "";
  return `<button type="button" class="${classes}"${style} onclick="event.preventDefault();event.stopPropagation();goMatch('${teamKey}','${game.opponentKey}')" aria-label="Open complete ${esc(DB.teams[teamKey].name)} versus ${esc(game.opponent)} series">${esc(game.opponent)}</button>`;
}'''
new = '''function opponentLinkMarkup(teamKey, game, extraClass = "") {
  const classes = ["opp-link", extraClass].filter(Boolean).join(" ");
  return `<button type="button" class="${classes}" onclick="event.preventDefault();event.stopPropagation();goMatch('${teamKey}','${game.opponentKey}')" aria-label="Open complete ${esc(DB.teams[teamKey].name)} versus ${esc(game.opponent)} series">${esc(game.opponent)}</button>`;
}'''
once(old, new, 'remove game-log school colors')

old = '''function opponentTableRows(key, rows) {
  return rows.map((row) => {
    const name = `<button type="button" class="series-link" onclick="goMatch('${key}','${row.key}')" aria-label="Open complete series against ${esc(row.name)}">${esc(row.name)}</button>`;
    return `<tr><td>${name}</td><td>${fmtRecord(row.wins, row.losses, row.ties)}</td><td>${fmtNum(row.games)}</td><td>${fmtWinPct(row.wins, row.losses, row.ties)}</td></tr>`;
  }).join("");
}'''
new = '''function opponentTableRows(key, rows) {
  return rows.map((row) => {
    const colors = opponentColorPresentation(row.key);
    const colorClass = colors ? " school-color-link" : "";
    const style = colors ? ` style="--opp-bg:${esc(colors.background)};--opp-fg:${esc(colors.foreground)}"` : "";
    const name = `<button type="button" class="series-link${colorClass}"${style} onclick="goMatch('${key}','${row.key}')" aria-label="Open complete series against ${esc(row.name)}">${esc(row.name)}</button>`;
    return `<tr><td>${name}</td><td>${fmtRecord(row.wins, row.losses, row.ties)}</td><td>${fmtNum(row.games)}</td><td>${fmtWinPct(row.wins, row.losses, row.ties)}</td></tr>`;
  }).join("");
}'''
once(old, new, 'move school colors to opponent table')

marker = '\nfunction opponentRowComparator(mode) {'
insert = '''
function syncSearchFilterClearButton(inputId, buttonId) {
  const input = document.getElementById(inputId);
  const button = document.getElementById(buttonId);
  if (!input || !button) return;
  button.hidden = !String(input.value || "").trim();
}

function clearTeamSearchFilter(key, inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.value = "";
  updateTeamGames(key, 0, true);
  input.focus();
}

function clearMatchupSearchFilter(teamA, teamB, inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.value = "";
  updateMatchupHistory(teamA, teamB);
  input.focus();
}

function opponentRowComparator(mode) {'''
once(marker, '\n' + insert, 'search filter helper functions')

once(
    '<div class="filter-field searchable-field"><label for="venueFilter">Venue</label><input id="venueFilter" list="venueFilterOptions" placeholder="All venues" autocomplete="off" oninput="updateTeamGames(\'${key}\',0,true)"><datalist id="venueFilterOptions">${venueOptions}</datalist></div>',
    '<div class="filter-field searchable-field"><label for="venueFilter">Venue</label><div class="searchable-filter-shell"><input id="venueFilter" list="venueFilterOptions" placeholder="All venues" autocomplete="off" onfocus="this.select()" oninput="updateTeamGames(\'${key}\',0,true)"><button type="button" id="venueFilterClear" class="search-filter-clear" hidden onclick="clearTeamSearchFilter(\'${key}\',\'venueFilter\')" aria-label="Clear venue filter">×</button></div><datalist id="venueFilterOptions">${venueOptions}</datalist></div>',
    'team venue clear button',
)
once(
    '<div class="filter-field searchable-field"><label for="locationFilter">Location</label><input id="locationFilter" list="locationFilterOptions" placeholder="All locations" autocomplete="off" oninput="updateTeamGames(\'${key}\',0,true)"><datalist id="locationFilterOptions">${locationOptions}</datalist></div>',
    '<div class="filter-field searchable-field"><label for="locationFilter">Location</label><div class="searchable-filter-shell"><input id="locationFilter" list="locationFilterOptions" placeholder="All locations" autocomplete="off" onfocus="this.select()" oninput="updateTeamGames(\'${key}\',0,true)"><button type="button" id="locationFilterClear" class="search-filter-clear" hidden onclick="clearTeamSearchFilter(\'${key}\',\'locationFilter\')" aria-label="Clear location filter">×</button></div><datalist id="locationFilterOptions">${locationOptions}</datalist></div>',
    'team location clear button',
)

once(
    '<div class="panel opponent-breakdown"><div class="panel-title">All Time Record by Opponent</div><div class="opponent-breakdown-controls"><label class="opponent-breakdown-control"><input id="groupByConference" type="checkbox" checked onchange="updateOpponentBreakdown(\'${key}\')"><span>Group by conference</span></label><label class="opponent-breakdown-control"><span>Sort by</span><select id="opponentSort" onchange="updateOpponentBreakdown(\'${key}\')"><option value="games" selected>Games played</option><option value="alpha">Alphabetical</option><option value="wins">Wins</option></select></label></div><div class="data-note" style="padding:11px 16px;border-bottom:1px solid var(--line)">Current D1 opponents use their ${esc(formatSeason(DB.referenceSeason))} conference; the team’s own conference stays first and Non-D1 / Historical stays last when grouping is on. Select any opponent to open the complete series.</div><div id="opponentBreakdownBody">${opponentBreakdown(key)}</div></div>',
    '<div class="panel opponent-breakdown"><div class="panel-title">All Time Record by Opponent</div><div class="opponent-breakdown-controls"><label class="opponent-breakdown-control"><span>Group by conference</span><span class="toggle-switch"><input id="groupByConference" type="checkbox" checked onchange="updateOpponentBreakdown(\'${key}\')"><span class="toggle-slider" aria-hidden="true"></span></span></label><label class="opponent-breakdown-control"><span>Sort by</span><select id="opponentSort" onchange="updateOpponentBreakdown(\'${key}\')"><option value="games" selected>Games played</option><option value="alpha">Alphabetical</option><option value="wins">Wins</option></select></label></div><div id="opponentBreakdownBody">${opponentBreakdown(key)}</div></div>',
    'opponent controls markup and note removal',
)

once(
    '  teamPageState[key] = state;\n\n  const allGames = DB.games[key] || [];',
    '  teamPageState[key] = state;\n  syncSearchFilterClearButton("venueFilter", "venueFilterClear");\n  syncSearchFilterClearButton("locationFilter", "locationFilterClear");\n\n  const allGames = DB.games[key] || [];',
    'team filter clear visibility sync',
)

marker = '\nfunction streakRuns(games, teamA, teamB) {'
insert = '''
function currentStreakSpanText(games, teamA, teamB) {
  if (!games.length) return "—";
  const newest = [...games].sort((a, b) => gameSortValue(b).localeCompare(gameSortValue(a)));
  const first = canonicalWinnerKey(newest[0], teamA, teamB);
  if (!first) return "—";
  if (first === "tie") return gameYearLabel(newest[0]);
  const runGames = [];
  for (const game of newest) {
    if (canonicalWinnerKey(game, teamA, teamB) === first) runGames.push(game);
    else break;
  }
  return runGames.length ? streakSpan({ games: [...runGames].reverse() }) : "—";
}

function streakRuns(games, teamA, teamB) {'''
once(marker, '\n' + insert, 'current streak span helper')

old = '''function matchupTeamName(program) {
  const label = [program.name, program.nickname].filter(Boolean).join(" ");
  const name = esc(label);
  if (!ACTIVE.has(program.key)) return name;
  return `<button type="button" class="team-title-link" onclick="goTeam('${program.key}')" aria-label="Open ${esc(program.name)} team history">${name}</button>`;
}'''
new = '''function matchupTeamName(program) {
  const school = ACTIVE.has(program.key)
    ? `<button type="button" class="team-title-link matchup-school-name" onclick="goTeam('${program.key}')" aria-label="Open ${esc(program.name)} team history">${esc(program.name)}</button>`
    : `<span class="matchup-school-name">${esc(program.name)}</span>`;
  const nickname = program.nickname ? `<span class="matchup-nickname">${esc(program.nickname)}</span>` : "";
  return `<span class="matchup-team-name">${school}${nickname}</span>`;
}'''
once(old, new, 'series team name/nickname split')

once(
    '  state.type = document.getElementById("matchupTypeFilter")?.value || "all";\n  const venueOptions = venueOptionsForGames(allGames);',
    '  state.type = document.getElementById("matchupTypeFilter")?.value || "all";\n  syncSearchFilterClearButton("matchupVenueFilter", "matchupVenueFilterClear");\n  syncSearchFilterClearButton("matchupLocationFilter", "matchupLocationFilterClear");\n  const venueOptions = venueOptionsForGames(allGames);',
    'series filter clear visibility sync',
)

once(
    '<div class="metric"><b>${streakText(games, teamA, teamB)}</b><span>Current Streak</span></div>',
    '<div class="metric"><b>${streakText(games, teamA, teamB)}</b><span>Current Streak<small>${esc(currentStreakSpanText(games, teamA, teamB))}</small></span></div>',
    'current streak years',
)
once('NCAA Tournament Series<small>', 'NCAA Tournament Games<small>', 'NCAA Tournament label')

once(
    '<div class="filter-field searchable-field"><label for="matchupVenueFilter">Venue</label><input id="matchupVenueFilter" list="matchupVenueOptions" placeholder="All venues" autocomplete="off" oninput="updateMatchupHistory(\'${teamA}\',\'${teamB}\')"><datalist id="matchupVenueOptions">${venueOptions}</datalist></div>',
    '<div class="filter-field searchable-field"><label for="matchupVenueFilter">Venue</label><div class="searchable-filter-shell"><input id="matchupVenueFilter" list="matchupVenueOptions" placeholder="All venues" autocomplete="off" onfocus="this.select()" oninput="updateMatchupHistory(\'${teamA}\',\'${teamB}\')"><button type="button" id="matchupVenueFilterClear" class="search-filter-clear" hidden onclick="clearMatchupSearchFilter(\'${teamA}\',\'${teamB}\',\'matchupVenueFilter\')" aria-label="Clear venue filter">×</button></div><datalist id="matchupVenueOptions">${venueOptions}</datalist></div>',
    'series venue clear button',
)
once(
    '<div class="filter-field searchable-field"><label for="matchupLocationFilter">Location</label><input id="matchupLocationFilter" list="matchupLocationOptions" placeholder="All locations" autocomplete="off" oninput="updateMatchupHistory(\'${teamA}\',\'${teamB}\')"><datalist id="matchupLocationOptions">${locationOptions}</datalist></div>',
    '<div class="filter-field searchable-field"><label for="matchupLocationFilter">Location</label><div class="searchable-filter-shell"><input id="matchupLocationFilter" list="matchupLocationOptions" placeholder="All locations" autocomplete="off" onfocus="this.select()" oninput="updateMatchupHistory(\'${teamA}\',\'${teamB}\')"><button type="button" id="matchupLocationFilterClear" class="search-filter-clear" hidden onclick="clearMatchupSearchFilter(\'${teamA}\',\'${teamB}\',\'matchupLocationFilter\')" aria-label="Clear location filter">×</button></div><datalist id="matchupLocationOptions">${locationOptions}</datalist></div>',
    'series location clear button',
)

path.write_text(text, encoding='utf-8')
