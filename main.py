import streamlit as st
import base64

import pandas as pd
import numpy as np # Needed for log calculations
import math

import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
# This command must be the first Streamlit command in your script.
st.set_page_config(layout="wide")
st.set_page_config(page_title="E.u.r.o.Tec GmbH", page_icon="🔩", layout="wide")



# --- HELPER FUNCTIONS ---

# --- Calculation function for AIRBORNE sound ---
def calculate_airborne_r_total(row):
    R_iw = row['R_iw']
    R_jw = row['R_jw']
    delta_R_ijw = row['delta_R_ijw']
    K_ij = row['K_ij']
    S_s = row['S_s']
    l_0 = row['l_0']
    l_f = row['l_f']

    if l_0 == 0 or l_f == 0 or S_s <= 0: return np.nan
    log_arg = S_s / (l_0 * l_f)
    if log_arg <= 0: return np.nan

    log_term = 10 * np.log10(log_arg)
    R_Total = ((R_iw + R_jw) / 2) + delta_R_ijw + K_ij + log_term
    return R_Total

# --- Calculation function for IMPACT sound ---
def calculate_impact_level(row):
    L_neq0w = row['L_neq0w']
    delta_Lw = row['delta_Lw']
    R_iw = row['R_iw']
    R_jw = row['R_jw']
    delta_R_jw = row['delta_R_jw']
    K_ij = row['K_ij']
    S_i = row['S_i']
    l_0 = row['l_0']
    l_ij = row['l_ij']

    if l_0 == 0 or l_ij == 0 or S_i <= 0: return np.nan
    log_arg = S_i / (l_0 * l_ij)
    if log_arg <= 0: return np.nan

    log_term = 10 * np.log10(log_arg)
    L_nijw = L_neq0w - delta_Lw + ((R_iw - R_jw) / 2) - delta_R_jw - K_ij - log_term
    return L_nijw

# --- Styling function (reusable for any table) ---
def style_table(df, final_col_name):
    def highlight_final_column(s):
        is_final_col = s.name == final_col_name
        return ['background-color: #008080; color: white' if is_final_col else 'background-color: #F5F5DC' for _ in s]
    
    return df.style.apply(highlight_final_column, axis=1).format("{:.8f}", na_rep="Invalid")



# --- App Layout ---
header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()
impact_sound_calc = st.container()

with header:

    LOGO_IMAGE = "eurotec-logo-2.png"
    # --- Add your logo to the header ---
    st.image(LOGO_IMAGE, width=200) # Adjust width as needed

    st.title('Sonotec V2 Sound Proofing')
    #st.text('This is my first text!')

    # col1, col2 = st.columns([3, 1])
    # with col1:
    #     st.title('Sonotec V2 Sound Profing')

    # with col2:
    #     # This is the right column, where we'll put the image
    #     st.image('sonotec_image.jpg', width=300) # Adjust width as needed

with dataset:
    st.header('Introduction')
    st.markdown(
    """
    <p style='font-size:16px; line-height:1.6;'>
    The new <b><span style='color:#d22d2d;'>SonoTec V2</span></b> linear bearing system enables targeted mitigation of flank sound transmission made of thermoplastic Polymer.
    </p>

    <p style='font-size:16px; line-height:1.6;'>
    Available in seven variants with hardness ratings up to 68 Shore A, these bearings are engineered for use even in high-rise applications, delivering a verified weighted sound reduction index (R′<sub>w</sub>) of up to 10 dB.
    </p>

    <p style='font-size:16px; line-height:1.6;'>
    Thanks to their adaptability, the bearings are suitable for integration with cross-laminated timber (<b>CLT</b>), glued laminated timber (<b>GLT/BSH</b>), laminated veneer lumber (<b>LVL</b>), as well as steel and concrete structures.
    </p>
    """,
    unsafe_allow_html=True
    )


