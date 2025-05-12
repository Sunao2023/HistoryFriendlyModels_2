# Chapter 5: Pharmaceutical Industry Model

This module implements the history-friendly model of the pharmaceutical industry as described in Chapter 5 of "Innovation and the Evolution of Industries: History-Friendly Models".

## Model Overview

The pharmaceutical industry model focuses on the dynamics of innovation, imitation, and competition in a context where patent protection plays a critical role. The model simulates:

1. **R&D processes**: Search for new therapeutic molecules and development of drugs
2. **Patent regime**: Protection of discovered molecules for a limited time period
3. **Demand dynamics**: Segmented markets with different requirements for drug quality
4. **Competitive dynamics**: Emergence of market structure with innovative and imitative firms

## Key Classes

- **C5Model**: Main model class that coordinates the simulation
- **Firm**: Represents pharmaceutical companies, can be innovators or imitators
- **TherapeuticCategory**: Represents therapeutic areas with different patient populations
- **Molecule**: Basic units of innovation that can be discovered and patented
- **Product**: Drugs developed from molecules and sold in the market
- **Files**: Handles file operations for saving simulation results
- **Statistic**: Collects and analyzes simulation data

## How to Run

You can run the model using the provided `run_chapter5.py` script:

```bash
# Run single simulation with default parameters
python -m src_py.Chapter5.run_chapter5 --mode single

# Run multiple simulations
python -m src_py.Chapter5.run_chapter5 --mode multiple --iterations 50

# Customize parameters
python -m src_py.Chapter5.run_chapter5 --mode single --time 150 --firms 60 --tcs 100 --patent 40
```

## Parameters

The model includes several key parameters that can be modified:

- **Patent duration**: Length of patent protection (default: 20 periods)
- **Number of therapeutic categories**: Fragmentation of market (default: 200)
- **Number of firms**: Size of potential firm population (default: 50)
- **Simulation time**: Length of simulation (default: 100 periods)
- **Search success rate**: Probability of finding promising molecules (default: 3%)

## Exercises

The model is designed to explore several key questions:

1. **Imitation and patent protection**: How do different patent regimes affect industry structure?
2. **Innovative opportunities**: How does the richness of technological opportunities affect industry evolution?
3. **Cumulativeness of innovation**: What happens when previous innovations enhance the capability for new discoveries?
4. **Market fragmentation**: How does the number of therapeutic areas affect industry concentration?

## Output

Simulation results are saved in the `results_py/Chapter5/` directory and include:

- Time series data on market concentration
- Firm survival and product statistics
- Innovation and imitation dynamics
- Price and quality evolution 