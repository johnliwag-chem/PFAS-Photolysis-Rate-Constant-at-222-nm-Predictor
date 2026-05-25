import streamlit as st
import numpy as np
import pandas as pd

def calculate_k(e_222nm, MaxAbsPartialCharge, pH, nitrate_conc):
    rate_constant = ((0.000734573169*e_222nm) + (0.00117804995*MaxAbsPartialCharge) - (0.0000284929074*pH) - (0.000705501740*nitrate_conc) + 0.002325329288)
    return rate_constant

if "predicted_k" not in st.session_state:
    st.session_state.predicted_k = None

st.set_page_config(page_title="Liwag-Dimzon Model", layout="wide")

st.title("LIWAG-DIMZON MODEL\nPredict the Photolysis Rate Constant of PFC at 222 nm", text_alignment = "center")
st.bottom.caption("Made by John Joseph Liwag, BS Chemistry, Ateneo de Manila University (Email: john.liwag@student.ateneo.edu | LinkedIn: www.linkedin.com/in/john-joseph-liwag)")

tab_calculate, tab_about, tab_references = st.tabs(["Predict", "About", "Acknowledgements"])

with tab_calculate:
    st.header("Calculate Photolysis Rate Constant", text_alignment="center")
    st.write("**Enter the values for the following parameters:**")
    st.caption("A warning will pop up if one of your inputs fall outside the range of training values for the model. You can still run the prediction but it will have significantly higher uncertainty.")

    LIMIT_e222nm_lower, LIMIT_e222nm_upper = 13.99, 105.67
    LIMIT_MAPC_lower, LIMIT_MAPC_upper = 0.4596, 0.4768
    LIMIT_pH_lower, LIMIT_pH_upper = 5, 10.5
    LIMIT_NO3conc_lower, LIMIT_NO3conc_upper = 0, 15
    out_of_bounds = False

    col_input, col_output = st.columns(2)

    with col_input:
        with st.container(border=True):
            st.text("MOLECULAR DESCRIPTORS", text_alignment="center")
            st.caption("Innate property of the PFC; Can be calculated using software")

            user_e_222nm = st.number_input("Molar absorption coefficient at 222 nm of the PFC", value=100.0)
            if not (LIMIT_e222nm_lower <= user_e_222nm <= LIMIT_e222nm_upper):
                st.warning("⚠️ Provided value is outside the model's training range.")
                out_of_bounds = True
            user_MaxAbsPartialCharge = st.number_input("Maximum absolute partial charge of the PFC", value=0.46)
            if not (LIMIT_MAPC_lower <= user_MaxAbsPartialCharge <= LIMIT_MAPC_upper):
                st.warning("⚠️ Provided value is outside the model's training range.")
                out_of_bounds = True

    with col_output:
        with st.container(border=True):
            st.text("EXPERIMENTAL CONDITIONS", text_alignment="center")
            st.caption("Conditions at which the PFC is exposed to 222 nm far-UVC light")

            user_pH = st.number_input("pH of the matrix", value = 8.5)
            if not (LIMIT_pH_lower <= user_pH <= LIMIT_pH_upper):
                st.warning("⚠️ Provided value is outside the model's training range.")
                out_of_bounds = True
            user_nitrate_conc = st.number_input("Nitrate concentration in matrix (ppm)", value=0.0)
            if not (LIMIT_NO3conc_lower <= user_nitrate_conc <= LIMIT_NO3conc_upper):
                st.warning("⚠️ Provided value is outside the model's training range.")
                out_of_bounds = True

    st.button("Calculate k at 222 nm", key="calculate", icon_position="left")

    with st.container(height="stretch", border=True):
        st.write("CALCULATED RATE CONSTANT")

        if st.session_state["calculate"]:
            st.session_state.predicted_k = calculate_k(user_e_222nm, user_MaxAbsPartialCharge, user_pH,
                                                       user_nitrate_conc)
        st.success(f"Predicted rate constant, k (/min): {st.session_state.predicted_k}")

        if out_of_bounds:
            st.warning("⚠️ The predicted k by the model will have high uncertainty as one of the descriptors used for the calculation are outside the applicability domain of the model.")

    with st.container(height="stretch", border=True):
        st.write("PREDICTED PFC CONCENTRATION DECAY OVER TIME")
        st.caption("This panel will update after a predicted rate constant is obtained.")
        if st.session_state.predicted_k is not None:
            col1, col2 = st.columns(2)
            with col1:
                initial_conc = st.number_input("Initial Concentration (μM)", value=10.0)
            with col2:
                max_time = st.slider("Simulation Duration (minutes)", min_value=1, max_value=600, value=60)

            # Step A: Create an array of 100 time points from 0 up to the max_time
            time_points = np.linspace(0, max_time, 100)

            # Step B: Calculate the concentration at every single time point
            # np.exp() is the numpy function for e^x
            concentrations = initial_conc * np.exp(-st.session_state.predicted_k * time_points)

            # Step C: Put the two arrays into a Pandas DataFrame
            chart_data = pd.DataFrame({
                "Time (mins)": time_points,
                "Concentration (μM)": concentrations
            })

            # Step D: Tell Pandas to use Time as the X-axis
            chart_data = chart_data.set_index("Time (mins)")

            # Step E: Let Streamlit draw the chart automatically!
            st.line_chart(chart_data, x_label="Time (mins)", y_label="Concentration (μM)")