col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("sonotec_image.jpg",
             caption="Figure 1: Sound proofing layer applications",
             use_container_width=True)


with features:
    col1, col2 = st.columns([3, 1])
    with col1:
        # This is the left column, where we'll put the text
        st.header('Airborne noise')

    with col2:
        # This is the right column, where we'll put the image
        st.image('airborne_noise.png', width=100) # Adjust width as needed


    #st.header('Airborne noise')
    st.text('Airborne noise is sound that travels through the air before it reaches a partition like a wall or floor. The sound waves hit the surface, causing it to vibrate, and this vibration is then radiated as sound on the other side.')
    # st.markdown("<u><b>Travel Path:</b></u>", unsafe_allow_html=True)
    # st.text('A source (like a person talking or a TV) creates sound waves that travel through the air.')
    # st.text('These airborne waves strike a building element (e.g., a wall).')
    # st.text('The wall vibrates from the energy of the sound waves.')
    # st.text('This vibration creates new sound waves on the other side of the wall, which are then heard in the adjacent room.')

    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>Travel Path:</b></u><br>
    A source (like a person talking or a TV) creates sound waves that travel through the air.<br>
    These airborne waves strike a building element (e.g., a wall).<br>
    The wall vibrates from the energy of the sound waves.<br>
    This vibration creates new sound waves on the other side of the wall, which are then heard in the adjacent room.
    </p>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>Common Examples of Airborne Noise:</b></u><br>
    Voices: People talking, shouting, or singing.<br>
    Music and Television: Sound coming from speakers.<br>
    Traffic: The sound of cars or planes heard from inside a building.<br>
    A dog barking.
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>How to Block It:</b></u><br>
    Airborne noise is best blocked by materials that have high mass and density . Heavy, solid materials like concrete, brick, and multiple layers of drywall are effective because they are harder to vibrate. Sealing air gaps is also critical, as sound will easily travel through any opening.<br>
    </p>
    """,
    unsafe_allow_html=True
    )

    # st.header('Impact noise')

    col1, col2 = st.columns([3, 1])
    with col1:
        # This is the left column, where we'll put the text
        st.header('Impact noise')

    with col2:
        # This is the right column, where we'll put the image
        st.image('impact_sound.png', width=100) # Adjust width as needed


    st.text("Impact noise (also called structure-borne noise) is sound that is generated when two objects collide, transmitting the vibration directly through a building's structure. The sound doesn't start in the air; it starts as a vibration in the material itself.")
    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>Travel Path:</b></u><br>
    An object makes a direct physical impact on a part of the building (e.g., a footstep on the floor).<br>
    This impact sends vibrations directly into the structure (the floorboards, joists, concrete slab).<br>
    These vibrations travel through the connected building materials.<br>
    The vibrating structure (like the ceiling of the room below) then radiates the energy as audible sound into the room.
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>Common Examples of AImpact Noise:</b></u><br>
    Footsteps from someone walking on the floor above.<br>
    Dropping an object on the floor.<br>
    Moving furniture and scraping a chair across the floor.<br>
    Slamming a door , which vibrates the connecting wall.<br>
    Drilling into a wall.
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <p style='font-size:16px; line-height:1.5;'>
    <u><b>How to Block It:</b></u><br>
    Impact noise is best managed by decoupling and absorption. This means separating structural elements to stop vibrations from traveling between them. Methods include:<br>
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown("""
    *   Using soft floor coverings like carpet.
    *   Installing an acoustic underlay beneath hard flooring.
    *   Building a "floating floor" that rests on a resilient layer.
    *   Using resilient channels to hang drywall on a ceiling, creating a gap that absorbs vibrations.
    """)

    # st.subheader('Summary of Key Differences')

    # # We use st.markdown() to create the table.
    # # The syntax uses "|" to separate columns and "---" to separate the header.
    # st.markdown("""
    # | Feature | Airborne Noise | Impact Noise |
    # |---|---|---|
    # | **Origin** | Sound waves traveling through the air. | A direct physical collision with a structure. |
    # | **Primary Path** | Air -> Structure -> Air | Structure -> Air |
    # | **Feels Like** | Hearing a muffled conversation or the bass from music. | Hearing thumps, thuds, and feeling vibrations. |
    # | **Soundproofing Strategy** | Add mass and density (e.g., thick walls). | Decouple structures and add absorption (e.g., floor underlay). |
    # """)

