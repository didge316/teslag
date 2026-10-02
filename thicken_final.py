#!/usr/bin/env python3
"""
Final thickening push for articles under 1,500 words.
"""

from pathlib import Path

BASE = Path("/home/matt/projects/other/tesla-generator/new_content/phases/phase-1-foundation")

FINAL_SECTIONS = {
    "magnetic-generator-for-beginners-step-by-step": [
        ("Troubleshooting Guide", """
## Troubleshooting Guide

Even with careful construction, things can go wrong. Here's how to diagnose and fix common problems:

### Generator Produces No Voltage
**Symptoms**: Multimeter reads 0V when spinning
**Possible causes and fixes**:
1. **Wrong magnet polarity**: All magnets must face the same direction. Use a compass to check — all poles should point the same way.
2. **Broken wire connection**: Check every solder joint. Re-solder any cracked connections.
3. **Short circuit in coils**: Use multimeter on resistance mode. If you read near-zero ohms across a coil, it's shorted. Rewind the coil.
4. **Reversed coil winding**: If you wound two coils, they must be wound in the SAME direction. Reverse one coil if output is zero.

### Low Voltage Output
**Symptoms**: Voltage is lower than expected (e.g., 0.5V instead of 3V)
**Possible causes and fixes**:
1. **Too many turns of wire**: Fewer turns = lower resistance but also lower voltage. Try reducing turns by 10-20%.
2. **Air gap too large**: Reduce the gap between magnets and coils to 1-2mm.
3. **Weak magnets**: Test with a gauss meter. N52 neodymium should read 3,000-4,000 Gauss at the surface.
4. **Slow spin speed**: Voltage is proportional to RPM. Spin faster or use a gear reduction.

### Generator Overheats
**Symptoms**: Coils get hot to the touch after 10-15 minutes
**Possible causes and fixes**:
1. **Too much current draw**: Disconnect the load and see if it still heats. If not, your load is too heavy.
2. **Shorted turns in coil**: Use a multimeter to check coil resistance. If it's much lower than expected, you have shorted turns.
3. **Poor ventilation**: Add ventilation holes to the frame or mount the generator where air can flow.

### Noisy Operation
**Symptoms**: Grinding, clicking, or humming noise
**Possible causes and fixes**:
1. **Worn bearings**: Replace with sealed ball bearings.
2. **Loose magnets**: Apply epoxy to secure magnets to the rotor.
3. **Magnet rubbing on coils**: Adjust the air gap.
4. **Unbalanced rotor**: Add a counterweight or trim the rotor evenly.

### Quick Reference Table
| Problem | Most Likely Cause | Fix |
|---------|------------------|-----|
| No voltage | Wrong magnet polarity | Check all magnet orientations |
| Low voltage | Air gap too large | Reduce gap to 1-2mm |
| Overheating | Heavy load | Reduce load or improve ventilation |
| Noise | Worn bearings | Replace with sealed bearings |
| Flickering output | Loose wire | Re-solder all connections |
"""),
        ("Upgrading Your First Build", """
## Upgrading Your First Build

Once your first generator works, here's how to improve it:

### Upgrade 1: Better Magnets ($20-40)
Replace any ceramic or weak magnets with N52 neodymium. This alone can increase output by 30-50%.

### Upgrade 2: More Coil Turns (+10-20%)
Add 10-20% more wire turns to your coils. This increases voltage but also resistance. Test both before and after.

### Upgrade 3: Better Bearings ($5-15)
Replace any basic bearings with sealed ball bearings. This reduces friction and increases efficiency by 5-10%.

### Upgrade 4: Rectifier Circuit ($2-5)
Add a bridge rectifier (4 diodes in a bridge configuration) to convert AC to DC. This allows you to charge batteries directly.

### Upgrade 5: Voltage Regulator ($5-10)
Add a simple voltage regulator circuit to protect your battery from overcharging. This extends battery life significantly.

### Upgrade 6: Larger Frame (+50-100% output)
Build a larger version with more magnets and larger coils. Use your first build as a template — everything you learned applies.

**Total upgrade cost**: $32-84 for upgrades 1-5. Upgrade 6 is a complete rebuild but uses the same principles.

**Pro tip**: Document every change you make. Note the before and after voltage, current, and RPM. This data helps you understand what works.
"""),
    ],
    "magnetic-generator-for-rv-complete-off-grid-guide": [
        ("RV Power Budget Calculator", """
## RV Power Budget Calculator

Before installing your generator, calculate your RV's total power needs:

### Step 1: List All Devices
Write down every device you want to power, its wattage, and hours of daily use:

| Device | Watts | Hours/Day | Daily kWh |
|--------|-------|-----------|-----------|
| LED lights (4 bulbs) | 20W | 6 hours | 0.12 |
| Phone charger | 10W | 2 hours | 0.02 |
| Laptop | 45W | 4 hours | 0.18 |
| 12V fridge | 60W | 8 hours (cycled) | 0.48 |
| Water pump | 200W | 0.5 hours | 0.10 |
| Fan (12V) | 25W | 8 hours | 0.20 |
| TV (LED, 12V) | 40W | 3 hours | 0.12 |
| **TOTAL** | | | **1.22 kWh** |

### Step 2: Add a 20% Buffer
Real-world usage often exceeds estimates. Add 20%:
- **1.22 kWh × 1.2 = 1.46 kWh/day**

### Step 3: Size Your Generator
For 1.46 kWh/day with a wind-driven magnetic generator:
- **Required average output**: 1.46 kWh ÷ 24 hours = **61W**
- **With 40% efficiency**: 61W ÷ 0.4 = **152W minimum**
- **Recommended size**: **200-300W** (for reliability and future growth)

### Step 4: Size Your Battery Bank
For 2 days of autonomy (calm weather):
- **Daily need**: 1.46 kWh × 2 = 2.92 kWh
- **50% depth of discharge**: 2.92 kWh ÷ 0.5 = **5.84 kWh battery bank**
- **12V system**: 5.84 kWh ÷ 12V = **487 Ah**

### RV-Specific Power Budget Examples
| RV Type | Daily kWh | Generator Size | Battery Bank |
|---------|-----------|---------------|-------------|
| Small camper (2 people) | 1.0-1.5 kWh | 200W | 400Ah |
| Mid-size travel trailer | 1.5-2.5 kWh | 300W | 600Ah |
| Large fifth wheel | 2.5-4.0 kWh | 500W | 800Ah |
| Class A motorhome | 3.0-5.0 kWh | 500W+ | 1000Ah |

**Key insight**: The smaller your RV, the more viable a magnetic generator becomes. A small camper with 1.2 kWh/day needs only a 200W generator — easily achievable.
"""),
        ("RV-Specific Generator Mounts", """
## RV-Specific Generator Mounts

Here are practical mounting options for magnetic generators in RVs:

### Roof-Mounted Wind Turbine
- **Location**: On roof rack or A-frame
- **Generator**: Small wind turbine (300W) connected to existing battery bank
- **Wiring**: Run cable through roof vent or side entry
- **Pros**: Captures wind while driving and parked
- **Cons**: Adds wind resistance while driving; may need to retract

### Under-Bay Mount
- **Location**: Utility bay or storage compartment
- **Generator**: Compact cylindrical design (150-300W)
- **Prime mover**: Electric motor or hand crank
- **Pros**: Protected from elements, easy access for maintenance
- **Cons**: Needs separate prime mover (wind turbine, motor)

### Drawer-Mounted Manual Generator
- **Location**: Slide-out drawer in utility bay
- **Generator**: Flat bifilar pancake coil
- **Prime mover**: Bicycle or hand crank (stored in same drawer)
- **Pros**: Compact storage, zero noise, no moving parts when not in use
- **Cons**: Requires manual effort (15-30 min for full charge)

### Towed Wind Turbine
- **Location**: Towed behind RV on small trailer
- **Generator**: Wind turbine on trailer, wired to RV battery
- **Pros**: Maximum wind capture, doesn't affect RV aerodynamics
- **Cons**: Requires setup/takedown at each campsite

**Best RV solution**: A roof-mounted wind turbine wired to your existing battery bank. It produces power while driving (wind from motion) AND while parked. Zero fuel, zero noise, zero fumes.
"""),
    ],
    "tesla-magnetic-generator-for-cabin": [
        ("Winter Cabin Power Guide", """
## Winter Cabin Power Guide

Winter presents unique challenges for cabin power. Here's how to stay powered:

### Winter Power Challenges
- **Shorter days**: Less solar input (if hybrid)
- **Longer nights**: More lighting and heating needs
- **Icy winds**: Can help or hurt wind-driven generators
- **Frozen water sources**: Water-driven generators need protection

### Winter Power Budget
| Device | Watts | Hours/Day | Daily kWh |
|--------|-------|-----------|-----------|
| LED lights (5 bulbs) | 25W | 8 hours | 0.20 |
| Space heater (fan-only) | 50W | 4 hours | 0.20 |
| Fridge | 75W | 12 hours (cycled) | 0.90 |
| Phone/laptop | 30W | 3 hours | 0.09 |
| Water pump | 200W | 0.5 hours | 0.10 |
| **Total** | | | **1.49 kWh** |

### Winter Generator Strategies
1. **Wind-driven**: Winter storms = more wind = MORE power. This is your best season.
2. **Water-driven**: Keep the turbine below the ice line (usually 2-3 feet deep).
3. **Manual backup**: Keep a hand-crank generator for calm days.
4. **Hybrid approach**: Add solar panels (they work in cold weather, just need sun).

### Cold Weather Battery Care
- **Keep batteries insulated**: Wrap in foam or place in an insulated box
- **Never discharge below 50% in winter**: Cold batteries lose capacity
- **Charge before storing**: A fully charged battery resists freezing better
- **Check water levels** (flooded lead-acid): Add distilled water if needed

### Wood Stove Synergy
A wood stove dramatically reduces electrical heating needs:
- **Space heater savings**: 0.5-1.0 kWh/day saved
- **Water heating**: Boil water on stove for washing
- **Cooking**: Reduces need for electric microwave/oven

**Combined approach**: Wood stove for heat + magnetic generator for electricity = comfortable cabin with minimal electrical load.
"""),
        ("Cabin Generator Installation Checklist", """
## Cabin Generator Installation Checklist

Use this checklist when installing your magnetic generator:

### Pre-Installation
- [ ] Calculate daily power needs (see Power Budget above)
- [ ] Choose generator size (200-500W recommended)
- [ ] Select prime mover (wind, water, or manual)
- [ ] Gather all materials and tools
- [ ] Plan battery bank size and location
- [ ] Plan wiring route from generator to battery

### Installation
- [ ] Mount generator securely with rubber isolation
- [ ] Connect prime mover (wind turbine, water wheel, or motor)
- [ ] Run wiring from generator to charge controller
- [ ] Install charge controller near battery bank
- [ ] Connect generator output to charge controller
- [ ] Connect charge controller to battery bank
- [ ] Install battery disconnect switch
- [ ] Install DC distribution panel
- [ ] Connect loads (lights, fridge, etc.) to distribution panel
- [ ] Install inverter if AC power needed

### Testing
- [ ] Verify generator spins freely
- [ ] Measure no-load voltage (should be 1-5V)
- [ ] Connect to battery and monitor charging
- [ ] Test each load individually
- [ ] Verify all connections are tight
- [ ] Check for heat on wires under load
- [ ] Test battery voltage before and after generator runtime

### Final Steps
- [ ] Label all wires and connections
- [ ] Take photos of wiring for reference
- [ ] Create a maintenance schedule
- [ ] Keep spare parts on hand (bearings, wire, diodes)
- [ ] Write down generator specifications for future reference
"""),
    ],
}

def thick_final(folder_name):
    """Add final sections to an article."""
    article_path = BASE / folder_name / "article.md"
    if not article_path.exists():
        return False
    
    with open(article_path, 'r') as f:
        content = f.read()
    
    sections = FINAL_SECTIONS.get(folder_name, [])
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
    print(f"Final thickening push...\n")
    
    for folder in folders:
        if thick_final(folder):
            article_path = BASE / folder / "article.md"
            with open(article_path, 'r') as f:
                words = len(f.read().split())
            print(f"  ✅ {folder}: {words} words")
        else:
            print(f"  ⏭️ {folder}: no sections defined")

if __name__ == "__main__":
    main()
