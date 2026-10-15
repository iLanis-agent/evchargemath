var EvChargeMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var DERATE = 0.8;
  function chargePlan(volts, amps, miPerKwh) {
    if (!pos(volts)) return { error: "the volts must be above zero" };
    if (!pos(amps)) return { error: "the amps must be above zero" };
    if (!pos(miPerKwh)) return { error: "the miles per kilowatt-hour must be above zero" };
    var kw = volts * amps / 1000;
    var mph = kw * miPerKwh;
    return { kw: r1(kw), mph: r1(mph) };
  }
  function renderCharge(r, volts, amps, miPerKwh) {
    return "The " + jsnum(volts) + "-volt, " + jsnum(amps) + "-amp plug feeds about " + jsnum(r.kw)
      + " kilowatts - about " + jsnum(r.mph) + " miles of charge an hour at " + jsnum(miPerKwh) + " miles per kilowatt-hour.";
  }
  function timePlan(miles, mph) {
    if (!pos(miles)) return { error: "the miles to add must be above zero" };
    if (!pos(mph)) return { error: "the charge pace must be above zero" };
    var hours = miles / mph;
    var verdict = hours <= 8 ? "back full by breakfast"
      : hours <= 14 ? "the evening and the night"
      : "more than a day on the plug";
    return { hours: r1(hours), verdict: verdict };
  }
  function renderTime(r, miles, mph) {
    return "Adding " + jsnum(miles) + " miles at " + jsnum(mph) + " miles an hour of charge takes about "
      + jsnum(r.hours) + " hours - " + r.verdict + ".";
  }
  function breakerPlan(chargerAmps, breakerAmps) {
    if (!pos(chargerAmps)) return { error: "the charger amps must be above zero" };
    if (!pos(breakerAmps)) return { error: "the breaker amps must be above zero" };
    var honest = breakerAmps * DERATE;
    var ratio = chargerAmps / honest * 100;
    var verdict = ratio <= 100 ? "the breaker holds the setting"
      : "the breaker trips on the setting";
    return { honest: r1(honest), ratio: r1(ratio), verdict: verdict };
  }
  function renderBreaker(r, chargerAmps, breakerAmps) {
    return "At " + jsnum(chargerAmps) + " amps on the " + jsnum(breakerAmps) + "-amp breaker, the charger asks for "
      + jsnum(r.ratio) + "% of the honest " + jsnum(r.honest) + " continuous amps - " + r.verdict + ".";
  }
  return { chargePlan: chargePlan, renderCharge: renderCharge, timePlan: timePlan, renderTime: renderTime, breakerPlan: breakerPlan, renderBreaker: renderBreaker };
})();
if (typeof module !== "undefined" && module.exports) module.exports = EvChargeMath;