#####INSERT FIGURE#####
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("sound.png",
             caption="Figure 2: Sound transmission pathways between two rooms",
             use_container_width=True)


st.divider()

with model_training:
    st.header('How to compute airborne and impact noise')
    st.subheader('Airborne noise')

    # Use st.markdown for the text paragraphs
    st.markdown("""
    EN ISO 12354-1:2017 - Building acoustics. Estimation of acoustic performance of buildings from the performance of elements - Airborne sound insulation between rooms provides a simplified calculation method for the airborne sound reduction index as follows:
    """)
    
    st.markdown("""
    The weighted sound reduction index for airborne direct transmission is determined from the input value for the separating element according to Formula 19 of EN ISO 12354-1:2017:
    """)
    
    # Use st.latex to render the mathematical formula professionally
    # The 'r' before the string makes it a "raw string", which is good practice for LaTeX
    st.latex(r'''
    \mathrm{R_{Dd,w} = R_{s,w} + \Delta R_{Dd,w} \quad \text{dB}}
    ''')

    # We use a single markdown block for the definitions.
    st.markdown("""
    **Where:**
    - **$\mathrm{R_{s,w}}$**: is the weighted sound reduction index of the separating element, in dB;
      :green[(project specific)]
    - **$\mathrm{\Delta_{RDd,w}}$**: is the total weighted sound reduction index improvement by additional lining on the source and/or receiving side of the separating element, in dB.
      :blue[(from test results)]
    
    The weighted flanking sound reduction indices are determined from the input values according to Formula 20 of EN ISO 12354-1:2017:
    """)

     # Use st.latex for each formula to ensure they are rendered correctly and on separate lines.
    st.latex(r'''
    \mathrm{R_{Ff,w} = \frac{R_{F,w} + R_{f,w}}{2} + \Delta R_{Ff,w} + K_{Ff} + 10 \cdot \log\left(\frac{S_s}{l_0 \cdot l_f}\right) \quad \text{dB}}
    ''')
    st.latex(r'''
    \mathrm{R_{Fd,w} = \frac{R_{F,w} + R_{s,w}}{2} + \Delta R_{Fd,w} + K_{Fd} + 10 \cdot \log\left(\frac{S_s}{l_0 \cdot l_f}\right) \quad \text{dB}}
    ''')
    st.latex(r'''
    \mathrm{R_{Df,w} = \frac{R_{s,w} + R_{f,w}}{2} + \Delta R_{Df,w} + K_{Df} + 10 \cdot \log\left(\frac{S_s}{l_0 \cdot l_f}\right) \quad \text{dB}}
    ''')
    
    # Use st.markdown for the definitions, including LaTeX for variables and color syntax for notes.
    st.markdown("""
    **Where:**
    - **$\mathrm{R_{F,w}}$**: is the weighted sound reduction index of the flanking element F in the source room, in dB;
      :green[(project specific)]
    - **$\mathrm{R_{f,w}}$**: is the weighted sound reduction index of the flanking element f in the receiving room, in dB;
      :green[(project specific)]
    - **$\mathrm{\Delta R_{Ff,w}}$**: is the total weighted sound reduction index improvement by additional lining on the source and/or receiving side of the flanking element, in dB;
      :blue[(from test results)]
    - **$\mathrm{\Delta R_{Fd,w}}$**: is the total weighted sound reduction index improvement by additional lining on the flanking element at the source side and/or separating element at the receiving side, in dB;
        :blue[(from test results)]
    - **$\mathrm{\Delta R_{Df,w}}$**: is the total weighted sound reduction index improvement by additional lining on the separating element at the source side and/or flanking element at the receiving side, in dB;
      :blue[(from test results)]
    - **$\mathrm{K_{Ff}}$**: is the vibration reduction index for the transmission path Ff, in dB;
      :blue[(from test results)]
    - **$\mathrm{K_{Fd}}$**: is the vibration reduction index for the transmission path Fd, in dB;
      :blue[(from test results)]
    - **$\mathrm{K_{Df}}$**: is the vibration reduction index for the transmission path Df, in dB;
      :blue[(from test results)]
    - **$\mathrm{S_s}$**: is the area of the separating element in meters;
      :green[(project specific)]
    - **$\mathrm{l_f}$**: is the common coupling length of the junction between separating element and the flanking elements F and f, in meters;
      :green[(project specific)]
    - **$\mathrm{l_0}$**: is the reference coupling length, $l_0 = 1$ m
      :green[(project specific)].
    """)



