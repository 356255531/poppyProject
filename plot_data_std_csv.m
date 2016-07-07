load('data.csv');

proc_data = mean(data,2)
stdeviation = std(data,0,2)

 


figure;
hold on

plot(proc_data,'k', 'LineWidth' , 2);
plot(proc_data+stdeviation,'b');
plot(proc_data-stdeviation,'b');


