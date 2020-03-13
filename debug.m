clear
close all
load('table.mat')
[data] = filereader('3sided_tx_run.ip',data);
scatter(data(:,2),data(:,3));
save('table.mat','data')