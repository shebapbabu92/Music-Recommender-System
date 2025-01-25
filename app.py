# Import necessary libraries
import streamlit as st
import rdflib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle

# Display the logo
logo_image = "sem.png"  
st.image(logo_image, width=100)  # Adjust the width as needed

# Display the background image
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://png.pngtree.com/background/20210710/original/pngtree-cool-bursting-note-vector-material-picture-image_1048854.jpg");
background-size: cover; 
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Display the title
st.title("Adaptive and Semantic Web Final Project")

# Spotify client id and secret key 
CLIENT_ID = "393423fd95cc45ae95224a1e0a9b5ed2"
CLIENT_SECRET = "088274b8c8de44ac8b62556c237346c3"

# Initialize the Spotify client to view the song image 
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get the album cover URL for a given song and artist
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # Fetch the song poster using the Spotify API
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit UI for Content-Based Music Recommender System
st.header('Content Based Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Dropdown to select a song
music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# Button to trigger the recommendation
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])

    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])

# Empty space in the app layout
app = st.empty()

# Load RDF ontology
g = rdflib.Graph()
g.parse("Music-Ontology.rdf")

# Function to generate SPARQL query based on genre
def generate_query_by_genre(Genre):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ab: <http://www.semanticweb.org/mobin/ontologies/2024/0/music-ontology#>
        SELECT ?title ?genre ?popu
        WHERE {{
            ?song ab:producedBy ?artist;
                  ab:hasGenre ?genre.
            FILTER regex(str(?genre), "{Genre}").
            ?song ab:hasPopularity ?popu;
                  ab:hasTitle ?title.
            ?artist ab:hasName ?artistname.
        }} ORDER BY DESC (?popu) LIMIT 605
        """
    return query

# Function to generate SPARQL query based on artist
def generate_query_by_artist(Artist):
    query = f"""
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ab: <http://www.semanticweb.org/mobin/ontologies/2024/0/music-ontology#>
        SELECT ?title ?genre ?popu
        WHERE {{
            ?song ab:producedBy ?artist.
            FILTER regex(str(?artist), "{Artist}").
            ?song ab:hasGenre ?genre;
                  ab:hasPopularity ?popu;
                  ab:hasTitle ?title.
            ?artist ab:hasName ?artistname.
        }} ORDER BY DESC (?popu) LIMIT 605
        """
    return query

# Function to display recommendations
def display_recommendations(title, recommendations):
    st.markdown(f"## {title} Recommendations")
    if recommendations:
        for i, recommendation in enumerate(recommendations):
            st.write(f"{i + 1}. {recommendation}")
    else:
        st.warning("No recommendations found.")

# Main function for the Music Ontology Recommendation System
def main():
    st.header("Music Ontology based Recommendation")

    # Dropdowns for selecting genre and artist
    Genre = st.selectbox("Pick a Genre", ["acousticPop", "alaskaIndie", "alternativeR&B", "artPop", "altHipHop", "australianDance", "australianHipHop", "australianPop", "barbadianPop", "baroquePop", "belgianEdm", "bigRoom", "boyBand", "britishSoul", "brostep", "canadianContemporaryR&B", "canadianLatin", "canadianPop", "canadianHipHop", "candyPop", "celticRock", "chicagoRap", "colombianPop", "complextro", "contemporaryCountry", "dancePop", "danishPop", "detroitPop", "downtempo", "edm", "electro", "electroHouse", "electronicTrap", "electroPop", "escapeRoom", "folkPop", "frenchIndiePop", "hipHop", "hipPop", "hollywood", "house", "indiePop", "irishSingerSongwriter", "latin", "metropopolis", "moroccanPop", "neoMellow", "permanentWave", "pop", "tropicalHouse"])
    Artist = st.selectbox("Who is your favourite Artist", ["Eminem", "Sia", "LadyGaga", "BrunoMars", "JustinBieber", "Coldplay", "Rihanna", "Maroon5", "DuaLipa", "Marshmello", "AlanWalker", "SelenaGomez", "SelenaGomez&TheScene", "Shakira", "Beyonce"])

    # Button to get recommendations
    if st.button("Get Recommendations"):
        genre_recommendations = []
        artist_recommendations = []

        # Generate SPARQL query and fetch genre recommendations
        if Genre:
            query_genre = generate_query_by_genre(Genre)
            genre_recommendations = [r['title'] for r in g.query(query_genre)]

        # Generate SPARQL query and fetch artist recommendations
        if Artist:
            query_artist = generate_query_by_artist(Artist)
            artist_recommendations = [r['title'] for r in g.query(query_artist)]

        # Display recommendations
        display_recommendations("Genre", genre_recommendations)
        display_recommendations("Artist", artist_recommendations)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
