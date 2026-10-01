#!/usr/bin/env python3
"""build_atlas.py - build the machine-readable "flow atlas" of the selenium-framework DB.

Input : ../knowledge/framework_atlas/raw/*.json   (row dumps of the fct_pr_* tables, no passwords)
Output: ../knowledge/framework_atlas/
          atlas.json          groups -> chains, flows, screens (fields + events), repos, dependencies
          INDEX.json          tags per flow (business area, market, screens, repos, groups) for selective loading
          reverse_index.json  menu option / screen name / flow text -> flows and groups
          anomalies.json      integrity findings (orphans, missing refs, inactive rows, ...)
          flows/<flow>.json   full embedded detail of one flow (fields + events per screen)
          flows/<flow>.md     one-page plain-language read-out per flow
          group_<id>.md       the whole cycle of a group as a numbered business story
          validation.json     group 11 chain vs the live SQL capture (raw/_validation_group11_sql.json)

Usage : python build_atlas.py            build everything
        python build_atlas.py --find "goods issue note"   look up flows/groups in reverse_index.json

Read-only w.r.t. the DB and the framework: this script only reads raw/*.json and the qa-os docs.
Every claim carries a "src" string: <table-short>:<key>, e.g. "sef:0010000101|serial 12".
Table shorts: gtf, gtfd, tf, tfd, mg, mgsm, sc, sf, sef, ce, cmpt, sq, app, lu, alg, toast.
"""
import argparse
import collections
import datetime
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNOW = os.path.normpath(os.path.join(HERE, "..", "knowledge"))
OUT = os.path.join(KNOW, "framework_atlas")
RAW = os.path.join(OUT, "raw")
NOTES_DIR = os.path.join(KNOW, "framework_flows")
PROFILE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "framework", "casedata_profile.json"))

DEFAULT_WORKBOOK_NOTE = "(app default workbook)"

# ------------------------------------------------------------------ loading

