
    
#Structure
   
    
    📂 Demo_Eilat
        📂 static/
            📜 styles_dolphin.css webpage design
        📂 templates
            📜 index.html page d'accueil : choix de l'année parmis celles disponibles (2023/2024)
            📜 select_day.html choix du jour parmis ceux disponibles
            📜 select_hour.html choix de l'heure parmis celles disponibles
            📜 select_month.html choix du mois parmis ceux disponibles
            📜 show_files.html choix de l'extrait vidéo parlmis ceux disponibles dans les deux channels pour le recording choisi.
            📜 thank_you.html page de remerciement après la soumission d'un commentaire, avce un lein de redirection vers index.html
            📜 video.html Interface permettant de commenter l'extrait
        📂 Vid_demo_Eilat
            📂 échantillon des résultats des extractions
        📜 app_demo_eilat.py backend du site web 
        📜 requirements.txt configuration pour le backend 
        📜 README.md 

#Indications

##To run the demo

cd Video_against_spectro/Demo_Eilat
pip install -r requirements.txt

##run app local : 
python app_demo_eilat.py
