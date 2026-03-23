import math
import random

# =========================
# Paramètres
# =========================
S0         = 100.0   # spot initial
K          = 100.0   # strike
T          = 1.0     # maturité (1 an)
r          = 0.02    # taux sans risque
sigma      = 0.20    # volatilité
steps      = 52      # rebalancing hebdomadaire
seed       = 42

# =========================
# Fonctions utilitaires
# =========================
def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs_price(S, K, T, r, sigma):
    if T <= 0:
        return max(S - K, 0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

def bs_delta(S, K, T, r, sigma):
    if T <= 0:
        return 1.0 if S > K else 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return norm_cdf(d1)

# =========================
# Simulation du chemin
# =========================
random.seed(seed)
dt = T / steps
path = [S0]
for _ in range(steps):
    z = random.gauss(0, 1)
    path.append(path[-1] * math.exp((r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z))

# =========================
# Delta Hedging
# =========================
# On vend 1 call et on se hedge en achetant delta actions
shares   = bs_delta(S0, K, T, r, sigma)
cash     = bs_price(S0, K, T, r, sigma) - shares * S0  # prime reçue - achat actions

print(f"{'Step':<5} {'Spot':<10} {'Delta':<10} {'Cash':<12} {'PnL':<10}")
print("-" * 50)

for i in range(1, steps + 1):
    t       = i * dt
    tau     = max(T - t, 0)
    S       = path[i]

    cash   *= math.exp(r * dt)                          # intérêts sur le cash
    new_delta = bs_delta(S, K, tau, r, sigma)
    cash   -= (new_delta - shares) * S                  # rebalancing
    shares  = new_delta

    option_val = bs_price(S, K, tau, r, sigma)
    pnl        = shares * S + cash - option_val         # hedge - option mark-to-market

    if i <= 5 or i == steps:
        label = " ← final" if i == steps else ""
        print(f"{i:<5} {S:<10.2f} {shares:<10.4f} {cash:<12.4f} {pnl:<10.4f}{label}")

# =========================
# Résumé final
# =========================
payoff = max(path[-1] - K, 0)
print("\n--- Résumé ---")
print(f"Spot final         : {path[-1]:.2f}")
print(f"Payoff du call     : {payoff:.4f}")
print(f"Valeur du hedge    : {shares * path[-1] + cash:.4f}")
print(f"PnL résiduel       : {pnl:.4f}  ← dû au hedging discret")