# st.subheader('Airborne reduction index calculator')


# ##NEW CODE##


# # Inputs
# R_iw = st.number_input(r"Weighted sound reduction index of flanking element i (source), $\mathrm{R_{i,w}}$ [dB]:",
#                        min_value=0.0, max_value=80.0, value=10.0, step=0.5)

# R_jw = st.number_input(r"Weighted sound reduction index of flanking element j (receiving), $\mathrm{R_{j,w}}$ [dB]:",
#                        min_value=0.0, max_value=80.0, value=10.0, step=0.5)

# delta_R_ijw = st.number_input(r"Total weighted sound reduction index improvement, $\mathrm{\Delta R_{ij,w}}$ [dB]:",
#                               min_value=0.0, max_value=50.0, value=5.0, step=0.5)

# K_ij = st.number_input(r"Vibration reduction index for transmission path, $\mathrm{K_{ij}}$ [dB]:",
#                        min_value=0.0, max_value=50.0, value=10.0, step=0.5)

# S_s = st.number_input(r"Area of the separating element, $\mathrm{S_s}$ [m²]:",
#                       min_value=0.01, max_value=100.0, value=10.0, step=0.1)

# l_0 = st.number_input(r"Reference coupling length, $\mathrm{l_0}$ [m]:",
#                       min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# l_f = st.number_input(r"Common coupling length, $\mathrm{l_f}$ [m]:",
#                       min_value=0.01, max_value=10.0, value=1.0, step=0.1)

# # Calculation button
# if st.button("Calculate $\mathrm{R_{ij,w}}$"):
#     try:
#         R_ij_w = ((R_iw + R_jw) / 2.0) + delta_R_ijw + K_ij + 10.0 * math.log10(S_s / (l_0 * l_f))

#         # show numeric result using LaTeX (no \u escapes)
#         st.markdown(rf"**Calculated weighted sound reduction index:**  $R_{{ij,w}} = {R_ij_w:.2f}\ \mathrm{{dB}}$")

#        # Equation rendered with LaTeX (real math notation)
#         st.markdown("### Calculation details")

#         st.latex(
#             rf"""
#             R_{{ij,w}} = \frac{{{R_iw:.2f} + {R_jw:.2f}}}{{2}} + {delta_R_ijw:.2f} + {K_ij:.2f}
#             + 10 \log_{{10}}\!\left(\frac{{{S_s:.2f}}}{{{l_0:.2f}\times {l_f:.2f}}}\right)
#             """
#         )

#         st.latex(
#             rf"""
#             \Rightarrow R_{{ij,w}} = {R_ij_w:.2f}\ \mathrm{{dB}}
#             """
#         )

#         # Highlight final result
#         st.success(f"Result: $R_{{ij,w}}$ = {R_ij_w:.2f} dB")

#     except Exception as e:
#         st.error(f"Error in calculation: {e}")



