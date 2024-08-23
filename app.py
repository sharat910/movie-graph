import os
import streamlit as st
from openai import OpenAI
from schema import PlotResponse
from graph import generate_graph
from metrics import count_tokens
import streamlit.components.v1 as components

# Streamlit app
st.set_page_config(page_title="Movie Graph", layout="wide")

st.title("Movie Graph")
st.write("Generate a character relationship graph from a movie plot using OpenAI's structured outputs.")
st.markdown("Try the demo with plot text in [The Shawshank Redemption Wiki](https://en.wikipedia.org/wiki/The_Shawshank_Redemption)")

# Sidebar for API key and model selection
with st.sidebar:
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    model_name = st.selectbox("Select OpenAI model", ["gpt-4o-mini", "gpt-4o-2024-08-06"], index=0)

# Main interface
plot_text = st.text_area("Enter the movie plot text:", height=300)

if plot_text:
    st.write("Token Count:", count_tokens(plot_text))

if st.button("Generate Graph"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not plot_text:
        st.error("Please enter the movie plot text.")
    else:
        with st.spinner("Generating graph..."):
            if not st.session_state.get("client"):
                st.session_state.client = OpenAI(api_key=api_key)
            
            if st.session_state.get("plot_text") != plot_text:
                # Get structured response from OpenAI
                st.session_state['completion'] = st.session_state.client.beta.chat.completions.parse(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that understands movie plots and scans for \
                        characters, understands their roles and relations between characters and locations mentioned in movie plot. \
                        You also generate a 1 paragraph intro to the movie plot in an engaging way just like imdb."},
                        {"role": "user", "content": plot_text},
                    ],
                    response_format=PlotResponse,
                )
                st.session_state['plot_text'] = plot_text

            # Parse response
            completion  = st.session_state['completion']
            st.write(completion.usage)
            message = completion.choices[0].message
            if not message.parsed:
                st.error("Failed to parse response. Please try again.")
                st.stop()
            
            plot_data = message.parsed

            # Display summary
            st.subheader("Plot Summary")
            st.write(plot_data.summary)

            # Display characters
            st.subheader("Characters")
            for character in plot_data.characters:
                st.write(f"**{character.name}**: {character.role}")

            st.write("---")

            st.subheader("Movie Character Graph")

            # Generate graph
            filename = "movie_graph.html"
            generate_graph(plot_data, filename)
            
            # Display the graph
            with open(filename, "r", encoding="utf-8") as f:
                html = f.read()
            components.html(html, height=600)

            # Delete the file
            os.remove(filename)