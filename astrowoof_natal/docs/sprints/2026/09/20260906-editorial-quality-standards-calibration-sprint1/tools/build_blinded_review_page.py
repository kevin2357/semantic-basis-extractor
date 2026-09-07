"""Build a local-only blinded editorial-review page from frozen private packets."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
from typing import Any


CHOICES = (
    "accept",
    "accept_with_advisory",
    "request_another_polish",
    "retain_prior_candidate",
    "terminal_review",
    "insufficient_context",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def build(input_dir: Path) -> tuple[str, dict[str, Any]]:
    packets = []
    for path in sorted(input_dir.glob("*.json")):
        packet = load(path)
        if packet.get("schema_version") != "astrowoof.private_blinded_editorial_review.v1":
            raise ValueError(f"unexpected packet schema: {path}")
        packets.append({
            "packet": packet,
            "packet_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    if not packets:
        raise ValueError("no blinded review packets found")
    rubric_versions = {item["packet"].get("rubric_version") for item in packets}
    if len(rubric_versions) != 1 or None in rubric_versions:
        raise ValueError("packets do not share one rubric version")
    payload = {
        "schema_version": "astrowoof.local_blinded_editorial_review_ui.v1",
        "rubric_version": next(iter(rubric_versions)),
        "choices": CHOICES,
        "packets": packets,
    }
    encoded = base64.b64encode(canonical(payload)).decode("ascii")
    html = TEMPLATE.replace("__PAYLOAD_BASE64__", encoded)
    manifest = {
        "schema_version": "astrowoof.local_blinded_editorial_review_ui_receipt.v1",
        "packet_count": len(packets),
        "packet_ids": [item["packet"]["packet_id"] for item in packets],
        "packet_file_sha256": {
            item["packet"]["packet_id"]: item["packet_file_sha256"] for item in packets
        },
        "rubric_version": payload["rubric_version"],
        "choice_vocabulary": list(CHOICES),
        "answer_key_embedded": False,
        "network_dependency_count": 0,
    }
    manifest["receipt_sha256"] = hashlib.sha256(canonical(manifest)).hexdigest()
    return html, manifest


TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AstroWoof blinded editorial review</title>
<style>
:root{color-scheme:light dark;--bg:#f5f1e8;--panel:#fffdf8;--ink:#28241f;--muted:#6f665d;--line:#d8cdbc;--accent:#77542c;--soft:#eee3d2;--good:#376846;--bad:#93453b}
@media(prefers-color-scheme:dark){:root{--bg:#191714;--panel:#24211d;--ink:#f2ece2;--muted:#bcb1a4;--line:#4b433a;--accent:#e1b777;--soft:#332d27;--good:#8bc69a;--bad:#e1958c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:24px}h1,h2,h3{line-height:1.2}header{display:grid;gap:12px;margin-bottom:22px}.bar{height:10px;background:var(--soft);border-radius:10px;overflow:hidden}.bar span{display:block;height:100%;background:var(--accent)}.meta,.nav,.choice-grid{display:flex;gap:12px;flex-wrap:wrap;align-items:center}.muted{color:var(--muted)}section{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;margin:16px 0}.transition{display:grid;grid-template-columns:1fr 1fr;gap:14px}.text{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--soft);padding:12px;border-radius:8px}.finding{border-left:4px solid var(--accent);padding-left:12px;margin:10px 0}label.choice{display:flex;gap:7px;align-items:center;background:var(--soft);padding:9px 11px;border-radius:8px}textarea,input[type=text]{width:100%;font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}button{font:inherit;padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);cursor:pointer}button.primary{background:var(--accent);color:var(--bg);border-color:var(--accent)}button:disabled{opacity:.45;cursor:not-allowed}.error{color:var(--bad)}.ok{color:var(--good)}code{overflow-wrap:anywhere}@media(max-width:700px){main{padding:14px}.transition{grid-template-columns:1fr}}
</style>
</head>
<body><main>
<header><h1>Blinded editorial calibration</h1><div class="meta"><strong id="position"></strong><span id="progressText" class="muted"></span></div><div class="bar" role="progressbar" aria-label="Review completion"><span id="progressBar"></span></div></header>
<section><label for="reviewerRole"><strong>Reviewer role</strong></label><input id="reviewerRole" type="text" placeholder="owner-human or independent-editorial-model" autocomplete="off"><p class="muted">Run and subject identities, historical decisions, and the answer key are not included.</p></section>
<div id="sample"></div>
<div class="nav"><button id="previous" type="button">Previous</button><button id="next" type="button">Next</button><button id="export" class="primary" type="button" disabled>Export completed judgments</button><span id="status" aria-live="polite"></span></div>
</main>
<script>
'use strict';
const payload=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob('__PAYLOAD_BASE64__'),c=>c.charCodeAt(0))));
const answers=Object.fromEntries(payload.packets.map(x=>[x.packet.packet_id,{deck:null,adoption:null,rationale:''}]));
let index=0;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pretty=s=>String(s).replaceAll('_',' ');
function findingBlock(title,value){const findings=value.findings||[];return `<section><h3>${esc(title)}</h3><p>Status: <strong>${esc(value.status)}</strong> · warnings: ${esc(value.warning_count)}</p>${findings.length?findings.map(f=>`<div class="finding"><strong>${esc(f.code)}</strong><div>${esc(f.field||'')}</div>${(f.values||[]).map(v=>`<div class="text">${esc(v.text)}</div>`).join('')}</div>`).join(''):'<p class="muted">No findings.</p>'}</section>`}
function choices(kind,current){return `<div class="choice-grid">${payload.choices.map(c=>`<label class="choice"><input type="radio" name="${kind}" value="${c}" ${current===c?'checked':''}>${esc(pretty(c))}</label>`).join('')}</div>`}
function render(){const p=payload.packets[index].packet,a=answers[p.packet_id];document.getElementById('position').textContent=`Sample ${index+1} of ${payload.packets.length}`;document.getElementById('sample').innerHTML=`<section><h2>Candidate ${esc(p.candidate_position)}</h2><code>${esc(p.packet_id)}</code><h3>Edited fields</h3>${p.transition.map(t=>`<div class="transition"><div><strong>${esc(t.path)} · before</strong><div class="text">${esc(t.before)}</div></div><div><strong>${esc(t.path)} · after</strong><div class="text">${esc(t.after)}</div></div></div>`).join('')}</section>${findingBlock('Prior findings',p.prior_findings)}${findingBlock('Candidate findings',p.candidate_findings)}<section><h3>Structural validation</h3><p>Status: <strong>${esc(p.candidate_validation.status)}</strong></p>${(p.candidate_validation.errors||[]).map(e=>`<div class="finding">${esc(typeof e==='string'?e:JSON.stringify(e))}</div>`).join('')}</section><section><h3>Deck acceptability</h3>${choices('deck',a.deck)}</section><section><h3>Candidate adoption</h3>${choices('adoption',a.adoption)}</section><section><label for="rationale"><strong>Optional rationale</strong></label><textarea id="rationale" rows="5">${esc(a.rationale)}</textarea></section>`;document.querySelectorAll('input[type=radio]').forEach(el=>el.addEventListener('change',e=>{answers[p.packet_id][e.target.name]=e.target.value;update()}));document.getElementById('rationale').addEventListener('input',e=>answers[p.packet_id].rationale=e.target.value);document.getElementById('previous').disabled=index===0;document.getElementById('next').disabled=index===payload.packets.length-1;update()}
function update(){const complete=payload.packets.filter(x=>answers[x.packet.packet_id].deck&&answers[x.packet.packet_id].adoption).length;document.getElementById('progressText').textContent=`${complete}/${payload.packets.length} complete`;document.getElementById('progressBar').style.width=`${100*complete/payload.packets.length}%`;document.querySelector('.bar').setAttribute('aria-valuenow',String(complete));const role=document.getElementById('reviewerRole').value.trim();document.getElementById('export').disabled=complete!==payload.packets.length||!role;document.getElementById('status').textContent=complete===payload.packets.length&&!role?'Add reviewer role to export.':''}
document.getElementById('reviewerRole').addEventListener('input',update);document.getElementById('previous').addEventListener('click',()=>{index--;render()});document.getElementById('next').addEventListener('click',()=>{index++;render()});document.getElementById('export').addEventListener('click',()=>{const role=document.getElementById('reviewerRole').value.trim();const output={schema_version:'astrowoof.private_editorial_judgments.v1',rubric_version:payload.rubric_version,reviewer_role:role,judgments:payload.packets.map(x=>({packet_id:x.packet.packet_id,packet_file_sha256:x.packet_file_sha256,deck_acceptability:answers[x.packet.packet_id].deck,candidate_adoption:answers[x.packet.packet_id].adoption,rationale:answers[x.packet.packet_id].rationale}))};const blob=new Blob([JSON.stringify(output,null,2)+'\n'],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='astrowoof-blinded-editorial-judgments.json';a.click();URL.revokeObjectURL(url);document.getElementById('status').textContent='Judgments exported.'});render();
</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    html, manifest = build(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8", newline="\n")
    args.receipt.write_bytes(canonical(manifest))
    print(json.dumps({"output": str(args.output), "receipt": str(args.receipt), **manifest}, sort_keys=True))


if __name__ == "__main__":
    main()
