# -*- coding: utf-8 -*-
"""
# ToDo: Add a brief description of the recommendation form functionality and purpose.
"""

import streamlit as st


try:
    from src.questions import (
        QUESTIONS,
    )
    from src.ml_models import (
        setup_nn_models,
        get_pet_recommendations,
    )
except ImportError:
    from ..src.questions import (
        QUESTIONS,
    )
    from ..src.ml_models import (
        setup_nn_models,
        get_pet_recommendations,
    )


def main():
    """Define the client view of the web-app, including the adoption form."""

    # Set up the Streamlit page configuration
    set_streamlit_page_config()

    # Set up the neural network models
    setup_nn_models()

    # Initialize session state variables
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    if "pet_recommendations" not in st.session_state:
        st.session_state.pet_recommendations = []
    if "current_pet_id" not in st.session_state:
        st.session_state.current_pet_id = 0
    if "number_of_recommendations" not in st.session_state:
        st.session_state.number_of_recommendations = 10
    if "next_recommendation" not in st.session_state:
        st.session_state.next_recommendation = False
    if "previous_recommendation" not in st.session_state:
        st.session_state.previous_recommendation = False

    # Create a form for pet adoption
    with st.form("adoption_form"):

        # Title and description
        st.title("Encuentra a tu mascota ideal 🐕")
        st.subheader("*Descubre al perro perfecto para ti y tu estilo de vida*")
        st.write(
            "A continuación encontrarás un cuestionario cuidadosamente diseñado para"
            + " identificar las características y preferencias más importantes a la"
            + " hora de adoptar un perro."
        )
        st.write(
            "Por favor, responde cada pregunta con sinceridad, ya que tus respuestas"
            + " nos ayudarán a encontrar la mascota que mejor se adapte a tu rutina,"
            + " entorno familiar y expectativas."
        )
        st.write("¡Comencemos el viaje hacia la adopción responsable!")

        # Separator
        st.write("---")
        st.subheader("Formulario de adopción:")

        # Initialize with "1" as the default value for "urgent_adoption"
        client_answers = [1]
        for question in QUESTIONS:
            answer = st.selectbox(
                question["question"],
                options=question["options"].keys(),
                index=None,
                placeholder="Selecciona una opción",
            )
            client_answers.append(
                None if answer is None else question["options"][answer]
            )

        # Separator
        st.write("---")

        # Terms and conditions and Privacy policy
        st.subheader("Términos y condiciones")

        terms = st.checkbox("Acepto los términos y condiciones")
        st.write(
            "Por favor, lee los términos y condiciones antes de enviar el formulario."
        )
        with st.expander("Leer términos y condiciones"):
            st.write(
                "Al enviar este formulario, aceptas que tus datos serán utilizados"
                + " para procesar tu solicitud de adopción."
            )

        privacy_policy = st.checkbox("Acepto la política de privacidad")
        st.write(
            "Por favor, lee la política de privacidad antes de enviar el formulario."
        )
        with st.expander("Leer política de privacidad"):
            st.write(
                "Tus datos serán tratados de forma confidencial y no serán compartidos"
                + " con terceros sin tu consentimiento."
            )
            st.write(
                "Por el momento, no se almacenarán tus datos en ninguna base de datos,"
                + " pero si en el futuro se decide almacenar tus datos, se actualizará"
                + " la política de privacidad para informarte de ello."
            )

        # Separator
        st.write("---")

        # Form submission button
        st.session_state.form_submitted = st.form_submit_button(
            "ENVIAR",
            use_container_width=True,
            type="primary",
            on_click=lambda: st.session_state.update(
                form_submitted=True,
                next_recommendation=False,
                previous_recommendation=False,
                current_pet_id=0,
            ),
        )

    if not (
        st.session_state.form_submitted
        or st.session_state.next_recommendation
        or st.session_state.previous_recommendation
    ):
        # If the form has not been submitted, do not process the input
        return

    if not (terms and privacy_policy):
        st.error(
            "Por favor, acepta los términos y condiciones y la política de privacidad"
            + " para poder proceder."
        )
        return

    if None in client_answers:
        st.error("Por favor, responde a todas las preguntas del formulario.")
        return

    if client_answers[6] == 0 or client_answers[7] == 0:
        st.warning(
            "Lo sentimos, pero no podemos recomendarte ninguna mascota en este momento,"
            + " ten en cuenta que si ya tienes una mascota no amigable en casa, no"
            + " podemos recomendarte una mascota que pueda no llevarse bien con ella."
        )
        return

    if not (
        st.session_state.next_recommendation or st.session_state.previous_recommendation
    ):
        st.session_state.pet_recommendations = get_pet_recommendations(
            client_answers,
            st.session_state.number_of_recommendations,
        )

    st.success("Formulario enviado con éxito!")

    st.write("---")
    st.header(
        f"Recomendación {st.session_state.current_pet_id + 1} de "
        f"{len(st.session_state.pet_recommendations)}"
    )
    left, right = st.columns(2)

    with left:
        st.session_state.previous_recommendation = st.button(
            "Recomendación anterior",
            use_container_width=True,
            disabled=(st.session_state.current_pet_id <= 0),
            on_click=lambda: st.session_state.update(
                current_pet_id=st.session_state.current_pet_id - 1,
                next_recommendation=False,
                previous_recommendation=True,
            ),
        )
    with right:
        st.session_state.next_recommendation = st.button(
            "Siguiente recomendación",
            use_container_width=True,
            disabled=(
                st.session_state.current_pet_id
                >= (len(st.session_state.pet_recommendations) - 1)
            ),
            on_click=lambda: st.session_state.update(
                current_pet_id=st.session_state.current_pet_id + 1,
                next_recommendation=True,
                previous_recommendation=False,
            ),
        )

    st.write("---")

    if st.session_state.current_pet_id < 0 or st.session_state.current_pet_id >= len(
        st.session_state.pet_recommendations
    ):
        st.error(
            "Felicidades, has encontrado un bug en la aplicación, por favor, no le des"
            + " tan rápido a los botones, gracias por tu paciencia."
        )
        return

    # Display the recommended pet
    current_pet = st.session_state.pet_recommendations[st.session_state.current_pet_id]
    display_pet_info(current_pet)


