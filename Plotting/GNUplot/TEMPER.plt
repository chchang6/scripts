# GNUPlot command file to plot out temperatures after processing of file
# "energies" by CHARMM_temper_ener_extr.
set terminal emf
set output "temper.emf"
set nokey
set xlabel "Time(ps)" font "Arial,16"
set ylabel "Temperature (deg K)" font "Arial,16"
set format xy "%0.1f"
plot 'tempener.gnu' using 1:3 axes x1y1 with linespoints lt 3
