# Magnetic Generator Battery Storage: Sizing and Setup Guide (2026)

A magnetic generator produces electricity, but to use it reliably you need battery storage. Proper battery sizing ensures you have power when the wind isn't blowing, the sun isn't shining, or you're not pedaling.

Here's how to size and set up battery storage for your magnetic generator.

## Why You Need Battery Storage

Magnetic generators are intermittent power sources. You need batteries to:
- **Smooth out variations** — Store excess when producing, draw when not
- **Handle surge loads** — Batteries absorb motor starting current
- **Provide backup** — Power during low-generation periods
- **Stabilize voltage** — Consistent output regardless of prime mover speed

## Battery Types for Magnetic Generators

### LiFePO4 (Lithium Iron Phosphate) — Best Choice

- **Cycle life:** 3,000–5,000+ cycles
- **Depth of discharge:** 80–90% (recommended)
- **Weight:** 1/3 the weight of lead-acid
- **Efficiency:** 95–98%
- **Cost:** $400–$600 per kWh
- **Lifespan:** 10–15 years
- **Best for:** Primary storage for magnetic generators

### AGM (Absorbent Glass Mat) — Budget Option

- **Cycle life:** 500–1,000 cycles
- **Depth of discharge:** 50% (recommended)
- **Weight:** Heavy
- **Efficiency:** 85–90%
- **Cost:** $200–$300 per kWh
- **Lifespan:** 3–5 years
- **Best for:** Budget builds, cold climates

### Gel — Middle Ground

- **Cycle life:** 800–1,200 cycles
- **Depth of discharge:** 50–60%
- **Efficiency:** 90–95%
- **Cost:** $250–$400 per kWh
- **Lifespan:** 4–6 years
- **Best for:** Deep cycle applications

## Sizing Your Battery Bank

### Step 1: Calculate Daily Energy Use

List every device and its daily energy consumption:

| Device | Watts | Hours/Day | Daily kWh |
|--------|-------|-----------|-----------|
| LED lights (5) | 25W | 6 | 0.15 |
| Refrigerator | 100W | 8 (cycle) | 0.80 |
| Laptop | 65W | 4 | 0.26 |
| TV | 100W | 3 | 0.30 |
| Phone charging | 15W | 4 | 0.06 |
| **Total daily** | | | **1.57 kWh** |

### Step 2: Determine Days of Autonomy

How many days should the system run without generation?
- **1 day:** Budget, backup only
- **2–3 days:** Recommended for most setups
- **5+ days:** Off-grid, remote locations

### Step 3: Calculate Battery Capacity

**Formula:** Daily kWh × Days of autonomy ÷ Depth of discharge = Required kWh

For a 1.57 kWh/day system with 2 days autonomy and 90% DoD:
- 1.57 × 2 ÷ 0.9 = **3.5 kWh minimum**

### Step 4: Convert to Amp-Hours

**Amp-hours = kWh × 1,000 ÷ System Voltage**

For a 48V system:
- 3.5 kWh × 1,000 ÷ 48V = **73Ah minimum**
- Recommended: **100Ah @ 48V** (for margin)

## Recommended Battery Bank Sizes

| Application | Daily kWh | Battery Bank (48V) | Estimated Cost |
|------------|-----------|-------------------|---------------|
| Lights + phone | 0.5 kWh | 50Ah | $400–$600 |
| Small home (essential) | 2 kWh | 200Ah | $1,200–$2,000 |
| Medium home | 4 kWh | 400Ah | $2,000–$3,500 |
| Large home | 8 kWh | 800Ah | $4,000–$7,000 |

## Wiring Batteries for Your Generator

### Series vs. Parallel

- **Series:** Increases voltage (adds voltages)
- **Parallel:** Increases capacity (adds amp-hours)

**Example:** Four 12V 100Ah batteries
- All series: 48V 100Ah (4.8 kWh)
- Two series pairs in parallel: 24V 200Ah (4.8 kWh)
- All parallel: 12V 400Ah (4.8 kWh)

**Best for magnetic generators:** Higher voltage (48V) reduces current and wire size.

### Charge Controller Connection

```
Generator → Charge Controller → Battery Bank → Inverter → Loads
```

- Use an **MPPT charge controller** for maximum efficiency
- Size controller for your generator's max output (e.g., 30A for 500W at 48V)
- Install a **battery monitor** (Victron BMV-712 or similar)

## Maintenance for Battery Banks

### LiFePO4

- **Monthly:** Check state of charge, cell balance
- **Quarterly:** Full charge cycle
- **Annually:** Visual inspection, terminal torque check
- **Every 5 years:** Replace (end of life)

### AGM

- **Monthly:** Check electrolyte (if accessible), terminal corrosion
- **Quarterly:** Equalization charge
- **Annually:** Load test
- **Every 3–5 years:** Replace

## Conclusion

Proper battery storage is essential for reliable magnetic generator operation. For most home applications, a 200–400Ah LiFePO4 bank at 48V provides reliable, long-lasting storage that will outlast the generator itself.

For sizing details, see our [how much electricity a magnetic generator produces](../how-much-electricity-does-a-magnetic-generator-produce.html) guide.

---

*Next: Learn about [magnetic generator inverter setups](../tesla-magnetic-generator-inverter-setup.html).*
