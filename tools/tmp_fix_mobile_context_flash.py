from pathlib import Path

path = Path("site/index.html")
text = path.read_text(encoding="utf-8")
marker = "Mobile route context scroll-reset guard"
if marker in text:
    print("Mobile context flash guard already applied")
    raise SystemExit(0)

old_guard = '''  document.body.classList.toggle("nav-team", Boolean(isTeam));
  document.body.classList.toggle("nav-series", Boolean(isSeries));
  document.body.classList.toggle("nav-home", !isTeam && !isSeries);

  if (isTeam) {'''
new_guard = '''  document.body.classList.toggle("nav-team", Boolean(isTeam));
  document.body.classList.toggle("nav-series", Boolean(isSeries));
  document.body.classList.toggle("nav-home", !isTeam && !isSeries);

  // Mobile route context scroll-reset guard: iOS can apply scrollTo(0, 0)
  // after the newly rendered heading has already been measured. Keep the
  // sticky context hidden until the route is actually settled at the top.
  if (routeContextResetPending) {
    hideTeamContextTitle();
    hideSeriesContextTitle();
    return;
  }

  if (isTeam) {'''
if text.count(old_guard) != 1:
    raise SystemExit(f"Expected route-class block once, found {text.count(old_guard)}")
text = text.replace(old_guard, new_guard, 1)

old_pending = '''let teamContextSyncPending = false;
function scheduleTeamContextTitleSync() {'''
new_pending = '''let teamContextSyncPending = false;
let routeContextResetPending = false;
let routeContextResetFrame = 0;

function settleRouteContextAfterScrollReset(attempt = 0) {
  if (!routeContextResetPending) return;
  if (Math.abs(window.scrollY) <= 1 || attempt >= 12) {
    routeContextResetPending = false;
    routeContextResetFrame = 0;
    syncStickyOffsets();
    syncTeamContextTitle();
    return;
  }
  window.scrollTo(0, 0);
  routeContextResetFrame = requestAnimationFrame(() => settleRouteContextAfterScrollReset(attempt + 1));
}

function scheduleTeamContextTitleSync() {'''
if text.count(old_pending) != 1:
    raise SystemExit(f"Expected pending-state block once, found {text.count(old_pending)}")
text = text.replace(old_pending, new_pending, 1)

old_render = '''function render() {
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
  window.scrollTo(0, 0);
  syncStickyOffsets();
  syncTeamContextTitle();
}'''
new_render = '''function render() {
  const route = (location.hash || "#home").slice(1).split("/");
  const app = document.getElementById("app");
  routeContextResetPending = true;
  if (routeContextResetFrame) cancelAnimationFrame(routeContextResetFrame);
  routeContextResetFrame = 0;
  if (route[0] === "team" && ACTIVE.has(route[1])) {
    app.innerHTML = teamView(route[1]);
    setTimeout(() => updateTeamGames(route[1]), 0);
  } else if (route[0] === "matchup" && ACTIVE.has(route[1]) && seriesGamesFor(route[1], route[2]).length) {
    app.innerHTML = matchupView(route[1], route[2]);
  } else {
    app.innerHTML = homeView();
  }
  window.scrollTo(0, 0);
  syncStickyOffsets();
  syncTeamContextTitle();
  routeContextResetFrame = requestAnimationFrame(() => settleRouteContextAfterScrollReset());
}'''
if text.count(old_render) != 1:
    raise SystemExit(f"Expected render block once, found {text.count(old_render)}")
text = text.replace(old_render, new_render, 1)

path.write_text(text, encoding="utf-8")
print("Applied mobile context badge scroll-reset guard")
