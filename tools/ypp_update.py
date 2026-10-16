"""Daily YPP push update. Run from repo root after latest.json is written:
  python3 tools/ypp_update.py --hours 700 --mixes 1 --shorts 1 --live --subs 3850 [--mix ID --h7 N | --h14 N] [--status ID Public]
Upserts today's row in data/ypp.json; added24 = hours - previous day's hours."""
import json, argparse, datetime
p = argparse.ArgumentParser()
p.add_argument('--day', default=datetime.date.today().isoformat())
p.add_argument('--hours', type=float, required=True)
p.add_argument('--mixes', type=int, default=0); p.add_argument('--shorts', type=int, default=0)
p.add_argument('--live', action='store_true'); p.add_argument('--subs', type=int)
p.add_argument('--note', default='')
p.add_argument('--mix'); p.add_argument('--h7', type=float); p.add_argument('--h14', type=float)
p.add_argument('--status', nargs=2, metavar=('ID', 'STATUS'))
a = p.parse_args()
F = 'data/ypp.json'; d = json.load(open(F))
rows = [r for r in d['daily'] if r['day'] != a.day]
prev = max((r for r in rows if r['day'] < a.day), key=lambda r: r['day'], default=None)
rows.append({"day": a.day, "hours": a.hours, "added24": round(a.hours - prev['hours'], 1) if prev else None,
             "mixes": a.mixes, "shorts": a.shorts, "live": a.live, "subs": a.subs, "note": a.note})
d['daily'] = sorted(rows, key=lambda r: r['day'])
for m in d['mixes']:
    if a.mix == m['id']:
        if a.h7 is not None: m['h7'] = a.h7
        if a.h14 is not None: m['h14'] = a.h14
    if a.status and a.status[0] == m['id']: m['status'] = a.status[1]
json.dump(d, open(F, 'w'), ensure_ascii=False, indent=1)
print('ok', d['daily'][-1])
