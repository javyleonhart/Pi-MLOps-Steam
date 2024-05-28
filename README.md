# Proyecto integrador 1 - MLOps

![](https://miro.medium.com/v2/resize:fit:847/1*9rS774Dl7GVfToyJlaKsOg.png)

En el siguiente proyecto se buscará emular el ciclo de vida de una proyecto de Machine Learning. Se desarrollarán las etapas correspondientes, primero un ETL sobre los datasets proporcionados y luego del tratamiento de los datos se hará un EDA. Al terminar esto se desarrollaran 5 consultas sobre el dataset y por último un sistema de recomendación.
Al terminar ese procedimiento, se disponibilizarán los datos por FastAPI y se cargará la app en Render.
Las consultas que se harán sobre el dataset serán las siguientes:

* def developer( desarrollador: str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

* def userdata( User_id: str ): Debe devolver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

* def UserForGenre( genero: str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

* def best_developer_year( año: int ): Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado (reviews.recommend = True y comentarios positivos).

* def developer_reviews_analysis( desarrolladora: str ): Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Una vez desarrollados los endpoints mencionados, se entrenará un modelo de ML para montar un sistema de recomendación. Para el desarrollo del modelo se aplicó la similitud del coseno:

* Sistema de recomendación ítem-ítem: Toma un ítem y, en base a su similitud con otros ítems, recomienda ítems similares. Aquí el input es el id de un juego y el output es una lista de juegos recomendados.

* Sistema de recomendación usuario-ítem: Toma un usuario y le recomienda 5 juegos en función de las características del juego más jugado.

## Datasets

Los datasets utilizados son muy grandes para cargarlos en este proyecto, por lo que se adjuntara un notebook con el ETL aplicado sobre los mismos y se presentarán una versión reducida utilizada para el EDA. Al final del ETL se hace un tratamiento particular para generar un dataset específico para cada endpoint ya que los recursos de la versión gratuita de Render son muy limitados. Los datasets del EDA contienen:

#### steam_games

* publisher: Editor del juego
* title: Nombre del juego
* release_date: Año en que se lanzó el juego
* price: Precio del juego
* item_id: ID del juego
* developer: Desarrollador del juego
* genres: Generos/etiquetas del juego

#### user_items

* item_id: ID del juego
* item_name: Nombre del juego
* playtime_forever: Cantidad de hora que el usuario jugó al juego
* user_id: Nombre/ID del usuario

#### game_reviews

* item_id: ID del juego
* recommend_True: Cantidad de recomendaciones que tiene el juego
* sent_neg: Cantidad de reviews negativas
* sent_neu: Cantidad de reviews neutrales
* sent_pos: Cantidad de reviews positivas

## Elementos del repositorio

Descripción general de los elementos:

* 1-ETL.ipynb: Notebook donde se desarrolla todo el ETL de los Datasets
* 2-EDA.ipynb: Notebook donde se desarrolla el EDA de los Datasets tratados
* 3-Funciones: Notebook con los endpoints y sistema de recomendación desarrollados en la app
* game_reviews - steam_games: Datasets utilizados en el EDA (Falta user_items debido al peso del archivo)
* Carpeta Aplicación: app dockerizada que se montó en render con FastAPI

# Tecnología utilizada
* Python
* FastAPI
* Pandas
* Scikit-learn
* NLTK
* Render 

# Enlaces

* (https://pisteam.onrender.com/ "API en Render")
* (https://hub.docker.com/r/javyleonhart/pisteam "Imagen de Docker")
* (https://youtu.be/gfhXLorEyN0?si=IJF5wzRhHMT2IdbX "Video de presentación")