with tab_about:
    st.header("About the Project", text_alignment = "center")
    st.write("The Liwag-Dimzon Model is the final model output ofr my bachelor's thesis study titled '*Understanding the Photodegradation "
             "Susceptibility of Perfluoro Compounds (PFCs) via QSAR/QSPR Modelling*'.")
    st.write("The goal of this study was to **gain insights into the "
             "photodegradation susceptibility of perfluoro compounds by leveraging QSAR/QSPR modelling and the limited data available on the "
             "direct photolysis of PFAS under exposure to 222 nm far-UVC light**.")

    st.subheader("What are perfluoro compounds?", text_alignment = "left")
    st.write("Perfluoro compounds (PFCs) are a subclass of the per- and polyfluoroalkyl substances (PFAS). PFCs are fully fluorinated, synthetic hydrocarbons which are used for various industrial applications, including water-resistant coatings, surfactants, and fire-fighting foams (Viberg & Eriksson, 2011). PFCs can be further classified depending on the functional group present within their structure. Some of the most common PFCs seen in the environment are perfluorinated sulfonates and perfluorinated carboxylates (Viberg & Eriksson, 2017). Due to their numerous carbon-fluorine bonds, which is one of the strongest bonds in organic chemistry, PFCs are generally resistant to any form of degradation (Sosnowska et al., 2023). This makes them stable during use and after release into the environment. Consequently, they can persist in the environment for long periods of time and can cause adverse effects to human health, wildlife, and environmental health (Viberg & Eriksson, 2017). PFCs can mix with water sources. When ingested, they can affect the different organ systems, increase risk of cancer, and hinder fetal development for humans (Sosnowska et al., 2023).")

    st.subheader("How the model addresses the PFAS problem")
    st.write("Recently, Xin et al. (2023) showed that the direct photolysis of representative PFAS under 222 nm far-UVC light shows great potential in the remediation of PFAS in water. However, they were only able to test the treatment on a select set of PFAS. Furthermore, there are barely any other data available regarding the performance of the method for photodegrading PFAS outside their study.")
    st.write("By using the limited data available on the direct photolysis of some representative PFAS from a previous study (Xin et al., 2023), the photolysis rate constants of PFCs can be approximated using QSAR modelling. Through this method, time and resources can be saved as it is impractical to test every single PFC there is.")

    st.subheader("About the model")
    st.write("The Liwag-Dimzon model follows a multiple linear regression trained on the data from the study of Xin et al. (2023). Both the molecular descriptors and experimental conditions during treatment were incorporated into the model to properly estimate the photolysis rate constant. For the molecular descriptors, the molar absorption coefficient at 222 nm and the maximum absolute partial charge of the PFC show the highest influence on the rate constant. Meanwhile, the pH and the concentration of nitrate ions in the solution matrix also significantly influence the photolysis rate. Together, these parameters can be defined to produce a rough estimated value for the photolysis rate constant at 222 nm of a PFC and, therefore, gain insights into how easy it is to degrade the PFC using this method.")

    st.subheader("Mechanistic interpretation of the model")
    st.image("Mechanistic Interpretation.png")
    st.caption("A visual representation of the proposed mechanism for the photolysis of perfluoro compounds based on their ε222nm and MaxAbsPartialCharge at 222 nm far-UVC light. ε222nm  dictates photon absorption capability of the PFCs while the MaxAbsPartialCharge determines whether the PFC is going to snap after absorbing the 222 nm photon.")
    st.write("Combining the molar absorption coefficient, environmental conditions, and MaxAbsPartialCharge to rationalize the photolysis of PFCs, the following mechanism is hereby proposed:")
    st.write("Firstly, the carboxylate group likely has a HOMO-LUMO gap that matches the energy carried by 222 nm photons. In this regard, PFCs with carboxylate groups and a higher ε222 nm will be more likely to degrade as they will likely absorb the photons. In contrast, those without carboxylate groups or have a low ε222nm are unlikely to undergo photolysis. Once a photon is absorbed, the value of the MaxAbsPartialCharge dictates whether or not the carboxylate group is going to snap and break to initiate the photodegradation; PFCs with higher MaxAbsPartialCharge values are more likely to do so. Furthermore, MaxAbsPartialCharge also captures inductive effects from the fluorine atoms in the chain. In effect, it captures the slight differences between the partial charges experienced by the carboxylate groups of PFCs with varying chain lengths and, by extension, their photolysis rates. ")
    st.write("The overall proposed mechanism, which is visually represented in the figure above, corresponds with the observed patterns in the raw data used to train the models. As observed, PFCs with carboxylate groups indeed have varying photolysis rate constants depending on chain length. It also is in good agreement with the currently accepted mechanism for the photodegradation of PFAS via UV-light at other wavelengths like 185 nm, involving a decarboxylation initiation step. While it is likely that there are other descriptors that could better explain the variations in photolysis behavior once more experimental data is available, the current mechanism is, at the very least, able to explain the variances observed with currently available data on photolysis of perfluoro compounds via far-UVC light.")
    st.write("Meanwhile, the environmental descriptors play a smaller role relative to the molar absorption coefficient but still influence photolysis as evidenced by their respective coefficients across the models. However, unlike  ε222 nm, it is worth noting that both the pH and [NO3-] negatively impact k222 nm of the PFCs.")
    st.write("In particular, the nitrate in the solution matrix interferes with the photon absorption of the PFCs by competing with the PFCs in absorbing photons. Because of this. higher concentrations of nitrate in solution reduce the photolysis rates. The models affirm this by showing a negative correlation between k222 nm and [NO3-]. In addition, recent studies support this role of NO3- in photolysis studies. A study from 2025 that looked at the role of nitrate ions in the photolysis of organic micropollutants using far-UVC light reported that on top of the high molar absorption of NO3- at this region, it exerts a light screening effect at higher concentrations in which it effectively prevents the photons from the far-UVC light to hit the target pollutants and effectively hindering photolysis from occurring (Mohammed & Xu, 2026).")
    st.write("Similarly, pH shows an inverse relationship with  the photolysis rate constants of the PFCs as seen in their respective coefficients in the model equations. This finding implies that if higher pH levels contribute to lower rates of photolysis, then acidic conditions are favored for the photolysis of the PFCs. At lower pH levels, most of the PFCs are protonated. As such, the explanation for this relationship is more environmental in nature. Specifically, it is highly likely that photolysis is hindered at basic conditions because higher pH levels in environmental water matrices shifts dissolved inorganic carbon into carbonate and bicarbonate ions. These ions are incredibly aggressive radical scavengers that soak up all the reactive species before they can assist in the degradation process. In other words, the favorable conditions for the formation of species that compete for radicals is the main explanation for the negative effect of pH on the photolysis rate constants, as also affirmed by newer studies (Xin et al., 2025).")

    st.caption("For a complete discussion of the developed model, including its specifics, applicability, and limitations, you may ask me for a link to a copy of my findings.")

