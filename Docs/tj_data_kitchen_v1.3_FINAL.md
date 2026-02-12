# TJ Data Kitchen — Project Bible v1.3 (FINAL)

**Last Updated:** 2025-02-12
**Status:** Committee Review Complete — Ready for Implementation
**Reviewed By:** Claude (Opus), Grok 4, ChatGPT (GPT-4.5), Gemini
**Target:** Claude Code — Build Phase 1 MVP

---

## 1. Project Overview

### What Is This?

TJ Data Kitchen is a combined YouTube channel + predictive cooking application. The channel is a **data-first kitchen** that uses data science and statistical principles to explore cooking — with a flagship tool ("The Predictive Pitmaster") that **quantifies uncertainty in complex cooks so you can plan dinner with confidence.**

> **Core Product Identity:** This is an **uncertainty planner**, not a prediction engine. BBQ is chaotic with soft bounds. The product's job is helping users make informed planning decisions despite irreducible variability. The messaging is: *"We quantify uncertainty so you can plan dinner,"* NOT *"We predict your cook time."*

### Who Is Behind This?

Trevor — Production Planner at Lam Research (semiconductor industry), completing MS in Data Science at SMU (graduating December 2025). 6+ years in supply chain/operations, fluent Mandarin (missionary service in Taiwan), former line cook, deep knowledge of both Asian cuisine and American BBQ. The "J" in TJ Data Kitchen is his wife's initial.

### Why Does This Exist?

1. **Mission-Driven:** Give representation to Asian BBQ and Asian cuisine on YouTube. Bridge heritage recipes (researched back to the Tang Dynasty) with American BBQ culture.
2. **Intellectual:** Demonstrate that cooking is applied science. Make content for the person who watches Smarter Every Day *and* smokes briskets on weekends.
3. **Business:** Build an audience of technically-minded viewers with disposable income for affiliate marketing (high-end thermometers, smokers, knives, cookware). Tech-adjacent enough to cross domains.

### Brand Principles

- **Name:** TJ Data Kitchen (not "grill" — intentionally flexible beyond BBQ)
- **Positioning:** Data-first, not data-only. The food is the star; the data is the lens.
- **Differentiators:** Asian-American pitmaster + data science rigor + heritage storytelling.
- **Tone:** Approachable technical — explain residuals over a wok without being condescending.
- **Product Name:** "The Predictive Pitmaster"

### Brand & IP Checklist (Pre-Launch)

- [ ] Secure domain: tjdatakitchen.com (and variants)
- [ ] File basic trademark application for "TJ Data Kitchen" and "Predictive Pitmaster"
- [ ] Secure social handles across YouTube, Instagram, TikTok, X
- [ ] Design visual identity readable at thumbnail scale
- [ ] Define tagline (e.g., "Cook smarter. Eat on time.")

---

## 2. Success Metrics & KPIs

### App Metrics

| Metric | V1 Target | Measurement |
|--------|-----------|-------------|
| Prediction MAE (Mean Absolute Error) | < 45 min after 5 cooks, < 30 min after 20 cooks | Predicted vs. actual finish time |
| 90th percentile coverage | > 85% of cooks finish within predicted 90th %ile window | Calibration tracking |
| User retention (personal use) | Used on > 80% of filmed cooks | Self-tracking |
| Spreadsheet prototype validation | > 60% of 10 testers say "I'd use this weekly" | Pre-build user test |

### Channel Metrics

| Metric | 6-Month Target | 12-Month Target |
|--------|---------------|-----------------|
| Subscribers | 1,000 | 5,000 |
| Average view duration | > 50% retention at 30s | > 50% at 2 min |
| Weekly upload consistency | > 90% hit rate | > 95% |
| Monthly experiment completion | > 80% hit rate | 100% |
| Affiliate click-through rate | Baseline established | > 2% on recommended gear |

### Pivot Triggers

- If after 20 logged cooks, physics-only MAE is < 10% better than simple linear regression → reduce physics complexity.
- If after 3 months, heritage/Asian content outperforms data-focused content by > 2x views → shift content mix toward heritage-first, data-second.
- If after 6 months, < 500 subscribers → reassess niche positioning.
- If spreadsheet prototype test yields < 40% "would use weekly" → redesign core UX before building app.

---

## 3. Audience Segmentation

| Segment | What They Want | How to Serve Them | Content Hook |
|---------|---------------|-------------------|--------------|
| **BBQ Nerds** | Accuracy, equipment comparisons, technique optimization | Monthly experiments, post-cook reports, equipment profile comparisons | "I cooked 10 pork butts to find the optimal temp" |
| **Data Nerds** | Model transparency, methodology, code | Weekly principle videos, dev series (Phase 2+), open-source contributions | "The math behind the stall" |
| **Casual Cooks** | "When should I start cooking?" | Normal Person Mode in app, backward planning, simple timeline view | "Dinner at 6? Start your fire at 7:45 AM" |

### UX Implication: Two Modes

- **Normal Person Mode (Default):** Single screen. "Start at 7:42 AM → Eat at 6:00 PM → Confidence: High." No distributions, no jargon.
- **Nerd Mode (Toggle):** Full distributions, residual plots, phase breakdowns, model diagnostics.

---

## 4. Competitive Landscape

### Cooking Prediction Tools

| Competitor | What They Do | Your Opportunity |
|-----------|-------------|------------------|
| **MEATER Cook Estimator** | Basic time estimate from probe temp curve | No physics model, no uncertainty bands, no environmental factors |
| **FireBoard Analyze** | Real-time finish prediction from probe data | Proprietary, hardware-locked, no explainability |
| **Combustion Inc Predictive Probe** | Embedded predictive thermometer | Hardware-only, no cultural content, no methodology transparency |
| **GrillTime / Pit Pal** | Basic timers with target temps | No prediction — just countdown clocks |
| **Weber iGrill** | Cook tracking and alerts | Logging only, no predictive capability |

### Content Competitors

| Competitor | What They Do | Your Opportunity |
|-----------|-------------|------------------|
| **HowToBBQRight / Meat Church** | Technique-focused BBQ content | "Trust my feel" culture, no data rigor |
| **Harry Soo** | Competition BBQ instruction | Asian-American pitmaster but not data-focused |
| **Blood Bros. BBQ / Khói Barbecue** | Asian-fusion BBQ (restaurant content) | Flavor fusion, not data science or educational |
| **Ken Jee / data science creators** | Use cooking *analogies* to explain DS | Not the reverse — don't actually cook with data |
| **Smarter Every Day / Mark Rober** | Science + entertainment | Not food-focused, but audience overlaps with yours |

### Your Moat

Your competitive advantage is **not** prediction accuracy. Hardware companies will always have better sensor integration. Your moat is:

> **Explainability + Cultural Identity + Narrative**

You show *why* the model thinks what it thinks, you bring a heritage story nobody else can tell, and you're building the audience and the tool simultaneously — creating trust no hardware company can replicate.

---

## 5. Content Strategy

### Content Hierarchy

