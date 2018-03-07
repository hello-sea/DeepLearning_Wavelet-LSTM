fs=1024;
t=1/fs:1/fs:1;
f1=100;f2=200;f3=300;
s=sin(2*pi*f1*t.*(t>=0&t<0.3))+2*sin(2*pi*f2*t.*(t>=0.3&t<0.8))+3*sin(2*pi*f3*t.*(t>=0.8&t<=1));

figure(1)
plot(t,s)
figure;

%% %%%%%%%%%%%%%%%小波时频图绘制%%%%%%%%%%%%%%%%%%
wavename='cmor3-3'; %选用带宽参数和中心频率均为3的复morlet小波
totalscal=256;      %尺度序列的长度，即scal的长度
fc=centfrq(wavename);   %小波的中心频率
cparam=2*fc*totalscal;  %为得到合适的尺度所求出的参数
a=totalscal:-1:1;
scal=cparam./a;         %得到各个尺度，以使转换得到频率序列为等差序列

coefs=cwt(s,scal,wavename);     %得到小波系数
f=scal2frq(scal,wavename,1/fs);    %将尺度转换为频率

figure(2)
imagesc(t,f,abs(coefs));            %绘制色谱图
colorbar;
xlabel('时间 t/s');
ylabel('频率 f/Hz');
title('小波时频图(二维)');

%%
figure(3)
mesh(t,f,abs(coefs)); 
axis tight; 
colorbar;
xlabel('时间 t/s');
ylabel('频率 f/Hz'); 
title(['小波时频图（三维）','(',num2str(wavename),')']);
%%