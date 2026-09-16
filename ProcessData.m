%This file is demonstrating the Data processing for the simulated kick
%height data. As such it will be bread and inefficient with handling data
%such that it can be adapted to suit the real data.
file = readtable('./ExtractedData/tackle.csv');
dataMatrix = file{:, 'EventData'};
dataMetricAverage = mean(dataMatrix);
dataMetricStandardDeviation = std(dataMatrix);

fig = figure('Visible', 'on'); %For .exe purposes
histogram(dataMatrix)
title('Distribution of Tackle')
xlabel('Height (cm)')
ylabel('Frequency (Count)')
grid on
uiwait(fig); %For .exe purposes