function generate_and_save_spectrograms(recording_folder_path, saving_folder)
    % Set initial parameters
    starting_record_index = 1;

    Files = dir(recording_folder_path);
    mask = ismember({Files.name}, {'.', '..'});
    Files(mask) = [];   %get rid of . and .. directories
    num_subfolder = sum([Files.isdir]);

    FileNames = {Files.name};

    % calculate the spectrogram
    wlen = 2048;                         % window length
    hop = round(0.8*wlen);               % window hop size
    nfft = 2048;                         % number of fft points
    win = blackman(wlen);                % window generation

    sliding_w = 0.4;
    cut_low_frequency = 30;              % cut below 3k
    cut_high_frequency = 47;             % cut above 20k

    for i = starting_record_index:length(FileNames)
        % load sound recording
        [x,fs] = audioread(fullfile(recording_folder_path, FileNames{i})); % x is data, fs is sampling rate
        x = single(x);           % convert to single precision to save memory
        N = length(x);           % signal length

        low = 1;
        up = low + (0.8*fs) - 1;
        file_name_ex = 0; % the start in second
        while up <= N
            x_w = x(low:up);

            [~, fg, tg, PSg] = spectrogram(x_w, win, wlen-hop, nfft, fs); % calculate the spectrogram
            fg = fg/1000;                                              % convert frequency to kHz
            PfSg = 20*log10(abs(PSg));                                 % convert to dB

            f = figure('visible', 'off');
            imagesc(tg, fg, PfSg);
            axis xy
            ylim([cut_low_frequency cut_high_frequency])
            set(gca,'XTick',[], 'YTick', [])
            colormap(gray)
            set(gca,'LooseInset',get(gca,'TightInset'),'Visible', 'off') % for removing white frames
            
            s = fullfile(saving_folder, [FileNames{i} '-' num2str(file_name_ex) '.jpg']);
            saveas(f, s);
            close;

            low = low + (sliding_w*fs);
            file_name_ex = file_name_ex + sliding_w;
            up = low + (0.8*fs) - 1;
            
        end
    end
end


