from pathlib import Path

path = Path("site/index.html")
text = path.read_text(encoding="utf-8")
marker = "Three-zone topbar without redundant Teams control"
if marker in text:
    print("Topbar refinement already applied")
    raise SystemExit(0)

old_topbar = '.topbar-inner{max-width:1280px;margin:0 auto;padding:14px 22px;display:grid;grid-template-columns:auto auto minmax(0,1fr) minmax(280px,350px);grid-template-areas:"brand nav title search";align-items:center;gap:16px;min-width:0}'
new_topbar = '.topbar-inner{max-width:1280px;margin:0 auto;padding:14px 22px;display:grid;grid-template-columns:auto minmax(0,1fr) minmax(280px,350px);grid-template-areas:"brand title search";align-items:center;gap:16px;min-width:0}'
if text.count(old_topbar) != 1:
    raise SystemExit(f"Expected desktop topbar rule once, found {text.count(old_topbar)}")
text = text.replace(old_topbar, new_topbar, 1)

old_nav = '.navlinks{grid-area:nav;display:flex;gap:4px}'
new_nav = '.navlinks{display:none;gap:4px}'
if text.count(old_nav) != 1:
    raise SystemExit(f"Expected base navlinks rule once, found {text.count(old_nav)}")
text = text.replace(old_nav, new_nav, 1)

old_teams = '<div class="navlinks"><button type="button" onclick="goHome()">Teams</button>'
new_teams = '<div class="navlinks">'
if text.count(old_teams) != 1:
    raise SystemExit(f"Expected Teams control once, found {text.count(old_teams)}")
text = text.replace(old_teams, new_teams, 1)

css = r'''
/* Three-zone topbar without redundant Teams control. */
body.nav-home .topbar-inner{display:grid;grid-template-columns:auto minmax(0,1fr) minmax(280px,350px);grid-template-areas:"brand title search";align-items:center;gap:16px}
body.nav-home .brand{grid-area:brand;width:auto;white-space:nowrap;text-align:left;line-height:normal}
body.nav-home .navlinks{display:none}
body.nav-home .searchbox{grid-area:search;margin-left:0;width:100%}
@media(max-width:950px){
  .topbar-inner,body.nav-home .topbar-inner,body.nav-team .topbar-inner,body.nav-series .topbar-inner{display:grid;grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:"brand title nav";align-items:center}
  .navlinks,body.nav-home .navlinks{grid-area:nav;display:flex;align-self:center;justify-self:end;margin-left:0;margin-right:0}
  body.nav-home .searchbox{display:none}
}
@media(max-width:720px){
  .navlinks,body.nav-home .navlinks{flex-direction:row;align-items:center;justify-content:center;gap:0}
  body.nav-home .navlinks{margin-right:0}
  body.nav-team .navlinks,body.nav-series .navlinks{align-self:center;justify-self:end;align-items:center;margin-right:8px}
  .navlinks button:first-child{text-decoration:none}
  .mobile-search-toggle{min-height:44px;padding:8px 7px;justify-content:center}
  body.nav-team .navlinks button,body.nav-series .navlinks button{min-height:44px;padding:8px 4px}
}
'''
if text.count('</style>') != 1:
    raise SystemExit("Expected one style close")
text = text.replace('</style>', css + '\n</style>', 1)

if '>Teams</button>' in text:
    raise SystemExit("Teams button still present after patch")

path.write_text(text, encoding="utf-8")
print("Removed redundant Teams control and restored three-zone topbar")
