function C = constallation(y, fs)

[T, f, SG]  = spectrogram(y, fs, 1);
idx         = f < 4000;
SG(~idx,:)  = [];
f(~idx)     = [];

T_skip = 5;
f_skip = 10;

YY          = SG(1:f_skip:end, 1:T_skip:end);
peaks       = peaks_2D(YY, 2);

C         = [];

if ~isempty(peaks)
    C.T         = T(peaks(:,2)*T_skip);
    C.f         = f(peaks(:,1)*f_skip);
end

