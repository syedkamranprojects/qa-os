/* QA OS page helpers: one file, injected into the app page through the browser MCP (execute_script).
 * Install (once per login):  localStorage.qaos_src = <the full text of this file>; eval(localStorage.qaos_src)   (no backticks in this file: it is often passed inside a template string)
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
  // _before (set by the watcher) logs the current screen first when it changed, so every entry lands on its own screen
  let _before = null;
  const rec = o => { if (_before && o.act !== 'screen') _before(); o.t = Date.now(); Q.log.push(o); try { localStorage.qaos_log = JSON.stringify(Q.log); } catch (e) {} return o; };
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
  // name (two "Sales Return" links exist) 'index' (default 0) picks one and the log records 'ambiguous'; (3) success needs the URL to change, or the
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
    const li = target.closest('li[id]') || target;
    rec({ act: 'nav_click', src: 'helper', value: term, id: li.id || '', locator: li.id ? '#' + li.id : '', search: term });
    target.click();
    const first = term.split(' ')[0];
    const ok = await Q.waitFor(() => (location.href !== before || Q.crumb().includes(first)) && /Data grid|Header|Detail|Order|Search|Date/.test(document.body.innerText), ms);
    rec({ act: 'nav', term, url: location.pathname + location.search, crumb: Q.crumb(), ok: !!ok, ambiguous: e.length > 1 ? e.length : undefined });
    return { ok: !!ok, url: location.pathname + location.search, ambiguous: e.length > 1 ? e.length : 0 };
  };
  Q.rows = () => { const t = document.body.innerText; return [...t.matchAll(/Data grid with (\d+) rows and (\d+) columns/g)].map(x => x.slice(1).map(Number)); };
  Q.headers = () => [...document.querySelectorAll('.dx-header-row td, .dx-header-row th')].map(txt).filter(Boolean);
  // read a value shown on screen (input, or 'Label: value' text) and log it under a repository name, e.g.
  // qaos.remember('#documentNo', 'QUICK_ORDERNUMBER') or qaos.remember('Net Amount', 'NET_AMOUNT')
  Q.remember = (target, name) => {
    let el = target.startsWith('#') || target.startsWith('//') ? (target.startsWith('#') ? document.querySelector(target) : document.evaluate(target, document, null, 9, null).singleNodeValue) : null;
    let value = null, label = target;
    if (el) { value = el.value !== undefined && el.tagName === 'INPUT' ? el.value : txt(el); label = labelOf(el) || target; }
    else { const c = Q.control(target); if (c && c.input) { el = c.input; value = el.value; }
      else { const line = document.body.innerText.split(String.fromCharCode(10)).find(l => l.trim().startsWith(target)); if (line) value = line.split(':').slice(1).join(':').trim(); } }
    return rec({ act: 'remember', src: 'helper', name, label, id: el && el.id || '', locator: el ? sel(el) : '', value });
  };
  Q.note = (msg, extra) => rec(Object.assign({ act: 'note', msg }, extra || {}));
  Q.dump = () => JSON.stringify(Q.log);

  /* ---- Passive watcher (2026-10-08) ------------------------------------------------------------
   * Real Selenium typing/clicks bypass the helper functions above, so recordings had to be rebuilt by
   * hand. The watcher observes the page itself and logs what the executor DISCOVERS: screens, elements
   * (label, id, type), tabs (label + tab id), grid cells (column, row), dropdown options, and every
   * message (toast / popup / alert). Entries carry src:'watch'. Helper functions set Q._quiet while they
   * act, so their own entries are not logged twice. Installed by Q.watch() (idempotent; re-run after a reload).
   */
  // DevExtreme generated ids (dx-<guid>) change on every page load: never use them as a locator (A20)
  const GEN_ID = /^dx-[0-9a-f]{4,}/i;
  const goodId = id => !!id && !GEN_ID.test(id);
  const sel = e => { if (!e || !e.tagName) return '';
    if (goodId(e.id)) return '#' + e.id;
    const n = e.getAttribute && (e.getAttribute('name') || e.getAttribute('formcontrolname'));
    if (n) return e.tagName.toLowerCase() + '[name="' + n + '"]';
    const t = txt(e); if (t && t.length < 60 && !e.children.length) return '//' + e.tagName.toLowerCase() + '[normalize-space(.)="' + t + '"]';
    return e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''); };
  const labelOf = el => {
    // grid cell -> column header text
    const td = el.closest && el.closest('td[aria-colindex]');
    if (td) { const grid = td.closest('.dx-datagrid, .dx-gridbase-container') || document; const ci = +td.getAttribute('aria-colindex');
      // 1) DevExtreme links each data/editor cell to its header cell (aria-describedby="dx-col-N"); a band header
      //    ("Order") sits above the leaf header ("CS") and covers it horizontally -> "Order CS"
      const head = td.getAttribute('aria-describedby') && document.getElementById(td.getAttribute('aria-describedby'));
      if (head && txt(head)) { const hr = head.getBoundingClientRect(); const cx = hr.left + hr.width / 2;
        const band = [...grid.querySelectorAll('.dx-header-row td')].find(h => { const r = h.getBoundingClientRect(); return h !== head && txt(h) && r.bottom <= hr.top + 2 && r.left <= cx && r.right >= cx; });
        return ((band ? txt(band) + ' ' : '') + txt(head)).replace(/\s+/g, ' ').trim(); }
      // 2) fallback: header rows by column index
      const rows = [...grid.querySelectorAll('.dx-header-row')];
      const parts = rows.map(r => { const c = [...r.querySelectorAll('td[aria-colindex]')].find(h => { const s0 = +h.getAttribute('aria-colindex'); const span = +(h.getAttribute('colspan') || 1); return ci >= s0 && ci < s0 + span; }); return c ? txt(c) : ''; }).filter(Boolean);
      const lbl = [...new Set(parts)].join(' ').replace(/\s+/g, ' ').trim();
      return lbl || ('column ' + ci); }
    if (el.id) { const l = document.querySelector('label[for="' + el.id + '"]'); if (l) return txt(l); }
    // form field -> nearest visible label to the left/above inside the same row/column block
    let cont = el.closest('[class*=col-], .form-group, .dx-field, tr, li') || el.parentElement;
    for (let i = 0; i < 4 && cont; i++, cont = cont.parentElement) {
      const l = cont.querySelector('label'); if (l && vis(l) && txt(l)) return txt(l).replace(/\s*\*$/, '');
      const p = cont.previousElementSibling; if (p && p.querySelector) { const pl = p.querySelector('label') || (p.tagName === 'LABEL' ? p : null); if (pl && txt(pl)) return txt(pl).replace(/\s*\*$/, ''); }
    }
    return el.getAttribute && (el.getAttribute('placeholder') || el.getAttribute('aria-label')) || '';
  };
  const widgetOf = el => { const w = el.closest && el.closest('dx-select-box, dx-autocomplete, dx-lookup, dx-date-box, dx-number-box, dx-text-box, dx-text-area, dx-check-box, .dx-selectbox, .dx-autocomplete, .dx-datebox, .dx-numberbox, .dx-textbox, .dx-checkbox');
    if (!w) return el.tagName ? el.tagName.toLowerCase() + (el.type ? ':' + el.type : '') : '';
    const c = (w.className || '') + ' ' + w.tagName.toLowerCase();
    return /select|lookup/.test(c) ? 'dropdown' : /autocomplete/.test(c) ? 'type-ahead' : /date/.test(c) ? 'date' : /number/.test(c) ? 'number' : /check/.test(c) ? 'checkbox' : 'text'; };
  // tab / section ids used by the framework's screen mappings (pmgsm_navigation_path); same pattern as the converter's TAB_ID
  const TAB_ID_RE = /^(?:Dem|Opr|Oth|addr)-\d+$|^tab(?:_group)?_\d+$/;
  const tabIdHost = el => { for (let n = el, i = 0; n && n.nodeType === 1 && i < 6; n = n.parentElement, i++) { if (n.id && TAB_ID_RE.test(n.id)) return n; } return null; };
  // A20: the stable id of a button is often on a wrapper (cent-button#forwardPopUpSaveBtn > dx-button). Walk up at most 3 levels
  // and accept a wrapper only while it holds this one button, so a container id is never taken for the button
  const BTN = 'button, dx-button, .dx-button, [role=button], a';
  const stableHost = b => { for (let n = b, i = 0; n && n.nodeType === 1 && i <= 3; n = n.parentElement, i++) {
      if (goodId(n.id)) return n;
      const p = n.parentElement; if (!p || [...p.querySelectorAll(BTN)].filter(vis).length > 1) return null; }
    return null; };
  // A20: masked editors (CNIC, cell numbers) show '_' for the empty mask positions; log the value without them
  const cleanVal = t => { const v = t.value || ''; const masked = t.closest && t.closest('.dx-texteditor-masked, [mask]');
    if (masked) return v.replace(/_/g, '').replace(/[-\s().\/]+$/, '');
    return /_$/.test(v) ? v.replace(/_+$/, '') : v; };
  // A20: grid row identity = the first data cell with text (e.g. DSR Code AUTO091013)
  // the framework clicks a grid row by the id of its cell content (row_1_outlet_code = first row, column outlet_code)
  const rowCellId = (raw, tr) => { for (let n = raw; n && n !== tr; n = n.parentElement) { if (/^row_\d+_/.test(n.id || '')) return n.id; }
    const td = raw.closest('td[aria-colindex]'); const c = td && [...td.querySelectorAll('[id]')].find(x => /^row_\d+_/.test(x.id)); return c ? c.id : ''; };
  const rowKey = tr => { const td = [...tr.querySelectorAll('td[aria-colindex]')].find(c => txt(c)); return td ? { keyColumn: labelOf(td), key: txt(td) } : {}; };
  const cellInfo = el => { const td = el.closest && el.closest('td[aria-colindex]'); if (!td) return null; const tr = td.closest('tr');
    const grid = td.closest('.dx-datagrid'); const gid = grid && (grid.id || (grid.closest('[id]') || {}).id) || '';
    return { grid: gid, column: labelOf(el), colindex: td.getAttribute('aria-colindex'), rowindex: tr ? tr.getAttribute('aria-rowindex') : null, cellId: td.id || '' }; };
  const screen = () => ({ url: location.pathname + location.search, title: (document.querySelector('.page-title, h1, h2, .breadcrumb') || {}).innerText || '', crumb: Q.crumb() });
  let lastScreen = '';
  const noteScreen = () => { const s = screen(); const k = s.url + '|' + s.crumb; if (k !== lastScreen) { lastScreen = k; rec(Object.assign({ act: 'screen', src: 'watch' }, s)); } };
  _before = noteScreen;
  Q.watch = () => {
    if (window.__qaosWatch) return 'watcher already on';
    window.__qaosWatch = true; noteScreen();
    const focusVal = new WeakMap();
    const pending = new Map();
    let lastInput = null, lastInputAt = 0;
    document.addEventListener('focusin', e => { const t = e.target; if (t && /INPUT|TEXTAREA/.test(t.tagName)) { focusVal.set(t, t.value); lastInput = t; lastInputAt = Date.now();
      // grid cell editors: remember the cell as soon as it is entered, so a cell left at its default (e.g. 0) is still logged
      const c = !Q._quiet && t.type !== 'hidden' && !t.readOnly && !t.disabled && cellInfo(t); if (c && !pending.has(t)) pending.set(t, { act: 'cell', src: 'watch', label: labelOf(t), id: t.id || '', locator: sel(t), widget: widgetOf(t), value: cleanVal(t), raw: t.value, ctx: c }); } }, true);
    // a dropdown/type-ahead field opened by a click (no focus) also counts as the field in use
    document.addEventListener('mousedown', e => { const w = e.target && e.target.closest && e.target.closest('.dx-dropdowneditor, .dx-selectbox, .dx-autocomplete, .dx-tagbox, dx-select-box, dx-autocomplete, dx-tag-box'); if (w) { const i = w.querySelector('input.dx-texteditor-input, input:not([type=hidden])'); if (i) { lastInput = i; lastInputAt = Date.now(); } } }, true);
    // A20: the last button clicked (not a field), so an option from a menu it opened is not taken for a field value
    let lastBtn = null;
    // typed values: logged when the field loses focus with a changed value
    // typed values. DevExtreme grid editors are re-rendered and cleared on commit, so the value and the cell
    // context are captured from 'input' events while typing and flushed once (focusout, Tab/Enter, or the next click).
    document.addEventListener('input', e => { const t = e.target; if (Q._quiet || !t || !/INPUT|TEXTAREA/.test(t.tagName) || t.type === 'hidden' || t.readOnly || t.disabled) return;
      if (focusVal.get(t) === '\u0000picked') return;
      const prev = pending.get(t); pending.set(t, { act: cellInfo(t) ? 'cell' : 'text', src: 'watch', label: (prev && prev.label) || labelOf(t), id: t.id || '', locator: sel(t), widget: widgetOf(t), value: cleanVal(t), raw: t.value, ctx: (prev && prev.ctx) || cellInfo(t) }); }, true);
    const flush = t => { const p = pending.get(t); if (!p) return; pending.delete(t);
      if (!p.ctx && focusVal.has(t) && focusVal.get(t) === p.raw) return;   // unchanged form field: nothing typed (grid cells are always logged)
      if (p.raw === p.value) delete p.raw;
      noteScreen(); const ctx = p.ctx; delete p.ctx; rec(Object.assign(p, ctx || {})); };
    Q._flushAll = () => [...pending.keys()].forEach(flush);
    // row snapshot: the editable cells of the grid row a button belongs to, read at the click (typed keystrokes can be noisy;
    // this is the authoritative value per column). One 'row' entry per click; the converter prefers it over 'cell' entries.
    Q._rowSnap = b => { const tr = b.closest('tr'); if (!tr) return; const ci = cellInfo(b);
      const cells = [...tr.querySelectorAll('td[aria-colindex]')].map(td => { const i = td.querySelector('input:not([type=hidden]), textarea');
        if (!i || i.readOnly || i.disabled) return null;
        return { label: labelOf(i), value: cleanVal(i), id: i.id || '', locator: sel(i), widget: widgetOf(i), colindex: td.getAttribute('aria-colindex') }; }).filter(Boolean);
      if (cells.length) rec({ act: 'row', src: 'watch', grid: ci.grid, rowindex: ci.rowindex, button: b.id || txt(b), cells }); };
    document.addEventListener('focusout', e => { if (!Q._quiet) flush(e.target); }, true);
    document.addEventListener('keydown', e => { if (!Q._quiet && (e.key === 'Tab' || e.key === 'Enter')) flush(e.target); }, true);
    // clicks: buttons, links, tabs, dropdown options, checkboxes, grid row links
    document.addEventListener('click', e => { if (Q._quiet) return; Q._flushAll(); const raw = e.target; if (!raw || !raw.closest) return; noteScreen();
      // DCODE tabs / sections (A18): the tab id (Dem-1, Opr-1, Oth-1, addr-1, tab_4, tab_group_2 ...) sits on the clicked
      // element or an ancestor (e.g. <div id="tab_4"><dx-button>Documents</dx-button></div>, or the Address item of the
      // Demographics drop-down); the framework navigates screens by that id, so log it as a tab, before options/buttons
      // list items first: a menu item may carry (duplicated) tab ids, so it must not be taken for a tab bar click
      const opt = raw.closest('.dx-list-item, [role=option], .dx-menu-item');
      if (opt) { const now = Date.now(); const ae = document.activeElement && /INPUT/.test(document.activeElement.tagName) && !document.activeElement.readOnly ? document.activeElement : null;
        const fieldList = opt.closest('.dx-dropdowneditor-overlay, .dx-selectbox-popup-wrapper, .dx-dropdownlist-popup-wrapper, .dx-tagbox-popup-wrapper, .dx-autocomplete-popup-wrapper, .dx-lookup-popup-wrapper') && !opt.closest('.dx-dropdownbutton-popup-wrapper');
        const btnLast = lastBtn && now - lastBtn.at < 15000 && (!lastInput || lastBtn.at > lastInputAt);
        // A20: an option from a menu opened by a button (Demographics / Address selector) is a menu choice, never a field value
        if (opt.closest('.dx-dropdownbutton-popup-wrapper, .dx-menu, .dx-context-menu') || (btnLast && !ae && !fieldList)) {
          const ids = [opt, ...opt.querySelectorAll('[id]')].map(n => n.id).filter(goodId);
          const tabId = ids.find(i => TAB_ID_RE.test(i)) || ''; const own = ids.find(i => !TAB_ID_RE.test(i)) || '';
          const dup = tabId ? document.querySelectorAll('[id="' + tabId + '"]').length > 1 : false;
          if (lastBtn && lastBtn.entry.act === 'click') { lastBtn.entry.act = 'menu_open'; try { localStorage.qaos_log = JSON.stringify(Q.log); } catch (x) {} }
          return rec({ act: 'menu_option', src: 'watch', value: txt(opt), id: own, tabId: dup ? '' : tabId, dupTabId: dup ? tabId : undefined,
            menu: lastBtn && btnLast ? lastBtn.entry.id : '', menuLocator: lastBtn && btnLast ? lastBtn.entry.locator : '' }); }
        const owner = ae || (lastInput && now - lastInputAt < 30000 ? lastInput : null);
        if (owner) focusVal.set(owner, '\u0000picked');  // the field's later focusout is the same choice, not a typed value
        return rec({ act: 'option', src: 'watch', value: txt(opt), label: owner ? labelOf(owner) : '', id: owner ? owner.id : '', locator: owner ? sel(owner) : '', widget: owner ? widgetOf(owner) : '', grid: owner && cellInfo(owner) ? cellInfo(owner).grid : undefined }); }
      const tabHost = tabIdHost(raw);
      // a tab host with no text is the drop-down toggle beside a tab (A20): logged below as a button click
      const worded = x => /[A-Za-z0-9]/.test(txt(x));   // an icon or arrow only (e.g. a caret) is no text
      if (tabHost && (worded(tabHost) || worded(raw))) return rec({ act: 'tab', src: 'watch', value: txt(tabHost) || txt(raw), id: tabHost.id, locator: '#' + tabHost.id, via: tabHost === raw ? 'self' : 'ancestor-id' });
      // sidebar menu entry (navigation): record its id and visible text so the flow's menu navigation is captured
      const menu = raw.closest('a.sub-menu-links, li.menu-child-node, [id^="DYL_"], li[id][class*=menu]');
      if (menu && !raw.closest('.dx-datagrid')) { const li = menu.closest('li[id]') || menu;
        return rec({ act: 'nav_click', src: 'watch', value: txt(menu), id: li.id || menu.id || '', locator: sel(li.id ? li : menu), search: (document.querySelector('input[name=filterText]') || {}).value || '' }); }
      const tab = raw.closest('[role=tab], .dx-tab, .nav-link, .nav-tabs a, .nav-tabs li');
      if (tab) { const a = tab.querySelector && tab.querySelector('a') || tab;
        return rec({ act: 'tab', src: 'watch', value: txt(tab), id: tab.id || a.id || '', locator: sel(tab.id ? tab : a), controls: tab.getAttribute('aria-controls') || a.getAttribute('href') || '' }); }
      const chk = raw.closest('.dx-checkbox, .dx-select-checkbox, input[type=checkbox]');
      if (chk) { const cell = cellInfo(chk); return rec(Object.assign({ act: 'check', src: 'watch', id: chk.id || '', locator: sel(chk), label: labelOf(chk) }, cell || {})); }
      const b = raw.closest('button, a, dx-button, .dx-button, [role=button], .dx-link') || (tabHost && !worded(tabHost) ? tabHost : null);
      // A20: a click on a grid data row (select / open a record): logged with the row key, not dropped
      const dr = raw.closest('tr.dx-data-row');
      if (dr && (!b || !dr.contains(b)) && !raw.closest('input, textarea')) { const td = raw.closest('td[aria-colindex]'); const ci = (td && cellInfo(td)) || {};
        const rid = rowCellId(raw, dr);
        return rec(Object.assign({ act: 'row_select', src: 'watch', grid: ci.grid || '', rowindex: dr.getAttribute('aria-rowindex'), column: td ? labelOf(td) : '', value: td ? txt(td) : '', clicks: e.detail || 1 },
          rid ? { id: rid, locator: '#' + rid } : {}, rowKey(dr))); }
      if (b && cellInfo(b)) Q._rowSnap(b);
      if (b) { const cell = cellInfo(b); const h = stableHost(b); const id = h ? h.id : '';
        const entry = rec(Object.assign({ act: 'click', src: 'watch', target: txt(b) || id || b.id, id, text: txt(b), locator: h ? '#' + h.id : sel(b), kind: '0004' },
          b.id && !goodId(b.id) ? { generatedId: b.id } : {}, h && h !== b ? { idFrom: 'ancestor' } : {}, cell ? { grid: cell.grid, rowindex: cell.rowindex } : {}));
        lastBtn = { at: Date.now(), entry }; return entry; }
    }, true);
    // A20: double click on a grid row (opens the record on some screens)
    document.addEventListener('dblclick', e => { if (Q._quiet) return; const raw = e.target; const dr = raw && raw.closest && raw.closest('tr.dx-data-row'); if (!dr) return;
      const td = raw.closest('td[aria-colindex]'); const ci = (td && cellInfo(td)) || {};
      rec(Object.assign({ act: 'row_open', src: 'watch', grid: ci.grid || '', rowindex: dr.getAttribute('aria-rowindex'), column: td ? labelOf(td) : '', value: td ? txt(td) : '' }, rowKey(dr))); }, true);
    // toasts and in-page popups/modals
    const seen = new Set(); const toastNodes = new WeakSet(); const toastAt = {};
    new MutationObserver(() => {
      // A20: one entry per toast element; the same text again within 2.5 s is the same message re-rendered
      document.querySelectorAll('.dx-toast-message, .toast-message').forEach(x => { const t = txt(x); if (!t || toastNodes.has(x)) return; toastNodes.add(x);
        const now = Date.now(); if (toastAt[t] && now - toastAt[t] < 2500) { toastAt[t] = now; return; } toastAt[t] = now;
        const box = x.closest('.dx-toast-content, .toast'); rec({ act: 'toast', src: 'watch', messages: [t], type: box ? (box.className.match(/dx-toast-(success|error|warning|info)/) || [])[1] || '' : '' }); });
      document.querySelectorAll('.modal.show .modal-content, .modal[style*="display: block"] .modal-content, .dx-popup-wrapper .dx-overlay-content').forEach(m => { if (!vis(m)) return;
        if (m.querySelector('.dx-list, .dx-scrollview, .dx-calendar, .dx-treeview, .dx-datagrid') || m.closest('.dx-dropdowneditor-overlay, .dx-selectbox-popup-wrapper, .dx-dropdownlist-popup-wrapper')) return;  // option lists / pickers, not messages
        if (!m.querySelector('.modal-title, .dx-popup-title, .modal-header, button, .dx-button')) return;
        const t = txt(m).replace(/\s+/g, ' ').slice(0, 300); if (!t || seen.has('P' + t)) return; seen.add('P' + t);
        const title = txt(m.querySelector('.modal-title, .dx-popup-title, .modal-header') || {}).replace(/\s+/g, ' ');
        const body = m.querySelector('.modal-body, .dx-popup-content'); const msgEl = body || m;
        rec({ act: 'popup', src: 'watch', title, text: txt(msgEl).replace(/\s+/g, ' ').slice(0, 300), locator: sel(msgEl), buttons: [...m.querySelectorAll('button, .dx-button, a.btn')].filter(vis).map(x => ({ text: txt(x), id: x.id || '', locator: sel(x) })) }); });
    }).observe(document.body, { childList: true, subtree: true });
    // browser dialogs: log the text, then behave exactly as before
    ['alert', 'confirm', 'prompt'].forEach(k => { const orig = window[k]; if (orig.__qaos) return;
      const w = function (msg) { rec({ act: 'alert', src: 'watch', dialog: k, text: String(msg) }); const r = orig.apply(window, arguments); if (k !== 'alert') rec({ act: 'alert_result', src: 'watch', dialog: k, result: r }); return r; };
      w.__qaos = true; window[k] = w; });
    return 'watcher on';
  };
  // helper actions are already logged by themselves: keep the watcher quiet while they run
  ['text', 'pick', 'click', 'clickCapture', 'tab', 'open'].forEach(k => { const f = Q[k]; if (!f || f.__q) return;
    Q[k] = async function () { Q._quiet = true; try { return await f.apply(Q, arguments); } finally { Q._quiet = false; } }; Q[k].__q = true; });
  Q.watch();
})();
