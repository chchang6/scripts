# GNUPlot command file to plot out time series data of total energy
# after processing of "energies" file by CHARMM_temper_ener_extr
set terminal emf
set output "energy.emf"
set nokey
set xlabel "Time(ps)" font "Arial,16"
set ylabel "Energy (kcal/mol)" font "Arial,16"
set format x "%0.1f"
set format y "%0.3f"
plot 'tempener.gnu' using 1:2 axes x1y1 with linespoints lt 3