| Tier | Cadence | Format | Purpose |
|------|---------|--------|---------|
| **Weekly Principle Videos** | Weekly | 8–12 min | Core engine. Question → Concept → Proof. Searchable, establishes authority. |
| **Shorts / Clips** | 2–3x weekly | 30–60 sec | Algorithm discovery. Compressed principles or visual hooks. |
| **Monthly Experiments** | Monthly to bimonthly | 15–25 min | Tentpole events. Multi-variable experiments producing definitive results. |
| **Heritage Series** | Monthly | 12–18 min | Trace a family/cultural recipe, explore history, optimize with data. Breakout candidates. |
| **App/Dev Series** | On-demand (post Month 4–6) | 10–15 min | Side playlist. Only when audience demand is demonstrated. |

### Weekly Video Formula: Question → Concept → Proof

- "Why does salting 24 hours early work?" → Fick's Law of Diffusion → Weigh-in experiment
- "Is overnight marinating better than 2 hours?" → Diminishing Returns & Log Curves → pH measurements
- "Why your thermometer lies" → Measurement Uncertainty & Confidence Intervals → Multi-probe test
- "The math behind the perfect sear" → Maillard kinetics & Arrhenius Equation → Thermal camera
- "Why low-and-slow beats hot-and-fast (sometimes)" → Heat Transfer Coefficients → Moisture loss data
- "The thermodynamics of char siu" → Heritage recipe + thermocouple (Mandarin crossover)

### Content Sequencing

- **Months 1–3:** Weekly videos + heritage pilot establish voice. Monthly experiments generate data. App exists off-camera. Mention casually: "my model predicted this would stall at 160°."
- **Month 1:** Launch with heritage series pilot — trace one recipe to hook emotionally.
- **Months 4–6:** App featured: "I built an app that predicts when my brisket is done — here's accuracy over 15 cooks." Dev series if demand exists.
- **Months 6+:** App becomes recurring character. Dev series as its own playlist.

### SEO & Discovery

- Titles lead with question, not concept: "Why Char Siu Stalls: Data Breakdown" > "Fourier's Law Applied to Char Siu"
- Every weekly video gets a companion Short
- Target keywords: "data-driven BBQ," "BBQ science," "smoking brisket data," "Asian BBQ," "pitmaster data science"

### Monetization

| Revenue Stream | Timeline | Details |
|---------------|----------|---------|
| **Affiliate Marketing** | Month 1+ | Thermapen MK5, FireBoard 2, MEATER+, Joetisserie, knives, woks |
| **Sponsorships (Gear)** | Month 6+ | Smoker brands, probe manufacturers, charcoal/wood companies |
| **Sponsorships (Tech)** | Month 9+ | Data tools, cloud platforms — leverage cross-domain audience |
| **Sponsorships (Cultural)** | Month 6+ | Asian ingredient brands, specialty sauces, cookware |
| **App (if public)** | Phase 4+ | Freemium: free physics-only, paid ML + real-time features |

---

## 6. Technical Architecture — The Predictive Pitmaster

### Design Philosophy