# ==============================================================
# 🧮 AIRBORNE SOUND REDUCTION INDEX CALCULATOR
# ==============================================================

with st.expander("🎵 🔊 Airborne Sound Reduction Index Calculator", expanded=False):

    # --- Inputs with descriptions ---
    R_iw = st.number_input(
        r"Weighted sound reduction index of flanking element i (source), $\mathrm{R_{i,w}}$ [dB]:",
        min_value=0.0, max_value=80.0, value=10.0, step=0.5, key="R_iw_air"
    )
    st.caption("Measured for the flanking element on the source room side.")

    R_jw = st.number_input(
        r"Weighted sound reduction index of flanking element j (receiving), $\mathrm{R_{j,w}}$ [dB]:",
        min_value=0.0, max_value=80.0, value=10.0, step=0.5, key="R_jw_air"
    )
    st.caption("Measured for the flanking element on the receiving room side.")

    delta_R_ijw = st.number_input(
        r"Total weighted sound reduction index improvement by additional lining, $\mathrm{\Delta R_{ij,w}}$ [dB]:",
        min_value=0.0, max_value=50.0, value=5.0, step=0.5, key="delta_R_ijw_air"
    )
    st.caption("Improvement due to linings or additional layers on either side of the flanking path.")

    K_ij = st.number_input(
        r"Vibration reduction index for transmission path, $\mathrm{K_{ij}}$ [dB]:",
        min_value=0.0, max_value=50.0, value=10.0, step=0.5, key="K_ij_air"
    )
    st.caption("Represents the vibration isolation efficiency between elements i and j.")

    S_s = st.number_input(
        r"Area of the separating element, $\mathrm{S_s}$ [m²]:",
        min_value=0.01, max_value=100.0, value=10.0, step=0.1, key="S_s_air"
    )
    st.caption("Total area of the separating element (e.g., wall or floor).")

    l_0 = st.number_input(
        r"Reference coupling length, $\mathrm{l_0}$ [m]:",
        min_value=0.1, max_value=10.0, value=1.0, step=0.1, key="l_0_air"
    )
    st.caption("Reference length, generally 1.0 m according to EN 12354.")

    l_f = st.number_input(
        r"Common coupling length between separating and flanking elements, $\mathrm{l_f}$ [m]:",
        min_value=0.01, max_value=10.0, value=1.0, step=0.1, key="l_f_air"
    )
    st.caption("Actual contact length between the separating and flanking elements.")

    # --- Calculation button ---
    if st.button("Calculate $\\mathrm{R_{ij,w}}$", key="btn_air"):
        try:
            R_ij_w = ((R_iw + R_jw) / 2.0) + delta_R_ijw + K_ij + 10.0 * math.log10(S_s / (l_0 * l_f))
            st.session_state["R_ij_result"] = R_ij_w
        except Exception as e:
            st.error(f"Error in calculation: {e}")

    # --- Display results ---
    if "R_ij_result" in st.session_state:
        R_ij_w = st.session_state["R_ij_result"]

        st.markdown(rf"**Calculated weighted sound reduction index:**  $R_{{ij,w}} = {R_ij_w:.2f}\ \mathrm{{dB}}$")
        st.markdown("### Calculation details")
        st.latex(
            rf"""
            R_{{ij,w}} = \frac{{{R_iw:.2f} + {R_jw:.2f}}}{{2}} + {delta_R_ijw:.2f} + {K_ij:.2f}
            + 10 \log_{{10}}\!\left(\frac{{{S_s:.2f}}}{{{l_0:.2f}\times {l_f:.2f}}}\right)
            """
        )
        st.latex(rf"\Rightarrow R_{{ij,w}} = {R_ij_w:.2f}\ \mathrm{{dB}}")
        st.success(f"Result: $R_{{ij,w}}$ = {R_ij_w:.2f} dB")
        st.markdown(rf"***Please note that the calculator performs calculations only for one transmission path. For other transmission paths, the calculations should be repeated with relevant input values..!")


