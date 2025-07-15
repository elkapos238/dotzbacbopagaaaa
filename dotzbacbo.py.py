
import random
import telegram
import time
import logging

# ============ CONFIGURATION =============
TOKEN = '7587673723:AAFolnHuHI2fR4Gr1Nzlw4Ga1dIevsz46nI'  # Ton token Telegram ici
CHANNEL_ID = '-1002817091645'     # Ton @canal ici
bot = telegram.Bot(token=TOKEN)

# ============ VARIABLES GLOBAL ============
green_count = 0
loss_count = 0
total_tries = 0
gale_level = 0
current_bet = None

# ============ LOGIQUE DE PREDICTION STRATÉGIQUE =============
def choose_color():
    return random.choice(['🟥 Vermelho', '🟦 Azul'])

def send_signal(prediction, gale):
    msg = f"""
🎯 Entrar em: {prediction}
🛡️ Segurança no 🟨 Empate
🎰 Estratégia: G{gale}
"""
    bot.send_message(chat_id=CHANNEL_ID, text=msg)

def update_stats(win):
    global green_count, loss_count, total_tries
    if win:
        green_count += 1
    else:
        loss_count += 1
    total_tries += 1

def send_result_summary():
    success_rate = (green_count / total_tries) * 100 if total_tries > 0 else 0
    msg = f"""
📊 RESULTADO ATUAL:
✅ Vitórias: {green_count}
❌ Derrotas: {loss_count}
📈 Taxa de acerto: {success_rate:.2f}%
"""
    bot.send_message(chat_id=CHANNEL_ID, text=msg)

# ============ SIMULATION D'UN RÉSULTAT LIVE BAC BO =============
def simulate_real_result():
    # 0 = empate, 1 = vermelho, 2 = azul
    return random.choices([0, 1, 2], weights=[0.1, 0.45, 0.45])[0]

# ============ BOUCLE PRINCIPALE =============
def main():
    global gale_level, current_bet

    logging.info("Bot iniciado...")

    while True:
        try:
            if gale_level == 0:
                current_bet = choose_color()
                send_signal(current_bet, 1)
                result = simulate_real_result()
                if (current_bet == '🟥 Vermelho' and result == 1) or                    (current_bet == '🟦 Azul' and result == 2) or result == 0:
                    update_stats(True)
                    gale_level = 0
                else:
                    gale_level = 1
                    time.sleep(180)  # Pause avant G2
                    continue

            elif gale_level == 1:
                send_signal(current_bet, 2)
                result = simulate_real_result()
                if (current_bet == '🟥 Vermelho' and result == 1) or                    (current_bet == '🟦 Azul' and result == 2) or result == 0:
                    update_stats(True)
                else:
                    update_stats(False)
                gale_level = 0

            send_result_summary()
            time.sleep(300)  # 5 min entre les signaux

        except Exception as e:
            logging.error(f"Erro: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()
