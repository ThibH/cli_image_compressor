Simon's Image Compressor is a free and opensource software to compress images from many
formats to .jpg format.
- Quality is defaulted to 75 in a scale from 1 (lower quality) to 95 (higher quality),
but you can change it (with the '--quality' option of the 'compress' command, or by letting
yourself be guided.
- Destination folder is defaulted to the Downloads folder. But if it doesn't exist, you will
be asked to specify your destination folder.
- Compressed images will keep the same name, or will be potentially renamed with a
numbered suffix added to the name if a file with the same name and extension already exists
in the destination folder.

Enjoy !

# Corrections

👉 J'ai regroupé et mieux séparé les fonctions dans différents modules pour plus de clarté.
Chaque module a un rôle bien précis (affichage, historique, compression, fonctions générales, base de données, etc).

👉 Utilise toujours des noms le plus explicite possible. Avec juste "welcome", on ne sait pas trop quand
on utilise la fonction dans un autre fichier ce qu'elle fait. Est-ce qu'elle demande des informations, est-ce
qu'elle récupère des données ? Avec un verbe comme display on indique clairement que le but de la fonction est
uniquement d'afficher un message de bienvenue.
    

👉 Tu n'utilises la fonction qu'à un seul endroit, donc pas besoin de faire une fonction pour ça.
Évite aussi de faire des fonctions à l'intérieur de fonction, ça complique souvent le code pour rien.
Préfère des fonctions bien séparées.

👉 Pour l'historique, j'ai ajouté un décorateur pour éviter la répétition qui vérifie si la BD est vide.
Tu aurais pu aussi utiliser une simple fonction que tu appelles au début de chaque fonction si tu n'es pas à l'aise
avec les décorateurs (qui sont un concept assez avancé). Le but ici est surtout de réduire la répétition de code.