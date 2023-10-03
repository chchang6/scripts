# GNUPlot command file to plot out time series data of RMS fluctuations
# about the mean
set terminal emf
set nokey
set output "initequil.emf"
set xlabel "Time(ps)" font "Arial,16"
set ylabel "RMS fluctuation from mean" font "Arial,16"
set format x "%0.1f"
set format y "%0.3f"
plot [0:20] 'initequil.rmsf' with linespoints lt 3
