clear
close all
load('table_2h.mat')
% data = [];
[data] = filereader('3sided_tx_run_2h.ip',data);
% scatter(data(:,2),data(:,3));
save('table_2h.mat','data')