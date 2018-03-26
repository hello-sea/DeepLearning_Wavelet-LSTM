
%% 读取数据
buf = load('data.txt');
s = buf';
buf_long = size(s,2);
t=1/buf_long:1/buf_long:1;

figure(1) % 绘制原始图形
plot(t,s)


%% %%%%%%%%%%%%%%%小波时频图绘制%%%%%%%%%%%%%%%%%%
wavename='cmor3-3'; %选用带宽参数和中心频率均为3的复morlet小波
totalscal=128 ;      %尺度序列的长度，即scal的长度
fc=centfrq(wavename);   %小波的中心频率
% fc = 730;
cparam=2*fc*totalscal;  %为得到合适的尺度所求出的参数
a=totalscal:-1:1;       %尺度序列
scal=cparam./a;         %得到各个尺度，以使转换得到频率序列为等差序列

delta = 500000;         %采样频率

coefs=cwt(s,scal,wavename);     %得到小波系数
f=scal2frq(scal,wavename,1/delta);    %将尺度转换为频率

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