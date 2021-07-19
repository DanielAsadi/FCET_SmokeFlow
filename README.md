# <img src= "Media/FCET_Logo.png" height = "60"> Smoke Flow Visualization Setup
This set of code is for the control of the smoke flow visualization experimental setup at the FCET lab wind tunnel in UTIAS. 
Using an Arduino which receives input from the user or active grid encoder, the circuit outputs timed controls to the valve, heated nichrome wire and camera to create and photograph the smoke flow.

## Code Structure
This code was operated using Ardino code which uses C++ and Python. The Arduino code controls the high/low signals and communication to the smoke flow instruments while the Python code controls the user interface and manual or automated control of these signals.

### Python Environment
This project uses the Anaconda virtual Python environment. The Pyserial package is installed to communicate with the arduino using python. See commands below.
```
> conda create --name arduino python=3.7
> conda activate arduino
(arduino) > conda install pyserial
```
## Smoke FLow Circuit Diagram
<img src= "Media/SmokeFlowCircuit.jpg">