###################################################################  



st.subheader('Impact noise')

    
st.markdown("""
    EN ISO 12354-2:2017 - Building acoustics. Estimation of acoustic performance of buildings from the performance of elements - Impact sound insulation between rooms provides a simplified calculation method for the normalized impact noise level as follows:
    """)

    # Use st.latex for the complex formula
st.latex(r'''
    \mathrm{L_{n,ij,w} = L_{n,eq,0,w} - \Delta L_w + \frac{R_{i,w} - R_{j,w}}{2} - \Delta R_{j,w} - K_{i,j} - 10 \cdot \log\left(\frac{S_i}{l_0 \cdot l_{ij}}\right) \quad \text{dB}}
    ''')

    # Use st.markdown for the definitions
st.markdown("""
    - **$\mathrm{L_{n,ij,w}}$**: is the weighted normalized flanking impact sound pressure level generated on floor (i) and radiated by element (j);
    - **$\mathrm{L_{n,eq,0,w}}$**: is the equivalent weighted normalized impact sound pressure level of the bare floor;
      :green[(project specific)]
    - **$\mathrm{\Delta L_w}$**: is the weighted reduction of impact sound pressure level by a floor covering;
      :green[(project specific)]
    - **$\mathrm{R_{i,w}}$**: is the weighted sound reduction index of the floor (i);
      :green[(project specific)]
    - **$\mathrm{R_{j,w}}$**: is the weighted sound reduction index of the element (j);
      :green[(project specific)]
    - **$\mathrm{K_{ij}}$**: is the vibration reduction index for transmission path ij;
      :blue[(from test results)]
    - **$\mathrm{\Delta R_{j,w}}$**: is the weighted sound reduction index of an additional layer on the receiving side of the flanking element (j);
      :blue[(from test results)]
    - **$\mathrm{S_i}$**: Ceiling area
      :green[(project specific)]
    """)


# --- NEW INTERACTIVE IMPACT SOUND CALCULATOR (FORM STYLE) ---
# st.markdown('***')
# st.subheader('Impact sound pressure level calculator')

# # --- Inputs ---
# # I have used the values from "Case 1" in your table as the default values.
# L_neq0w = st.number_input(
#     r"Equivalent weighted normalized impact sound pressure level of the bare floor, $\mathrm{L_{n,eq,0,w}}$ [dB]:",
#     min_value=0.0, max_value=120.0, value=20.0, step=0.5, key="L_neq0w"
# )
# delta_Lw = st.number_input(
#     r"Weighted reduction of impact sound pressure level by a floor covering, $\mathrm{\Delta L_w}$ [dB]:",
#     min_value=0.0, max_value=50.0, value=10.0, step=0.5, key="delta_Lw"
# )
# R_iw = st.number_input(
#     r"Weighted sound reduction index of the floor (i), $\mathrm{R_{i,w}}$ [dB]:",
#     min_value=0.0, max_value=80.0, value=20.0, step=0.5, key="R_iw_impact"
# )
# R_jw = st.number_input(
#     r"Weighted sound reduction index of the element (j), $\mathrm{R_{j,w}}$ [dB]:",
#     min_value=0.0, max_value=80.0, value=15.0, step=0.5, key="R_jw_impact"
# )
# delta_R_jw = st.number_input(
#     r"Weighted sound reduction index of an additional layer on the receiving side, $\mathrm{\Delta R_{j,w}}$ [dB]:",
#     min_value=0.0, max_value=50.0, value=5.0, step=0.5, key="delta_R_jw"
# )
# K_ij = st.number_input(
#     r"Vibration reduction index for transmission path, $\mathrm{K_{ij}}$ [dB]:",
#     min_value=0.0, max_value=50.0, value=15.0, step=0.5, key="K_ij_impact"
# )
# S_i = st.number_input(
#     r"Ceiling area, $\mathrm{S_i}$ [m²]:",
#     min_value=0.01, max_value=100.0, value=10.0, step=0.1, key="S_i"
# )
# l_0 = st.number_input(
#     r"Reference coupling length, $\mathrm{l_0}$ [m]:",
#     min_value=0.1, max_value=10.0, value=10.0, step=0.1, key="l_0_impact"
# )
# l_ij = st.number_input(
#     r"Common coupling length, $\mathrm{l_{ij}}$ [m]:",
#     min_value=0.01, max_value=10.0, value=10.0, step=0.1, key="l_ij"
# )

