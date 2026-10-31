import sys,json,csv
sys.path.insert(0,'.')
from q import *
from concurrent.futures import ThreadPoolExecutor
names=["PALANTIR TECHNOLOGIES INC.","PALANTIR USA INC.","PALANTIR USG INC"]
fy=json.load(open("fy_totals.json"))["results"]
tot={int(x["time_period"]["fiscal_year"]):x["aggregated_amount"] for x in fy}
def dodfor(y):
    f={"time_period":[{"start_date":f"{y-1}-10-01","end_date":f"{y}-09-30"}],"recipient_search_text":names,"award_type_codes":["A","B","C","D"]}
    r=post("/api/v2/search/spending_by_category/awarding_agency/",{"filters":f,"limit":10,"page":1},tries=2)
    d=[x["amount"] for x in r.get("results",[]) if x.get("name")=="Department of Defense"]
    return y,(d[0] if d else 0)
with ThreadPoolExecutor(7) as ex: res=dict(ex.map(dodfor,range(2013,2027)))
with open("palantir_obligations_by_fy.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["fiscal_year","contract_obligations_usd","dod_obligations_usd","dod_share"])
    for y in range(2013,2027):
        t=tot[y]; w.writerow([y,round(t),round(res[y]),round(res[y]/t,3)])
        print(y, round(t/1e6,1), round(res[y]/1e6,1), f"{100*res[y]/t:.0f}%")
print("cum thru FY2024 $M:",round(sum(tot[y] for y in range(2008,2025))/1e6,1))
aw=json.load(open("award_details.json"))
with open("palantir_top120_awards_competition.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["award_id","obligation_usd","start_date","awarding_sub_agency","extent_competed","solicitation_procedures","offers","description"])
    for r in aw: w.writerow([r["id"],r["obl"],r["start"],r["agency"],r["extent"],r["sol"],r["offers"],r["desc"]])
gid="CONT_IDV_W519TC25D0039_9700"
ch=post("/api/v2/idvs/awards/",{"award_id":gid,"type":"child_awards","limit":100,"page":1,"sort":"obligated_amount","order":"desc"})
with open("ea_W519TC25D0039_orders.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["order_piid","awarding_agency","obligated_usd","start_date","description"])
    for c in ch["results"]: w.writerow([c.get("piid"),c.get("awarding_agency"),c.get("obligated_amount"),c.get("period_of_performance_start_date"),c.get("description")])
print("orders:",len(ch["results"]),"sum $M",round(sum(c["obligated_amount"] for c in ch["results"])/1e6,1))
