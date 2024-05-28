from fastapi import FastAPI, Query
from fastapi import Request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.responses import HTMLResponse


app = FastAPI()
app.title = "Steam_Games"

@app.get('/', tags=['inicio'])
async def inicio():
    cuerpo = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="shortcut icon" href="https://emoji.slack-edge.com/TPRS7H4PN/henry-pm/4658c1bc769b53ae.png">
    <title>Proyecto Individual 1</title>
    <style>
     *{
    margin: 0;
	padding: 0;
	box-sizing: border-box;
}


body{
    font-family: Arial, Helvetica, sans-serif;
    background-color: beige;
    
}

header{
    display: flex;
    justify-content: center;
}

main{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 15px;
    margin: 15px;
}

img{
    object-fit: cover;
    width:50%;
    height:50%;
}

.portada{
    background-color: black;
    color: yellow;
    padding: 15px;
    margin: 15px;
    width: 80%;
    border-radius: 10px;
    box-shadow: 0 0 6px rgba(0, 0, 0, .5);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.txt{
    background-color: yellow;
    width: 60%;
    padding: 15px;
    margin: 15px;
    border-radius: 5px;
    box-shadow: 0 0 6px rgba(0, 0, 0, .5);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
 </style>
</head>
<body>
    <header>
        <div class="portada">
            <img src="https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png" alt="">
        
            <h1>Proyecto Integrador 1 - Henry labs - MLOps</h1>
    
        </div>
    </header>    

    <main>
        <div class="txt">
            <p>En el presente proyecto se presentará el despliegue de una API que efectuará consultas
            sobre una base de datos de Steam. Tambien se montará un sistema de recomendación de juegos
            y de usuarios de steam en base a las preferencias de un usuario.</p>

        </div>

        <div class="txt">
            <p>En el siguiente link podemos ir al docs para hacer las consultas</p>
            <a href="https://pisteam.onrender.com/docs"> Link a las consultas</a>
        </div>
    </main>
</body>
</html> """
    return HTMLResponse(cuerpo)


@app.get("/consulta1", tags=["developer"],
         description='Devuelve cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. Valores que se encuentran: Valve-Capcom-Sacada-kotoshiro')
async def developer(desarrollador: str):
    resp= ['Año:', 'Cantidad de items:', 'Contenido Free (%):']
    l = []
    df = pd.read_parquet('/code/app/data/endpoint1', engine='auto')
    c = df[(df['developer'] == desarrollador.lower().strip())]
    f = c.groupby(['release_date'])['free'].sum().reset_index(name='free')
    c = c.groupby(['release_date'])['developer'].count().reset_index(name="count")
    c['free'] = f['free']
    
    for i in range(len(c)):
        d = [c['release_date'][i], c['count'][i], round(c['free'][i]*100 / c['count'][i])]
        z = dict(zip(resp,d))
        l.append(z)
    
    r = pd.DataFrame(l).to_dict(orient='records')

    return "No se encontraron datos" if len(l) == 0 else r

@app.get("/consulta2", tags=["userdata"],
         description='Devuelve cantidad de dinero gastado, el porcentaje de juegos recomendados sobre juegos jugados y cantidad de items del usuario dado. Valores que se encuentran: blue76gaming-76561197970982479-strobies-sp3ctre')
async def  userdata(User_id: str):
    df = pd.read_parquet('/code/app/data/endpoint2', engine='auto')

    if df[(df['user_id'] == User_id.lower().strip())].empty == True:
        response = "No se encontraron datos"
    
    else:        
        df = df[(df['user_id'] == User_id.lower().strip())]

        if df[df['playtime_forever'] > 0].count().empty == True:
            jugados = 0
        else:
            jugados = df[df['playtime_forever'] > 0].count()[0]

        if df.groupby('user_id').sum('price').empty == True:
            dinero = 0
        else:
            dinero = df.groupby('user_id').sum('price')['price'][0]

    
    
        if df['rec_games'].iloc[0] == 0:
            porcentaje = 0
        else:
            porcentaje = df['rec_games'].iloc[0] * 100 / jugados
    

        response = {'Usuario' : User_id.title(), 'Dinero gastado' : dinero, '% recomendación': porcentaje,
                'Cantidad de items': df['items_count'].iloc[0]}
    
    return response


@app.get("/consulta3", tags=["User_for_genre"],
         description='Devuelve el usuario con más horas jugadas para el género dado y cantidad de horas jugadas por año. Valores que se encuentras en el dataset: RPG-Action-FPS-strategy')
async def UserForGenre(genre: str):
    genero = f"Usuario con más horas jugadas para Género {genre.title()}"
    df = pd.read_parquet('/code/app/data/endpoint3', engine='auto')

    c = df[(df['genres'].str.contains(genre.lower().strip()))]
    c.drop(columns='genres', inplace=True)
    max = c.groupby(['user_id'])['playtime_forever'].sum().sort_values(ascending=False).head(1).index[0]
    c = c[(c['user_id'] == max)].groupby(['release_date']).sum(['playtime_forever']).reset_index(names= 'anio')
    
    l = []
    for i in range(len(c)):
            d = {"Año": c['anio'].tolist()[i], "Horas": c['playtime_forever'].tolist()[i]}
            l.append(d)
    
    response = {genero : max, "Horas jugadas" : l}
    
    return response

@app.get("/consulta4", tags=["best_developer_year"],
         description='Devuelve el top 3 de desarrolladores con mas juegos recomendados en el año ingresado. Valores que se encuentran: 2007-2008-2015-2017')
async def best_developer_year(año : int):
    df = pd.read_parquet('/code/app/data/endpoint45', engine='auto')


    df.drop(columns='sent_neg')
    df = df[(df['release_date'] == año)]
    if df.empty:
        return "No se encontraron datos"
    df = df.groupby(['developer', 'release_date']).sum(['sent_pos', 'recommend_True']).sort_values(by='recommend_True',ascending=False).head(3)

    response = {"Puesto 1": df.index[0][0].title(), "Puesto 2": df.index[1][0].title(), "Puesto 3": df.index[2][0].title()}

    return response
  

@app.get("/consulta5", tags=["developer_reviews_analysis"],
         description='Función que devuelve la cantidad de reseñas positivas y negativas que tiene el desarrollador ingresado. Valores que se encuentran dentro del dataset: Radical Entertainment-Valve-Capcom-saber interactive')
async def developer_reviews_analysis(desarrolladora: str):
    df = pd.read_parquet('/code/app/data/endpoint45', engine='auto')

    df.drop(columns=['recommend_True', 'release_date'])
    df = df[(df['developer'] == desarrolladora.lower().strip())]
    if df.empty:
        return "No se encontraron datos"
    df = df.groupby(['developer']).sum(['sent_pos', 'sent_neg'])
    
    neg = f"Negativo = {df['sent_neg'][0]}"
    pos = f"Positivo = {df['sent_pos'][0]}"

    response = {desarrolladora.title(): [neg, pos]}

    return response



@app.get("/ML_gamerecommend", tags=["recomendación_juego"],
         description="Modelo de ML que recomienda 5 juegos en funcion de las características del juego ingresado. IDs que se encuentran en el dataset: 20 - 40 - 670290	- 658870")
async def recomendacion_juego( idproducto : int):
    df = pd.read_parquet('/code/app/data/recom_juegos',engine='auto')
    juego = df[(df['item_id'] == idproducto)]

    if juego.empty:
        return "No se encontraron datos"
    
    r = f"Juegos recomendados similares a {juego['titles'].iloc[0].capitalize()}"
    df = df[((df['main_genre'] == juego['main_genre'].iloc[0]))].reset_index()
    indice = df.index[df['titles'] == juego['titles'].iloc[0]][0]
    df['score'] = df['sent_pos'] - df['sent_neg']
    vector = TfidfVectorizer()
    cosine = cosine_similarity(vector.fit_transform(df['genres']))
    df['similarity'] = list(cosine[indice])
    recs = df.sort_values(['similarity', 'score'], ascending=False)[1:6]
    recs['titles'] = recs['titles'].apply(lambda x: x.capitalize())

    response = {r : recs['titles'].tolist()}

    return response
    
@app.get('/Ml_recommendForUser', tags=["recomendación_usuario"],
         description='Modelo de ML que recomienda 5 juegos en función del juego más jugado del usuario dado. Usuarios que se pueden encontrar: chocota-frozentreasure-rakurix-gamerz_united')
async def recomendacion_usuario(id_de_usuario : str):
    df = pd.read_parquet('/code/app/data/recom_juegos2')
    pref = df[(df['user_id'] == id_de_usuario.lower().strip())].sort_values(by='playtime_forever', ascending=False)[:1] #localizamos el juego que el usuario jugó mas

    if pref.empty: #Si no encuentra datos, termina la función
        return 'No se encontraron datos'
    
    r = f"Juegos recomendados para el usuario {id_de_usuario.capitalize()}" #Generamos la primera etiqueta de respuesta
    df = df.drop_duplicates(subset='titles', keep='last') #Sacamos del dataframe los valores repetidos
    df = df[((df['main_genre'] == pref['main_genre'].iloc[0]))].reset_index() #Filtramos el dataframe segun el genero principal del juego localizado
    indice = df.index[df['titles'] == pref['titles'].iloc[0]][0] #Obtenemos el indice del juego preferido del usuario
    df['score'] = df['sent_pos'] - df['sent_neg'] # Generamos nueva columna con un puntaje donde a las reviews positivas se le restan las negativas
    vector = TfidfVectorizer() #Instansiamos el vectorizador
    cosine = cosine_similarity(vector.fit_transform(df['genres'])) #Aplicamos el coseno de similitud sobre la vectorización de la columna de referencia sobre las que se van a calcular las similitudes
    df['similarity'] = list(cosine[indice])  #Creamos una columna con el coseno de similitud calculado en funcion del juego con ese indice
    

    recs = df.sort_values(['similarity', 'score'], ascending=False)[1:6] # Ordenamos los valores según similitud y puntaje y extraemos los primeros 5,excluyendo el juego ingresado
    recs['titles'] = recs['titles'].apply(lambda x: x.capitalize()) # Le ponemos la primera letra mayuscula a los titulos extraidos

    response = {r : recs['titles'].tolist()} #Generamos respuesta

    return response