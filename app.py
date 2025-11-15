from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

class NeuroCasino:
    def __init__(self):
        self.balance = 1000
        self.games_played = 0
        self.ai_personality = random.choice([
            "🤖 Холодный алгоритм", "🔮 Мистический оракул", 
            "🎭 Таинственный незнакомец", "👾 Кибер-пророк"
        ])
    
    def spin_slots(self, bet_amount):
        if bet_amount > self.balance:
            return {"error": "Недостаточно средств!"}
        
        self.balance -= bet_amount
        self.games_played += 1
        
        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣", "💎", "🎯", "🌈"]
        results = [random.choice(symbols) for _ in range(3)]
        
        # Логика выигрыша
        win_amount = 0
        if results[0] == results[1] == results[2]:
            win_amount = bet_amount * 20
            message = "🎉 НЕЙРО-ДЖЕКПОТ!"
        elif results[0] == results[1] or results[1] == results[2]:
            win_amount = bet_amount * 3
            message = "⭐ СОВПАДЕНИЕ!"
        else:
            message = "🌪️ НЕЙРО-ХАОС!"
        
        self.balance += win_amount
        
        return {
            "results": results,
            "win_amount": win_amount,
            "balance": self.balance,
            "message": message,
            "games_played": self.games_played
        }
    
    def coin_flip(self, bet_amount, choice):
        if bet_amount > self.balance:
            return {"error": "Недостаточно средств!"}
        
        self.balance -= bet_amount
        self.games_played += 1
        
        result = random.choice(["орёл", "решка"])
        if choice == result:
            win_amount = bet_amount * 2
            self.balance += win_amount
            message = f"🌈 ВЫИГРЫШ! Выпал {result}"
        else:
            win_amount = 0
            message = f"🌪️ ПРОИГРЫШ! Выпал {result}"
        
        return {
            "result": result,
            "win_amount": win_amount,
            "balance": self.balance,
            "message": message,
            "games_played": self.games_played
        }

casino = NeuroCasino()

@app.route('/')
def index():
    return render_template('neuro_casino.html')

@app.route('/api/spin', methods=['POST'])
def api_spin():
    data = request.json
    bet_amount = data.get('bet_amount', 100)
    result = casino.spin_slots(bet_amount)
    return jsonify(result)

@app.route('/api/coinflip', methods=['POST'])
def api_coinflip():
    data = request.json
    bet_amount = data.get('bet_amount', 100)
    choice = data.get('choice', 'орёл')
    result = casino.coin_flip(bet_amount, choice)
    return jsonify(result)

@app.route('/api/status')
def api_status():
    return jsonify({
        "balance": casino.balance,
        "games_played": casino.games_played,
        "ai_personality": casino.ai_personality
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