def set_streamlit_page_config():
    """Set up the Streamlit page configuration and custom styles."""
    st.set_page_config(
        page_title="Formulario de adopción",
        page_icon=":dog:",
        layout="centered",
    )

    max_width_str = f"max-width: {80}%;"
    st.markdown(
        f"""
        <style>
            .stApp {{
                primary-color: #4bf5ff;
                background-color: #ffffff;
                secondary-background-color: #f0f2f5;
                text-color: #333333;
            }}
            .reportview-container .main .block-container{{{max_width_str}}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def display_pet_info(pet):
    """Display the information of the recommended pet."""

    st.title(pet["name"])
    st.subheader(" 🔴 ¡Urge adopción! 🔴" if pet["urgent_adoption"] else "")
    st.image(pet["img_url"], caption="", use_container_width=True)

    st.subheader("Descripción:")
    if isinstance(pet["description_1"], str) and pet["description_1"].strip() != "":
        st.write(pet["description_1"].strip())
    if (
        isinstance(pet["description_2"], str)
        and pet["description_2"].strip() != ""
        and pet["description_2"] != pet["description_1"]
    ):
        st.write(pet["description_2"].strip())

    left_col_1, right_col_1 = st.columns(2, border=True)

    with left_col_1:
        st.subheader("Características:")

        st.write(
            ("♂" if pet["gender"] == "Macho" else "♀") + f" Género: {pet['gender']}"
        )
        st.write(f"🎂 Edad: {pet['age']} años")
        st.write(f"📏 Tamaño: {pet['size']}")
        st.write(f"🐾 Raza: {pet['breed']}")
        st.write(f"🌍 Provincia: {pet['province']}")
        st.write(f"🛩️ Puede viajar: {'Sí' if pet['can_travel'] else 'No'}")

    with right_col_1:
        st.subheader("Salud y cuidados:")
        st.write(
            "🩺 "
            + (
                "Necesita cuidados veterinarios"
                if pet["needs_vet_care"]
                else "No necesita cuidados veterinarios especiales"
            )
        )
        if pet["is_healthy"]:
            st.write("💚 Está sano")
        st.write(
            "💉 " + ("Está vacunado" if pet["is_vaccinated"] else "No está vacunado")
        )
        st.write(
            "🪱 "
            + ("Está desparasitado" if pet["is_dewormed"] else "No está desparasitado")
        )
        st.write(
            "✂️ "
            + ("Está esterilizado" if pet["is_sterilized"] else "No está esterilizado")
        )
        st.write(
            "🪪 "
            + ("Está identificado" if pet["is_identified"] else "No está identificado")
        )
        st.write(
            "📌 "
            + ("Tiene microchip" if pet["has_microchip"] else "No tiene microchip")
        )
        st.write(
            "🛂 " + ("Tiene pasaporte" if pet["has_passport"] else "No tiene pasaporte")
        )

    left_col_2, right_col_2 = st.columns(2, border=True)

    with left_col_2:
        st.subheader("Compatibilidades:")
        st.write(
            "👶 "
            + (
                "Compatible con niños"
                if pet["good_with_children"]
                else "No es compatible con niños"
            )
        )
        st.write(
            "🐱 "
            + (
                "Compatible con gatos"
                if pet["good_with_cats"]
                else "No es compatible con gatos"
            )
        )
        st.write(
            "🐶 "
            + (
                "Compatible con perros"
                if pet["good_with_dogs"]
                else "No es compatible con perros"
            )
        )

    with right_col_2:
        if any(
            [
                pet["is_affectionate"],
                pet["is_hyperactive"],
                pet["is_fearful"],
                pet["is_sociable"],
                pet["is_calm"],
                pet["is_sedentary"],
            ]
        ):
            st.subheader("Personalidad de la mascota:")
            if pet["is_affectionate"]:
                st.write("❤️ Cariñoso")
            if pet["is_hyperactive"]:
                st.write("⚡ Hiperactivo")
            if pet["is_fearful"]:
                st.write("😨 Miedoso")
            if pet["is_sociable"]:
                st.write("👥 Sociable")
            if pet["is_calm"]:
                st.write("🛏️ Tranquilo")
            if pet["is_sedentary"]:
                st.write("🐢 Sedentario")

    st.write("---")

    st.subheader("¿Quieres adoptar a esta mascota?")
    st.write(
        "Si te parece buena la recomendación y quieres adoptar,"
        + " por favor visita el siguiente enlace:"
    )

    st.link_button(
        "Ir a la web de adopción",
        url=pet["info_url"],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
