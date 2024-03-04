def select_section(quiz_section):
    selected_subsection = ""

    while True:
        print("Choose a quiz section:")
        for idx, section in enumerate(quiz_section.keys()):
            print(f"{idx}: {section}")

        user_input = input("Enter the number corresponding to the quiz section: ")

        if user_input.isdigit():
            section_idx = int(user_input)

            if 0 <= section_idx < len(quiz_section):
                selected_section = list(quiz_section.keys())[section_idx]
                print(f"You selected: {selected_section}")

                if isinstance(quiz_section[selected_section], dict):
                    target_tuple, selected_subsection = select_subsection(quiz_section[selected_section])
                else:
                    target_tuple = quiz_section[selected_section]
                    print(f"Section tuple: {target_tuple}")
                break
            else:
                print("Invalid input. Please enter a number within the specified range.")
        else:
            print("Invalid input. Please enter a valid number.")

    return target_tuple, selected_section, selected_subsection

def select_subsection(subsections):
    while True:
        print("Choose a subsection:")
        for idx, subsection in enumerate(subsections.keys()):
            print(f"{idx}: {subsection}")

        user_input = input("Enter the number corresponding to the subsection: ")

        if user_input.isdigit():
            subsection_idx = int(user_input)

            if 0 <= subsection_idx < len(subsections):
                selected_subsection = list(subsections.keys())[subsection_idx]
                print(f"You selected: {selected_subsection}")
                target_tuple = subsections[selected_subsection]
                print(f"Subsection tuple: {target_tuple}")
                break
            else:
                print("Invalid input. Please enter a number within the specified range.")
        else:
            print("Invalid input. Please enter a valid number.")

    return target_tuple, selected_subsection

quiz_sections_entro = {
    'teoria_dello_scafo' : (0,125),
    'motori' : (126,229),
    'sicurezza_della_navigazione':
        {
            "all" : (230,444),
            "prevenzione_degli_incendi_e_uso_degli_estintori" : (230,260),
            "dotazioni_di_sicurezza_e_mezzi_di_salvataggio" : (274,320)
        },
    'manovra_e_condotta' : (445,599),
    'colreg_e_segnalamento_marittimo' : (600,846),
    'meteorologia' : (847,966),
    'navigazione_cartografica_ed_elettronica' : 
        {
            "all" : (967,1288),
            "coordinate_geografiche" : (967,1011),
            "carte_nautiche_e_proiezione_di_Mercatore" : (1012,1067),
            "navigazione_elettronica" : (1068,1080),
            "orientamento_e_rosa_dei_venti" : (1081,1091),
            "bussole magnetiche" : (1092,1129),
            "elementi_di_navigazione_stimata:_tempo,_spazio_e_velocità" : (1130,1201),
            "elementi_di_navigazione_costiera" : (1202,1250),
            "prora_e_rotta,_scarroccio_e_deriva_per_effetto_del_vento_e_della_corrente" : (1251,1280),
            "pubblicazioni" : (1281,1288)
        },
    'normativa_diportistica': 
        {
            'all' : (1288,1472),
            'leggi_e_regolamenti' : (1288,1330),
            'comandante_conduttore_utilizzatore' : (1331,1333),
            'attivita_commerciale_e_documenti': (1334,1413),
            'sci_nautico_pesca_norme_ambientali' : (1414,1472)
        }
}

quiz_sections_vela = {
    'all' : (0,250),
    'teoria' : (0,99),
    'attrezzatura': (100,185),
    'manovre' : (186,250)
}