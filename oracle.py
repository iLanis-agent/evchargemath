import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

DERATE=0.8

def charge_plan(volts,amps,mi_per_kwh):
    if not pos(volts): return {"error":"the volts must be above zero"}
    if not pos(amps): return {"error":"the amps must be above zero"}
    if not pos(mi_per_kwh): return {"error":"the miles per kilowatt-hour must be above zero"}
    kw=volts*amps/1000
    mph=kw*mi_per_kwh
    return {"kw":r1(kw),"mph":r1(mph)}

def render_charge(r,volts,amps,mi_per_kwh):
    return ("The "+jsnum(volts)+"-volt, "+jsnum(amps)+"-amp plug feeds about "+jsnum(r["kw"])
            +" kilowatts - about "+jsnum(r["mph"])+" miles of charge an hour at "+jsnum(mi_per_kwh)+" miles per kilowatt-hour.")

def time_plan(miles,mph):
    if not pos(miles): return {"error":"the miles to add must be above zero"}
    if not pos(mph): return {"error":"the charge pace must be above zero"}
    hours=miles/mph
    if hours<=8: verdict="back full by breakfast"
    elif hours<=14: verdict="the evening and the night"
    else: verdict="more than a day on the plug"
    return {"hours":r1(hours),"verdict":verdict}

def render_time(r,miles,mph):
    return ("Adding "+jsnum(miles)+" miles at "+jsnum(mph)+" miles an hour of charge takes about "
            +jsnum(r["hours"])+" hours - "+r["verdict"]+".")

def breaker_plan(charger_amps,breaker_amps):
    if not pos(charger_amps): return {"error":"the charger amps must be above zero"}
    if not pos(breaker_amps): return {"error":"the breaker amps must be above zero"}
    honest=breaker_amps*DERATE
    ratio=charger_amps/honest*100
    if ratio<=100: verdict="the breaker holds the setting"
    else: verdict="the breaker trips on the setting"
    return {"honest":r1(honest),"ratio":r1(ratio),"verdict":verdict}

def render_breaker(r,charger_amps,breaker_amps):
    return ("At "+jsnum(charger_amps)+" amps on the "+jsnum(breaker_amps)+"-amp breaker, the charger asks for "
            +jsnum(r["ratio"])+"% of the honest "+jsnum(r["honest"])+" continuous amps - "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="charge": r=charge_plan(*args); fn=render_charge
    elif tool=="time": r=time_plan(*args); fn=render_time
    else: r=breaker_plan(*args); fn=render_breaker
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(240,32,3.5),(120,12,3.5),(240,40,3.5),(240,16,3.0),(208,24,3.5),(240,48,4.0)]:
    add("charge",a)
for a in [(250,26.9),(120,26.9),(60,5.0),(300,33.6),(400,17.5),(40,46.1)]:
    add("time",a)
for a in [(32,40),(40,40),(16,20),(48,60),(40,50),(24,20)]:
    add("breaker",a)
add("charge",[0,32,3.5]); add("charge",[240,0,3.5]); add("charge",[240,32,0])
add("time",[0,26.9]); add("time",[250,0])
add("breaker",[0,40]); add("breaker",[32,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
