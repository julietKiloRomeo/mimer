clear all
[y1, fs1] = audioread('daisy.wav');
[y2, fs2] = audioread('sorry_dave.wav');

% [y1, fs1] = audioread('HOC_s02e01.mp3');
% [y2, fs2] = audioread('HOC_s02e02.mp3');
%%

audiowrite('daisy16.wav',y1,fs1,'BitsPerSample',16);
audiowrite('sorry16.wav',y2,fs2,'BitsPerSample',16);

%%
C1 = constellation(y1, fs1);
%%
C2 = constellation(y2, fs2);

%%
c = containers.Map;

put(C1, c, 'daisy')
put(C2, c, 'sorry_dave')



%%

% clear all

[y, fs] = audioread('sorry_dave.wav');

% load hashtable

T_vec = (0:numel(y)-1)/fs;

matches     = [];


dT  = 2;


for T_0 = linspace(0,T_vec(end)-dT,50);
    idx         = ( T_vec >= T_0 ) & ( T_vec <= T_0+dT );
    soundbite   = y(idx);
    C           = constellation(soundbite, fs);
    
    
    for i=1:numel(C)
        key     = num2str( round(C.f(i)) );
        if isKey(c, key)
            val     = c(key);
            for j=1:numel(val)
                name    = val.name;
                T       = val.T;
                if isfield(matches, name)
                    matches.(name).hash_T(end+1) = T;
                    matches.(name).song_T(end+1) = T_0;
                else
                    matches.(name).hash_T = T;
                    matches.(name).song_T = T_0;
                end
            end
        end
    end
    T_0
end
%%
figure(1), clf
hold all
plot(matches.daisy.hash_T, matches.daisy.song_T, 's')
plot(matches.sorry_dave.hash_T, matches.sorry_dave.song_T, 'o')
axis([0 10 0 10])