# # --- Calculation button ---
# if st.button("Calculate $\mathrm{L_{n,ij,w}}$"):
#     try:
#         # The formula from your image
#         L_nijw = L_neq0w - delta_Lw + ((R_iw - R_jw) / 2.0) - delta_R_jw - K_ij - 10.0 * math.log10(S_i / (l_0 * l_ij))

#         # Show numeric result using LaTeX
#         st.markdown(rf"**Calculated normalized flanking impact sound pressure level:**  $L_{{n,ij,w}} = {L_nijw:.2f}\ \mathrm{{dB}}$")

#         # Equation rendered with substituted values
#         st.markdown("### Calculation details")
#         st.latex(
#             rf"""
#             L_{{n,ij,w}} = {L_neq0w:.2f} - {delta_Lw:.2f} + \frac{{{R_iw:.2f} - {R_jw:.2f}}}{{2}} - {delta_R_jw:.2f} - {K_ij:.2f}
#             - 10 \log_{{10}}\!\left(\frac{{{S_i:.2f}}}{{{l_0:.2f}\times {l_ij:.2f}}}\right)
#             """
#         )
#         st.latex(
#             rf"""
#             \Rightarrow L_{{n,ij,w}} = {L_nijw:.2f}\ \mathrm{{dB}}
#             """
#         )

#         # Highlight final result
#         st.success(f"Result: $L_{{n,ij,w}}$ = {L_nijw:.2f} dB")

#     except ValueError as e:
#         st.error(f"Error in calculation: Invalid input value. Please check that values for the logarithm are positive. Details: {e}")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {e}")


#######REVEISED CALCULATOR FOR IMPACT############

# ==============================================================
# 🎧 IMPACT SOUND PRESSURE LEVEL CALCULATOR
# ==============================================================

