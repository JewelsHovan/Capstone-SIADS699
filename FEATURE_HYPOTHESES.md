# Feature Hypotheses for Work Zone Crash Risk Prediction

## Research Questions
1. Can we predict which active work zones will have high crash risk?
2. What road/traffic/weather factors most influence crash severity?
3. Can we identify optimal timing for work zones (lower risk windows)?

## Feature Hypotheses

### 🛣️ Road Geometry Features (OSMnx)

**H1: Highway Type**
- **Hypothesis**: Motorways (interstates) have higher crash severity than residential roads
- **Reasoning**: Higher speeds → more severe impacts
- **Expected**: motorway > motorway_link > secondary > residential

**H2: Number of Lanes**
- **Hypothesis**: More lanes = higher crash risk (more lane changes, merging)
- **Reasoning**: Work zones reduce lanes → forced merging → conflicts
- **Expected**: Positive correlation with crash count

**H3: Road Curvature (Sinuosity)**
- **Hypothesis**: Curved roads + work zones = higher crash risk
- **Reasoning**: Reduced visibility, surprise work zone encounters
- **Expected**: sinuosity > 1.1 increases risk by 2x

**H4: Bridges/Tunnels**
- **Hypothesis**: Infrastructure + work zones = elevated risk
- **Reasoning**: Confined space, no escape routes
- **Expected**: is_bridge=1 or is_tunnel=1 → higher severity

**H5: Speed Limit**
- **Hypothesis**: High speed limit + work zone = severe crashes
- **Reasoning**: Higher speeds at work zone entry → rear-end collisions
- **Expected**: speed_limit > 60mph increases severity

### 🚗 Traffic Features

**H6: AADT (Traffic Volume)**
- **Hypothesis**: High AADT = more crashes, but not necessarily more severe
- **Reasoning**: More exposure, but speeds may be lower due to congestion
- **Expected**: AADT > 50,000 → 3x crash rate, but similar severity

**H7: AADT × Work Zone Interaction**
- **Hypothesis**: High traffic + lane closure = extreme risk
- **Reasoning**: Bottleneck effect, aggressive driving
- **Expected**: AADT > 50k AND lanes_closed > 50% → 5x risk

### ⏰ Temporal Features

**H8: Rush Hour**
- **Hypothesis**: Rush hour work zones have higher crash rate but lower severity
- **Reasoning**: More vehicles (exposure) but slower speeds
- **Expected**: is_rush_hour=1 → 2x crashes, 0.7x severity

**H9: Weekend vs Weekday**
- **Hypothesis**: Weekend crashes more severe
- **Reasoning**: Higher speeds, less traffic enforcement, possible impairment
- **Expected**: is_weekend=1 → 1.3x severity

**H10: Time of Day**
- **Hypothesis**: Night work zones are most dangerous
- **Reasoning**: Reduced visibility, fatigue, insufficient lighting
- **Expected**: night (10pm-6am) → 2x severity

### 🌦️ Weather Features

**H11: Adverse Weather**
- **Hypothesis**: Rain/fog + work zone = severe crashes
- **Reasoning**: Reduced visibility, longer stopping distance, slippery roads
- **Expected**: adverse_weather=1 → 2x severity

**H12: Low Visibility**
- **Hypothesis**: Visibility < 5 miles dramatically increases risk
- **Reasoning**: Can't see work zone signs in time
- **Expected**: low_visibility=1 → 3x crash rate

**H13: Temperature Extremes**
- **Hypothesis**: Freezing temps increase severity
- **Reasoning**: Ice, reduced tire traction
- **Expected**: temp_category='freezing' → 1.8x severity

**H14: Weather × Time Interaction**
- **Hypothesis**: Adverse weather + night = extreme danger
- **Reasoning**: Compounding factors (can't see AND conditions bad)
- **Expected**: adverse_weather=1 AND night → 4x risk

### 🏙️ Location Features

**H15: Urban vs Rural**
- **Hypothesis**: Urban work zones have more crashes but lower severity
- **Reasoning**: High exposure but lower speeds
- **Expected**: is_urban=1 → 2x crashes, 0.6x severity

**H16: Infrastructure Density**
- **Hypothesis**: Areas with many signals/intersections = higher risk
- **Reasoning**: More conflict points, confusion
- **Expected**: Traffic_Signal=1 OR Junction=1 → 1.4x risk

## Interaction Hypotheses (Most Important!)

**H17: The Perfect Storm**
```
High Risk = motorway AND AADT > 50k AND rush_hour AND adverse_weather
Expected Risk Multiplier: 8-10x baseline
```

**H18: Safe Work Zone Profile**
```
Low Risk = residential AND AADT < 10k AND NOT rush_hour AND clear_weather AND daytime
Expected Risk Multiplier: 0.2x baseline (80% reduction)
```

**H19: Work Zone Timing Optimization**
```
Risk Reduction: Same road, night work (10pm-5am) vs day work (7am-6pm)
Expected: 60% crash reduction for night work on high-traffic roads
```

## Expected Model Performance

**Baseline (Random)**: 24% high severity rate
**Target Performance**:
- Accuracy: 75-80%
- Precision (high severity): 60-70%
- Recall (high severity): 50-60%
- AUC-ROC: 0.75-0.85

**Most Important Features (Expected Top 5)**:
1. AADT (traffic volume)
2. highway_type (road class)
3. is_rush_hour (temporal)
4. adverse_weather (weather)
5. num_lanes (capacity)

## Validation Strategy

1. **Feature Importance**: Check if hypotheses H1-H19 align with model weights
2. **SHAP Values**: Understand feature interactions
3. **Subgroup Analysis**: Validate hypotheses on specific road types
4. **Temporal Validation**: Ensure 2022 val performs similar to 2021 train

## Application to Active Work Zones

Once model is trained:
```python
# For each active work zone
risk_score = model.predict_proba(work_zone_features)

# Recommendations
if risk_score > 0.7:
    -> "High Risk: Add extra signage, enforce speed limit, consider night work"
elif risk_score > 0.4:
    -> "Medium Risk: Standard precautions, monitor closely"
else:
    -> "Low Risk: Standard work zone procedures"
```

## Success Metrics

**Research Success**: Hypotheses validated or rejected with p < 0.05
**Application Success**: Reduce work zone crashes by 20% through better planning
**Deployment Success**: TxDOT adopts risk scoring for work zone permits

