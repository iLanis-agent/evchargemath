# EV Charge Math

The home charging honesty tool. The plug on the wall has a pace, the
range you want has a clock, and the breaker in the panel keeps a fifth
of itself back from every continuous load. EV Charge Math turns volts
and amps into miles of charge an hour, holds the miles you want
against that pace, and checks the charger setting against the
breaker's honest continuous amps.

- Live app: https://ilanis-agent.github.io/evchargemath/app.html
- Landing: https://ilanis-agent.github.io/evchargemath/

## What it does

1. **The charge truth** - volts x amps / 1000 into kilowatts, x miles
   per kilowatt-hour into miles of charge an hour.
2. **The time truth** - miles to add / charge pace into hours, with
   verdicts at breakfast (8), the evening and the night (14), and more
   than a day on the plug.
3. **The breaker truth** - a continuous load gets 0.8x the breaker's
   name (labeled norm); the charger setting as a percent of the honest
   amps decides whether the breaker holds the setting or trips on it.

## Files

- `engine.js` - pure functions (`chargePlan`, `timePlan`, `breakerPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 25 oracle cases, `node test.js` runs green

The derate is a labeled norm; the extension cord keeps the honest ledger.
