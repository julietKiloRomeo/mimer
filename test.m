
clear all

[y, fs] = audioread('daisy.wav');

[T1, f1, SG1]  = spectrogram(y, fs, 1);

iidx = (1:50000) + 40000;
[T2, f2, SG2]  = spectrogram(y(iidx), fs, 1);
%%
di = 25000;
iidx = (1:50000) + di;
dT = di/fs;
C1 = constellation(y, fs);
C2 = constellation(y(iidx), fs);
%%
figure(1), clf
hold all
for i=1:numel(C1.T)
    plot(C1.T(i), C1.f(i), 'ko')
end
for i=1:numel(C2.T)
    plot(C2.T(i)+dT, C2.f(i), 'bx')
end

%%
figure(1), clf

subplot(211)
imagesc(T1, f1, SG1)
 xlim([0 10])
caxis([0 0.15])

subplot(212)
imagesc(T2+40000/fs, f2, SG2)
 xlim([0 10])
caxis([0 0.15])
