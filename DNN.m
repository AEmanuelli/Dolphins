% Imports
addpath('path/to/your/models'); % Include the path to your model if not in the same directory
images_path = 'images/';
positive_dir = 'predicted_images/positive/';
negative_dir = 'predicted_images/negative/';
csv_path = ['whistles' datestr(now,'yyyymmdd-HHMMSS') '.csv'];

% Load the model
model = importKerasNetwork('model_vgg.h5','OutputLayerType','classification');

% Get list of all files
all_files = dir(images_path);
all_files = all_files(~[all_files.isdir]); % Remove directories
all_files_path = {all_files.name};

% Initialize arrays
record_names = {};
positive_initial = [];
positive_finish = [];
class_1_scores = [];

% Loop through all files
for i = 1:numel(all_files_path)
    file_path = fullfile(images_path, all_files_path{i});
    
    % Prediction
    image = imread(file_path);
    image = imresize(image, [224 224]);
    image = repmat(image, [1 1 3]); % Convert grayscale to RGB
    image = preprocess_input(image);
    prediction = predict(model, image);
    predictions{i,1} = file_path;
    predictions{i,2} = prediction;
    
    % Move file to appropriate directory
    if prediction(2) > prediction(1)
        movefile(file_path, positive_dir);
        class_1_scores(end+1) = prediction(2);
        
        % Prepare data for CSV
        part = strsplit(all_files_path{i}, 'wav-');
        record_names{end+1} = [part{1} 'wav'];
        ini = str2double(strrep(part{2}, '.jpg', ''));
        positive_initial(end+1) = ini;
        positive_finish(end+1) = round(ini + 0.8, 1);
    else
        movefile(file_path, negative_dir);
    end
end

% Save CSV
T = table(record_names', positive_initial', positive_finish', class_1_scores',...
    'VariableNames', {'file_name', 'initial_point', 'finish_point', 'confidence'});
writetable(T, csv_path);

function prediction = predict(model, image)
    prediction = model.predict(image);
end
