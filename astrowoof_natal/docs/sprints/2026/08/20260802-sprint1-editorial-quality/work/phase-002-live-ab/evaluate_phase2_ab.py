#!/usr/bin/env python3
"""Deterministic comparative metrics for the Phase-2 live A/B decks."""
from __future__ import annotations
import json, math, re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")

def words(text): return TOKEN.findall(text.lower())
def jaccard(a, b):
    x, y = set(words(a)), set(words(b))
    return len(x & y) / len(x | y) if x | y else 0.0
def cosine(a, b):
    x, y = Counter(words(a)), Counter(words(b)); common = set(x) & set(y)
    den = math.sqrt(sum(v*v for v in x.values()) * sum(v*v for v in y.values()))
    return sum(x[k]*y[k] for k in common) / den if den else 0.0

def card_items(deck):
    out=[]
    for card in deck["cards"]:
        cid=card["claim_id"]
        for density in ("no_astro","light_astro","full_astro"):
            for kind in ("headline","body"):
                for audience,text in card["card"][density][kind].items():
                    out.append({"claim_id":cid,"priority_id":card["priority_id"],
                        "field":f"{density}.{kind}.{audience}","kind":kind,"text":text})
        for kind in ("funny_dog_quotes","imperative_dog_quotes","applicable_canine_jokes"):
            for i,text in enumerate(card.get(kind, [])):
                out.append({"claim_id":cid,"priority_id":card["priority_id"],
                    "field":f"{kind}.{i}","kind":kind,"text":text})
        for kind in ("dos","donts"):
            for i,text in enumerate(card.get(kind, [])):
                out.append({"claim_id":cid,"priority_id":card["priority_id"],
                    "field":f"{kind}.{i}","kind":kind,"text":text})
    return out

def metrics(deck, assignment):
    items=card_items(deck); bodies=[x for x in items if x["kind"]=="body"]
    headlines=[x for x in items if x["kind"]=="headline"]
    pass_of={p:int(n) for n,ids in assignment["passes"].items() for p in ids}
    openings=defaultdict(set)
    for x in bodies: openings[(x["field"]," ".join(words(x["text"])[:3]))].add(x["claim_id"])
    repeated_openings=sorted(({"field":f,"opening":o,"claim_count":len(ids),"claim_ids":sorted(ids)}
        for (f,o),ids in openings.items() if len(ids)>=3),key=lambda x:(-x["claim_count"],x["field"],x["opening"]))
    ngrams=defaultdict(set)
    for x in items:
        ws=words(x["text"])
        for n in range(5,13):
            for i in range(len(ws)-n+1): ngrams[(n," ".join(ws[i:i+n]))].add(x["claim_id"])
    repeated={}
    for n in range(5,13):
        groups=[(text,ids) for (size,text),ids in ngrams.items() if size==n and len(ids)>=2]
        repeated[str(n)]={"group_count":len(groups),"same_pass_group_count":sum(
            1 for _,ids in groups if len({pass_of[next(c["priority_id"] for c in deck["cards"] if c["claim_id"]==cid)] for cid in ids})==1)}
    exact=defaultdict(set)
    for x in headlines: exact[x["text"].strip().lower()].add(x["claim_id"])
    exact_dupes=[{"text":t,"claim_ids":sorted(ids)} for t,ids in exact.items() if len(ids)>=2]
    pairs=[]
    byfield=defaultdict(list)
    for x in bodies: byfield[x["field"]].append(x)
    for field,group in byfield.items():
        for a,b in combinations(group,2):
            score=cosine(a["text"],b["text"])
            pairs.append({"field":field,"score":round(score,4),"a":a["claim_id"],"b":b["claim_id"],
                "same_pass":pass_of[a["priority_id"]]==pass_of[b["priority_id"]]})
    pairs.sort(key=lambda x:-x["score"])
    voice=[]
    for card in deck["cards"]:
        for density in ("no_astro","light_astro","full_astro"):
            body=card["card"][density]["body"]
            voice.append({"claim_id":card["claim_id"],"density":density,
                "handler_hybrid":jaccard(body["handler"],body["hybrid"]),
                "handler_d2d":jaccard(body["handler"],body["direct_to_dog"]),
                "hybrid_d2d":jaccard(body["hybrid"],body["direct_to_dog"])})
    allwords=[w for x in items for w in words(x["text"])]
    return {"item_count":len(items),"total_words":len(allwords),"unique_words":len(set(allwords)),
        "type_token_ratio":round(len(set(allwords))/len(allwords),5),
        "mean_body_words":round(sum(len(words(x["text"])) for x in bodies)/len(bodies),2),
        "mean_headline_words":round(sum(len(words(x["text"])) for x in headlines)/len(headlines),2),
        "exact_duplicate_headlines":exact_dupes,"repeated_openings":repeated_openings,
        "repeated_cross_claim_ngrams":repeated,"top_body_similarity_pairs":pairs[:30],
        "body_pair_count_over_0_65":sum(x["score"]>=.65 for x in pairs),
        "body_pair_count_over_0_55":sum(x["score"]>=.55 for x in pairs),
        "mean_top_100_body_similarity":round(sum(x["score"] for x in pairs[:100])/100,4),
        "same_pass_share_top_100":round(sum(x["same_pass"] for x in pairs[:100])/100,4),
        "voice_jaccard_means":{k:round(sum(x[k] for x in voice)/len(voice),4) for k in
            ("handler_hybrid","handler_d2d","hybrid_d2d")}}

def main():
    result={}
    for arm in ("contiguous","stratified-v1"):
        base=ROOT/arm
        deck=json.loads((base/"final/kevin/natal.kevin.cards.json").read_text(encoding="utf-8"))
        assignment=json.loads((base/"sbe/semantic-basis-output/kevin/kevin.split-assignment.json").read_text(encoding="utf-8"))
        result[arm]=metrics(deck,assignment)
    result["summary_identical"]=(json.loads((ROOT/"contiguous/final/kevin/natal.kevin.cards.json").read_text(encoding="utf-8"))["summary"]
        ==json.loads((ROOT/"stratified-v1/final/kevin/natal.kevin.cards.json").read_text(encoding="utf-8"))["summary"])
    (ROOT/"deterministic-quality-metrics.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
