"""
Exercício 9 - Abordagem Dinâmica para Integração Numérica - VERSÃO CORRETA
"""

def trapezio_simples(f, a, b):
    """Regra do trapézio simples T(f,a,b)"""
    return (b - a) * (f(a) + f(b)) / 2

def simpson_simples(f, a, b):
    """Regra de Simpson simples S(f,a,b)"""
    m = (a + b) / 2
    return (b - a) * (f(a) + 4*f(m) + f(b)) / 6

def integracao_dinamica_correta(f, c, d, epsilon, nivel=0, contador=None):
    """
    Algoritmo dinâmico CORRETO para calcular I(f,c,d)
    
    Critério de subdivisão CORRETO:
    Para cada subintervalo [ci,di], comparar:
    |T(f,ci,di) - S(f,ci,di)| > epsilon_local
    
    Se o erro for grande, subdivide em [ci,meio] e [meio,di]
    """
    
    if contador is None:
        contador = [0]
    
    # Proteções de segurança
    if nivel > 15:
        return simpson_simples(f, c, d), contador[0] + 1
    
    if abs(d - c) < 1e-10:
        return 0, contador[0]
    
    # Calcular T(f,c,d) e S(f,c,d) para o MESMO intervalo
    f_c = f(c)
    f_d = f(d)
    meio = (c + d) / 2
    f_meio = f(meio)
    contador[0] += 3
    
    # Trapézio no intervalo [c,d]
    T_intervalo = (d - c) * (f_c + f_d) / 2
    
    # Simpson no intervalo [c,d]
    S_intervalo = (d - c) * (f_c + 4*f_meio + f_d) / 6
    
    # Critério de paragem: comparar T e S no MESMO intervalo
    erro_local = abs(T_intervalo - S_intervalo)
    tolerancia_local = epsilon / (2**(nivel + 1))
    
    if erro_local <= tolerancia_local:
        # Usar Simpson como melhor aproximação
        return S_intervalo, contador[0]
    else:
        # Subdividir o intervalo ao meio
        integral_esq, _ = integracao_dinamica_correta(f, c, meio, epsilon, nivel + 1, contador)
        integral_dir, _ = integracao_dinamica_correta(f, meio, d, epsilon, nivel + 1, contador)
        
        return integral_esq + integral_dir, contador[0]

def integracao_dinamica_otimizada(f, c, d, epsilon):
    """
    Versão otimizada com cache
    """
    
    cache = {}
    contador = [0]
    
    def f_cached(x):
        # Arredondar para evitar problemas de precisão
        x_round = round(x, 12)
        if x_round not in cache:
            cache[x_round] = f(x)
            contador[0] += 1
        return cache[x_round]
    
    def algoritmo_recursivo(a, b, nivel):
        if nivel > 15:
            meio = (a + b) / 2
            fa = f_cached(a)
            fb = f_cached(b)
            fmeio = f_cached(meio)
            return (b - a) * (fa + 4*fmeio + fb) / 6
        
        if abs(b - a) < 1e-10:
            return 0
        
        # Valores necessários
        fa = f_cached(a)
        fb = f_cached(b)
        meio = (a + b) / 2
        fmeio = f_cached(meio)
        
        # Trapézio e Simpson no mesmo intervalo [a,b]
        T_ab = (b - a) * (fa + fb) / 2
        S_ab = (b - a) * (fa + 4*fmeio + fb) / 6
        
        # Critério de paragem
        erro_local = abs(T_ab - S_ab)
        tolerancia_local = epsilon / (2**(nivel + 1))
        
        if erro_local <= tolerancia_local:
            return S_ab
        else:
            integral_esq = algoritmo_recursivo(a, meio, nivel + 1)
            integral_dir = algoritmo_recursivo(meio, b, nivel + 1)
            return integral_esq + integral_dir
    
    resultado = algoritmo_recursivo(c, d, 0)
    return resultado, contador[0]


# Exemplo de uso
if __name__ == "__main__":
    # Função de teste
    def f_teste(x):
        return x**2 + 1
    
    # Parâmetros
    c, d = 0, 2
    epsilon = 1e-4
    
    print("=== TESTE DO ALGORITMO DINÂMICO CORRETO ===")
    
    # Versão básica
    resultado1, avaliacoes1 = integracao_dinamica_correta(f_teste, c, d, epsilon)
    print(f"Versão básica:")
    print(f"  Resultado: {resultado1:.8f}")
    print(f"  Avaliações: {avaliacoes1}")
    
    # Versão otimizada
    resultado2, avaliacoes2 = integracao_dinamica_otimizada(f_teste, c, d, epsilon)
    print(f"Versão otimizada:")
    print(f"  Resultado: {resultado2:.8f}")
    print(f"  Avaliações: {avaliacoes2}")
    
    # Valor exato para comparação
    # ∫(x² + 1)dx de 0 a 2 = [x³/3 + x] de 0 a 2 = 8/3 + 2 = 14/3
    valor_exato = 14/3
    print(f"Valor exato: {valor_exato:.8f}")
    
    print(f"\nErro versão básica: {abs(resultado1 - valor_exato):.8f}")
    print(f"Erro versão otimizada: {abs(resultado2 - valor_exato):.8f}")
    
    if avaliacoes1 > avaliacoes2:
        reducao = (avaliacoes1 - avaliacoes2) / avaliacoes1 * 100
        print(f"Redução de avaliações: {avaliacoes1 - avaliacoes2} ({reducao:.1f}%)")
    
    print("\n")