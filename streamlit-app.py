"""
Pseudo-profound Bullshit Generator

This Streamlit app uses OpenAI 3.5 to generate pseudo-profound bullshit based on
the parameters chosen by the user.

Author: Matthew R. DeVerna
"""

import streamlit as st

from openai import OpenAI


def main():
    """
    Main function to run the Streamlit app.
    """
    global client
    st.title("Pseudo-profound Bullshit Generator")

    # Add app description
    st.markdown(
        """
    Welcome to the Pseudo-profound Bullshit Generator!

    This app uses OpenAI's GPT-3.5 model to generate [pseudo-profound bullshit](https://press.princeton.edu/books/hardcover/9780691122946/on-bullshit) based on parameters you choose.

    To get started, enter your OpenAI API key below.
    """
    )

    # OpenAI API key input
    openai_api_key = st.text_input("OpenAI API Key", type="password")

    # Initialize OpenAI client if API key is provided
    if openai_api_key:
        client = OpenAI(api_key=openai_api_key)
        st.success("OpenAI client initialized successfully!")
    else:
        st.warning("Please provide an OpenAI API key to proceed.")
        return

    # Create container for input options
    input_container = st.container()

    with input_container:
        st.subheader("Theme Words")
        st.caption(
            "Enter up to 3 words to steer the topic of pseudo-profound bullshit."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            word1 = st.text_input("Word 1", key="word1")
        with col2:
            word2 = st.text_input("Word 2", key="word2")
        with col3:
            word3 = st.text_input("Word 3", key="word3")

        theme_words = [word for word in [word1, word2, word3] if word.strip()]

        if theme_words:
            st.success(f"Theme words: {', '.join(theme_words)}")

        st.subheader("Parameters")

        col1, col2, col3 = st.columns(3)
        with col1:
            num_words = st.number_input(
                "Number of words per sentence",
                min_value=5,
                max_value=30,
                value=10,
                help="Choose the length of the generated text (between 7 and 30 words).",
            )
        with col2:
            num_sentences = st.number_input(
                "Number of sentences",
                min_value=1,
                max_value=10,
                value=3,
                help="Choose the number of pseudo-profound bullshit sentences to generate (between 1 and 10).",
            )
        with col3:
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Control the randomness of the generated text. Higher values make the output more random.",
            )

        generate_button = st.button("Generate Pseudo-profound Bullshit")

        if generate_button:
            with st.spinner("Generating..."):
                prompt = f"Please generate {num_sentences} pseudo-profound bullshit sentences, each containing {num_words} words. "
                prompt += "The sentences should be syntactically correct but have no intended meaning. "
                prompt += "Use a prose style similar to the following example: 'Hidden meaning transforms unparalleled abstract beauty.' "
                prompt += "Ensure that the sentences sound deep and meaningful but are actually nonsensical. "
                prompt += f"Incorporate the following words where possible: {', '.join(theme_words)}. "

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a generator of pseudo-profound bullshit.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                )

                generated_text = response.choices[0].message.content

            st.subheader("Generated Pseudo-profound Bullshit:")
            st.write(generated_text)


if __name__ == "__main__":
    main()