def load(name):
    with open(os.path.join(RAW, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def by(rows, key):
    d = {}
    for r in rows:
        d[r[key]] = r
    return d


def group_by(rows, key):
    d = collections.defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


def num(x, default=0):
    try:
        return int(x)
    except (TypeError, ValueError):
        return default


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", (s or "").lower())).strip()


ENGINE_REPOS = {"LOGIN_USERNAME", "LOGIN_PASSWORD", "SELECTED_DIST"}


def canon_repo(x):
    x = (x or "").strip().upper()
    return x[2:] if x.startswith("G_") else x

# ------------------------------------------------------------------ vocab

EVENT_KIND = {
    ("0000", "0001"): "load_data", ("0000", "0002"): "verification", ("0000", "0003"): "refresh",
    ("0000", "0004"): "toast_record", ("0000", "0005"): "q2q_verification", ("0000", "0006"): "wait",
    ("0000", "0007"): "screen_validation", ("0000", "0012"): "fill_repo", ("0000", "0013"): "assertion",
    ("0000", "0014"): "group_assertion", ("0000", "0015"): "checkbox_click", ("0000", "0016"): "mobile_calendar",
    ("0000", "0017"): "search_and_row_click", ("0000", "0018"): "swipe_left", ("0000", "0019"): "swipe_right",
    ("0000", "0021"): "file_upload", ("0000", "0023"): "flow_control", ("0000", "0025"): "frame_switch",
    ("0001", "0001"): "fill_text", ("0002", "0001"): "fill_dropdown", ("0003", "0001"): "fill_date",
    ("0004", "0002"): "click", ("0004", "0003"): "long_click", ("0005", "0002"): "alert_click",
    ("0015", "0001"): "fill_alert",
}
PARENT_CAPABLE = {"load_data": "per_row_child", "assertion": "assertion_branch", "group_assertion": "assertion_branch",
                  "flow_control": "flow_control_child"}

AREA_RULES = [
    ("Login/Logout", r"\blogin\b|\blogout\b|user login"),
    ("Dispatch Advice", r"dispatch advice|dispatch_advice|\bDA\b|dis advice|transfer.?in.?da|post modification da"),
    ("Order Booking", r"order booking|order_booking|\bOB\b|book"),
    ("Order Editing", r"order editing|editing after|order edit"),
    ("Order Cancellation", r"order cancell"),
    ("Stock Allocation", r"stock allocation|stock unallocation|unallocation"),
    ("Delivery Date Change", r"delivery date change"),
    ("GIN (Goods Issue Note)", r"goods issue|good issue|\bgin\b|gin/grn|goods issue n"),
    ("GRN (Goods Return Note)", r"return note|\bgrn\b"),
    ("Sales Return", r"sales return|sale return|sales_return|fresh.?sales.?return|fresh return"),
    ("Cashmemo", r"cash ?memo"),
    ("Deposit Slip", r"deposit slip"),
    ("Route Settlement", r"route settlement|offset amount"),
    ("Cheque", r"cheque status"),
    ("DSR/PJP/Route", r"\bdsr\b|\bpjp\b|delivery man|daily visit"),
    ("Stock Adjustment (SAN)", r"\bsan\b|stock adjustment"),
    ("Stock Validation/Inquiry", r"stock valid|stock inq|opening & closing|otc stock out|stock zero|free sku stock|stock master"),
    ("Transaction Inquiry", r"transaction inq|trans inq|transection|trans_val|inquiryval|trans section|charges valid|amounts? valid|received amount valid"),
    ("Claims", r"claim"),
    ("Promotion", r"promo"),
    ("Charges/Tax", r"charge|\btax\b"),
    ("Debit/Credit Note", r"debit|credit note"),
    ("Approval/Reject/Terminate", r"approv|reject|terminat|appr\b"),
    ("Master/Setup", r"asset|outlet|prospect|section|vehicle|vehical|warehouse|distributor|product|analysis|analaysis|selling category|"
                     r"segment|frequency|target|\blocation\b|user profile|role_option|validation (header|setup)|business class|"
                     r"company mapping|configuration|change track|profile|non unilever|nup|insurance|charges$"),
    ("Negative test", r"negative|\breject"),
]
AREA_RX = [(a, re.compile(rx, re.I)) for a, rx in AREA_RULES]

MARKET_RULES = [
    ("VN", r"\bvn\b|vietnam"), ("PH", r"\bph\b|\bphp\b|philip"), ("BD", r"\bbd\b|bangla|\bbg\b"), ("KH", r"\bkh\b"),
    ("LA", r"\bla\b"), ("TH", r"\bth\b|thai|ithd|_thi\b"), ("Astron", r"astron"), ("UP", r"\bup\b|up_coming|upcoming"),
    ("PK", r"\bpak\b|\bpk\b"),
]
MARKET_RX = [(m, re.compile(rx, re.I)) for m, rx in MARKET_RULES]
BASE_PATH_VARIANT = {"PAK_QA": "Pak", "PHP_QA": "PHP", "BD_QA": "Bangla", "VN_QA": "Vietnam"}
VARIANT_FILE = {"Pak": "NG_Dcode_QA_OTC (Pak).xlsx", "PHP": "NG_Dcode_QA_OTC (PHP).xlsx",
                "Bangla": "NG_Dcode_QA_OTC (Bangla).xlsx", "Vietnam": "NG_Dcode_QA_OTC (Vietnam).xlsx",
                "default": "NG_Dcode_QA_OTC.xlsx"}


def areas_of(text):
    res = []
    for a, rx in AREA_RX:
        if rx.search(text or ""):
            res.append(a)
    return res


def market_of(text):
    for m, rx in MARKET_RX:
        if rx.search(text or ""):
            return m
    return None

# ------------------------------------------------------------------ model build


class Atlas:
    def __init__(self):
        L = load
        self.gtf = L("fct_pr_gtf_group_test_flow")
        self.gtfd = L("fct_pr_gtfd_group_test_flow_detail")
        self.tf = L("fct_pr_tf_test_flow")
        self.tfd = L("fct_pr_tfd_test_flow_details")
        self.mg = L("fct_pr_mg_menu_group")
        self.mgsm = L("fct_pr_mgsm_menu_group_screen_mapping")
        self.sc = L("fct_pr_sc_screens")
        self.sf = L("fct_pr_sf_screen_field")
        self.sef = L("fct_pr_sef_screen_events_flow")
        self.ce = L("fct_pr_ce_component_event")
        self.cmpt = L("fct_pr_cmpt_component_type")
        self.sq = L("fct_pr_sq_screen_query")
        self.app = L("fct_pr_app_application")
        self.lu = L("fct_pr_lu_login_users")
        self.alg = L("fct_pr_alg_app_allowable_groups")
        try:
            self.toast = L("fct_rp_set_screen_event_toast")
        except OSError:
            self.toast = []
        self.tf_by = by(self.tf, "ptf_testflowid")
        self.mg_by = by(self.mg, "pmg_menugroupid")
        self.sc_by = by(self.sc, "psc_screenid")
        self.lu_by = by(self.lu, "plu_serial_no")
        self.app_by = by(self.app, "papp_app_id")
        self.cmpt_by = by(self.cmpt, "pcmpt_componenttypeid")
        self.ce_by = {(r["pcmpt_componenttypeid"], r["pce_comp_event"]): r for r in self.ce}
        self.gtf_by = by(self.gtf, "pgtf_grouptestflowid")
        self.tfd_by_flow = group_by(self.tfd, "ptf_testflowid")
        self.mgsm_by_mg = group_by(self.mgsm, "pmg_menugroupid")
        self.sf_by_sc = group_by(self.sf, "psc_screenid")
        self.sef_by_sc = group_by(self.sef, "psc_screenid")
        self.sq_by_sc = group_by(self.sq, "psc_screenid")
        self.gtfd_by_group = group_by(self.gtfd, "pgtf_grouptestflowid")
        self.alg_by_group = group_by(self.alg, "pgtf_grouptestflowid")
        self.toast_by_sc = collections.defaultdict(collections.Counter)
        for r in self.toast:
            self.toast_by_sc[r["psc_screenid"]][(r["pset_message"] or "")[:200]] += 1
        self.profile = None
        if os.path.exists(PROFILE):
            with open(PROFILE, encoding="utf-8") as f:
                self.profile = json.load(f)
        self.notes = self._load_notes()
        self.screens = {}
        self.flows = {}
        self.groups = {}
        self.anomalies = collections.defaultdict(list)

    # ---- live notes (from replay logs)
    def _load_notes(self):
        notes = []
        if not os.path.isdir(NOTES_DIR):
            return notes
        for fn in sorted(os.listdir(NOTES_DIR)):
            if fn.endswith(".md"):
                with open(os.path.join(NOTES_DIR, fn), encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        line = line.rstrip()
                        if line:
                            notes.append((fn, i, line))
        return notes

    def notes_for(self, flow_id, screen_ids, mg_id, desc):
        ids = [flow_id] + [s for s in screen_ids if len(s) >= 6]
        rx = re.compile(r"(?<![0-9])(" + "|".join(re.escape(i) for i in ids) + r")(?![0-9])")
        mgrx = re.compile(r"\b(mg|menu group|menu-group)\s*" + re.escape(mg_id or "@@") + r"\b", re.I) if mg_id else None
        out = []
        for fn, i, line in self.notes:
            if rx.search(line) or (mgrx and mgrx.search(line)):
                out.append({"src": "%s:%d" % (fn, i), "text": line[:400]})
            if len(out) >= 14:
                break
        return out

    # ---- screens
    def build_screen(self, sid):
        if sid in self.screens:
            return self.screens[sid]
        sc = self.sc_by.get(sid)
        fields = []
        for r in sorted(self.sf_by_sc.get(sid, []), key=lambda r: (num(r["psf_sequenceno"]), r["psf_fieldid"])):
            ctype = r["pcmpt_componenttypeid"]
            fields.append({
                "src": "sf:%s|%s|%s|%s|%s" % (sid, r["psf_fieldid"], r["prv_version"], r["psf_sequenceno"], r["psf_iteration_number"]),
                "seq": r["psf_sequenceno"], "field_id": r["psf_fieldid"], "locate_by": r["psf_locateby"],
                "label": r["psf_field_db_column"], "db_column": r["psf_field_db_column"],
                "component_type": ctype, "component_name": (self.cmpt_by.get(ctype) or {}).get("pcmp_description"),
                "fixed_value": r["psf_fixed_value"], "mandatory": r["psf_mandatory_field"] == "Y",
                "value_source": r["psf_field_source"] or "EXCEL(default)", "repo_id": r["psf_repoid"],
                "sub_field_id": r["psf_subfieldid"], "extra_config": r["psf_extra_config"],
                "iteration": r["psf_iteration_number"], "version": r["prv_version"],
                "check_assertion": r["psf_check_assertion"] == "Y", "assertion_type": r["psf_assertion_type"],
                "wait_s": r["psef_field_waitingtime"], "status": r["psf_field_status"], "addition": r["psf_field_addition"],
                "active": r["psf_field_status"] == "Y" and r["psf_field_addition"] == "+",
                "trace_key": "%s:f%s" % (sid, r["psf_sequenceno"]),
            })
        raw_ev = self.sef_by_sc.get(sid, [])
        serials = {r["psef_serialno"] for r in raw_ev}
        kind_by_serial = {}
        for r in raw_ev:
            kind_by_serial[r["psef_serialno"]] = EVENT_KIND.get((r["pcmpt_componenttypeid"], r["pce_comp_event"]), "unknown")
        children = collections.defaultdict(list)
        tops = []
        for r in raw_ev:
            ref = r["psef_ref_serialno"]
            if not ref or ref == r["psef_serialno"] or ref not in serials:
                tops.append(r)
                if ref and ref not in serials:
                    self.anomalies["sef_ref_missing_parent"].append({"src": "sef:%s|serial %s" % (sid, r["psef_serialno"]), "ref": ref})
            else:
                children[ref].append(r)
        keyf = lambda r: (num(r["psef_sequenceno"]), r["psef_serialno"])
        events = []

        def emit(r, depth, parent):
            t, e = r["pcmpt_componenttypeid"], r["pce_comp_event"]
            kind = EVENT_KIND.get((t, e), "unknown")
            active = r["psef_status"] in ("Y", "A")
            ref = r["psef_ref_serialno"]
            if parent is None:
                role = "top_level" if not ref else "orphan_ref_runs_top_level"
            else:
                pk = kind_by_serial[parent]
                role = PARENT_CAPABLE.get(pk, "NEVER_RUNS_parent_is_" + pk)
            ev = {
                "src": "sef:%s|serial %s" % (sid, r["psef_serialno"]), "serial": r["psef_serialno"], "seq": r["psef_sequenceno"],
                "depth": depth, "parent": parent, "type": t, "event": e, "kind": kind,
                "event_name": (self.ce_by.get((t, e)) or {}).get("pce_description"), "in_ce_table": (t, e) in self.ce_by,
                "desc": r["psef_desc"], "status": r["psef_status"], "active": active, "locate_by": r["psef_locateby"],
                "field_id": r["psef_fieldid"], "fixed_value": r["psef_fixed_value"], "fixed_value_type": r["psef_fixedvalue_type"] or None,
                "validation_type": r["psef_validationtype"], "mandatory_validation": r["psef_mandatory_validation"],
                "engine_role": role, "trace_key": "%s:e%s" % (sid, r["psef_serialno"]),
            }
            fv = r["psef_fixed_value"] or ""
            if kind == "assertion":
                ev["assertion"] = {"kind": fv or None, "target_element": r["psef_fieldid"]}
            elif kind == "group_assertion":
                a, _, sheet = fv.partition(",")
                ev["assertion"] = {"kind": a or None, "sheet": sheet.strip() or None}
            elif kind == "wait":
                ev["wait_s"] = fv or "1"
            events.append(ev)
            for c in sorted(children.get(r["psef_serialno"], []), key=keyf):
                emit(c, depth + 1, r["psef_serialno"])

        for r in sorted(tops, key=keyf):
            emit(r, 0, None)

        # ---- repos
        active_fill_repo = [e for e in events if e["kind"] == "fill_repo" and e["active"]]
        writes, reads = [], []
        if active_fill_repo:
            for f in fields:
                if f["active"] and f["repo_id"]:
                    writes.append({"repo": f["repo_id"], "canon": canon_repo(f["repo_id"]),
                                   "scope": "global(no PK prefix)" if (f["field_id"] or "").startswith("g_") else "per PK (<PK>_<repo>)",
                                   "field": f["label"], "field_id": f["field_id"],
                                   "src": [f["src"], active_fill_repo[0]["src"]]})
        for f in fields:
            if f["active"] and f["value_source"] == "REPO" and f["repo_id"]:
                reads.append({"repo": f["repo_id"], "canon": canon_repo(f["repo_id"]), "via": "field(REPO)", "target": f["label"], "src": [f["src"]]})
        for e in events:
            if e["active"] and e["fixed_value_type"] == "REPO" and e["fixed_value"]:
                reads.append({"repo": e["fixed_value"], "canon": canon_repo(e["fixed_value"]), "via": "event(fixedvalue_type=REPO)",
                              "target": e["field_id"], "src": [e["src"]]})
        has_q = any(e["active"] and e["kind"] in ("q2q_verification", "screen_validation") for e in events)
        sq_rows = []
        for q in self.sq_by_sc.get(sid, []):
            params = []
            for k in ("psq_qryparameters", "psq_qryparameters_target"):
                params += [p.strip() for p in (q[k] or "").split(",") if p.strip()]
            sq_rows.append({"src": "sq:%s|%s|%s" % (sid, q["prv_version"], q["psn_serialno"]), "type": q["psq_validationtype"] or "SCREEN(default)",
                            "is_verification": q["psv_isverification"], "description": q["psq_qrydesc"], "params": params,
                            "params_target": [p.strip() for p in (q["psq_qryparameters_target"] or "").split(",") if p.strip()],
                            "has_target_query": bool(q["psq_query_target"])})
            if has_q and q["psq_validationtype"] == "Q2Q":
                for p in params:
                    reads.append({"repo": p, "canon": canon_repo(p), "via": "sq_param(Q2Q)", "target": q["psq_qrydesc"],
                                  "src": ["sq:%s|%s|%s" % (sid, q["prv_version"], q["psn_serialno"])]})
        name = sc["psc_screenname"] if sc else None
        scr = {
            "src": "sc:%s" % sid, "screen_id": sid, "name": name, "sheet": name, "type": sc["psc_screentype"] if sc else None,
            "sheet_name_len": len(name or ""), "exists_in_sc": sc is not None,
            "fields": fields, "events": events, "queries": sq_rows, "repo_writes": writes, "repo_reads": reads,
            "counts": {"fields": len(fields), "fields_active": sum(1 for f in fields if f["active"]),
                       "events": len(events), "events_active": sum(1 for e in events if e["active"])},
            "assertion_sheets": sorted({e["assertion"]["sheet"] for e in events if e["active"] and e.get("assertion", {}).get("sheet")}),
            "observed_toasts_event0004": [{"message": m, "count": c} for m, c in self.toast_by_sc.get(sid, collections.Counter()).most_common(8)],
        }
        self.screens[sid] = scr
        return scr

    # ---- flows
    def build_flow(self, fid):
        tf = self.tf_by.get(fid)
        tfd_rows = sorted(self.tfd_by_flow.get(fid, []), key=lambda r: num(r["ptfd_sequenceno"]))
        f = {"src": "tf:%s" % fid, "flow_id": fid, "description": tf["ptf_description"] if tf else None, "exists_in_tf": tf is not None,
             "status": tf["ptf_status"] if tf else None, "test_type": tf["ptt_testtypeid"] if tf else None,
             "master_app_id": tf["master_app_id"] if tf else None,
             "tfd": [{"src": "tfd:%s|%s|%s" % (fid, r["pmg_menugroupid"], r["ptfd_sequenceno"]), "seq": r["ptfd_sequenceno"],
                      "menu_group": r["pmg_menugroupid"], "filename": r["ptfd_filename"] or None} for r in tfd_rows]}
        f["menus"], f["screens_exec"], f["screen_ids"] = [], [], []
        flow_files = []
        for r in tfd_rows:
            mgid = r["pmg_menugroupid"]
            mg = self.mg_by.get(mgid)
            f["menus"].append({"src": "mg:%s" % mgid, "menu_group": mgid, "exists": mg is not None,
                               "description": mg["pmg_description"] if mg else None, "search_text": mg["pmg_searchtext"] if mg else None,
                               "navigation": mg["pmg_navigation"] if mg else None, "navigation_type": mg["pmg_navigation_type"] if mg else None})
            rows = sorted(self.mgsm_by_mg.get(mgid, []), key=lambda x: (num(x["pmgsm_sequenceno"]), x["psc_screenid"]))
            top = [x for x in rows if not x["pmgsm_parent_screenid"]]
            kids = group_by([x for x in rows if x["pmgsm_parent_screenid"]], "pmgsm_parent_screenid")

            def ent(x, child_of=None):
                wb = r["ptfd_filename"] or x["pmgsm_screen_filename"] or None
                wb_src = "tfd.ptfd_filename" if r["ptfd_filename"] else ("mgsm.pmgsm_screen_filename" if x["pmgsm_screen_filename"] else "default")
                scr = self.build_screen(x["psc_screenid"])
                if x["psc_screenid"] not in f["screen_ids"]:
                    f["screen_ids"].append(x["psc_screenid"])
                return {"src": "mgsm:%s|%s|%s" % (mgid, x["psc_screenid"], x["pmgsm_sequenceno"]), "mgsm_seq": x["pmgsm_sequenceno"],
                        "screen_id": x["psc_screenid"], "screen_name": scr["name"], "sheet": scr["name"],
                        "runs": x["pmgsm_status"] in (None, "Y"), "mgsm_status": x["pmgsm_status"], "child_of": child_of,
                        "tab_nav_type": x["pmgsm_navigation_type"], "tab_nav_path": x["pmgsm_navigation_path"],
                        "workbook": wb or DEFAULT_WORKBOOK_NOTE, "workbook_source": wb_src,
                        "workbook_filename_status": x["pmgsm_screen_filename_status"]}

            idx = 0
            for x in top:
                e = ent(x)
                idx += 1
                e["exec_index"] = idx
                e["children"] = [ent(k, x["psc_screenid"]) for k in sorted(kids.get(x["psc_screenid"], []), key=lambda k: (num(k["pmgsm_sequenceno"]), k["psc_screenid"]))]
                f["screens_exec"].append(e)
            # child mappings whose parent is not a top-level row of this menu group
            tops_ids = {x["psc_screenid"] for x in top}
            for pid, ks in kids.items():
                if pid not in tops_ids:
                    self.anomalies["mgsm_child_parent_not_top_level"].append({"src": "mgsm:%s|parent %s" % (mgid, pid), "flow": fid})
                    for k in ks:
                        self.build_screen(k["psc_screenid"])
                        if k["psc_screenid"] not in f["screen_ids"]:
                            f["screen_ids"].append(k["psc_screenid"])
            if r["ptfd_filename"]:
                flow_files.append(r["ptfd_filename"])
        # workbook / sheets
        wb_names = sorted({e["workbook"] for e in f["screens_exec"]} | {c["workbook"] for e in f["screens_exec"] for c in e["children"]})
        f["workbook"] = {"flow_level_filename": flow_files[0] if flow_files else None, "effective_files": wb_names,
                         "rule": "ptfd_filename, else pmgsm_screen_filename, else app default (runtime.md 2.3)"}
        sheets = collections.OrderedDict()
        for sid in f["screen_ids"]:
            s = self.screens[sid]
            if s["name"]:
                sheets.setdefault(s["name"], {"sheet": s["name"], "kind": "screen", "screen_ids": []})["screen_ids"].append(sid)
            for sh in s["assertion_sheets"]:
                sheets.setdefault(sh, {"sheet": sh, "kind": "assertion(_ASSR)", "screen_ids": []})["screen_ids"].append(sid)
        if any(self.screens[s]["repo_reads"] or self.screens[s]["repo_writes"] for s in f["screen_ids"]):
            sheets.setdefault("GLOBAL-REPO", {"sheet": "GLOBAL-REPO", "kind": "global repo (optional, default workbook)", "screen_ids": []})
        f["sheets"] = list(sheets.values())
        f["sheet_name_over_31"] = [s["sheet"] for s in f["sheets"] if len(s["sheet"]) > 31]
        f["workbook_coverage"] = self.coverage(f)
        mx = max([v["ratio"] for v in f["workbook_coverage"].values()] or [0])
        f["best_sample_workbooks"] = [k for k, v in f["workbook_coverage"].items() if mx > 0 and v["ratio"] == mx]
        # repos
        w, rd = [], []
        for sid in f["screen_ids"]:
            w += [dict(x, screen_id=sid) for x in self.screens[sid]["repo_writes"]]
            rd += [dict(x, screen_id=sid) for x in self.screens[sid]["repo_reads"]]
        f["repos"] = {"writes": w, "reads": rd,
                      "writes_canon": sorted({x["canon"] for x in w}), "reads_canon": sorted({x["canon"] for x in rd}),
                      "reads_not_written_by_this_flow": sorted({x["canon"] for x in rd} - {x["canon"] for x in w}),
                      "note": "Excel repo_* columns and GLOBAL-REPO rows are inside the workbooks and are not visible in the DB"}
        # assertions / counts
        ev = [e for sid in f["screen_ids"] for e in self.screens[sid]["events"] if e["active"]]
        c = collections.Counter(e["kind"] for e in ev)
        f["assertions"] = {
            "message_assertions_0013": [dict(e["assertion"], screen_id=sid, src=e["src"]) for sid in f["screen_ids"] for e in self.screens[sid]["events"] if e["active"] and e["kind"] == "assertion"],
            "group_assertions_0014": [dict(e["assertion"], screen_id=sid, src=e["src"]) for sid in f["screen_ids"] for e in self.screens[sid]["events"] if e["active"] and e["kind"] == "group_assertion"],
            "validations_0007": c["screen_validation"], "q2q_0005": c["q2q_verification"], "toast_records_0004": c["toast_record"],
            "flow_control_0023": c["flow_control"]}
        f["counts"] = {"screens": len(f["screen_ids"]), "fields": sum(self.screens[s]["counts"]["fields"] for s in f["screen_ids"]),
                       "fields_active": sum(self.screens[s]["counts"]["fields_active"] for s in f["screen_ids"]),
                       "events": sum(self.screens[s]["counts"]["events"] for s in f["screen_ids"]), "events_active": len(ev),
                       "events_by_kind": dict(c)}
        mg0 = f["menus"][0] if f["menus"] else {}
        text = " ; ".join(filter(None, [f["description"], mg0.get("description"), mg0.get("search_text")]))
        f["tags"] = {"areas": areas_of(text) or ["Other"], "market": market_of(f["description"] or ""),
                     "menu_option": mg0.get("navigation"), "menu_search_text": mg0.get("search_text")}
        f["live_notes"] = self.notes_for(fid, f["screen_ids"], mg0.get("menu_group"), f["description"])
        return f

    def coverage(self, f):
        """per sample workbook: which of the flow's sheets exist, rows, and missing columns (market differences)."""
        if not self.profile:
            return {}
        res = {}
        for wbname, sheets in self.profile.items():
            low = {k.lower(): k for k in sheets}
            info = {"sheets_present": 0, "sheets_total": len(f["sheets"]), "missing_sheets": [], "missing_columns": {}, "rows": {}}
            for sh in f["sheets"]:
                if sh["kind"].startswith("global"):
                    continue
                key = sh["sheet"] if sh["sheet"] in sheets else low.get(sh["sheet"].lower())
                if key is None:
                    info["missing_sheets"].append(sh["sheet"])
                    continue
                info["sheets_present"] += 1
                info["rows"][sh["sheet"]] = sheets[key].get("rows")
                if sh["kind"] == "screen":
                    heads = {h.lower() for h in sheets[key].get("headers", []) if h}
                    miss = []
                    for sid in sh["screen_ids"]:
                        for fl in self.screens[sid]["fields"]:
                            if fl["active"] and fl["component_type"] != "0010" and fl["value_source"] in ("EXCEL(default)", "EXCEL") \
                                    and fl["db_column"] and fl["db_column"].lower() not in heads and fl["db_column"] not in miss:
                                miss.append(fl["db_column"])
                    if miss:
                        info["missing_columns"][sh["sheet"]] = miss[:25]
            info["complete"] = not info["missing_sheets"]
            info["ratio"] = round(info["sheets_present"] / max(1, info["sheets_total"] - sum(1 for x in f["sheets"] if x["kind"].startswith("global"))), 3)
            res[wbname] = info
        return res

    # ---- groups
    def build_groups(self):
        # writers per flow, computed lazily
        for gid in sorted(self.gtf_by, key=num):
            g = self.gtf_by[gid]
            rows = sorted(self.gtfd_by_group.get(gid, []), key=lambda r: (num(r["pgtfd_sequenceno"]), r["ptf_testflowid"]))
            alg_apps = []
            for a in self.alg_by_group.get(gid, []):
                ap = self.app_by.get(a["papp_app_id"], {})
                bp = (ap.get("papp_base_path") or "")
                token = [t for t in re.split(r"[\\/]+", bp) if t]
                token = token[-1] if token else None
                alg_apps.append({"src": "alg:%s|%s" % (a["papp_app_id"], gid), "app_id": a["papp_app_id"], "app": ap.get("papp_description"),
                                 "url": ap.get("papp_url"), "base_path": bp or None, "db_name": ap.get("papp_app_db_name_only(credentials redacted)"),
                                 "login_flow": ap.get("ptf_testflowid_login"), "logout_flow": ap.get("ptf_testflowid_logout"),
                                 "workbook_variant_inferred": BASE_PATH_VARIANT.get(token or "", None)})
            chain, cur_user, cur_serial = [], None, None
            avail = {}
            login_flows = {a["ptf_testflowid_login"] for a in self.app if a.get("ptf_testflowid_login")}
            for r in rows:
                fid = r["ptf_testflowid"]
                flow = self.flows.get(fid)
                lstat = r["pgtf_testflow_login_status"]
                switch = lstat not in (None, "N")
                user = self.lu_by.get(r["plu_serial_no"]) if r["plu_serial_no"] is not None else None
                active = r["pgtfd_status"] == "Y"
                row = {"src": "gtfd:%s|%s|%s" % (gid, r["pgtfd_sequenceno"], fid), "seq": r["pgtfd_sequenceno"], "flow_id": fid,
                       "flow": (flow or {}).get("description"), "status": r["pgtfd_status"], "active": active,
                       "plu_serial_no": r["plu_serial_no"], "user": user["plu_name"] if user else None,
                       "user_app_id": user["papp_app_id"] if user else None,
                       "login_status": lstat, "login_action": ("SWITCH: logout+login as " + (user["plu_name"] if user else "?(no user)")) if switch else "same session",
                       "switch_user": switch, "app_switch": r["pgtf_testflow_appid"],
                       "trace_prefix": "%s:%s:%s" % (gid, r["pgtfd_sequenceno"], fid)}
                if active:
                    if switch:
                        row["user_changes"] = bool(user) and user["plu_serial_no"] != cur_serial
                        if user:
                            cur_user, cur_serial = user["plu_name"], user["plu_serial_no"]
                    row["effective_user"] = cur_user
                    if flow:
                        reads = flow["repos"]["reads"]
                        needs, seen = [], set()
                        own = set(flow["repos"]["writes_canon"])
                        for x in reads:
                            if x["canon"] in seen:
                                continue
                            seen.add(x["canon"])
                            if x["canon"] in own:
                                needs.append({"repo": x["repo"], "status": "produced_within_same_flow"})
                            elif x["canon"] in ENGINE_REPOS:
                                needs.append({"repo": x["repo"], "status": "engine_provided(login/distributor at run time)", "src": x["src"]})
                            elif x["canon"] in avail:
                                p = avail[x["canon"]]
                                needs.append({"repo": x["repo"], "status": "satisfied", "provided_by_seq": p[0], "provided_by_flow": p[1],
                                              "src": x["src"]})
                            else:
                                needs.append({"repo": x["repo"], "status": "UNRESOLVED_in_group(expected from workbook repo_ column, GLOBAL-REPO sheet or RepoValues.csv)",
                                              "src": x["src"]})
                        row["needs"] = needs
                        row["produces"] = sorted({x["repo"] for x in flow["repos"]["writes"]})
                        for x in flow["repos"]["writes"]:
                            avail[x["canon"]] = (r["pgtfd_sequenceno"], fid)
                chain.append(row)
            active_rows = [c for c in chain if c["active"]]
            first = active_rows[0]["flow_id"] if active_rows else None
            gr = {"src": "gtf:%s" % gid, "group_id": gid, "description": g["pgtf_description"], "status": g["ptgf_status"],
                  "test_type": g["ptt_testtypeid"], "master_app_id": g["master_app_id"],
                  "market_guess_from_description": market_of(g["pgtf_description"]) or ("PK(none in name)" if "Daily Cycle" in g["pgtf_description"] else None),
                  "allowable_apps": alg_apps,
                  "starts_with_app_login_flow": first in login_flows, "first_active_flow": first,
                  "counts": {"rows": len(chain), "active": len(active_rows), "inactive": len(chain) - len(active_rows),
                             "switch_points": sum(1 for c in active_rows if c["switch_user"]),
                             "distinct_flows_active": len({c["flow_id"] for c in active_rows})},
                  "switch_points": [c["seq"] for c in active_rows if c["switch_user"]],
                  "chain": chain}
            self.groups[gid] = gr

    # ---- anomalies
    def check(self):
        A = self.anomalies
        gflows = {r["ptf_testflowid"] for r in self.gtfd}
        for r in self.gtfd:
            if r["ptf_testflowid"] not in self.tf_by:
                A["gtfd_flow_missing_in_tf"].append({"src": "gtfd:%s|%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"], r["ptf_testflowid"])})
            if r["pgtf_grouptestflowid"] not in self.gtf_by:
                A["gtfd_group_missing_in_gtf"].append({"src": "gtfd:%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"])})
            if r["plu_serial_no"] is not None and r["plu_serial_no"] not in self.lu_by:
                A["gtfd_user_missing_in_lu"].append({"src": "gtfd:%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"]), "plu": r["plu_serial_no"]})
            ls = r["pgtf_testflow_login_status"]
            if ls not in (None, "N") and r["plu_serial_no"] is None:
                A["gtfd_login_Y_without_user"].append({"src": "gtfd:%s|%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"], r["ptf_testflowid"])})
            if ls == "N" and r["plu_serial_no"] is not None:
                A["gtfd_login_N_with_user_ignored"].append({"src": "gtfd:%s|%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"], r["ptf_testflowid"]), "note": "user ignored by engine: same session"})
            if r["pgtfd_status"] == "Y" and r["ptf_testflowid"] in self.tf_by and self.tf_by[r["ptf_testflowid"]]["ptf_status"] != "Y":
                A["gtfd_active_row_flow_inactive_in_tf"].append({"src": "gtfd:%s|%s|%s" % (r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"], r["ptf_testflowid"])})
        c = collections.Counter((r["pgtf_grouptestflowid"], r["pgtfd_sequenceno"]) for r in self.gtfd)
        for k, n in c.items():
            if n > 1:
                A["gtfd_duplicate_group_seq(two flows same seq)"].append({"group": k[0], "seq": k[1], "n": n})
        for gid in self.gtf_by:
            apps = {a["papp_app_id"] for a in self.alg_by_group.get(gid, [])}
            if not apps:
                A["group_without_allowable_app(alg)"].append({"src": "gtf:%s" % gid})
            if not self.gtfd_by_group.get(gid):
                A["group_without_rows"].append({"src": "gtf:%s" % gid})
            for r in self.gtfd_by_group.get(gid, []):
                u = self.lu_by.get(r["plu_serial_no"]) if r["plu_serial_no"] is not None else None
                if u and apps and u["papp_app_id"] not in apps and r["pgtfd_status"] == "Y" and r["pgtf_testflow_login_status"] not in (None, "N"):
                    A["switch_user_belongs_to_app_not_allowed_for_group"].append({"src": "gtfd:%s|%s" % (gid, r["pgtfd_sequenceno"]), "user": u["plu_name"], "user_app": u["papp_app_id"], "group_apps": sorted(apps)})
        for r in self.alg:
            if r["pgtf_grouptestflowid"] not in self.gtf_by:
                A["alg_group_missing"].append({"src": "alg:%s|%s" % (r["papp_app_id"], r["pgtf_grouptestflowid"])})
        for r in self.tf:
            fid = r["ptf_testflowid"]
            n = len(self.tfd_by_flow.get(fid, []))
            if n == 0:
                A["flow_without_tfd(not runnable)"].append({"src": "tf:%s" % fid, "desc": r["ptf_description"], "in_group": fid in gflows})
            if n > 1:
                A["flow_with_multiple_tfd(runs N times)"].append({"src": "tf:%s" % fid, "n": n})
            if r["ptf_status"] != "Y":
                A["flow_inactive_in_tf"].append({"src": "tf:%s" % fid, "in_group": fid in gflows})
        for r in self.tfd:
            if r["ptf_testflowid"] not in self.tf_by:
                A["tfd_flow_missing_in_tf"].append({"src": "tfd:%s" % r["ptf_testflowid"]})
            if r["pmg_menugroupid"] not in self.mg_by:
                A["tfd_menugroup_missing"].append({"src": "tfd:%s|%s" % (r["ptf_testflowid"], r["pmg_menugroupid"])})
            elif not self.mgsm_by_mg.get(r["pmg_menugroupid"]):
                A["tfd_menugroup_without_screens"].append({"src": "tfd:%s|%s" % (r["ptf_testflowid"], r["pmg_menugroupid"])})
        used_mg = {r["pmg_menugroupid"] for r in self.tfd}
        for r in self.mg:
            if r["pmg_menugroupid"] not in used_mg:
                A["menu_group_not_used_by_any_flow"].append({"src": "mg:%s" % r["pmg_menugroupid"], "desc": r["pmg_description"]})
        mapped = set()
        for r in self.mgsm:
            mapped.add(r["psc_screenid"])
            if r["psc_screenid"] not in self.sc_by:
                A["mgsm_screen_missing_in_sc"].append({"src": "mgsm:%s|%s" % (r["pmg_menugroupid"], r["psc_screenid"])})
            if r["pmg_menugroupid"] not in self.mg_by:
                A["mgsm_menugroup_missing"].append({"src": "mgsm:%s|%s" % (r["pmg_menugroupid"], r["psc_screenid"])})
            if r["pmgsm_status"] not in (None, "Y"):
                A["mgsm_inactive_rows"].append({"src": "mgsm:%s|%s|%s" % (r["pmg_menugroupid"], r["psc_screenid"], r["pmgsm_sequenceno"])})
        c = collections.Counter((r["pmg_menugroupid"], r["psc_screenid"]) for r in self.mgsm)
        for k, n in c.items():
            if n > 1:
                A["mgsm_same_screen_twice_in_menu_group(valid: e.g. re-search)"].append({"menu_group": k[0], "screen": k[1], "n": n})
        reach = set()
        for f in self.flows.values():
            reach.update(f["screen_ids"])
        for r in self.sc:
            if r["psc_screenid"] not in mapped:
                A["screen_without_mgsm_row(orphan)"].append({"src": "sc:%s" % r["psc_screenid"], "name": r["psc_screenname"]})
            if len(r["psc_screenname"] or "") > 31:
                A["screen_name_over_31_chars(excel sheet limit)"].append({"src": "sc:%s" % r["psc_screenid"], "name": r["psc_screenname"]})
        names = collections.defaultdict(list)
        for r in self.sc:
            names[norm(r["psc_screenname"])].append(r["psc_screenid"])
        A["screen_name_shared_by_several_screens(shared sheet)"] = [{"name": k, "screens": v} for k, v in names.items() if len(v) > 1][:60]
        for r in self.sf:
            if r["psc_screenid"] not in self.sc_by:
                A["sf_screen_missing"].append({"src": "sf:%s|%s" % (r["psc_screenid"], r["psf_fieldid"])})
            if r["pcmpt_componenttypeid"] not in self.cmpt_by:
                A["sf_component_type_unknown"].append({"src": "sf:%s|%s" % (r["psc_screenid"], r["psf_fieldid"]), "type": r["pcmpt_componenttypeid"]})
            if r["psf_field_status"] == "Y" and r["psf_field_addition"] != "+":
                A["sf_active_but_addition_not_plus(engine removes field)"].append({"src": "sf:%s|%s" % (r["psc_screenid"], r["psf_fieldid"])})
        for r in self.sef:
            k = (r["pcmpt_componenttypeid"], r["pce_comp_event"])
            if r["psc_screenid"] not in self.sc_by:
                A["sef_screen_missing"].append({"src": "sef:%s|serial %s" % (r["psc_screenid"], r["psef_serialno"])})
            if k not in self.ce_by and r["psef_status"] in ("Y", "A"):
                A["sef_active_pair_not_in_ce(silently dropped by engine)"].append({"src": "sef:%s|serial %s" % (r["psc_screenid"], r["psef_serialno"]), "pair": k})
            if r["psef_status"] in ("Y", "A") and not r["psef_desc"]:
                A["sef_active_with_null_desc(kills event cache)"].append({"src": "sef:%s|serial %s" % (r["psc_screenid"], r["psef_serialno"])})
            if r["psef_status"] not in ("Y", "N", "I"):
                A["sef_status_unusual"].append({"src": "sef:%s|serial %s" % (r["psc_screenid"], r["psef_serialno"]), "status": r["psef_status"]})
        for sid, s in self.screens.items():
            for e in s["events"]:
                if e["engine_role"].startswith("NEVER_RUNS") and e["active"]:
                    A["sef_active_event_parent_is_not_a_container(never runs)"].append({"src": e["src"], "role": e["engine_role"]})
        for r in self.sq:
            if r["psc_screenid"] not in self.sc_by:
                A["sq_screen_missing_in_sc"].append({"src": "sq:%s|%s|%s" % (r["psc_screenid"], r["prv_version"], r["psn_serialno"])})
        for r in self.toast:
            if r["psc_screenid"] not in self.sc_by:
                A["toast_screen_missing_in_sc"].append({"src": "toast:%s" % r["pset_serialno"], "screen": r["psc_screenid"]})
        # repo case variants + never-written
        writers, readers, variants = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
        for fid, f in self.flows.items():
            for x in f["repos"]["writes"]:
                writers[x["canon"]].add(fid); variants[x["canon"]].add(x["repo"])
            for x in f["repos"]["reads"]:
                readers[x["canon"]].add(fid); variants[x["canon"]].add(x["repo"])
        A["repo_id_spelling_variants(same key, different case/prefix)"] = [{"canon": k, "spellings": sorted(v)} for k, v in variants.items() if len(v) > 1]
        A["repo_read_but_never_written_by_any_flow(workbook/global/engine supplied)"] = [{"repo": k, "readers": sorted(v)[:8], "n_readers": len(v)} for k, v in readers.items() if k not in writers]
        A["repo_written_but_never_read"] = [{"repo": k, "writers": sorted(v)[:8]} for k, v in writers.items() if k not in readers]
        self.repo_writers, self.repo_readers = writers, readers
        # groups: unresolved needs
        for gid, g in self.groups.items():
            for c in g["chain"]:
                for n in c.get("needs", []):
                    if n["status"].startswith("UNRESOLVED"):
                        A["group_flow_repo_unresolved_in_chain"].append({"src": c["src"], "repo": n["repo"]})
            if g["counts"]["active"] and not g["starts_with_app_login_flow"]:
                A["group_does_not_start_with_an_app_login_flow"].append({"src": g["src"], "first_flow": g["first_active_flow"]})

# ------------------------------------------------------------------ writers


def md_escape(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def user_label(c):
    if c["switch_user"]:
        return "%s (serial %s)" % (c["user"] or "?", c["plu_serial_no"])
    return "same session (%s)" % (c["effective_user"] or "runner default login")


def flow_md(A, f):
    fid = f["flow_id"]
    L = []
    L.append("# Flow %s - %s" % (fid, f["description"] or "(flow row missing)"))
    L.append("")
    L.append("Status `%s`, test type `%s`, master app `%s`. Source: `%s`." % (f["status"], f["test_type"], f["master_app_id"], f["src"]))
    L.append("Business area (inferred from names): **%s**. Market tag (from name): **%s**." % (", ".join(f["tags"]["areas"]), f["tags"]["market"] or "none/PK default"))
    L.append("")
    L.append("## Where it is used")
    used = A.flow_groups.get(fid, [])
    if used:
        for u in used:
            L.append("- group %s (%s) seq %s, %s, user: %s" % (u["group"], u["group_desc"], u["seq"], "active" if u["active"] else "INACTIVE", u["user"]))
    else:
        L.append("- not referenced by any group")
    L.append("")
    L.append("## Navigation")
    for m in f["menus"]:
        L.append("- menu group `%s` (%s): type `%s` in the menu search, then click `%s` (%s). Source `%s`" % (
            m["menu_group"], m["description"], m["search_text"], m["navigation"], m["navigation_type"], m["src"]))
    if not f["menus"]:
        L.append("- **no tfd row: this flow cannot run** (`tfd` missing)")
    L.append("")
    L.append("## Screens in execution order")
    L.append("| # | screen | sheet (case-data) | tab nav | runs | workbook |")
    L.append("|---|---|---|---|---|---|")
    for e in f["screens_exec"]:
        L.append("| %s | `%s` %s | %s | %s %s | %s | %s |" % (e["exec_index"], e["screen_id"], md_escape(e["screen_name"]), md_escape(e["sheet"]), e["tab_nav_type"] or "", e["tab_nav_path"] or "", "yes" if e["runs"] else "NO (mgsm status %s)" % e["mgsm_status"], md_escape(e["workbook"])))
        for c in e["children"]:
            L.append("| ^ child | `%s` %s | %s | %s %s | %s | %s |" % (c["screen_id"], md_escape(c["screen_name"]), md_escape(c["sheet"]), c["tab_nav_type"] or "", c["tab_nav_path"] or "", "yes (inside parent row loop)" if c["runs"] else "NO", md_escape(c["workbook"])))
    L.append("")
    L.append("## What it does (auto-read-out from screen, field and event names)")
    for e in f["screens_exec"]:
        for s in [e] + e["children"]:
            scr = A.screens[s["screen_id"]]
            act = [x for x in scr["fields"] if x["active"]]
            fill = [x for x in act if x["component_type"] != "0010"]
            readable = [x for x in act if x["component_type"] == "0010"]
            clicks = [x for x in scr["events"] if x["active"] and x["kind"] in ("click", "long_click", "checkbox_click", "search_and_row_click")]
            parts = []
            if fill:
                parts.append("fills %d field(s): %s" % (len(fill), ", ".join("%s%s" % (x["label"], "*" if x["mandatory"] else "") for x in fill[:14]) + (" ..." if len(fill) > 14 else "")))
            if readable:
                parts.append("reads %d display field(s): %s" % (len(readable), ", ".join(x["label"] or x["field_id"] for x in readable[:8])))
            if clicks:
                parts.append("clicks %s" % ", ".join("`%s`" % (x["field_id"] or x["desc"]) for x in clicks[:10]))
            for x in scr["events"]:
                if x["active"] and x["kind"] == "assertion":
                    parts.append("asserts %s" % x["assertion"]["kind"])
                if x["active"] and x["kind"] == "group_assertion":
                    parts.append("asserts %s from sheet `%s`" % (x["assertion"]["kind"], x["assertion"]["sheet"]))
                if x["active"] and x["kind"] == "screen_validation":
                    parts.append("validates display values against workbook/DB (0007)")
                if x["active"] and x["kind"] == "q2q_verification":
                    parts.append("query-to-query data check (0005)")
                if x["active"] and x["kind"] == "fill_repo":
                    parts.append("stores document number(s) in repos (0012)")
            L.append("- `%s` %s: %s." % (scr["screen_id"], scr["name"], "; ".join(dict.fromkeys(parts)) if parts else "no active fields or events"))
    L.append("")
    L.append("## Data in / out (repos)")
    L.append("- writes: %s" % (", ".join("`%s`" % r for r in sorted({x["repo"] for x in f["repos"]["writes"]})) or "none"))
    L.append("- reads: %s" % (", ".join("`%s`" % r for r in sorted({x["repo"] for x in f["repos"]["reads"]})) or "none"))
    unres = f["repos"]["reads_not_written_by_this_flow"]
    if unres:
        L.append("- needs from an earlier flow / workbook: %s" % ", ".join("`%s`" % r for r in unres))
    for u in used:
        pass
    L.append("")
    L.append("## Assertions")
    a = f["assertions"]
    for x in a["message_assertions_0013"]:
        L.append("- 0013 `%s` on screen %s (%s)" % (x["kind"], x["screen_id"], x["src"]))
    for x in a["group_assertions_0014"]:
        L.append("- 0014 `%s` sheet `%s` on screen %s (%s)" % (x["kind"], x["sheet"], x["screen_id"], x["src"]))
    L.append("- validations 0007: %d, Q2Q 0005: %d, toast records 0004: %d, flow-control 0023: %d" % (a["validations_0007"], a["q2q_0005"], a["toast_records_0004"], a["flow_control_0023"]))
    for sid in f["screen_ids"]:
        ts = A.screens[sid]["observed_toasts_event0004"]
        if ts:
            L.append("- observed toasts recorded by event 0004 on %s: %s" % (sid, "; ".join("`%s` x%d" % (t["message"][:80], t["count"]) for t in ts[:4])))
    L.append("")
    L.append("## Case-data workbook")
    L.append("- effective file(s): %s" % ", ".join("`%s`" % w for w in f["workbook"]["effective_files"]))
    L.append("- sheets: %s" % ", ".join("`%s`" % s["sheet"] for s in f["sheets"]))
    if f["sheet_name_over_31"]:
        L.append("- WARNING sheet name over 31 chars: %s" % f["sheet_name_over_31"])
    if f["workbook_coverage"]:
        L.append("- best-fitting sample workbook(s): %s" % (", ".join("`%s`" % b for b in f["best_sample_workbooks"]) or "none of the 5 samples has this flow's sheets"))
        L.append("- market coverage in the 5 sample workbooks (sheets present / needed):")
        for wb, info in f["workbook_coverage"].items():
            L.append("  - `%s`: %d/%d%s" % (wb, info["sheets_present"], info["sheets_total"], "" if info["complete"] else " (missing: %s)" % ", ".join("`%s`" % m for m in info["missing_sheets"][:6])))
    L.append("")
    L.append("## Fields and events per screen")
    for sid in f["screen_ids"]:
        scr = A.screens[sid]
        L.append("### Screen `%s` %s (%s)" % (sid, scr["name"], scr["src"]))
        L.append("Fields (active/total %d/%d):" % (scr["counts"]["fields_active"], scr["counts"]["fields"]))
        for x in scr["fields"]:
            if not x["active"]:
                continue
            extra = []
            if x["mandatory"]: extra.append("mandatory")
            if x["fixed_value"]: extra.append("fixed=%s" % x["fixed_value"])
            if x["repo_id"]: extra.append("repo=%s(%s)" % (x["repo_id"], x["value_source"]))
            if x["extra_config"]: extra.append("extra=%s" % x["extra_config"])
            L.append("- %s. `%s` **%s** [%s %s]%s" % (x["seq"], x["field_id"], md_escape(x["label"]), x["component_type"], x["component_name"], (" - " + ", ".join(extra)) if extra else ""))
        L.append("Events (active only; indent = child of parent):")
        for e in scr["events"]:
            if not e["active"]:
                continue
            L.append("%s- e%s seq %s **%s** (%s/%s)%s%s%s" % ("  " * e["depth"], e["serial"], e["seq"], e["event_name"] or e["kind"], e["type"], e["event"],
                     (" `%s`" % e["field_id"]) if e["field_id"] else "", (" = `%s`" % e["fixed_value"]) if e["fixed_value"] else "",
                     (" [%s]" % e["fixed_value_type"]) if e["fixed_value_type"] else ""))
        L.append("")
    if f["live_notes"]:
        L.append("## Known live quirks (from framework_flows replay logs, verbatim lines)")
        for n in f["live_notes"]:
            L.append("- (%s) %s" % (n["src"], n["text"]))
    L.append("")
    L.append("Trace key format for this flow: `<group>:<seq>:%s:<screen>:e<event serial>`." % fid)
    return "\n".join(L) + "\n"


def group_md(A, g):
    L = []
    L.append("# Group %s - %s" % (g["group_id"], g["description"]))
    L.append("")
    L.append("Source `%s`. Market guess (from name): %s. Rows: %d (active %d, inactive %d). User switch points: %d (%s)." % (
        g["src"], g["market_guess_from_description"], g["counts"]["rows"], g["counts"]["active"], g["counts"]["inactive"], g["counts"]["switch_points"], ", ".join(str(s) for s in g["switch_points"]) or "none"))
    L.append("")
    L.append("Allowed apps (alg): " + ("; ".join("app %s %s -> %s (workbook variant inferred: %s)" % (a["app_id"], a["app"], a["base_path"], a["workbook_variant_inferred"]) for a in g["allowable_apps"]) or "none"))
    L.append("Starts with an app login flow: %s (first active flow %s)." % (g["starts_with_app_login_flow"], g["first_active_flow"]))
    L.append("")
    L.append("Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.")
    L.append("")
    L.append("## The cycle, step by step (active rows)")
    n = 0
    for c in g["chain"]:
        if not c["active"]:
            continue
        n += 1
        f = A.flows.get(c["flow_id"])
        areas = ", ".join(f["tags"]["areas"]) if f else "?"
        line = "%d. **seq %s - %s** (`%s`) - area: %s" % (n, c["seq"], c["flow"], c["flow_id"], areas)
        if c["switch_user"]:
            line += "\n   - **SWITCH USER POINT**: log out and log in as **%s** (serial %s)%s" % (c["user"], c["plu_serial_no"], "" if c.get("user_changes") else " (same user as before: re-login only)")
        else:
            line += "\n   - actor: %s" % user_label(c)
        if f:
            if c.get("needs"):
                line += "\n   - consumes: " + "; ".join("`%s` %s" % (x["repo"], ("from seq %s (%s)" % (x["provided_by_seq"], x["provided_by_flow"])) if x["status"] == "satisfied" else x["status"].split("(")[0].lower().replace("_", " ")) for x in c["needs"])
            if c.get("produces"):
                line += "\n   - produces: " + ", ".join("`%s`" % p for p in c["produces"])
            a = f["assertions"]
            bits = []
            if a["message_assertions_0013"] or a["group_assertions_0014"]:
                bits.append("%d message/field assertion(s)" % len(a["message_assertions_0013"]))
                sheets = sorted({x["sheet"] for x in a["group_assertions_0014"] if x["sheet"]})
                if sheets:
                    bits.append("group assertion sheet(s): " + ", ".join("`%s`" % s for s in sheets))
            if a["validations_0007"] or a["q2q_0005"]:
                bits.append("value validations %d, Q2Q %d" % (a["validations_0007"], a["q2q_0005"]))
            line += "\n   - checks: " + ("; ".join(bits) if bits else "none configured")
            scr = " -> ".join(A.screens[s]["name"] or s for s in f["screen_ids"][:6])
            line += "\n   - screens: %s%s" % (scr, " ..." if len(f["screen_ids"]) > 6 else "")
            line += "\n   - detail: flows/%s.md ; trace prefix `%s`" % (c["flow_id"], c["trace_prefix"])
        L.append(line)
    inactive = [c for c in g["chain"] if not c["active"]]
    if inactive:
        L.append("")
        L.append("## Inactive rows (skipped by the engine)")
        for c in inactive:
            L.append("- seq %s %s (`%s`) status %s" % (c["seq"], c["flow"], c["flow_id"], c["status"]))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--find", help="look up flows/groups by text in reverse_index.json")
    args = ap.parse_args()
    if args.find:
        return find(args.find)
    A = Atlas()
    gflows = sorted({r["ptf_testflowid"] for r in A.gtfd} | set(A.tf_by))
    for fid in gflows:
        A.flows[fid] = A.build_flow(fid)
    # flows referenced but missing in tf still get a shell
    A.build_groups()
    # where used
    A.flow_groups = collections.defaultdict(list)
    for gid, g in A.groups.items():
        for c in g["chain"]:
            A.flow_groups[c["flow_id"]].append({"group": gid, "group_desc": g["description"], "seq": c["seq"], "active": c["active"],
                                                "user": user_label(c) if c["active"] else c["user"], "login_status": c["login_status"]})
    A.check()
    # ---- write
    os.makedirs(os.path.join(OUT, "flows"), exist_ok=True)
    for fn in os.listdir(os.path.join(OUT, "flows")):
        os.remove(os.path.join(OUT, "flows", fn))
    for fn in os.listdir(OUT):
        if fn.startswith("group_") and fn.endswith(".md"):
            os.remove(os.path.join(OUT, fn))
    for fid, f in A.flows.items():
        f["groups"] = A.flow_groups.get(fid, [])
        emb = dict(f)
        emb["screens"] = {sid: A.screens[sid] for sid in f["screen_ids"]}
        with open(os.path.join(OUT, "flows", fid + ".json"), "w", encoding="utf-8") as fh:
            json.dump(emb, fh, ensure_ascii=False, indent=1)
        with open(os.path.join(OUT, "flows", fid + ".md"), "w", encoding="utf-8") as fh:
            fh.write(flow_md(A, f))
    for gid, g in A.groups.items():
        with open(os.path.join(OUT, "group_%s.md" % gid), "w", encoding="utf-8") as fh:
            fh.write(group_md(A, g))
    flows_slim = {}
    for fid, f in A.flows.items():
        s = {k: v for k, v in f.items() if k not in ("screens_exec",)}
        s["screens_exec"] = [{k: v for k, v in e.items() if k != "children"} | {"children": [c["screen_id"] for c in e["children"]]} for e in f["screens_exec"]]
        flows_slim[fid] = s
    atlas = {"generated": datetime.datetime.now().isoformat(timespec="seconds"), "source": "selenium-framework-db CTA_CONFIG_ASSERTION raw dumps",
             "trace_key_format": "<group>:<seq>:<flow>:<screen>:e<event serial>  e.g. 11:10:00010001:000101:e3",
             "counts": counts(A), "groups": A.groups, "flows": flows_slim, "screens": A.screens,
             "users": [{k: v for k, v in u.items()} for u in A.lu],
             "apps": A.app, "component_types": A.cmpt, "component_events": A.ce}
    with open(os.path.join(OUT, "atlas.json"), "w", encoding="utf-8") as fh:
        json.dump(atlas, fh, ensure_ascii=False)
    write_index(A)
    write_anomalies(A)
    validate(A)
    print(json.dumps(counts(A), indent=1))
    print("wrote", OUT)


def counts(A):
    ref_flows = {r["ptf_testflowid"] for r in A.gtfd}
    scr_ref = set()
    for fid in ref_flows:
        if fid in A.flows:
            scr_ref.update(A.flows[fid]["screen_ids"])
    return {"groups": len(A.groups), "groups_with_rows": sum(1 for g in A.groups.values() if g["counts"]["rows"]),
            "group_rows": len(A.gtfd), "group_rows_active": sum(1 for r in A.gtfd if r["pgtfd_status"] == "Y"),
            "flows_in_tf": len(A.tf), "flows_referenced_by_groups": len(ref_flows), "flows_referenced_but_missing_in_tf": len(ref_flows - set(A.tf_by)),
            "menu_groups": len(A.mg), "screens_in_sc": len(A.sc), "screens_reachable_from_group_flows": len(scr_ref),
            "screens_reachable_from_any_flow": len(A.screens), "fields_total": len(A.sf), "fields_active": sum(1 for r in A.sf if r["psf_field_status"] == "Y" and r["psf_field_addition"] == "+"),
            "events_total": len(A.sef), "events_active": sum(1 for r in A.sef if r["psef_status"] in ("Y", "A")),
            "screen_queries": len(A.sq), "users": len(A.lu), "apps": len(A.app), "toast_rows": len(A.toast)}


def write_index(A):
    idx = {"note": "Tags for selective loading. flow file: flows/<id>.json|md ; group file: group_<id>.md ; full data: atlas.json",
           "areas": collections.defaultdict(list), "markets": collections.defaultdict(list), "families": collections.defaultdict(lambda: collections.defaultdict(list)),
           "flows": {}, "groups": {}, "repos": {}}
    for fid, f in A.flows.items():
        t = f["tags"]
        entry = {"desc": f["description"], "status": f["status"], "areas": t["areas"], "market": t["market"], "menu_option": t["menu_option"],
                 "menu_search_text": t["menu_search_text"], "screen_ids": f["screen_ids"], "screen_names": [A.screens[s]["name"] for s in f["screen_ids"]],
                 "repos_written": f["repos"]["writes_canon"], "repos_read": f["repos"]["reads_canon"], "workbook": f["workbook"]["effective_files"],
                 "groups": sorted({u["group"] for u in A.flow_groups.get(fid, [])}, key=num), "in_active_group_row": any(u["active"] for u in A.flow_groups.get(fid, [])),
                 "counts": f["counts"], "files": {"md": "flows/%s.md" % fid, "json": "flows/%s.json" % fid}}
        idx["flows"][fid] = entry
        for a in t["areas"]:
            idx["areas"][a].append(fid)
            idx["families"][a][t["market"] or "PK/default"].append(fid)
        idx["markets"][t["market"] or "PK/default"].append(fid)
    for gid, g in A.groups.items():
        idx["groups"][gid] = {"desc": g["description"], "market_guess": g["market_guess_from_description"], "apps": [a["app_id"] for a in g["allowable_apps"]],
                              "workbook_variants_inferred": sorted({a["workbook_variant_inferred"] for a in g["allowable_apps"] if a["workbook_variant_inferred"]}),
                              "counts": g["counts"], "switch_points": g["switch_points"], "story": "group_%s.md" % gid,
                              "flows_active": [c["flow_id"] for c in g["chain"] if c["active"]]}
    for canon in sorted(set(A.repo_writers) | set(A.repo_readers)):
        idx["repos"][canon] = {"writers": sorted(A.repo_writers.get(canon, [])), "readers": sorted(A.repo_readers.get(canon, []))}
    idx["families"] = {a: dict(m) for a, m in idx["families"].items()}
    with open(os.path.join(OUT, "INDEX.json"), "w", encoding="utf-8") as fh:
        json.dump(idx, fh, ensure_ascii=False, indent=1)
    # ---- reverse index
    phr = collections.defaultdict(lambda: {"kinds": set(), "flows": set()})
    menu = collections.defaultdict(lambda: {"search_texts": set(), "menu_groups": set(), "flows": set()})
    scr = collections.defaultdict(lambda: {"screen_ids": set(), "flows": set()})
    for fid, f in A.flows.items():
        def add(text, kind):
            k = norm(text)
            if k:
                phr[k]["kinds"].add(kind); phr[k]["flows"].add(fid)
        add(f["description"], "flow_description")
        for m in f["menus"]:
            add(m["description"], "menu_group_description"); add(m["search_text"], "menu_search_text"); add(m["navigation"], "menu_navigation_id")
            if m["navigation"]:
                for nav in [x.strip() for x in m["navigation"].split(",") if x.strip()]:
                    menu[nav]["search_texts"].add(m["search_text"] or ""); menu[nav]["menu_groups"].add(m["menu_group"]); menu[nav]["flows"].add(fid)
        for sid in f["screen_ids"]:
            nm = A.screens[sid]["name"]
            add(nm, "screen_name")
            if nm:
                scr[nm]["screen_ids"].add(sid); scr[nm]["flows"].add(fid)
    def groups_of(fl):
        gs = collections.defaultdict(list)
        for fid in fl:
            for u in A.flow_groups.get(fid, []):
                if u["active"]:
                    gs[u["group"]].append(u["seq"])
        return {g: sorted(v) for g, v in sorted(gs.items(), key=lambda x: num(x[0]))}
    rev = {"note": "keys are normalised text (lower case, alphanumerics). groups = {group: [active seq numbers]}",
           "phrases": {k: {"kinds": sorted(v["kinds"]), "flows": sorted(v["flows"]), "groups": groups_of(v["flows"])} for k, v in phr.items()},
           "menu_options": {k: {"search_texts": sorted(v["search_texts"]), "menu_groups": sorted(v["menu_groups"]), "flows": sorted(v["flows"]), "groups": groups_of(v["flows"])} for k, v in menu.items()},
           "screen_names": {k: {"screen_ids": sorted(v["screen_ids"]), "flows": sorted(v["flows"]), "groups": groups_of(v["flows"])} for k, v in scr.items()}}
    with open(os.path.join(OUT, "reverse_index.json"), "w", encoding="utf-8") as fh:
        json.dump(rev, fh, ensure_ascii=False)


def write_anomalies(A):
    out = {k: {"count": len(v), "examples": v[:25]} for k, v in sorted(A.anomalies.items())}
    with open(os.path.join(OUT, "anomalies.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


def validate(A):
    """group 11 chain must equal the live SQL capture (order by sequence, status Y)."""
    p = os.path.join(RAW, "_validation_group11_sql.json")
    res = {"group": "11", "checked_against": None, "ok": None}
    g = A.groups.get("11")
    mine = "|".join("%s:%s:%s:%s:%s" % (c["seq"], c["flow_id"], c["plu_serial_no"] if c["plu_serial_no"] is not None else "",
                                        c["login_status"] or "", c["app_switch"] or "") for c in g["chain"] if c["active"]) if g else ""
    sw = ",".join(str(c["seq"]) for c in g["chain"] if c["active"] and c["login_status"] == "Y") if g else ""
    res["atlas_rows"] = mine.count("|") + 1 if mine else 0
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            v = json.load(fh)
        res["checked_against"] = "raw/_validation_group11_sql.json (%s)" % v.get("captured")
        res["sql_rows"] = v["n"]
        res["chain_equal"] = mine == v["chain"]
        res["switch_points_equal"] = sw == v["switches"]
        res["ok"] = res["chain_equal"] and res["switch_points_equal"] and res["atlas_rows"] == v["n"]
        if not res["chain_equal"]:
            a, b = mine.split("|"), v["chain"].split("|")
            res["diff_only_in_atlas"] = [x for x in a if x not in b]
            res["diff_only_in_sql"] = [x for x in b if x not in a]
    res["switch_points_atlas"] = sw
    res["note"] = "the task text said 44 rows; the live DB has %s active rows for group 11 (the same 46 the DISPATCH_ADVICE.md session plan lists)" % res.get("sql_rows")
    with open(os.path.join(OUT, "validation.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print("VALIDATION group 11:", json.dumps(res))


def find(q):
    with open(os.path.join(OUT, "reverse_index.json"), encoding="utf-8") as fh:
        rev = json.load(fh)
    nq = norm(q)
    hits = {k: v for k, v in rev["phrases"].items() if nq and (nq in k or (len(k) > 3 and k in nq))}
    flows, groups = set(), collections.defaultdict(set)
    for k, v in hits.items():
        flows.update(v["flows"])
        for g, s in v["groups"].items():
            groups[g].update(s)
    print("phrases matched:", len(hits))
    for k in sorted(hits)[:20]:
        print("  ", k, hits[k]["kinds"])
    print("flows (%d):" % len(flows), ", ".join(sorted(flows)[:60]))
    print("groups:", {g: sorted(s) for g, s in sorted(groups.items(), key=lambda x: num(x[0]))})


if __name__ == "__main__":
    main()
