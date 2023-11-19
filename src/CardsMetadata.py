from src.card_effects.analisis import analisis
from src.card_effects.cambio_de_lugar import cambio_de_lugar
from src.card_effects.lanzallamas import lanzallamas
from src.card_effects.mas_vale_que_corras import mas_vale_que_corras
from src.card_effects.puerta_atrancada import puerta_atrancada
from src.card_effects.seduccion import seduccion
from src.card_effects.sospecha import sospecha
from src.card_effects.whisky import whisky
from src.card_effects.vigila_tus_espaldas import vigila_tus_espaldas
from src.card_effects.hacha import hacha
from src.card_effects.determinacion import determinacion
from src.card_effects.cuarentena import cuarentena


CARDS_METADATA = {

    # CONTAGIO
    "La Cosa": {
        "category": 'contagion',
        "number": 4,
        "quantity": 1,
        "description": """Eres “La Cosa”, y tu objetivo es infectar o destruir a los Humanos. NO
        PUEDES descartar o intercambiar esta carta, incluso si el efecto de una carta te pide
        hacerlo.""",
    },

    "¡Infectado!": {
        "category": 'contagion',
        "number": 4,
        "quantity": 12,
        "description": """Si robas esta carta, no estás Infectado y puedes descartarla si quieres.
        Pero recuerda esto: ¡si alguien descubre que tienes esta carta, pensará que estás
        Infectado! Si eres Humano, ¡no puedes darle esta carta a ningún jugador! Si otro
        jugador te pasa una carta “¡Infectado!” (y sólo La Cosa puede hacerlo), quedas
        Infectado y puedes darle otras cartas “¡Infectado!” a La Cosa (únicamente a ella).
        Pero recuerda que siempre debes quedarte al menos 1 carta “¡Infectado!”, y que
        NUNCA puedes descartar o intercambiar esa carta, incluso si el efecto de una carta
        te pide hacerlo""",
    },

    # ACCION
    "Lanzallamas": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Ésta es la única carta que puede eliminar a un jugador adyacente.""",
        "play": lanzallamas
    },
    "Análisis": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Si juegas esta carta sobre un jugador adyacente, debe mostrarte todas las
        cartas de su mano.""",
        "play": analisis
    },
    "Hacha": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Puedes jugar esta carta sobre ti mismo o sobre un jugador adyacente para
        retirar una carta “Puerta atrancada” o “Cuarentena” que afecte a ese jugador.""",
        "play": hacha
    },
    "Sospecha": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Coge 1 carta aleatoria de un jugador adyacente, mirala y devuélvesela.""",
        "play": sospecha
    },
    "Whisky": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Enséñales todas tus cartas a los demás jugadores. Esta carta sólo puedes
        jugarla sobre ti mismo""",
        "play": whisky
    },
    "Determinación": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Roba 3 cartas ¡Aléjate!, quédate con 1 en la mano y descarta el
        resto. A continuación, juega o descarta 1 carta. Puedes jugar otra carta
        “Determinación” en el mismo turno. Si hay cartas de ¡Pánico! en la parte superior del
        mazo, debes descartarlas sin mirarlas, hasta que haya 3 cartas ¡Aléjate! que puedas
        robar para resolver el efecto.""",
        "play": determinacion
    },
    "Vigila tus espaldas": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Invierte el orden de juego. Así que si el turno pasaba hacia la
        izquierda, ahora lo hace hacia la derecha. Esto afecta tanto al orden de turnos como
        a los intercambios de cartas.""",
        "play": vigila_tus_espaldas
    },
    "¡Cambio de lugar!": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Cámbiate de sitio físicamente con un jugador que tengas al lado,
        salvo que te lo impida un obstáculo como “Cuarentena” o “Puerta atrancada”, Llévate
        tu mano de cartas al cambiar de lugar. A continuación, intercambia 1 carta con el
        siguiente jugador desde tu nueva ubicación y termina tu turno. El siguiente turno
        comienza con el jugador con el que hayas realizado el intercambio, siguiendo el
        orden de juego activo.""",
        "play": cambio_de_lugar
    },
    "¡Más vale que corras!": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Cámbiate de sitio físicamente con cualquier jugador que no
        esté bajo los efectos de “Cuarentena”, ignorando cualquier carta “Puerta atrancada”
        que haya en la mesa. Llévate tu mano de cartas al cambiar de lugar. A continuación,
        intercambia 1 carta con el siguiente jugador desde tu nueva ubicación y termina tu
        turno. El siguiente turno comienza con el jugador con el que hayas realizado el
        intercambio, siguiendo el orden de juego activo""",
        "play": mas_vale_que_corras
    },
    "Seducción": {
        "category": 'action',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Intercambia 1 carta con cualquier jugador que no esté en Cuarentena y
        luego termina tu turno.""",
        "play": seduccion
    },

    # DEFENSA
    "Aterrador": {
        "category": 'defense',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Sólo puedes jugar esta carta como respuesta a un ofrecimiento de
        intercambio de cartas. Niégate a un intercambio de cartas solicitado por un jugador o
        por el efecto de una carta. Mira la carta que te has negado a coger y devuélvesela a
        su dueño.""",
    },
    "Aquí estoy bien": {
        "category": 'defense',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Sólo puedes jugar esta carta como respuesta a una carta “¡Cambio
        de lugar!” o “¡Más vale que corras!” para cancelar su efecto.""",
    },
    "¡No, gracias!": {
        "category": 'defense',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Sólo puedes jugar esta carta como respuesta a un ofrecimiento de
        intercambio de cartas. Niégate a un intercambio de cartas solicitado por un jugador o
        por el efecto de una carta.""",
    },
    "¡Fallaste!": {
        "category": 'defense',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Sólo puedes jugar esta carta como respuesta a un ofrecimiento de
        intercambio de cartas. Niégate a un intercambio de cartas solicitado por un jugador o
        por el efecto de una carta. El siguiente jugador después de ti (siguiendo el orden de
        juego) debe intercambiar cartas en lugar de hacerlo tú. Si este jugador recibe una
        carta “¡Infectado!” durante el intercambio, no queda Infectado, ¡pero sabrá que ha
        recibido una carta de La Cosa o de un jugador Infectado! Si hay “obstáculos” en el
        camino, como una “Puerta atrancada” o “Cuarentena”, no se produce ningún
        intercambio, y el siguiente turno lo jugará el jugador siguiente a aquel que inició el
        intercambio.""",
    },
    "¡Nada de barbacoas!": {
        "category": 'defense',
        "number": 4,
        "quantity": 3,
        "needs_target": False,
        "description": """Sólo puedes jugar esta carta como respuesta a una carta
        “Lanzallamas” para evitar ser eliminado de la partida.""",
    },

    # OBSTACULO
    "Cuarentena": {
        "category": 'obstacle',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Puedes jugar esta carta sobre un jugador adyacente de tu elección.
        Durante las 2 siguientes rondas, el jugador “en Cuarentena” robará, intercambiará y
        descartará cartas mostrándoselas siempre a los demás jugadores. Además, no
        puede eliminar jugadores ni jugar o ser objetivo de cartas que permitan un cambio
        de lugar, salvo que la carta especifique algo distinto.
        Por ejemplo, si el jugador que está bajo los efectos de una “Cuarentena” es La Cosa,
        tendrá que tener en cuenta que todos los ofrecimientos de cartas “¡Infectado!” serán
        visibles para todos.
        La “Cuarentena” puede ser retirada y descartada antes de que acabe el plazo de 2
        rondas si se usá una carta “Hacha” o mediante el efecto de algunas cartas de
        ¡Pánico!.""",
        "play": cuarentena
    },
    "Puerta atrancada": {
        "category": 'obstacle',
        "number": 4,
        "quantity": 3,
        "needs_target": True,
        "description": """Puedes jugar esta carta sobre la mesa, entre un adyacente y tú.
        Ninguno de los dos podéis realizar acciones que tengan como objetivo al otro (jugar
        cartas, intercambiar cartas y cambiar de lugar). La carta permanece boca arriba
        entre ambos hasta que sea retirada por una carta “Hacha” o por el efecto de una
        carta de ¡Pánico!
        Si los jugadores cambian de lugar por el efecto de otra carta, la “Puerta atrancada”
        sigue en su posición original de la mesa, pero los jugadores afectados por ella
        podrían cambiar.""",
        "play": puerta_atrancada
    },
}
