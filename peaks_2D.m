function peaks = peaks_2D(Y, h)

k           = 11;
grid = (-(k-1)/2:(k-1)/2);

peaks       = [];
peaks_a     = [];

[N_i, N_j]  = size(Y);


s = zeros(N_i, N_j);

for i = (k+1)/2 : N_i - (k-1)/2
    for j = (k+1)/2 : N_j - (k-1)/2
        dY      = Y( grid + i , grid + j);
        s(i,j)  = spikyness(dY);
    end
end

mu  = mean(s(:));
rho = std(s(:));

for i = (k+1)/2 : N_i - (k-1)/2
    for j = (k+1)/2 : N_j - (k-1)/2
        is_positive             = s(i,j)>0;
        is_globally_significant = ( s(i,j) - mu ) > h*rho;
        is_peak = is_positive && is_globally_significant;
        if is_peak
            peaks(end+1,:)   = [i,j];
            peaks_a(end+1,:) = s(i,j);
        end
    end
end

N_raw_peaks = size(peaks,1);
to_remove   = [];
for i=1:N_raw_peaks
    is_close    = max(abs(bsxfun(@minus, peaks, peaks(i,:))),[], 2) < (k-1)/2;
    is_bigger   = (peaks_a - peaks_a(i)) > 0;
    if any( is_close & is_bigger )
        to_remove(end+1)=i;
    end
end

peaks(to_remove,:)=[];


function s = spikyness(dY)

N           = size(dY, 1);
val         = dY((N+1)/2, (N+1)/2) ;

s           = val - median(dY(:));