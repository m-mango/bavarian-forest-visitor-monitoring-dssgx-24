# import libraries
import streamlit as st


def get_other_information():

    """
    Get the other information section.
    """
    st.markdown("### Other Information")


    with st.expander(":green[Visitor Centers]"):
        st.markdown(":green[🏛️ Find information about the main visitor centers in the Bavarian Forest.]")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/index.htm)")

    with st.expander(":green[Popular Entrances to the Park]"):
        st.markdown(":green[🚪 Explore the two most popular entrances to the park.]")
        st.markdown(":green[**Entrance 1: Falkenstein**]")
        st.markdown(":green[This entrance offers access to the Falkenstein mountain and is popular for its hiking trails.]")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/npc_falkenstein/index.htm)")

        st.markdown(":green[**Entrance 2: Lusen**]")
        st.write(":green[The Lusen entrance is the gateway to the Lusen mountain and is known for its challenging trails.]")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/npc_lusen/index.htm)")

    with st.expander(":green[Best Way to Get There]"):
        st.markdown(":green[🚌 Learn about the best ways to reach the Bavarian Forest.]")
        st.markdown("[Learn More](https://www.nationalpark-bayerischer-wald.bayern.de/english/service/getting_there/index.htm)")


    

