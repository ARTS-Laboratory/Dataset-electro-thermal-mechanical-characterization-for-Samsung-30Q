% Load the CSV data
filename = 'C:\Users\Connor\Documents\GitHub\Dataset-battery-Samsung-30Q-electro-thermal-deformation-characterization\data\S001\Q30_S001_1C.csv'; % Replace with your actual file name
data = readmatrix(filename);

% Extract relevant columns
time = data(:, 1);        % First column: Time (seconds)
voltage = data(:, 3);     % Third column: Voltage
temperature = data(:, 5); % Fifth column: Temperature

% Create the plot
figure;
yyaxis left
plot(time/60, voltage, '-b', 'LineWidth', 1.5); % Voltage plot
ylabel('voltage (V)');
xlabel('time (min)');
title('1C Electrothermal Response');

yyaxis right
plot(time/60, temperature, '-r', 'LineWidth', 1.5); % Temperature plot
ylabel('temperature (°C)');

% Enhance the plot
grid off;
legend('voltage', 'Temperature','Location','south');