with st.expander("🔨 Impact Sound Pressure Level Calculator", expanded=False):

    # --- Inputs with descriptions ---
    L_neq0w = st.number_input(
        r"Equivalent weighted normalized impact sound pressure level of the bare floor, $\mathrm{L_{n,eq,0,w}}$ [dB]:",
        min_value=0.0, max_value=120.0, value=20.0, step=0.5, key="L_neq0w_imp"
    )
    st.caption("Measured value of the bare structural floor before any coverings are added.")

    delta_Lw = st.number_input(
        r"Weighted reduction of impact sound pressure level by a floor covering, $\mathrm{\Delta L_w}$ [dB]:",
        min_value=0.0, max_value=50.0, value=10.0, step=0.5, key="delta_Lw_imp"
    )
    st.caption("Reduction provided by the resilient floor covering or floating floor system.")

    R_iw2 = st.number_input(
        r"Weighted sound reduction index of the floor (i), $\mathrm{R_{i,w}}$ [dB]:",
        min_value=0.0, max_value=80.0, value=20.0, step=0.5, key="R_iw_imp"
    )
    st.caption("Sound reduction index for the flanking element in the source room (floor).")

    R_jw2 = st.number_input(
        r"Weighted sound reduction index of the element (j), $\mathrm{R_{j,w}}$ [dB]:",
        min_value=0.0, max_value=80.0, value=15.0, step=0.5, key="R_jw_imp"
    )
    st.caption("Sound reduction index for the flanking element in the receiving room (ceiling).")

    delta_R_jw = st.number_input(
        r"Weighted sound reduction index improvement by additional layer on receiving side, $\mathrm{\Delta R_{j,w}}$ [dB]:",
        min_value=0.0, max_value=50.0, value=5.0, step=0.5, key="delta_R_jw_imp"
    )
    st.caption("Improvement due to linings or suspended ceiling on the receiving side.")

    K_ij2 = st.number_input(
        r"Vibration reduction index for transmission path, $\mathrm{K_{ij}}$ [dB]:",
        min_value=0.0, max_value=50.0, value=15.0, step=0.5, key="K_ij_imp"
    )
    st.caption("Vibration isolation efficiency between the connected elements i and j.")

    S_i = st.number_input(
        r"Ceiling area, $\mathrm{S_i}$ [m²]:",
        min_value=0.01, max_value=100.0, value=10.0, step=0.1, key="S_i_imp"
    )
    st.caption("Surface area of the flanking ceiling element in the receiving room.")

    l_0_2 = st.number_input(
        r"Reference coupling length, $\mathrm{l_0}$ [m]:",
        min_value=0.1, max_value=10.0, value=10.0, step=0.1, key="l_0_impact"
    )
    st.caption("Reference coupling length, typically 1.0 m according to EN 12354.")

    l_ij = st.number_input(
        r"Common coupling length between the flanking elements, $\mathrm{l_{ij}}$ [m]:",
        min_value=0.01, max_value=10.0, value=10.0, step=0.1, key="l_ij"
    )
    st.caption("Actual length of junction between elements i and j.")

    # --- Calculation button ---
    if st.button("Calculate $\\mathrm{L_{n,ij,w}}$", key="btn_imp"):
        try:
            L_nijw = (
                L_neq0w - delta_Lw
                + ((R_iw2 - R_jw2) / 2.0)
                - delta_R_jw
                - K_ij2
                - 10.0 * math.log10(S_i / (l_0_2 * l_ij))
            )
            st.session_state["L_nij_result"] = L_nijw
        except Exception as e:
            st.error(f"Error in calculation: {e}")

    # --- Display results ---
    if "L_nij_result" in st.session_state:
        L_nijw = st.session_state["L_nij_result"]

        st.markdown(rf"**Calculated normalized flanking impact sound pressure level:**  $L_{{n,ij,w}} = {L_nijw:.2f}\ \mathrm{{dB}}$")
        st.markdown("### Calculation details")
        st.latex(
            rf"""
            L_{{n,ij,w}} = {L_neq0w:.2f} - {delta_Lw:.2f} + \frac{{{R_iw2:.2f} - {R_jw2:.2f}}}{{2}} - {delta_R_jw:.2f} - {K_ij2:.2f}
            - 10 \log_{{10}}\!\left(\frac{{{S_i:.2f}}}{{{l_0_2:.2f}\times {l_ij:.2f}}}\right)
            """
        )
        st.latex(rf"\Rightarrow L_{{n,ij,w}} = {L_nijw:.2f}\ \mathrm{{dB}}")
        st.success(f"Result: $L_{{n,ij,w}}$ = {L_nijw:.2f} dB")

# st.markdown("---")  # horizontal line
# st.markdown(
#     """
#     <div style='text-align: center; font-size: 16px;'>
#         Developed by <b>Dr. Cagatay Demirci</b><br>
#         For any queries, please contact:<br>
#         📧 <a href='mailto:c.demirci@eurotec.team'>c.demirci@eurotec.team</a>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

st.markdown(
    """
    <div style='background-color:#f0f2f6; padding: 15px; border-radius: 10px; text-align: center;'>
        <b>Developed by Global Technical Advisory team at E.u.r.o.Tec</b><br>
        For any queries, please contact: 
        <a href='mailto:gta@eurotec.team'>technik@eurotec.team</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "For more information, please visit [www.eurotec.team](https://www.eurotec.team) 🌐"
)


