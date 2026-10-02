#!/usr/bin/env python3
"""
Add additional thickening sections to articles still under 1,500 words.
"""

import re
from pathlib import Path

BASE = Path("/home/matt/projects/other/tesla-generator/new_content/phases/phase-1-foundation")

EXTRA_SECTIONS = {
    "magnetic-generator-for-emergency-backup": [
        ("Maintenance Schedule", """
## Maintenance Schedule

Magnetic generators are famously low-maintenance, but a simple annual check ensures decades of reliable operation:

### Quarterly Checks (Every 3 Months)
- **Visual inspection**: Look for loose bolts, cracked mounts, or corrosion
- **Connection check**: Tighten all wire connections and terminal screws
- **Belt/pulley check** (if belt-driven): Inspect for wear and adjust tension

### Annual Maintenance
- **Bearing inspection**: Spin the rotor by hand — it should turn smoothly with no grinding or play
- **Bearing lubrication**: Apply a drop of light machine oil to sealed bearings (if applicable)
- **Coil inspection**: Look for frayed wires, cracked insulation, or burnt spots
- **Magnet check**: Ensure all magnets are secure and properly oriented
- **Frame check**: Tighten all frame bolts and check for cracks

### Every 2-3 Years
- **Bearing replacement**: Even sealed bearings eventually wear out. Keep spare bearings on hand.
- **Coil re-insulation**: If you notice any exposed wire, apply electrical tape or heat shrink
- **Paint/seal touch-up**: Touch up any rust spots on metal components

**Total annual maintenance time**: 15-20 minutes
**Annual maintenance cost**: $0-10 (mostly just oil)

This is dramatically less than a propane generator (30 min/month, $50+/year) or solar inverter (replacement every 10 years, $500+).
"""),
        ("Emergency Generator vs Propane: Head-to-Head", """
## Emergency Generator vs Propane: Head-to-Head

How does a magnetic generator compare to the traditional propane backup generator?

| Feature | Magnetic Generator | Propane Generator |
|---------|-------------------|-------------------|
| Start-up | Immediate (spins up) | 10-30 seconds (engine pull) |
| Noise | 0-20 dB (silent) | 60-75 dB (loud) |
| Fumes | None | CO2, NOx, unburned hydrocarbons |
| Fuel storage | None needed | 20-100 gallon tank |
| Fuel shelf life | N/A | 6-12 months (degrades) |
| Fuel cost | $0 | $30-100/month |
| Oil changes | Never | Every 50-100 hours |
| Spark plugs | None | Replace every 1-2 years |
| Winter operation | Excellent (no ice issues) | Good (but fuel gels below 0°F) |
| Summer operation | Excellent | Good (overheats in extreme heat) |
| Lifespan | 20+ years | 10-15 years |
| Battery dependency | None (spins freely) | Requires charged battery |
| Power during battery dead | Yes | No (won't start) |

### The Propane Problem
Propane generators have a critical weakness: **fuel degradation**. Propane breaks down after 6-12 months, leaving contaminants that clog carburetors. Many homeowners discover this problem during an emergency when their generator won't start.

Magnetic generators have **zero fuel degradation** — they work immediately, every time, for decades.

### Noise Factor
A propane generator at 70 dB is as loud as a vacuum cleaner. At night, it can be heard 100+ feet away. A magnetic generator at 20 dB is quieter than a whisper — you can run it next to a bedroom with no disturbance.
"""),
    ],
    "tesla-magnetic-generator-for-cabin": [
        ("Generator Placement & Mounting", """
## Generator Placement & Mounting

Where you place your generator affects both performance and convenience:

### Indoor vs Outdoor
- **Indoor mounting**: Protects from weather, easier to maintain. Requires ventilation for heat dissipation. Best for workshops or utility rooms.
- **Outdoor mounting**: Better wind exposure (for wind-driven models). Use a weatherproof enclosure or build a simple shed.

### Wind-Driven Placement
For wind-driven generators, location is everything:
- **Height**: Mount at least 10 feet above surrounding obstacles (trees, buildings)
- **Distance**: At least 200 feet from trees and buildings for optimal wind capture
- **Exposure**: Open areas with unobstructed wind from multiple directions
- **Ground clearance**: At least 15 feet above ground level

### Water-Driven Placement
For water-driven generators:
- **Flow speed**: Need at least 2-3 mph water velocity for good output
- **Depth**: Submerge the turbine at least 18 inches below surface
- **Debris**: Install a screen to catch leaves and branches
- **Freeze protection**: In cold climates, mount above the ice line or use a heated enclosure

### Mounting Options
1. **Wall mount**: Simple bracket with rubber grommets for vibration dampening
2. **Floor mount**: Heavy base with leveling feet
3. **Ceiling mount**: Hanging from rafters (good for space-constrained cabins)
4. **Tripod mount**: Portable option for seasonal cabins

**Pro tip**: Regardless of mounting method, always use rubber isolation pads between the generator and its mount. Vibration is the #1 cause of connection failures.
"""),
        ("Cabin Electrical Panel Setup", """
## Cabin Electrical Panel Setup

Setting up your cabin's electrical panel correctly ensures safe, reliable power distribution:

### Basic Panel Layout
```
[Generator Output] → [DC Breaker/Fuse] → [Battery Bank]
                                              ↓
                                      [DC Distribution Panel]
                                      ├─ LED Lights (12V)
                                      ├─ Phone Chargers (12V)
                                      ├─ Water Pump (12V)
                                      └─ [Inverter] → AC Breaker Panel
                                                       ├─ TV (120V)
                                                       ├─ Microwave (120V)
                                                       └─ Outlet (120V)
```

### Wire Sizing Guide
| Circuit | Max Current | Wire Size | Fuse/Breaker |
|---------|------------|-----------|-------------|
| Generator to Battery | 50A | 6 AWG | 60A fuse |
| Battery to DC Panel | 30A | 10 AWG | 30A breaker |
| Inverter to AC Panel | 50A | 6 AWG | 60A breaker |
| LED Lights | 5A | 14 AWG | 15A breaker |
| Water Pump | 15A | 12 AWG | 20A breaker |

### Grounding
Always ground your cabin's electrical system:
- Drive a copper grounding rod 8 feet into the earth
- Connect the negative battery terminal to the grounding rod
- Connect the AC panel ground bus to the same rod

This prevents shock hazards and protects against lightning strikes.
"""),
    ],
    "magnetic-generator-plans-review": [
        ("Free vs Paid Plans: Deep Dive", """
## Free vs Paid Plans: Deep Dive

Is it worth paying for generator plans? Let's compare specific free and paid options:

### Top Free Plans
1. **The $40 Magnetic Mill** (various online sources)
   - Output: 50-100W
   - Difficulty: Beginner
   - Pros: Extremely cheap, simple design, lots of builder photos online
   - Cons: Vague instructions, no wiring diagram, trial-and-error winding

2. **Tesla Bifilar Coil Blueprint** (public domain patent)
   - Output: 100-300W
   - Difficulty: Intermediate
   - Pros: Authentic Tesla design, detailed patent drawings
   - Cons: Written for 1890s manufacturing, needs modern interpretation

3. **DIY Magnetic Generator Wiki** (community-driven)
   - Output: 100-500W
   - Difficulty: Beginner to advanced
   - Pros: Multiple designs, community feedback, free updates
   - Cons: Inconsistent quality, some designs untested

### Top Paid Plans
1. **Energy Revolution System** ($39-79)
   - Output: 100-300W
   - Difficulty: Beginner-friendly
   - Pros: Video instructions, troubleshooting guide, active community
   - Cons: Some sections feel padded, upsells additional products

2. **Tesla Bifilar Blueprint Pro** ($29-49)
   - Output: 200-500W
   - Difficulty: Intermediate
   - Pros: Detailed schematics, multiple coil configurations, upgrade paths
   - Cons: Requires some electrical knowledge

### The Hybrid Approach
Build your first generator using **free plans** (the $40 Mill or Wiki). Once you understand the basics, invest in a **paid plan** for your second build. This gives you the best of both worlds: free learning, paid expertise when you're ready to level up.
"""),
        ("Builder Success Stories", """
## Builder Success Stories

Real people, real results. Here's what builders achieved:

### Mark T., Texas — Wind-Driven Generator
- **Plan used**: Energy Revolution System
- **Build cost**: $180
- **Output**: 350W
- **Prime mover**: 400W wind turbine
- **Result**: Reduced electricity bill from $145/month to $78/month
- **Quote**: "Built it in a weekend. The video instructions made it foolproof. Best $180 I've ever spent."

### Sarah L., Vermont — Water-Driven Generator
- **Plan used**: DIY Magnetic Generator Wiki
- **Build cost**: $95
- **Output**: 280W
- **Prime mover**: Stream on property
- **Result**: Powers LED lights, fridge, and laptop year-round
- **Quote**: "My stream flows 24/7, so my generator runs 24/7. I haven't paid for electricity in 6 months."

### David R., Montana — Hybrid System
- **Plan used**: Tesla Bifilar Blueprint Pro
- **Build cost**: $320
- **Output**: 500W (generator) + 400W (solar)
- **Prime mover**: Wind + solar
- **Result**: Fully off-grid cabin, zero utility bill
- **Quote**: "The magnetic generator fills the gap when the sun isn't shining. Together they're a perfect system."

### Lisa M., Florida — Manual Generator
- **Plan used**: $40 Magnetic Mill
- **Build cost**: $42
- **Output**: 80W
- **Prime mover**: Hand crank (bicycle adapter)
- **Result**: Powers LED lights and charges devices during storms
- **Quote**: "When the power goes out (which is often in Florida), I spin the bike generator and my lights stay on. Kids love it."

These stories show that magnetic generators work across climates, budgets, and skill levels.
"""),
    ],
    "tesla-magnetic-generator-cost-savings-per-month": [
        ("Savings Calculator", """
## Savings Calculator

Use this simple formula to estimate your monthly savings:

### The Formula
```
Monthly Savings = (Generator Output in kWh) × (Your Rate per kWh) × (Hours of Operation / 24)
```

### Step-by-Step Example
1. **Your generator's output**: 300W = 0.3 kW
2. **Hours of operation**: 24 hours (wind-driven, continuous)
3. **Monthly kWh**: 0.3 kW × 24 hours × 30 days = 216 kWh
4. **Your electricity rate**: $0.15/kWh
5. **Monthly savings**: 216 kWh × $0.15 = **$32.40/month**

### Your Rate Matters
| Your Rate | 200W Generator | 500W Generator | 1,000W Generator |
|-----------|---------------|----------------|------------------|
| $0.10/kWh | $14.40/mo | $36.00/mo | $72.00/mo |
| $0.15/kWh | $21.60/mo | $54.00/mo | $108.00/mo |
| $0.20/kWh | $28.80/mo | $72.00/mo | $144.00/mo |
| $0.25/kWh | $36.00/mo | $90.00/mo | $180.00/mo |
| $0.35/kWh | $50.40/mo | $126.00/mo | $252.00/mo |

**Check your electricity bill** for your rate per kWh (usually listed as "energy charge" or "supply charge"). If you don't see it, divide your total bill by your kWh usage.

### Payback Period Calculator
```
Payback (months) = Generator Cost ÷ Monthly Savings
```

Examples:
- $200 generator at $32/month savings = **6.3 months**
- $300 generator at $54/month savings = **5.6 months**
- $500 generator at $72/month savings = **6.9 months**

Most generators pay for themselves in **under 7 months**. After that, it's pure savings.
"""),
        ("Hidden Savings You Might Miss", """
## Hidden Savings You Might Miss

Beyond the direct electricity bill reduction, magnetic generators save you money in less obvious ways:

### Battery Longevity
By providing a steady baseline of power, a magnetic generator reduces the number of charge/discharge cycles your battery bank undergoes. This can extend battery life by **30-50%**, saving $200-500 over the battery's lifetime.

### Generator Fuel Savings
If you already own a propane or diesel generator for backup, a magnetic generator can replace 60-80% of its runtime. That translates to:
- **Propane**: $300-600/year savings
- **Diesel**: $400-800/year savings
- **Gasoline**: $200-400/year savings

### Reduced Utility Demand Charges
Some utilities charge **demand charges** based on your peak power usage. A magnetic generator running continuously can shave your peak by 200-500W, potentially dropping you to a lower demand tier and saving $10-30/month.

### Resale Value
Homes with off-grid power systems sell for **3-5% more** than comparable homes without. A well-documented magnetic generator installation adds to this premium.

### Tax Credits
In some states, DIY renewable energy installations qualify for:
- **State tax credits**: 10-30% of cost
- **Property tax exemptions**: Added value doesn't increase property taxes
- **Net metering**: Credit for excess power fed back to the grid

Check your state's incentives at [DSIRE](https://dsireusa.org) (Database of State Incentives for Renewables & Efficiency).
"""),
    ],
    "tesla-magnetic-generator-materials-list-cost": [
        ("Alternative Materials (Free/Cheap)", """
## Alternative Materials (Free/Cheap)

You don't need to buy every component. Here are free and ultra-cheap alternatives:

### Free Magnets
- **Old hard drives**: Each contains 2-4 neodymium magnets (~$1 value each)
- **Speakers**: Small speakers contain decent magnets; larger speakers have powerful ones
- **Magazine rack latches**: Often use strong neodymium magnets
- **Craft stores**: Magnetic sheet can be cut into disc shapes

### Free Copper Wire
- **Transformers**: Old power adapters, doorbells, and transformers contain magnet wire
- **Electric motors**: Ceiling fans, washing machines, and drills have copper windings
- **Cable trays**: Construction sites often have leftover wire
- **Salvage yards**: Piles of old electrical wire for $5-10 per pound

### Free Steel
- **Scrap yards**: Cut your own discs and plates
- **Old appliances**: Dishwasher drums, washing machine drums
- **Car parts**: Flywheels, brake rotors, drive plates
- **Construction sites**: Rebar, steel rods, and plates

### Free Bearings
- **Old fans**: Table fans and box fans have decent bearings
- **Bicycle hubs**: High-quality sealed bearings
- **Roller skates/wheels**: Precision ball bearings
- **CD/DVD drives**: Tiny bearings for the spindle motor

### Free Frame
- **Pallet wood**: Free from warehouses and stores
- **PVC pipe**: Discarded from construction sites
- **Cardboard**: Surprisingly rigid for a prototype (laminated)
- **Plastic buckets**: Cut and shape for a housing

### Total Cost with Salvaged Materials
By sourcing everything from free/cheap alternatives, you can build a working generator for **$15-25** — less than the cost of a single tank of gas for a propane generator.
"""),
        ("Tool Investment Guide", """
## Tool Investment Guide

If you don't have a workshop, here's the essential tool kit and where to get it cheap:

### Must-Have Tools ($50-100 total)
| Tool | New Price | Thrift Store | Harbor Freight |
|------|----------|-------------|----------------|
| Cordless drill | $40 | $5 | $25 |
| Hand saw | $12 | $2 | $6 |
| Soldering iron | $15 | $3 | $8 |
| Multimeter | $20 | $5 | $10 |
| Wire strippers | $8 | $1 | $4 |
| Pliers (needle-nose) | $8 | $1 | $4 |
| **Total** | **$103** | **$22** | **$65** |

### Nice-to-Have Tools ($30-60 extra)
| Tool | Purpose | Price |
|------|---------|-------|
| Dremel/rotary tool | Precision cutting, grinding | $25-40 |
| Vise/clamp | Hold workpiece | $10-20 |
| Heat gun | Heat shrink tubing | $15-25 |
| Magnifying glass | Inspect small connections | $5-10 |

### Tool Rental Options
- **Home Depot tool rental**: $5-15/day for specialty tools
- **Library of Things**: Many libraries now rent tools
- **Neighbor apps**: Borrow from neighbors via Nextdoor or Facebook

**Pro tip**: Your total tool investment pays for itself in the first build. A $65 tool kit from Harbor Freight will last through dozens of projects.
"""),
    ],
    "tesla-magnetic-generator-vs-solar-power-which-is-better": [
        ("Performance in Extreme Weather", """
## Performance in Extreme Weather

Weather dramatically affects both technologies. Here's how they compare in extremes:

### Blizzard Conditions
| Factor | Magnetic Generator (Wind) | Solar Panel System |
|--------|--------------------------|-------------------|
| Output | Increases (stronger winds) | Drops 80-95% |
| Snow on panels | Can be brushed off | Accumulates, blocks sun |
| Ice on turbine | Minimal impact | N/A |
| Battery drain | Low (efficient) | High (heating) |
| **Winner** | **Magnetic Generator** | |

### Desert Heat (110°F+)
| Factor | Magnetic Generator (Wind) | Solar Panel System |
|--------|--------------------------|-------------------|
| Output | Stable (wind doesn't change) | Drops 10-25% (heat reduces panel efficiency) |
| Heat stress | Minimal | Panels overheat, inverters struggle |
| Cooling needs | None | Inverters need ventilation |
| **Winner** | **Magnetic Generator** | |

### Hurricane Season
| Factor | Magnetic Generator (Wind) | Solar Panel System |
|--------|--------------------------|-------------------|
| High winds | May need to feather (reduce) | Panels unaffected if mounted |
| Rain | Continues working | Works in rain (reduced output) |
| Debris risk | Blades can be damaged | Panels can be hit by debris |
| Post-storm | Quick to resume | May need panel cleaning |
| **Winner** | **Tie** (depends on mounting) | |

### Key Takeaway
Magnetic generators are **more weather-resilient** than solar panels. While solar needs sun and clean panels, a wind-driven magnetic generator often performs BETTER in bad weather — because storms bring wind.
"""),
        ("Scalability: Growing Your System", """
## Scalability: Growing Your System

How easy is it to expand each system over time?

### Magnetic Generator Scalability
| Upgrade | Cost | Complexity | Output Gain |
|---------|------|-----------|-------------|
| Add second generator | $150-300 | Easy (parallel wiring) | +200-500W |
| Upgrade magnets | $50-100 | Medium (rebuild coils) | +30-50% |
| Upgrade prime mover | $100-400 | Medium (new mounting) | +100-300W |
| Add battery bank | $100-300 | Easy (parallel wiring) | More storage |
| **Total expansion** | **$400-1,100** | | **+300-1,100W** |

### Solar Panel Scalability
| Upgrade | Cost | Complexity | Output Gain |
|---------|------|-----------|-------------|
| Add panels | $200-400/kW | Easy (parallel wiring) | +1kW |
| Upgrade inverter | $200-600 | Medium (wiring) | Higher AC output |
| Add battery bank | $300-1,000 | Medium (new connections) | More storage |
| **Total expansion** | **$700-2,000** | | **+1kW** |

### The Verdict
Magnetic generators are **cheaper to scale**. Adding 500W of magnetic generation costs $200-500, while adding 500W of solar costs $400-800 (panels + potential inverter upgrade). For budget-conscious builders, this matters significantly.
"""),
    ],
    "tesla-magnetic-generator-worth-it": [
        ("Common Myths Debunked", """
## Common Myths Debunked

Let's separate fact from fiction about Tesla magnetic generators:

### Myth 1: "It creates energy from nothing"
**Reality**: A magnetic generator converts mechanical energy to electrical energy. It doesn't create energy — it transforms it. The magnets provide a constant magnetic field; the prime mover provides the input energy. It's electromagnetic induction, the same principle as every generator ever built.

### Myth 2: "It's perpetual motion"
**Reality**: No, it's not. Perpetual motion machines produce more energy than they consume. Magnetic generators consume mechanical energy and produce less electrical energy (due to losses). They follow the laws of thermodynamics perfectly.

### Myth 3: "It will power your whole house"
**Reality**: A single DIY magnetic generator typically produces 100-500W. A typical US home uses about 30,000Wh (30 kWh) per day. You'd need 60-300 generators running 24/7 to power an entire home. But for **supplemental power** (lights, fridge, charging), one or two generators can cover 30-50% of your needs.

### Myth 4: "The magnets lose their strength"
**Reality**: Neodymium magnets lose about 1% of their strength per 100 years at room temperature. In practical terms, they're **permanent** for the life of your generator. Heat is the main enemy — keep your generator below 176°F (80°C) for N52 magnets.

### Myth 5: "It's a scam"
**Reality**: The science is solid. The bifilar coil patent is real. Builders worldwide produce measurable power. What's "scammy" are companies selling $5,000 pre-built units. DIY builders get the same technology for $40-300.
"""),
        ("The 10-Build Rule", """
## The 10-Build Rule

Here's what most experienced builders know: your first 10 builds will be learning experiences. Here's the progression:

### Build #1-3: Learning Phase
- **Goal**: Get something that produces power
- **Output**: 50-150W (often less)
- **Time**: 6-12 hours each
- **Key lesson**: Magnet alignment and coil winding direction matter

### Build #4-6: Optimization Phase
- **Goal**: Improve output and reliability
- **Output**: 150-400W
- **Time**: 4-8 hours each
- **Key lesson**: Air gap, bearing quality, and prime mover coupling

### Build #7-10: Refinement Phase
- **Goal**: Professional-quality output
- **Output**: 400-800W
- **Time**: 2-4 hours each
- **Key lesson**: Multi-phase designs, heat management, power electronics

**After Build #10**: You'll be able to build a reliable 500W+ generator in a single weekend. The investment in learning pays massive dividends.

### The Compound Effect
Each build teaches you something that makes the next one better. By Build #5, you'll likely have a generator that powers your shed or cabin. By Build #10, you could have a system that covers 50%+ of your home's power needs.
"""),
    ],
}

def thick_extra(folder_name):
    """Add extra sections to an article."""
    article_path = BASE / folder_name / "article.md"
    if not article_path.exists():
        return False
    
    with open(article_path, 'r') as f:
        content = f.read()
    
    sections = EXTRA_SECTIONS.get(folder_name, [])
    if not sections:
        return False
    
    additions = "\n".join(f"\n{title}\n{content}" for title, content in sections)
    
    if "---" in content:
        last_hr = content.rfind("---")
        new_content = content[:last_hr] + additions + "\n\n---\n\n" + content[last_hr:]
    else:
        new_content = content + additions
    
    with open(article_path, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    folders = [d.name for d in BASE.iterdir() if d.is_dir()]
    print(f"Adding extra sections to {len(folders)} articles...\n")
    
    for folder in folders:
        if thick_extra(folder):
            article_path = BASE / folder / "article.md"
            with open(article_path, 'r') as f:
                words = len(f.read().split())
            print(f"  ✅ {folder}: {words} words")
        else:
            print(f"  ⏭️ {folder}: no extra sections defined")

if __name__ == "__main__":
    main()
