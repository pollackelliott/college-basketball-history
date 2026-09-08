from pathlib import Path

path = Path('site/index.html')
text = path.read_text(encoding='utf-8')
marker = 'mobile-search-icon'
if marker in text:
    print('Mobile nav affordance refinement already implemented')
    raise SystemExit(0)

old_button = '<button type="button" class="mobile-search-toggle" onclick="toggleMobileSearch(true)" aria-label="Search programs">Search</button>'
new_button = '<button type="button" class="mobile-search-toggle" onclick="toggleMobileSearch(true)" aria-label="Search programs"><svg class="mobile-search-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg><span>Search</span></button>'
if text.count(old_button) != 1:
    raise SystemExit(f'Expected mobile search button once, found {text.count(old_button)}')
text = text.replace(old_button, new_button, 1)

css = r'''
/* Mobile navigation affordance polish. */
.mobile-search-icon{display:none}
@media(max-width:720px){
  .navlinks button:first-child{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
  .mobile-search-toggle{display:inline-flex;align-items:center;justify-content:flex-end;gap:4px}
  .mobile-search-icon{display:block;width:11px;height:11px;flex:0 0 11px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
  body.nav-team .navlinks,body.nav-series .navlinks{gap:1px}
  body.nav-team .navlinks button,body.nav-series .navlinks button{min-height:22px;padding:1px 4px}
}
'''
if text.count('</style>') != 1:
    raise SystemExit('Expected one style close')
text = text.replace('</style>', css + '\n</style>', 1)
path.write_text(text, encoding='utf-8')
print('Mobile nav affordance refinement applied')
