
VideoFilePath = '/home/alexis/Documents/GitHub/Dolphins/extrait_1637_1649.mp4';
videoReader = VideoReader(VideoFilePath);
ImageFilePath = '/home/alexis/Documents/GitHub/Dolphins/DNN_whistle_detection/images_/Exp_01_Feb_2024_1145_channel_0.wav-2250.jpg';
Imagen = imread(ImageFilePath);
figure;
subplot(1, 2, 1);
videoAxis = gca;
subplot(1, 2, 2);
imshow(Imagen, []);
title('Imagen');
while hasFrame(videoReader)
     frame = readFrame(videoReader);
     axes(videoAxis); % Cambia el focus al axis del video
     imshow(frame, []);
     title('Video');
     pause(1/videoReader.FrameRate); % Tiempo real
end