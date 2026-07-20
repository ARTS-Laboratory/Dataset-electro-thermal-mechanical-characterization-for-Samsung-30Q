% Load the CSV data
filenameC10 = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S002\Q30_S002_C10.csv'; % Replace with your actual file name
dataC10 = readmatrix(filenameC10);
filename1C = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S002\Q30_S002_1C.csv'; % Replace with your actual file name
data1C = readmatrix(filename1C);
filename2C = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S002\Q30_S002_2C.csv'; % Replace with your actual file name
data2C = readmatrix(filename2C);
filename3C = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S002\Q30_S002_3C.csv'; % Replace with your actual file name
data3C = readmatrix(filename3C);
filename4C = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S002\Q30_S002_4C.csv'; % Replace with your actual file name
data4C = readmatrix(filename4C);

% Extract relevant columns
timeC10 = dataC10(:, 1);        % First column: Time (seconds)
variableC10 = dataC10(:, 6); % Set column # to desired variable
time1C = data1C(:, 1);
variable1C = data1C(:, 6);
time2C = data2C(:, 1);
variable2C = data2C(:, 6);
time3C = data3C(:, 1);
variable3C = data3C(:, 6);
time4C = data4C(:, 1);
variable4C = data4C(:, 6);

% Create the plot
figure()
plot(10*timeC10/3600, (-1)*variableC10, 'k', 'LineStyle', '-', 'LineWidth', 1.5);
hold on
plot(10*time1C*10/3600, (-1)*variable1C, 'b', 'LineStyle', '-', 'LineWidth', 1.5);
%hold on
plot(10*time2C*20/3600, (-1)*variable2C, 'g', 'LineStyle', '-', 'LineWidth', 1.5);
plot(10*time3C*30/3600, (-1)*variable3C, 'r', 'LineStyle', '-', 'LineWidth', 1.5);
plot(10*time4C*40/3600, (-1)*variable4C, 'm', 'LineStyle', '-', 'Marker', 'none', 'LineWidth', 1.5);
ylabel('strain (m/m)');
xlabel('Depth of Discharge (%)');
title('Rate Comparison');

% Enhance the plot
grid off;
% Adjust location based on data type
legend('C/10','1C','2C','3C','4C','location','southwest')