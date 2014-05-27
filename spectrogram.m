function [T f SG] = spectrogram(y, Fs, T_window)

N_y         = numel(y);
N_window    = Fs*T_window;
N_map       = floor(N_y/N_window);
SG          = [];
T           = [];
for i=1:100:N_y-N_window+1
    idx         = (1:N_window) + i - 1;
    y_piece     = y(idx);
    [f norm_Y]  = fourier(y_piece, Fs);
    SG(:,end+1) = norm_Y;
    T(end+1)    = i/Fs;
end

function [f norm_Y] = fourier(y, Fs)

L       = numel(y);                 % Length of signal

NFFT    = 2^nextpow2(L); % Next power of 2 from length of y
Y       = fft(y,NFFT)/L;
f       = Fs/2*linspace(0,1,NFFT/2+1);
norm_Y  = 2*abs(Y(1:NFFT/2+1));
