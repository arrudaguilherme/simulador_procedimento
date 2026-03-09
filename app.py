import streamlit as st
import streamlit_authenticator as stauth
import yaml

# -------------------
# Configuração do app
# -------------------
st.set_page_config(
    page_title="Simulador de Procedimento",
    layout="wide",
)

# -------------------
# Carregando credenciais do YAML
# -------------------
with open("config.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
)

# -------------------
# Centralizando login e logo
# -------------------
st.write("")  # espaço superior
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    st.write("")  # espaço
    name, authentication_status, username = authenticator.login(
        "Simulador Financeiro de Procedimento",
        location="main"
    )

# -------------------
# Após login
# -------------------
if authentication_status:
    # Logout no sidebar
    authenticator.logout("Logout", "sidebar")

    # Cabeçalho com logo e título
    header_col1, header_col2 = st.columns([1, 8])
    with header_col1:
        st.image("assets/logo_titulo.jpeg", width=60)
    with header_col2:
        st.markdown("## Simulador Financeiro de Procedimento")

    st.write("📊 Simulação do fluxo financeiro do procedimento, considerando fluxos operacionais e repasse ao médico.")

    # -------------------
    # Taxas e constantes
    # -------------------
    taxas_pagamento = {
        "Crédito": 0.1341,
        "Débito": 0.0258,
        "Tap - Crédito": 0.1341,
        "Tap - Débito": 0.0258,
        "Smart POS - Crédito": 0.1341,
        "Smart POS - Débito": 0.0258,
        "Link": 0.1666
    }

    TAXA_ADMIN = 0.03

    # -------------------
    # Layout em colunas
    # -------------------
    col1, col2 = st.columns(2)

    # -------------------
    # Coluna esquerda: Inputs
    # -------------------
    with col1:
        st.subheader("📝 Dados do Procedimento")

        input_col1, input_col2 = st.columns([1, 1])

        with input_col1:
            st.markdown("Valor do Procedimento médico")
            valor_procedimento = st.number_input(
                "",
                min_value=0.0,
                value=450.0,
                step=10.0,
                format="%.2f"
            )

        with input_col2:
            st.markdown("Valor dos dispositivos utilizados")
            valor_equipamento = st.number_input(
                "",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f"
            )

        metodo_pagamento = st.selectbox(
            "Forma de pagamento do paciente",
            list(taxas_pagamento.keys())
        )

        taxa_metodo = taxas_pagamento[metodo_pagamento]
        st.write(f"**Custo da operação financeira:** {taxa_metodo*100:.2f}%")
        
        st.image("assets/logo.jpeg", width=300)

    # -------------------
    # Cálculos individuais
    # -------------------
    crm_pay = valor_procedimento * TAXA_ADMIN

    # Valor ajustado = soma procedimento + equipamento + CRM
    valor_procedimento_ajustado = valor_procedimento + valor_equipamento + crm_pay

    # Aplicando taxa do método sobre valor ajustado
    valor_pos_taxa = valor_procedimento_ajustado / (1 - taxa_metodo)

    # Valor da taxa do método (apenas referência)
    valor_taxa_metodo = valor_pos_taxa - valor_procedimento_ajustado

    # Repasse médico atualizado (não inclui taxa do método)
    repasse_medico = valor_procedimento - crm_pay

    # -------------------
    # Coluna direita: Resultados
    # -------------------
    with col2:
        st.subheader("📈 Resultado Financeiro da Operação")

        st.write(f"Procedimento: **R$ {valor_procedimento:,.2f}**") 
        st.write(f"Dispositivos: **R$ {valor_equipamento:,.2f}**")
        st.write(f"Operadora (valor taxa): **R$ {valor_taxa_metodo:,.2f}**")
        st.write(f"CRM Pay (3%): **R$ {crm_pay:,.2f}**")
        st.write(f"Valor Final para o paciente: **R$ {valor_pos_taxa:,.2f}**")

        st.write("---")
        st.subheader("🏥 Honorário Médico")
        st.success(f"Valor: **R$ {repasse_medico:,.2f}**")
        st.write("O paciente poderá realizar o pagamento em até 12x no cartão")

elif authentication_status == False:
    st.error("Usuário ou senha incorretos")
else:
    st.warning("Por favor, faça login")