with tab_references:
    st.header("Acknowledgements", text_alignment = "center")
    st.write("First and foremost, I would like to express my sincerest gratitude to my mentor, Dr. Ian Ken Dimzon, for his unwavering guidance and support throughout this study. This would not have been possible without your help. I would also like to thank the Department of Science and Technology and the Office of Admission and Aid of Ateneo for the gift of scholarship; I would not be writing this had it not been for the  opportunity you gave me to study and pursue my passion for chemistry.")
    st.write("I would also like to give special thanks to my ASPAC Family for taking care of me as one of their scholars. It would not have been easy at all for me to study here in Ateneo without your parental care and support for me. Your care and concern for me has taken me places and I will never forget you for that.")
    st.write("To the people I hold close to my heart–my family, most especially my mother and my beautiful siblings, for the emotional support and the love that they have given me throughout my college journey, my dearest college roommates who have seen me in my best and worst as a college student, my dearest blockmates that continuously gave me advice and became my safe space, my high school constants who served as my rest and relief when things got stressful as an adult, the Ateneo Chemistry Society Executive Board 2425 for being ever present, and the Ateneo Special Education Society Executive Council 2526 for the growth and encouragement–my fight has been and always will be for you, the people I love and cherish the most in this world.")
    st.write("Lastly, I would like to thank God for his divine guidance. It took a while but regaining my way to you made my college life complete. May you continue to guide me as I continue my journey as an Atenean scholar, a growing scientist for and with others, and as a person who strives to always choose the most loving option.")
