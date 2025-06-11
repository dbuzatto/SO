# 🖥️ Simulador de Sistema Operacional

Este projeto é um simulador didático de um sistema operacional em Python, com funcionalidades básicas de gerenciamento de processos, alocação de memória e detecção de deadlocks. É uma excelente ferramenta para fins educacionais e demonstrações interativas de conceitos fundamentais de sistemas operacionais.

---

## 📋 Funcionalidades

- **Gerenciamento de Processos**: Criação, listagem e finalização de processos.
- **Gerenciamento de Memória**: Alocação de memória dinâmica e cálculo de memória disponível.
- **Detecção de Deadlocks**: Simulação de situações de deadlock com recursos cruzados e verificação de ciclos.
- **Menu Interativo em Console**: Interface simples para usuários interagirem com o sistema simulado.
- **Programas Pré-definidos**: Lista de programas fictícios disponíveis para "execução".

---

## 🚀 Como Executar

1. **Requisitos**:
   - Python 3.7 ou superior

2. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/simulador-so.git
   cd simulador-so
   ```

3. **Execute o script**:
   ```bash
   python so.py
   ```

---

## 📸 Exemplo de Execução

```
╔════════════════════════════════════════════════════════════╗
║ Memória Livre: 1024 MB / 1024 MB                          ║
╠═══════ Programas Disponíveis para Iniciar ══════════════╣
║ -> Navegador Web             (Requer: 256 MB)           ║
║ -> Editor de Texto           (Requer: 128 MB)           ║
║ -> Player de Musica          (Requer: 64 MB)            ║
║ -> IDE de Programacao        (Requer: 384 MB)           ║
║ -> Jogo 3D                   (Requer: 512 MB)           ║
║ -> Calculadora               (Requer: 32 MB)            ║
╠═══════════════════════════ MENU ═══════════════════════════╣
║ 1. Iniciar um Programa                                     ║
║ 2. Finalizar um Processo                                   ║
║ 3. Simular e Analisar Deadlock                             ║
║ 4. Listar Processos Ativos                                 ║
║ 5. Sair                                                    ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🛠️ Estrutura de Código

- `Process`, `ProcessManager`: classes responsáveis por representar e gerenciar processos.
- `MemoryManager`: controla a alocação e liberação de memória.
- `DeadlockDetector`: simula e identifica deadlocks baseando-se em dependências entre processos e recursos.
- `OperatingSystem`: orquestra os componentes e fornece funções principais.
- `main()`: função que exibe o menu interativo e responde a comandos do usuário.

---

## 🧪 Teste de Deadlock

A simulação de deadlock cria dois processos com recursos distintos e pedidos cruzados, reproduzindo um ciclo de espera típico de deadlocks. O sistema identifica e notifica o usuário sobre o ciclo detectado.

