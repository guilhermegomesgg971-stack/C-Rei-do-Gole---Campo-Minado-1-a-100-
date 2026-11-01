import random
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Rei do Gole - Campo Minado", page_icon="🍺", layout="centered"
)

# Estilização visual rápida via Markdown/CSS
st.markdown(
    """
    <style>
    .main { background-color: #121214; color: #f3f4f6; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🍺 REI DO GOLE")
st.subheader("Campo Minado (1 a 100)")

# Inicialização do Estado do Jogo (Sessão do Streamlit)
if "bombas" not in st.session_state:
  st.session_state.num_bombas = 3
  st.session_state.bombas = random.sample(range(1, 101), st.session_state.num_bombas)
  st.session_state.descobertos = []
  st.session_state.jogadores = ["Amigo 1", "Amigo 2"]
  st.session_state.pontuacao = {"Amigo 1": 0, "Amigo 2": 0}
  st.session_state.turno = 0
  st.session_state.jogo_acabou = False

# Sidebar de Configurações
with st.sidebar:
  st.header("⚙️ Configurações")

  # Escolha de bombas
  novas_bombas = st.selectbox(
      "Quantidade de Bombas", [1, 2, 3, 4, 5], index=2
  )
  if novas_bombas != st.session_state.num_bombas:
    st.session_state.num_bombas = novas_bombas
    st.session_state.bombas = random.sample(range(1, 101), novas_bombas)
    st.session_state.descobertos = []
    st.session_state.jogo_acabou = False
    st.rerun()

  st.divider()
  st.subheader("👥 Jogadores")
  novo_jogador = st.text_input("Adicionar Amigo:")
  if st.button("Adicionar") and novo_jogador:
    if novo_jogador not in st.session_state.jogadores:
      st.session_state.jogadores.append(novo_jogador)
      st.session_state.pontuacao[novo_jogador] = 0
      st.rerun()

  if st.button("🔄 Reiniciar Jogo"):
    st.session_state.bombas = random.sample(
        range(1, 101), st.session_state.num_bombas
    )
    st.session_state.descobertos = []
    st.session_state.jogo_acabou = False
    st.rerun()

# Painel da Vez
jogador_atual = (
    st.session_state.jogadores[
        st.session_state.turno % len(st.session_state.jogadores)
    ]
    if st.session_state.jogadores
    else "Ninguém"
)
st.markdown(
    f"### 🎯 Vez de: <span style='color: #f59e0b;'>{jogador_atual}</span>",
    unsafe_allow_html=True,
)

# Placar Lateral / Abaixo
st.write("---")
cols_placar = st.columns(len(st.session_state.jogadores) or 1)
for i, jg in enumerate(st.session_state.jogadores):
  with cols_placar[i]:
    st.metric(label=jg, value=f"{st.session_state.pontuacao[jg]} doses")

st.write("---")
st.markdown("### 🎲 Escolha um número na grade:")

# Grade de 1 a 100 dividida em linhas de 10 botões
for linha in range(10):
  cols = st.columns(10)
  for coluna in range(10):
    num = linha * 10 + coluna + 1
    with cols[coluna]:
      if num in st.session_state.descobertos:
        if num in st.session_state.bombas:
          st.button("💥", key=f"btn_{num}", disabled=True)
        else:
          st.button("🍺", key=f"btn_{num}", disabled=True)
      else:
        if st.button(str(num), key=f"btn_{num}"):
          st.session_state.descobertos.append(num)
          if num in st.session_state.bombas:
            st.session_state.pontuacao[jogador_atual] += 1
            st.error(
                f"💥 BOOM! {jogador_atual} achou a bomba e deve BEBER 1 DOSE!"
            )
          else:
            # Avança o turno se for seguro
            st.session_state.turno += 1
          st.rerun()