**Physics-Informed stack** — every prediction is explainable. This serves scientific rigor, YouTube content (show *why* the model thinks what it thinks), and the uncertainty planner positioning.

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│  Layer 3: Monte Carlo Simulation            │
│  5,000 iterations                           │
│  Output: 10th / 50th / 90th %ile bands      │
├─────────────────────────────────────────────┤
│  Layer 2: Residual Learner                   │
│  V1: INACTIVE (no data)                      │
│  V2: Bayesian Linear (15-30 cooks)           │
│  V3: XGBoost (30+ cooks)                     │
├─────────────────────────────────────────────┤
│  Layer 1: Physics Kernel                     │
│  1D Heat Diffusion (Fourier's Law)           │
│  + Biological Variability (stochastic)       │
│  + Altitude Correction                       │
│  + Logistic Stall Model                      │
└─────────────────────────────────────────────┘
```

> **V1 ships Layers 1 + 3 only.** Physics kernel with biological variability feeds directly into Monte Carlo. Uncertainty quantification from day one, zero training data required. Layer 2 activates when sufficient cook data exists.

---

### Cook State Machine

> **Note:** Added per GPT-4.5 review. A cook is inherently state-based. Without explicit states, implementation devolves into nested conditionals. Claude Code should implement this as a clean state engine.

```
SETUP → PREHEAT → RAMP → STALL_WATCH → STALLING → POST_STALL → FINISHING → RESTING → DONE
```

| State | Entry Condition | Active Behaviors | Exit Condition |
|-------|----------------|-----------------|----------------|
| **SETUP** | User opens new cook | Collect inputs (protein, equipment, weather fetch, target dinner time). Run initial Monte Carlo. Display pre-cook prediction. | User presses "Start Cook" |
| **PREHEAT** | Cook started, no probe readings yet | Timer running. Waiting for first probe reading. | First probe reading logged |
| **RAMP** | First probe reading logged, temp < 140°F | Track temp slope. Update finish prediction on each reading. Normal progress messaging. | Internal temp ≥ 140°F (enters stall watch zone) |
| **STALL_WATCH** | Internal temp 140–185°F, not yet stalling | Run stall hazard model on each reading. Display stall probability in Nerd Mode. Normal Person Mode: "Cook may slow down soon." | Stall detected (slope < 0.02°F/min for ≥ 10 min) OR temp > 185°F without stall |
| **STALLING** | Stall detected by slope override OR hazard probability > 0.9 | Trigger intervention prompt (wrap options). Recalculate finish estimate. Display stall duration counter. | User wraps (adjusts evaporative cooling) OR slope resumes > 0.05°F/min naturally |
| **POST_STALL** | Stall exited (slope recovery or wrap effect) | Resume normal temp tracking. Tightened uncertainty bands. Updated finish prediction. | Internal temp within 5°F of target |
| **FINISHING** | Within 5°F of target temp | Alert: "Almost there — prepare your rest setup." Frequent prediction updates. | User logs pull temp and end time |
| **RESTING** | User pulls meat and selects rest method | Hold phase calculator active (Newton's Law of Cooling). Timer. "Safe to eat" countdown based on rest method. | Rest complete (user marks done) |
| **DONE** | Rest complete | Generate post-cook report. Prompt quality assessment. Save all data. | Cook session closed |

**Implementation notes:**
- State transitions are driven by user probe entries (V1) — not automatic sensor data.
- The state machine should be visible in Nerd Mode as a progress indicator.
- Normal Person Mode shows simplified phase messaging without state labels.
- Every state transition is timestamped and logged as part of the cook session data.

---

### Layer 1: Physics Kernel

#### 1D Heat Diffusion (Core Model)

Models thermal conductivity from surface to geometric center using Fourier's Law.

**Why 1D, not 3D FEA:** The dominant thermal gradient is surface-to-center along the thickest axis. The dominant *error* sources are biological (fat, moisture, connective tissue), not geometric. 1D is sufficient through at least Phase 2. Revisit only if residual analysis implicates geometry as a primary error source.

#### Altitude Correction

Ceiling on surface temperature based on local boiling point:

```
T_bp = 212°F - (1.5°F × Altitude / 1000)
```

#### Biological Variability

Stochastic noise in thermal diffusivity, fat distribution, and connective tissue density is modeled **in Layer 1**, not deferred to Monte Carlo. Meat isn't a uniform copper block — it's a biological variable. This ensures Monte Carlo simulations are grounded in reality from day one.

#### Stall Model: Hazard-Based Probability + Detection Override

##### Philosophy

> *The model does not attempt to deterministically predict the stall. It probabilistically bounds the stall window pre-cook, estimates onset probability as the cook progresses, and detects actual stall onset from probe data in real time.*

The stall is an **event**, not a value. We model the probability that the stall begins in the next time interval — not the exact moment it will start. This is more stable, more honest, and better UX.

##### Architecture: Two Complementary Systems

| System | Type | Purpose |
|--------|------|---------|
| **Stall Probability Model** | Predictive (logistic hazard) | Estimates stall likelihood as conditions evolve |
| **Stall Detection Override** | Deterministic (slope monitor) | Confirms stall onset from actual probe data |

Both run simultaneously. The probability model informs uncertainty bands. The detection override provides ground truth.

##### The Hazard Model

Stall onset probability at time *t*:

```
P(stall at t) = σ(Z)

where σ = logistic function: 1 / (1 + e^(-Z))

Z = β₀
  + β₁(humidity)
  + β₂(wind_speed)
  + β₃(thickness)
  + β₄(temp_slope)              ← most important feature
  + β₅(-|current_temp - 160|)   ← distance from stall zone center
```

##### Temperature Gating (Stability Feature)

The model only activates within the physically possible stall window:

```python
if internal_temp < 140:
    P(stall) = 0       # Too early — evaporation hasn't dominated yet
elif internal_temp > 185:
    P(stall) = 0       # Past stall zone — evaporation phase complete
else:
    P(stall) = σ(Z)    # Run hazard model
```

This eliminates false positives and massively stabilizes predictions.

##### Physics-Informed Prior Coefficients (Pre-Data)

Directionally correct starting values. The residual learner (Phase 2) and empirical calibration will refine them.

| Variable | Coefficient | Direction | Physical Rationale |
|----------|------------|-----------|-------------------|
| Intercept (β₀) | -3.0 | — | Base rate: stall is not the default state |
| Humidity (β₁) | +0.02 | Higher → more evaporative cooling | Wet-bulb effect |
| Wind speed (β₂) | +0.1 | More airflow → more surface evaporation | Convective mass transfer |
| Thickness (β₃) | +0.5 | Thicker → more water reservoir | More moisture to evaporate |
| Temp slope (β₄) | -4.0 | Fast-rising temp → not stalling | Direct contradiction of stall state |
| Distance from 160°F (β₅) | +0.15 | Closer to 160°F → higher likelihood | Stall zone center ~155–165°F |

##### Stall Detection Override (Deterministic)

Regardless of hazard model output, hard-detect the stall when:

```
IF temp_slope < 0.02°F/min for ≥ 10 consecutive minutes of logged readings
→ STALL DETECTED (override probability to 1.0)
```

This ensures even if the hazard model misjudges conditions, the system catches the stall from observed data.

##### Stall UX Output

**Normal Person Mode:**
- Pre-stall: No mention of stall (don't confuse casual users).
- Stall zone entered (140°F+): "Your cook may slow down for a while — this is normal."
- Stall detected: Triggers intervention recommendation (see below).

**Nerd Mode:**
- Live stall probability gauge (0–100%) updating with each probe reading.
- Slope chart showing dT/dt with stall threshold line.
- Stall zone shading on temperature timeline (140–185°F band).

##### Evolution Path

| Phase | Upgrade |
|-------|---------|
| V1 | Physics-informed prior coefficients (hardcoded). Detection override. |
| V2 | Learn β weights from logged cook data. |
| V2+ | Add interaction terms (humidity × wind, thickness × fat cap). |
| V3 | Replace logistic with gradient-boosted hazard model. |
| V3+ | Per-equipment stall calibration. |

---

#### Stall-Triggered Intervention Recommendations

When stall is detected, the app surfaces a contextual recommendation with tradeoff explanation. This is a **suggestion, not a directive** — different users have different goals.

##### The Science Behind the Recommendation

Smoke ring formation is driven by NO₂ and CO reacting with myoglobin. This reaction effectively stops at ~140–150°F when surface proteins denature. Since the stall occurs at 150–170°F, **by the time the stall begins, smoke absorption is essentially complete.** Wrapping at stall onset does not sacrifice meaningful smoke flavor.

##### Intervention Prompt

**Normal Person Mode** (when stall detected):

```
┌─────────────────────────────────────────────┐
│  🌡️ Your brisket has entered the stall.     │
│                                             │
│  This is normal — the meat is sweating,     │
│  which slows cooking.                       │
│                                             │
│  Wrapping now could save ~60–90 min.        │
│  Your smoke flavor is already locked in.    │
│                                             │
│  Trade-off:                                 │
│  • Wrap → Faster finish, more moisture,     │
│           softer bark                        │
│  • No wrap → Crunchier bark, longer wait    │
│                                             │
│  [🫔 I'm wrapping]  [🔥 Riding it out]      │
└─────────────────────────────────────────────┘
```

**Nerd Mode** adds:
- Estimated time saved by wrapping (from current stall depth and humidity)
- Wrap material comparison: butcher paper (semi-permeable, preserves some bark) vs. foil (full steam, fastest but softest bark) vs. foil boat (compromise — bottom/sides wrapped, top exposed)
- Physics explanation (smoke ring chemistry, latent heat of vaporization)

##### Wrap Options (Logged as Intervention Events)

| Option | Effect on Model | Data Logged |
|--------|----------------|-------------|
| **Butcher Paper** | Reduces evaporative cooling ~60%. Adjusts stall duration estimate. | {timestamp, action: "wrap_butcher_paper", temp_at_wrap} |
| **Foil (Texas Crutch)** | Eliminates evaporative cooling ~95%. Predicts stall exit within 30–60 min. | {timestamp, action: "wrap_foil", temp_at_wrap} |
| **Foil Boat** | Partial wrap. Reduces evaporative cooling ~40–50%. Preserves top bark. | {timestamp, action: "wrap_foil_boat", temp_at_wrap} |
| **No Wrap** | No adjustment. Continue monitoring slope for natural stall exit. | {timestamp, action: "no_wrap_decision"} |

##### Post-Wrap Model Adjustment

When user selects a wrap option:
- **Evaporative cooling coefficient** reduced based on wrap type
- **Stall exit prediction** recalculated with new evaporation rate
- **Finish time estimate** updated and displayed immediately
- **Uncertainty bands** narrow (wrapping reduces a major variance source)

This creates a satisfying feedback loop: user decides → model shows impact → finish time tightens.

#### Hold Phase (Post-Cook)

- **Passive Hold:** Newton's Law of Cooling in insulated environment (cooler/Cambro) until 145°F safety floor.
- **Active Hold:** Low-temp oven (~150°F), modeling moisture retention vs. continued collagen breakdown.

#### Pasteurization (V2+ — Sous Vide Only)

Logarithmic Reduction Tables (USDA-FSIS). Lethality = f(Time × Temperature). Deferred from V1.

---

### Layer 2: Residual Learner (V2+)

Predicts the **residual** (error) between Layer 1 and reality. Does NOT predict cook time directly.

**Activation Path:**

| Cook Count | Model | Rationale |
|-----------|-------|-----------|
| 0–15 | Inactive | Insufficient data. Physics + Monte Carlo only. |
| 15–30 | Bayesian Linear Model | Better small-sample performance than tree models. |
| 30+ | XGBoost (aggressive L1/L2 regularization, 5–8 features max) | Enough data for tree-based learning. |

**Requirements when activated:**
- Feature normalization
- Temporal features (time of day, season)
- Leakage prevention checklist before training
- SHAP values for interpretability post-training (also great content)

---

### Layer 3: Monte Carlo Simulation

**Active from V1.** This is what produces the uncertainty bands that define the product.

- Passes Layer 1 output through **5,000 iterations**
- Varies: smoker temp fluctuations, wind gusts, fuel inconsistency, biological variability
- **Output:** 10th, 50th, and 90th percentile finish times
- V1: Fixed 5,000 iterations (computationally trivial, converges reliably at this problem scale)
- V2+: Adaptive convergence (stop when CI width stabilizes < 1 min over last 500 samples)

---

### Real-Time Bayesian Updating (Phase 3)

Mid-cook prediction revision using live probe data.

- **Update trigger:** Event-driven, not time-based. Fire on: new probe reading, OR slope deviation > 5°F from predicted curve.
- **V1:** Manual probe logging (enter temp readings in app).
- **V2:** Manufacturer API integration (MEATER Cloud, FireBoard).
- **V3 (if ever):** Native Bluetooth.

---

### Backward Planning ("Dinner at 6 PM")

Primary UX entry point for Normal Person Mode. Works backwards from target meal time to calculate fire-start time. **Includes rest time in the calculation.**

---

### Equipment Profiles

Selectable profiles adjusting Monte Carlo variance parameters:

| Equipment Type | Temp Variance | Recovery Speed | Notes |
|---------------|---------------|----------------|-------|
| Offset stick-burner | High | Slow | Massive temp swings, high skill floor |
| Pellet grill (Traeger, RecTeq) | Low | Fast | PID-controlled, tight variance |
| Kamado (BGE, Kamado Joe) | Low | Slow | Excellent insulation, stable |
| Weber Smokey Mountain | Medium | Medium | Well-characterized baseline |
| Custom / Other | User-defined | User-defined | Manual variance input |

---

### Fire-Out Detection (Phase 3)

> **Note:** Identified by Gemini. None of the other reviewers caught this.

The system must distinguish between two events that look similar from the internal probe's perspective:

| Event | Internal Temp | Ambient Temp | Correct Response |
|-------|--------------|--------------|-----------------|
| **The Stall** | Plateaus | Stays at setpoint | "This is normal. Be patient." |
| **Fire Going Out** | Plateaus or drops | Drops below setpoint | "⚠️ Check your fire!" |

**Implementation (Phase 3 — requires Live Dashboard):**
- Monitor ambient temp curve alongside internal probe.
- If ambient drops > 25°F below setpoint for > 15 minutes → trigger "Check Your Fire" alert.
- This is critical for overnight cooks where the user is sleeping.
- Distinct visual/audio alert from stall notifications.

---

### Model Execution Pipeline (V1)

> **Note:** Added per GPT-4.5 review. The architecture sections above describe *what* each layer does. This section defines *the exact procedural sequence* when events occur.

#### On Cook Start (SETUP → PREHEAT)

```
1. Collect user inputs: protein, cut, mass, thickness, grade, fat cap, bone-in, aspect ratio
2. Collect cook method: equipment profile, target smoker temp, fuel, target internal temp, planned interventions
3. Fetch weather data (API call): ambient temp, humidity, wind speed, altitude
4. Cache weather data locally (offline fallback)
5. Calculate altitude-corrected boiling point
6. Load equipment variance profile
7. Load thermal diffusivity for protein/cut (textbook + biological noise range)
8. Run Monte Carlo simulation (5,000 iterations):
   - For each iteration:
     a. Sample thermal diffusivity from biological noise distribution
     b. Sample smoker temp from equipment variance profile
     c. Sample wind/humidity perturbations
     d. Run 1D heat diffusion forward in time
     e. Apply stall model (logistic hazard) to estimate stall window
     f. If stall predicted: estimate stall duration based on humidity/wrap plan
     g. Add hold/rest phase (Newton's Law of Cooling)
     h. Record total time to dinner
9. Compute percentiles: 10th, 50th, 90th
10. If target dinner time provided: calculate backward to fire-start time
11. Assign confidence level: HIGH (90th-10th spread < 90 min), MEDIUM (90-150 min), LOW (> 150 min)
12. Display results in Normal Person Mode / Nerd Mode
```

#### On Probe Reading Entry (RAMP / STALL_WATCH / STALLING / POST_STALL / FINISHING)

```
1. Log {timestamp, probe_temp} to cook session
2. Calculate temp slope (dT/dt) from last 3+ readings
3. Check state transition conditions:
   - If temp ≥ 140°F and state is RAMP → transition to STALL_WATCH
   - If slope < 0.02°F/min for ≥ 10 min and state is STALL_WATCH → transition to STALLING
   - If stalling and slope recovers > 0.05°F/min → transition to POST_STALL
   - If temp within 5°F of target → transition to FINISHING
4. If in STALL_WATCH (140-185°F):
   - Run stall hazard model: compute P(stall) = σ(Z) with current conditions
   - If P > 0.9 → transition to STALLING (even without 10-min slope confirmation)
5. If transitioning to STALLING:
   - Trigger intervention prompt (wrap options)
   - Await user decision → log structured wrap event
   - If wrap selected: adjust evaporative cooling coefficient
6. Recalculate finish estimate:
   - Use remaining heat diffusion from current temp to target
   - Apply adjusted stall parameters (if wrapped)
   - Re-run simplified Monte Carlo (1,000 iterations — lighter for responsiveness)
   - Update displayed prediction and confidence
7. Update Nerd Mode visualizations (slope chart, stall probability, timeline)
```

#### On Cook Complete (FINISHING → RESTING → DONE)

```
1. User logs pull temp and end time
2. User selects rest method (cooler/cambro/oven/none) and starts rest timer
3. Run hold phase calculator:
   - Newton's Law of Cooling from pull temp
   - Display "safe to serve" countdown (above 145°F floor)
   - Estimate when temp will stabilize
4. When rest complete (user marks done):
   - Prompt quality assessment (tenderness, moisture, bark, serve-to-guests flag)
   - If previous cooks of same cut exist: prompt pairwise comparison
   - Generate post-cook report:
     a. Predicted vs. actual temp curve overlay
     b. Predicted vs. actual finish time
     c. Residual (error) calculation and breakdown
     d. Phase timing comparison (predicted stall window vs. actual)
   - Save complete cook session to local storage
   - Update cook count toward Layer 2 activation threshold
   - Display: "Cook #X logged. Y more cooks until the model starts learning."
```

---

### Model Trust & Confidence Strategy

> **Note:** Added per GPT-4.5 review. Defines how the model handles degraded conditions, missing data, and anomalies. Prevents silent model failure — the #1 risk in predictive apps.

#### Confidence Levels

| Level | Condition | Display |
|-------|-----------|---------|
| **HIGH** | 90th–10th percentile spread < 90 min AND weather data fresh AND ≥ 3 consistent probe readings | Green indicator. "Confidence: HIGH" |
| **MEDIUM** | Spread 90–150 min OR weather data > 2 hrs old OR fewer than 3 probe readings | Yellow indicator. "Confidence: MEDIUM — prediction will tighten with more readings" |
| **LOW** | Spread > 150 min OR weather data missing OR anomalous probe readings detected | Orange indicator. "Confidence: LOW — wide uncertainty range" |
| **UNRELIABLE** | Probe readings contradictory OR model inputs missing critical fields | Red indicator. "⚠️ Not enough data for a reliable estimate" |

#### Anomaly Detection (Simple Rules, V1)

| Anomaly | Detection Rule | Response |
|---------|---------------|----------|
| **Probe reading gap** | No reading logged for > 30 min during active cook | Downgrade confidence one level. Prompt: "Haven't heard from you — log a temp reading to keep predictions accurate." |
| **Temperature spike** | Reading > 20°F above previous in < 5 min | Flag as possible probe error. Prompt: "That's a big jump — is your probe positioned correctly?" Do NOT incorporate into slope calculation until confirmed. |
| **Temperature drop** | Reading drops > 10°F from previous | Could be lid open, fire issue, or probe shift. Prompt: "Temperature dropped — did you open the lid?" Log response. |
| **Impossible reading** | Temp > smoker setpoint + 50°F OR < ambient temp | Reject reading. Prompt: "That reading seems off — please re-check your probe." |
| **Stale weather** | Cached weather data > 4 hrs old | If online: refresh. If offline: continue with cached data but note in Nerd Mode: "Weather data is X hours old." |

#### Model Freeze Conditions

In extreme edge cases, the model should **freeze predictions** rather than display garbage:

- If 0 probe readings have been logged and cook has been running > 2 hours → freeze with message: "Log a probe reading to get an updated prediction."
- If 3+ consecutive readings are flagged as anomalous → freeze with message: "Recent readings seem unreliable — check your probe setup."
- Frozen predictions display last known good estimate with a "STALE" indicator.

---

## 7. Data Schema

### A. Protein & Geometry

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Category | Enum | Yes | Beef, Pork, Poultry, Lamb, Other |
| Cut | Enum (nested) | Yes | e.g., Beef → Brisket → Packer |
| Grade / Marbling | Enum | Yes | Select, Choice, Prime, Wagyu (or visual 1–5) |
| Mass | Float (lbs/kg) | Yes | Weighed at start |
| Thickness | Float (in/cm) | Yes | Measured at thickest point |
| Aspect Ratio | Float | Recommended | Length / Width |
| Initial Temp | Float (°F/°C) | Yes | Fridge (~38°F) vs. Room Temp (~68°F) |
| Bone-in | Boolean | Yes | Affects thermal conductivity |
| Fat Cap Thickness | Float (in/cm) | Recommended | Insulation layer |

### B. Environmental (API-Driven)

| Field | Source | Notes |
|-------|--------|-------|
| Ambient Temp | Weather API + GPS | Heat loss rate from vessel |
| Humidity | Weather API | Critical for stall prediction |
| Altitude / Barometric Pressure | GPS + API | Boiling point correction |
| Wind Speed | Weather API | Convective heat loss |

### C. Cooking Method

| Field | Type | Notes |
|-------|------|-------|
| Equipment Profile | Enum / Custom | See Equipment Profiles |
| Target Smoker Temp | Float | Setpoint temperature |
| Fuel Source | Enum | Charcoal, wood (species), pellets, gas, electric |
| Target Internal Temp | Float | Desired final internal temperature |
| Planned Interventions | Array | Wrap type + trigger temp, spritzing schedule, etc. |

### D. Per-Cook Logging (Training Data + Production Notes)

| Field | Type | Collection Method |
|-------|------|-------------------|
| Cook ID | UUID | Auto-generated |
| Start Time | Timestamp | Manual |
| Probe Readings | Array of {timestamp, temp} | Manual (V1); API (V2+) |
| Lid Open Events | Array of {timestamp, duration_min} | Manual toggle |
| Intervention Log | Array of {timestamp, action, notes} | Manual — includes structured wrap events (see below) |
| Weather Snapshots | Array of {timestamp, conditions} | Auto (API poll every 30 min) |
| Equipment Used | Equipment Profile ID | Manual selection |
| End Time | Timestamp | Manual |
| Pull Temp | Float | Manual |
| Rest Method | Enum | Cooler, Cambro, Oven, None |
| Rest Duration | Duration | Manual |
| **Quality Assessment** | | |
| Tenderness (1–10) | Integer | Anchored: 1=inedible, 5=serviceable, 10=competition |
| Moisture (1–10) | Integer | Same scale |
| Bark Quality (1–10) | Integer | Same scale |
| Would Serve to Guests | Boolean | Binary quality signal |
| Pairwise Comparison | Enum (A>B, A=B, A<B) | After 2+ cooks of same cut |
| Bite Test Photo | Image (optional) | Visual record |
| Notes / Anomalies | Text | Free-form |

#### Structured Wrap Event Format

Wrap decisions triggered by the stall intervention system are logged as structured events:

```json
{
  "timestamp": "2025-03-15T14:32:00",
  "action": "wrap_butcher_paper",       // wrap_foil | wrap_foil_boat | no_wrap_decision
  "internal_temp_at_event": 164.5,
  "stall_duration_at_wrap_min": 47,
  "stall_probability_at_wrap": 0.91,
  "notes": "Bark looked good. Wrapping to hit 6 PM dinner."
}
```

This enables future analysis of optimal wrap timing by cut/equipment, wrap material effectiveness, and correlation between wrap timing and quality scores.

### E. Thermal Diffusivity — Source Hierarchy

1. **Empirical calibration** (your own instrumented cooks — best, also content)
2. Academic food science journals
3. Engineering handbooks (Engineering Toolbox)
4. USDA tables (reference only — not designed for modeling)

**Starting values (to be replaced empirically):**

| Protein | α (× 10⁻⁷ m²/s) | Notes |
|---------|-------------------|-------|
| Beef | 1.23–1.33 | Lower end for fattier cuts (brisket) |
| Pork | 1.2–1.4 | Similar range to beef |
| Poultry | 1.3–1.5 | Higher moisture content |

---

### F. Implementable Data Models

> **Note:** Added per GPT-4.5 review. The tables above define fields conceptually. These are the code-level structures Claude Code should implement.

#### Core Models

```python
# --- Enums ---

class MeatCategory(str, Enum):
    BEEF = "beef"
    PORK = "pork"
    POULTRY = "poultry"
    LAMB = "lamb"
    OTHER = "other"

class MeatGrade(str, Enum):
    SELECT = "select"
    CHOICE = "choice"
    PRIME = "prime"
    WAGYU = "wagyu"

class EquipmentType(str, Enum):
    OFFSET = "offset"
    PELLET = "pellet"
    KAMADO = "kamado"
    WSM = "wsm"
    CUSTOM = "custom"

class FuelSource(str, Enum):
    CHARCOAL = "charcoal"
    WOOD_OAK = "wood_oak"
    WOOD_HICKORY = "wood_hickory"
    WOOD_MESQUITE = "wood_mesquite"
    WOOD_CHERRY = "wood_cherry"
    WOOD_APPLE = "wood_apple"
    PELLETS = "pellets"
    GAS = "gas"
    ELECTRIC = "electric"

class RestMethod(str, Enum):
    COOLER = "cooler"
    CAMBRO = "cambro"
    OVEN = "oven"
    NONE = "none"

class WrapType(str, Enum):
    BUTCHER_PAPER = "wrap_butcher_paper"
    FOIL = "wrap_foil"
    FOIL_BOAT = "wrap_foil_boat"
    NO_WRAP = "no_wrap_decision"

class CookState(str, Enum):
    SETUP = "setup"
    PREHEAT = "preheat"
    RAMP = "ramp"
    STALL_WATCH = "stall_watch"
    STALLING = "stalling"
    POST_STALL = "post_stall"
    FINISHING = "finishing"
    RESTING = "resting"
    DONE = "done"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNRELIABLE = "unreliable"


# --- Data Models ---

class ProteinProfile:
    category: MeatCategory
    cut: str                    # e.g., "packer_brisket", "pork_butt"
    grade: MeatGrade
    mass_lbs: float
    thickness_in: float
    aspect_ratio: float | None  # length / width, optional
    initial_temp_f: float       # typically 38 (fridge) or 68 (room)
    bone_in: bool
    fat_cap_thickness_in: float | None

class EnvironmentSnapshot:
    timestamp: datetime
    ambient_temp_f: float
    humidity_pct: float         # 0-100
    wind_speed_mph: float
    altitude_ft: float
    barometric_pressure_inhg: float | None

class EquipmentProfile:
    equipment_type: EquipmentType
    name: str                   # user-facing label
    temp_variance_f: float      # std dev of temp fluctuations (°F)
    recovery_speed: str         # "slow", "medium", "fast"
    # Custom overrides (only for CUSTOM type):
    custom_variance: float | None
    custom_recovery: str | None

class CookMethod:
    equipment: EquipmentProfile
    target_smoker_temp_f: float
    fuel_source: FuelSource
    target_internal_temp_f: float
    planned_wrap: WrapType | None
    planned_wrap_temp_f: float | None

class ProbeReading:
    timestamp: datetime
    internal_temp_f: float
    is_anomalous: bool = False  # flagged by anomaly detection
    anomaly_reason: str | None

class LidOpenEvent:
    timestamp: datetime
    duration_min: float

class InterventionEvent:
    timestamp: datetime
    action: WrapType            # or free-form for non-wrap interventions
    internal_temp_at_event: float
    stall_duration_at_event_min: float | None
    stall_probability_at_event: float | None
    notes: str | None

class QualityAssessment:
    tenderness: int             # 1-10, anchored scale
    moisture: int               # 1-10
    bark_quality: int           # 1-10
    would_serve_to_guests: bool
    pairwise_comparison_cook_id: str | None  # UUID of compared cook
    pairwise_result: str | None              # "better", "equal", "worse"
    bite_test_photo_path: str | None
    notes: str | None

class StateTransition:
    timestamp: datetime
    from_state: CookState
    to_state: CookState
    trigger: str                # e.g., "temp_threshold", "slope_detection", "user_action"

class CookSession:
    id: str                     # UUID
    created_at: datetime
    protein: ProteinProfile
    cook_method: CookMethod
    environment_at_start: EnvironmentSnapshot
    weather_snapshots: list[EnvironmentSnapshot]   # polled every 30 min
    target_dinner_time: datetime | None

    # Predictions (updated throughout cook)
    initial_prediction_minutes: dict    # {"p10": int, "p50": int, "p90": int}
    current_prediction_minutes: dict    # updated on each probe reading
    recommended_start_time: datetime | None
    confidence: ConfidenceLevel

    # Live data
    current_state: CookState
    state_history: list[StateTransition]
    probe_readings: list[ProbeReading]
    lid_open_events: list[LidOpenEvent]
    interventions: list[InterventionEvent]

    # Completion
    start_time: datetime
    end_time: datetime | None
    pull_temp_f: float | None
    rest_method: RestMethod | None
    rest_duration_min: float | None
    quality: QualityAssessment | None

    # Post-cook analysis
    actual_total_minutes: float | None
    prediction_error_minutes: float | None  # actual - predicted p50
    stall_detected: bool
    stall_start_time: datetime | None
    stall_end_time: datetime | None
    stall_duration_min: float | None


# --- Prediction Output ---

class PredictionResult:
    p10_minutes: float          # optimistic (10th percentile)
    p50_minutes: float          # median
    p90_minutes: float          # conservative (90th percentile)
    p10_finish_time: datetime
    p50_finish_time: datetime
    p90_finish_time: datetime
    recommended_start_time: datetime | None  # if dinner time specified
    confidence: ConfidenceLevel
    predicted_stall_window: tuple[float, float] | None  # (earliest_min, latest_min) from cook start
    predicted_phases: list[dict]  # [{name, start_min, end_min, uncertainty_min}]
```

---

## 8. User-Facing Output Design

### Normal Person Mode (Default)

```
┌─────────────────────────────────────┐
│  🔥 Start your fire at: 7:42 AM    │
│  🍽️  Eat at: 6:00 PM               │
│  📊 Confidence: HIGH                │
│                                     │
│  ─────────────────────────────      │
│  [Timeline]  Smoke → Stall → Rest  │
│  ─────────────────────────────      │
│                                     │
│  [See Full Analysis] ← Nerd Mode   │
└─────────────────────────────────────┘
```

### Nerd Mode (Behind Toggle)

#### A. Timeline View (Pre-Cook)
- Gantt-style bar: **Smoke** → **Stall** (uncertainty width) → **Wrap** → **Target** → **Rest**
- Color-coded confidence bands (tight = high confidence, wide = uncertainty)
- Backward-planned start time prominent

#### B. Live Dashboard (Mid-Cook, Phase 3)
- Real-time temp curve overlaid on predicted envelope
- Bayesian revision delta (current vs. original prediction)
- Phase indicator: "Currently in: THE STALL"
- Updating countdown with confidence interval
- Alerts: "Running 45 min behind 50th %ile — consider wrapping to hit 6 PM"
- **Fire-out alert** (distinct from stall): "⚠️ Ambient temp dropping — check your fire!"

#### C. Post-Cook Report
- Predicted vs. actual curves
- Residual analysis
- Comparison to previous cooks of same protein
- Data auto-staged for Layer 2 retraining
- Shareable summary card (social media / YouTube community tab)

### Engagement Mechanics

- **Accuracy Streak:** Consecutive cooks within predicted 90th %ile band
- **"Beat the Model" Challenges:** Log cooks, compare to predictions (data collection + engagement)
- **Cook Library:** Searchable history with trend analysis

---

## 9. Development Roadmap

### Phase 0 — Foundation (Pre-Code) ← CURRENT PHASE

- [x] Three-layer architecture defined
- [x] Content strategy and sequencing defined
- [x] Committee review complete (Claude, Grok, ChatGPT, Gemini)
- [ ] Secure brand assets (domain, trademark, social handles)
- [ ] Set up cook logging spreadsheet — **START LOGGING IMMEDIATELY**
- [ ] Run audience validation survey (30–50 responses: r/smoking, r/datascience, r/BBQ)
- [ ] Build Google Sheets physics prototype → test with 10 pitmasters
- [ ] Design Normal Person Mode + Nerd Mode wireframes
- [ ] Define reference cook profiles (pork butt, brisket packer, ribs, chicken)
- [ ] Estimate detailed budget

### Phase 1 — Physics Engine MVP ← CLAUDE CODE BUILDS THIS

**Scope: BBQ/Smoking only. PWA. Layers 1 + 3. No ML.**

- [ ] Implement data models from Section 7F
- [ ] Cook state machine (10 states, transition engine per Section 6)
- [ ] 1D heat diffusion with textbook + empirical thermal diffusivity
- [ ] Biological variability as stochastic noise in Layer 1
- [ ] Weather API integration (OpenWeather free tier: ambient temp, humidity, wind, altitude)
- [ ] Altitude → boiling point correction
- [ ] Stall hazard model (logistic, physics-informed priors, temp-gated 140–185°F)
- [ ] Stall detection override (slope monitor on manual probe readings)
- [ ] Stall-triggered intervention recommendations (wrap prompt with tradeoff + model adjustment)
- [ ] Monte Carlo simulation (5,000 iterations) → uncertainty bands
- [ ] Backward planning: "Dinner at X" → "Start fire at Y"
- [ ] Model trust system (confidence levels, anomaly detection, freeze conditions per Section 6)
- [ ] Model execution pipeline (procedural sequences per Section 6)
- [ ] Normal Person Mode (single screen, default, stall messaging, wrap prompt)
- [ ] Nerd Mode (Timeline View + stall probability gauge + slope chart + state indicator, behind toggle)
- [ ] Manual probe logging interface (drives state transitions)
- [ ] Lid-open event logging
- [ ] Equipment profile selection (5 presets + custom)
- [ ] Post-cook report (predicted vs. actual, residual calculation, quality assessment)
- [ ] Cook logging capturing all Section 7D fields (including structured wrap events)
- [ ] Mobile-first responsive design (used outdoors next to smoker)
- [ ] Offline capability for core predictions (PWA service worker, weather cached on cook start)

### Phase 2 — Learning Loop

- [ ] Data ingestion from cook logs
- [ ] Bayesian linear model for residuals (15–30 cooks)
- [ ] XGBoost transition (30+ cooks, L1/L2 regularization, ≤8 features)
- [ ] SHAP value analysis
- [ ] Equipment profile calibration from empirical data
- [ ] Pairwise quality comparison system
- [ ] Model accuracy tracking dashboard

### Phase 3 — Real-Time + Engagement

- [ ] Bayesian updating (event-driven triggers)
- [ ] Live Dashboard view
- [ ] Fire-out detection and alerting (ambient temp monitoring)
- [ ] Probe manufacturer API integration (MEATER Cloud, FireBoard)
- [ ] Schedule risk alerts
- [ ] "Beat the Model" challenge mode
- [ ] Accuracy streak tracking
- [ ] Shareable post-cook summary cards
- [ ] Adaptive Monte Carlo convergence

### Phase 4 — Expansion (Gated)

- [ ] Sous vide module (pasteurization curves)
- [ ] Oven roasting module
- [ ] Community data sharing
- [ ] Public app release (freemium)
- [ ] Cook leaderboard

**Expansion gates — do NOT proceed without:**
- 50+ personally logged cooks
- 5,000+ YouTube subscribers
- Demonstrated user demand (survey or waitlist)

---

## 10. Pre-Code Experiments

### Experiment 1 — Prediction Baseline

5 pork butts (~$15–20 each), varied conditions. Compare: gut feel vs. linear regression vs. physics model.
**Gate:** If physics beats linear by < 10% → simplify physics.
**Content:** "My gut vs. math vs. physics: who wins?"

### Experiment 2 — Variance Source Analysis

3–5 cooks, same cut, same equipment, one variable changed:
- Series A: Different weather days → environmental variance
- Series B: Different meat sources → biological variance
**Gate:** Higher-variance source gets modeling priority.
**Content:** "Does weather or meat quality matter more?"

### Experiment 3 — User Value Test

Google Sheets physics prototype → 10 pitmasters.
Ask: "Would you use this weekly?"
**Gate:** < 60% yes → redesign UX. < 40% → rethink product.
**Not filmed.** Product validation only.

---

## 11. Resolved Technical Questions

| # | Question | Resolution | Resolved By |
|---|----------|-----------|-------------|
| 1 | Stall trigger logic | Logistic transition function. Replace with empirical fit over time. | ChatGPT + Gemini |
| 2 | Feature multicollinearity (altitude × humidity) | Tree models handle natively. Standardize for interpretability. SHAP post-training. | Grok + ChatGPT |
| 3 | Bayesian updating frequency | Event-driven: on probe reading or slope deviation > 5°F threshold. | ChatGPT + Claude |
| 4 | Probe integration path | Manual V1 → Manufacturer API V2 → No native Bluetooth. | All four |
| 5 | Thermal diffusivity sources | Empirical > journals > handbooks > USDA. Start textbook, replace measured. | Claude + Grok |
| 6 | Quality scoring bias | Anchored 1–10 + binary "serve to guests" (V1) → pairwise comparison (V2+). | ChatGPT + Claude |
| 7 | Tech stack | PWA through Phase 2 minimum. No native discussion until Phase 3+. | All four |
| 8 | Layer 2 model choice | Bayesian linear (15–30 cooks) → XGBoost (30+). Not XGBoost from start. | ChatGPT + Claude |
| 9 | Biological variability placement | Stochastic noise in Layer 1, not deferred to Layer 3. | ChatGPT |
| 10 | 1D vs 3D FEA | 1D sufficient. Dominant errors are biological, not geometric. | Claude + ChatGPT |
| 11 | Fire-out vs. stall discrimination | Monitor ambient temp; alert if > 25°F below setpoint for > 15 min. Phase 3. | Gemini |
| 12 | Stall modeling approach | Dual system: hazard-based probability (logistic, physics-informed priors, temp-gated 140–185°F) + deterministic slope detection override. Prediction + detection, not prediction alone. | GPT-4.5 + Claude |
| 13 | Intervention recommendations at stall | Non-judgmental wrap prompt with tradeoff quantification. Wrap type adjusts evaporative cooling coefficient and recalculates finish time. Decision logged as structured training data. Smoke flavor locked in by stall onset (myoglobin reaction stops ~140–150°F). | Claude |
| 14 | Cook state management | Explicit state machine: SETUP → PREHEAT → RAMP → STALL_WATCH → STALLING → POST_STALL → FINISHING → RESTING → DONE. State engine, not conditional logic. | GPT-4.5 + Claude |
| 15 | Model execution procedure | Step-by-step pipeline defined for cook start (12 steps), probe reading entry (7 steps), and cook complete (4 steps). See Section 6. | GPT-4.5 + Claude |
| 16 | Model trust / confidence | Four-tier confidence system (HIGH/MEDIUM/LOW/UNRELIABLE) with explicit anomaly detection rules and model freeze conditions. | GPT-4.5 + Claude |
| 17 | Data schema specificity | Code-level data models (Python classes) defined in Section 7F. Claude Code implements these directly. | GPT-4.5 + Claude |

---

## 12. Sustainability & Operations

### Burnout Prevention

- Weekly uploads are the commitment. Monthly experiments are stretch goals.
- Budget for video editing outsourcing by Month 3 if traction exists.
- The app is a personal tool until Phase 4. No public release pressure.

### Community

- [ ] Discord for beta testers (Month 3+)
- [ ] Engage r/smoking, r/BBQ, r/datascience for validation and distribution
- [ ] Consider open-sourcing physics kernel (GitHub) for credibility

### Budget Estimates

| Item | Cost | Frequency |
|------|------|-----------|
| Weather API (OpenWeather free tier) | $0 | Ongoing |
| Domain + hosting (PWA) | ~$15–30/mo | Monthly |
| Meat for experiments | ~$50–150/mo | Monthly |
| Filming gear (if not owned) | $200–500 | One-time |
| Video editing (outsourced) | $100–300/mo | Monthly (Month 3+) |
| Trademark filing | ~$250–350 | One-time |

---

## 13. Claude Code Implementation Guide

> **This section is the handoff spec. Claude Code should read this first.**

### What to Build

**Phase 1 MVP only.** Do not build Phases 2–4.

### Tech Stack

- **Frontend:** React (or Svelte) — mobile-first responsive PWA
- **Backend:** Python (FastAPI or Flask)
- **Simulation:** Python (NumPy/SciPy for physics + Monte Carlo)
- **Weather:** OpenWeather API (free tier)
- **Storage:** SQLite for cook logs (single-user personal tool — no need for Postgres in V1)
- **Deployment:** PWA with service worker for offline core predictions

### Key Implementation References

| What | Where | Why It Matters |
|------|-------|----------------|
| Data models (code-level) | Section 7F | **Use these structures directly.** Do not invent your own schemas. |
| Cook state machine | Section 6 (Cook State Machine) | **Implement as a state engine**, not nested conditionals. |
| Model execution pipeline | Section 6 (Model Execution Pipeline) | **Follow this exact procedural sequence** for cook start, probe readings, and cook complete. |
| Model trust / confidence | Section 6 (Model Trust Strategy) | Implement confidence levels and anomaly detection rules as specified. |
| Stall model | Section 6 (Layer 1, Stall Model) | Dual system: hazard probability + slope detection override. Use the specified prior coefficients. |
| Intervention system | Section 6 (Stall-Triggered Interventions) | Wrap prompt with tradeoff display. Log decisions as structured events. |

### Build Order (Critical Path)

1. **Data models** — Implement all models from Section 7F. This is the foundation everything else depends on.
2. **State machine** — Implement CookState enum and state transition engine per Section 6 state machine table.
3. **Physics kernel** — 1D heat diffusion with textbook diffusivity values per protein/cut
4. **Biological noise** — Stochastic variability in diffusivity parameters
5. **Altitude correction** — Boiling point adjustment from user location
6. **Monte Carlo wrapper** — 5,000 iterations over physics kernel with noisy inputs
7. **Backward planner** — "Dinner at X" → "Start at Y" (include rest time)
8. **Stall hazard model** — Logistic function with physics-informed prior coefficients (see Section 6). Temperature-gated: only active 140–185°F. Inputs: humidity, wind, thickness, temp slope, distance-from-160.
9. **Stall detection override** — Slope monitor on manually logged probe readings. Trigger when dT/dt < 0.02°F/min for ≥ 10 consecutive minutes of entries.
10. **Intervention recommendation system** — When stall detected, prompt user with wrap options (butcher paper / foil / foil boat / no wrap). Display tradeoff. Log decision as structured intervention event. Adjust evaporative cooling coefficient by wrap type. Recalculate and display updated finish estimate immediately.
11. **Weather API integration** — Fetch ambient temp, humidity, wind, altitude on cook start; cache for offline
12. **Equipment profiles** — 5 presets + custom; each defines variance parameters for Monte Carlo
13. **Model trust system** — Confidence levels, anomaly detection rules, model freeze conditions per Section 6.
14. **Cook logging interface** — All fields from Section 7D, including structured wrap events. Drive state transitions on probe entry.
15. **Normal Person Mode** — Single screen: start time, eat time, confidence level. Stall messaging when in zone. Wrap prompt when detected.
16. **Nerd Mode** — Timeline View with phase bars, confidence bands, stall probability gauge, slope chart, state indicator.
17. **Post-cook report** — Predicted vs. actual overlay, residual calculation, quality assessment prompt, auto-save to cook history.
18. **Hold phase calculator** — Newton's Law of Cooling for rest period estimation

### Design Constraints

- **Mobile-first.** Used outdoors next to a smoker, often in sunlight. High contrast, large touch targets.
- **Offline-capable.** Core predictions must work without internet after initial weather fetch.
- **Two UX modes from day one.** Normal Person Mode is default. Nerd Mode behind a clearly labeled toggle.
- **No ML in V1.** Layer 2 is stubbed out (interface exists, model inactive, displays "Collecting data — X more cooks needed").
- **Data persistence.** Every cook logged is stored locally and exportable as CSV/JSON for future ML training.
- **Stall model uses hardcoded physics-informed coefficients in V1.** No learned weights. Coefficients are directionally correct priors refined by residual learner in Phase 2.
- **Intervention prompts are non-judgmental.** Both "wrap" and "ride it out" are valid choices. The app quantifies the tradeoff; the user decides.
- **Every wrap/no-wrap decision is logged** as structured training data with timestamp, internal temp, stall duration, and stall probability at decision point.

### What NOT to Build

- No Bluetooth probe integration
- No real-time Bayesian updating (Phase 3)
- No live dashboard (Phase 3)
- No fire-out detection (Phase 3)
- No sous vide or oven roasting modules (Phase 4)
- No community features or data sharing (Phase 4)
- No user authentication or multi-user support (personal tool only)
- No app store deployment (PWA only)

---

## Revision Log

| Date | Reviewer | Changes |
|------|----------|---------|
| 2025-02-11 | Claude (Opus) | v1.0 — Initial consolidated spec. |
| 2025-02-12 | Grok 4 | Review — Competitors, SEO, gamification, monetization, thermal values. |
| 2025-02-12 | ChatGPT (GPT-4.5) | Review — Uncertainty reframe, KPIs, segmentation, Normal/Nerd UX, missing variables, logistic stall, pairwise scoring, pre-code experiments, Layer 1 bio noise. |
| 2025-02-12 | Gemini | Review — Validated v1.0 and v1.1. Added fire-out vs. stall discrimination. Confirmed logistic stall, Bayesian updating, backward planning as primary UX. |
| 2025-02-12 | Claude (Opus) | v1.1 — Full committee reconciliation. |
| 2025-02-12 | Claude (Opus) | **v1.2 (FINAL)** — Added fire-out detection spec (Gemini). Tightened Claude Code handoff with explicit build order and "what NOT to build" list. Cleaned revision log. Committee stamp: COMPLETE. |
| 2025-02-12 | GPT-4.5 | Post-v1.2 — Proposed hazard-based stall probability model with physics-informed priors, temperature gating, detection override, and realistic accuracy targets by model stage. |
| 2025-02-12 | Claude (Opus) | **v1.2.1 (FINAL — MERGED)** — Integrated hazard-based stall model into Layer 1. Added intervention recommendation system (wrap prompt with tradeoff quantification, wrap-type model adjustment, structured event logging). Updated Claude Code build order (6→8 stall-related steps), design constraints, Phase 1 checklist, data schema, and resolved questions. |
| 2025-02-12 | GPT-4.5 | Post-v1.2.1 — Identified implementation gaps: missing state machine, execution pipeline, data model schemas, trust strategy, API contract. Scored spec as ~80% ready for AI build agent. |
| 2025-02-12 | Claude (Opus) | **v1.3 (FINAL)** — Added cook state machine (10 states with explicit transitions). Added model execution pipeline (procedural step-by-step for cook start, probe entry, cook complete). Added model trust & confidence strategy (4-tier confidence, anomaly detection, model freeze conditions). Added code-level data models (Python classes for all entities). Restructured Claude Code handoff with key reference table and updated 18-step build order. All implementation-blocking gaps resolved. |
