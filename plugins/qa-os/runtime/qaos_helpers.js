/* QA OS page helpers: one file, injected into the app page through the browser MCP (execute_script).
 * Install (once per login):  localStorage.qaos_src = String.raw`<this file>`; eval(localStorage.qaos_src)
 * After a page reload:       eval(localStorage.qaos_src)   (the login session keeps localStorage; a new login clears it)
 * Every action is appended to window.qaos.log (mirrored in localStorage.qaos_log) so the recorder
 * (framework/tools/qaos_record.py) can turn a run into flow_spec.json. UI steps must run one at a time.
 * Read-only helpers (read, options, rows, headers, session) do not write to the log.
 */
(() => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const vis = e => e && e.offsetParent !== null && e.getBoundingClientRect().width > 0;
  const txt = e => (e.innerText || e.textContent || '').trim();
  const Q = window.qaos = window.qaos || {};
  try { Q.log = Q.log || JSON.parse(localStorage.qaos_log || '[]'); } catch (e) { Q.log = []; }
  const rec = o => { o.t = Date.now(); Q.log.push(o); try { localStorage.qaos_log = JSON.stringify(Q.log); } catch (e) {} return o; };
  Q.sleep = sleep;
  Q.reset = () => { Q.log = []; localStorage.qaos_log = '[]'; return 'log cleared'; };
  Q.waitFor = async (fn, ms = 15000, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { try { const v = fn(); if (v) return v; } catch (e) {} await sleep(step); } return null; };
  Q.session = () => ({ url: location.pathname + location.search, token: !!localStorage.accessToken, crumb: Q.crumb() });
  Q.crumb = () => document.body.innerText.split('\n').slice(4, 10).join(' > ');
  // label -> control (the input/select/date box beside a label)
  Q.control = label => {
    const l = [...document.querySelectorAll('label')].find(x => vis(x) && txt(x).replace(/\s+/g, ' ') === label);
    if (!l) return null;
    let cont = l.closest('[class*=col-]') || l.parentElement;
    for (let i = 0; i < 3 && cont; i++, cont = cont.parentElement) {
      const sib = cont.nextElementSibling;
      const c = sib && sib.querySelector('input, textarea, dx-select-box, dx-date-box');
      if (c) return { label: l, root: sib, input: sib.querySelector('input.dx-texteditor-input, input:not([type=hidden]), textarea') };
    }
    const r = l.getBoundingClientRect(); const e = document.elementFromPoint(r.right + 250, r.top + 8);
    return e ? { label: l, root: e, input: e.tagName === 'INPUT' || e.tagName === 'TEXTAREA' ? e : e.querySelector('input.dx-texteditor-input, input:not([type=hidden]), textarea') } : null;
  };
  const ident = c => { const e = c.input || c.root; const w = c.root.closest('dx-select-box, dx-date-box, dx-text-box, cent-textbox, cent-selectbox, cent-datebox') || c.root;
    return { id: (e && e.id) || (w && w.id) || (w && w.getAttribute && (w.getAttribute('name') || w.getAttribute('formcontrolname'))) || '', widget: w ? w.tagName.toLowerCase() : '' }; };
  Q.read = label => { const c = Q.control(label); return c && c.input ? c.input.value : null; };
  Q.options = async label => {
    const c = Q.control(label); if (!c) return null;
    const btn = c.root.querySelector('.dx-dropdowneditor-button, .dx-texteditor-input') || c.input; btn.click();
    await Q.waitFor(() => document.querySelector('.dx-list-item'), 5000);
    const o = [...new Set([...document.querySelectorAll('.dx-list-item')].filter(vis).map(txt))];
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    return o;
  };
  Q.text = async (label, value) => {
    const c = Q.control(label); if (!c || !c.input) throw new Error('no text control: ' + label);
    const i = c.input; i.focus();
    Object.getOwnPropertyDescriptor(i.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype, 'value').set.call(i, value);
    i.dispatchEvent(new Event('input', { bubbles: true })); i.dispatchEvent(new Event('change', { bubbles: true })); i.blur(); await sleep(300);
    return rec(Object.assign({ act: 'text', label, value, kind: '0001' }, ident(c)));
  };
  Q.pick = async (label, option) => {
    const c = Q.control(label); if (!c) throw new Error('no dropdown: ' + label);
    (c.root.querySelector('.dx-dropdowneditor-button') || c.input).click();
    const ok = await Q.waitFor(() => [...document.querySelectorAll('.dx-list-item')].some(x => vis(x)), 6000);
    if (!ok) throw new Error('no options: ' + label);
    const it = [...document.querySelectorAll('.dx-list-item')].filter(vis).find(x => txt(x) === option) || [...document.querySelectorAll('.dx-list-item')].filter(vis).find(x => txt(x).startsWith(option));
    if (!it) throw new Error('option not found: ' + option);
    it.click(); await sleep(800);
    return rec(Object.assign({ act: 'pick', label, value: txt(it), kind: '0002' }, ident(c)));
  };
  // click a visible button/link by element id, or by exact visible text; scoped to visible elements only
  Q.find = target => { const all = [...document.querySelectorAll('[id="' + target + '"], button, a, dx-button, .dx-button, [role=tab], .nav-link, span')].filter(vis);
    return all.find(e => e.id === target) || all.find(e => txt(e) === target); };
  Q.click = async (target, wait = 800) => { const e = Q.find(target); if (!e) throw new Error('not found/visible: ' + target);
    const b = e.closest('dx-button') || e; b.click(); await sleep(wait);
    return rec({ act: 'click', target, id: b.id || '', text: txt(b), kind: '0004' }); };
  // click and capture the toast text (toasts vanish in under a second)
  Q.clickCapture = async (target, ms = 6000) => {
    const e = Q.find(target); if (!e) throw new Error('not found/visible: ' + target);
    const seen = []; const b = e.closest('dx-button') || e; b.click(); const t0 = Date.now();
    while (Date.now() - t0 < ms) { await sleep(200);
      document.querySelectorAll('[class*=toast],[class*=Toast],[role=alert],.dx-toast-message,.dx-overlay-content').forEach(x => { const t = txt(x); if (t && t.length < 240 && !seen.includes(t)) seen.push(t); });
      if (seen.length && Date.now() - t0 > 1500) break; }
    rec({ act: 'click', target, id: b.id || '', text: txt(b), kind: '0004' });
    rec({ act: 'toast', after: target, messages: seen });
    return seen;
  };
  Q.tab = async name => { const e = [...document.querySelectorAll('*')].filter(vis).find(x => !x.children.length && txt(x) === name && x.getBoundingClientRect().top < 260);
    if (!e) throw new Error('tab not found: ' + name); e.click(); await sleep(1500); return rec({ act: 'tab', value: name }); };
  // open a screen through the sidebar search box (works on every environment); waits for the screen, not a fixed time.
  // Fixed 2026-10-01 after the live harvest: (1) the search icon is clicked only when the search box is not already visible (clicking it while
  // results were showing opened a result); (2) menu links are matched as <a class="sub-menu-links"> with the exact text, and when several share the
  // name (two "Sales Return" links exist) `index` (default 0) picks one and the log records `ambiguous`; (3) success needs the URL to change, or the
  // breadcrumb to contain the term, so a scan can no longer read the PREVIOUS screen.
  Q.open = async (term, ms = 25000, index = 0) => {
    const before = location.href;
    let i = document.querySelector("input[placeholder='Search Here']");
    if (!i || !vis(i)) { const ic = document.elementFromPoint(38, 366); if (ic) ic.click(); await sleep(900); i = document.querySelector("input[placeholder='Search Here']"); }
    if (!i) throw new Error('sidebar search box not found (expand the sidebar with the hamburger icon)');
    i.focus(); i.value = term; i.dispatchEvent(new Event('input', { bubbles: true })); await sleep(1100);
    let e = [...document.querySelectorAll('a.sub-menu-links')].filter(x => vis(x) && txt(x) === term);
    if (!e.length) e = [...document.querySelectorAll('*')].filter(x => vis(x) && !x.children.length && txt(x) === term).map(x => x.closest('a') || x);
    if (!e.length) throw new Error('menu entry not found: ' + term);
    const target = e[Math.min(index, e.length - 1)];
    target.click();
    const first = term.split(' ')[0];
    const ok = await Q.waitFor(() => (location.href !== before || Q.crumb().includes(first)) && /Data grid|Header|Detail|Order|Search|Date/.test(document.body.innerText), ms);
    rec({ act: 'nav', term, url: location.pathname + location.search, crumb: Q.crumb(), ok: !!ok, ambiguous: e.length > 1 ? e.length : undefined });
    return { ok: !!ok, url: location.pathname + location.search, ambiguous: e.length > 1 ? e.length : 0 };
  };
  Q.rows = () => { const t = document.body.innerText; return [...t.matchAll(/Data grid with (\d+) rows and (\d+) columns/g)].map(x => x.slice(1).map(Number)); };
  Q.headers = () => [...document.querySelectorAll('.dx-header-row td, .dx-header-row th')].map(txt).filter(Boolean);
  Q.note = (msg, extra) => rec(Object.assign({ act: 'note', msg }, extra || {}));
  Q.dump = () => JSON.stringify(Q.log);
})();
