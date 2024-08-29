import streamlit as st


def get_other_information():

    """
    Get the other information section.
    """
    st.markdown("### Other Information")


    with st.expander("Visitor Centers"):
        st.write("🏛️ Find information about the main visitor centers in the Bavarian Forest.")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/index.htm)")

    with st.expander("Popular Entrances to the Park"):
        st.write("🚪 Explore the two most popular entrances to the park.")

        # Entrance 1
        # st.image("https://example.com/falkenstein.jpg", use_column_width=True)
        st.markdown("**Entrance 1: Falkenstein**")
        st.write("This entrance offers access to the Falkenstein mountain and is popular for its hiking trails.")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/npc_falkenstein/index.htm)")

        # Entrance 2
        # st.image("https://example.com/lusen.jpg", use_column_width=True)
        st.markdown("**Entrance 2: Lusen**")
        st.write("The Lusen entrance is the gateway to the Lusen mountain and is known for its challenging trails.")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/npc_lusen/index.htm)")

    with st.expander("Best Way to Get There"):
        st.write("🚌 Learn about the best ways to reach the Bavarian Forest.")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/service/getting_there/index.htm)")


    # with st.expander("Cross-Country Skiing"):
    #     st.write("⛷️ Discover the best cross-country skiing routes in the park in Germany and the Czech Republic.")
    #     st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm)")

