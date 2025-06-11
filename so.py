import threading
import time
import os

# --- Repositório de Programas Disponíveis (como se estivessem "no HD") ---
AVAILABLE_PROGRAMS = {
    "Navegador Web": 256,
    "Editor de Texto": 128,
    "Player de Musica": 64,
    "IDE de Programacao": 384,
    "Jogo 3D": 512,
    "Calculadora": 32,
}

# As classes Process, ProcessManager e DeadlockDetector não precisam de alterações.
# Vou incluí-las aqui para que o código esteja completo.

class Process:
    READY = 'PRONTO'
    RUNNING = 'EXECUTANDO'
    BLOCKED = 'BLOQUEADO'

    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.state = Process.READY
        self.memory_footprint = 0
        self.resources_held = []

    def __repr__(self):
        return f"[PID={self.pid}, Nome='{self.name}', Estado={self.state}, Mem={self.memory_footprint} MB]"

class ProcessManager:
    def __init__(self):
        self.process_table = {}
        self.next_pid = 1

    def create_process(self, name, memory_needed):
        pid = self.next_pid
        process = Process(pid, name)
        process.memory_footprint = memory_needed
        self.process_table[pid] = process
        self.next_pid += 1
        print(f"📢 [PROCESSO] Criado: {process}")
        return process
    
    def remove_process(self, pid):
        if pid in self.process_table:
            del self.process_table[pid]
            return True
        return False

class MemoryManager:
    """
    MODIFICADO: Adicionada a função get_free_memory
    """
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.allocations = {}

    def get_used_memory(self):
        return sum(p.memory_footprint for p in self.allocations.values())

    def get_free_memory(self):
        return self.total_memory - self.get_used_memory()

    def allocate(self, process):
        if process.memory_footprint > self.get_free_memory():
            print(f"🧠 [MEMÓRIA] Falha ao alocar {process.memory_footprint} MB para {process.name}. Memória insuficiente.")
            return False
        self.allocations[process.pid] = process
        print(f"🧠 [MEMÓRIA] {process.name} alocado com {process.memory_footprint} MB.")
        return True

    def free(self, process):
        if process.pid in self.allocations:
            del self.allocations[process.pid]
            print(f"🧠 [MEMÓRIA] Liberação de memória por {process.name}")
            return True
        return False

class DeadlockDetector:
    def __init__(self, process_manager):
        self.process_manager = process_manager
        self.requests = {}

    def request_resource(self, process, resource):
        print(f"🚦 [DEADLOCK] {process.name} solicitou '{resource}'")
        self.requests[process.pid] = resource

    def check(self):
        print("\n🚦 [DEADLOCK] Verificando...")
        for pid1, req1 in self.requests.items():
            if pid1 not in self.process_manager.process_table: continue
            p1 = self.process_manager.process_table[pid1]
            
            for pid2, p2 in self.process_manager.process_table.items():
                if pid1 == pid2: continue
                if req1 in p2.resources_held:
                    req2 = self.requests.get(pid2)
                    if req2 and req2 in p1.resources_held:
                        print(f"🚨🚨🚨 [DEADLOCK] Detectado ciclo entre '{p1.name}' e '{p2.name}'!")
                        return True
        print("✅ [DEADLOCK] Nenhum deadlock encontrado no momento.")
        return False
    
    def clear_requests(self):
        self.requests.clear()

class OperatingSystem:
    def __init__(self):
        print("--- Sistema Operacional Simulado Inicializado ---")
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager(1024) # Total de 1024 MB (1 GB)
        self.deadlock_detector = DeadlockDetector(self.process_manager)

    def list_processes(self):
        print("\n--- LISTA DE PROCESSOS ATIVOS ---")
        if not self.process_manager.process_table:
            print("Nenhum processo ativo.")
        else:
            for pid, process in self.process_manager.process_table.items():
                print(process)
        print(f"Memória Usada: {self.memory_manager.get_used_memory()} MB / {self.memory_manager.total_memory} MB")
        print("---------------------------------")
        
    def terminate_process(self, pid):
        if pid not in self.process_manager.process_table:
            print(f"❌ [ERRO] Processo com PID {pid} não encontrado.")
            return False

        process = self.process_manager.process_table[pid]
        print(f"🔪 Finalizando {process.name} (PID: {pid})...")
        self.memory_manager.free(process)
        self.process_manager.remove_process(pid)
        print(f"✅ Processo {process.name} finalizado com sucesso.")
        return True

    def simulate_deadlock(self):
        print("\n--- SIMULANDO CENÁRIO DE DEADLOCK ---")
        p1 = self.process_manager.create_process("App_Banco", 100)
        p2 = self.process_manager.create_process("App_Relatorio", 100)
        r1 = "Impressora"
        r2 = "Scanner"

        p1.resources_held.append(r1)
        print(f"➡️ {p1.name} alocou o recurso '{r1}'")
        p2.resources_held.append(r2)
        print(f"➡️ {p2.name} alocou o recurso '{r2}'")
        self.deadlock_detector.request_resource(p1, r2)
        self.deadlock_detector.request_resource(p2, r1)
        self.deadlock_detector.check()
        self.terminate_process(p1.pid)
        self.terminate_process(p2.pid)
        self.deadlock_detector.clear_requests()
        print("--- FIM DA SIMULAÇÃO DE DEADLOCK ---\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    MODIFICADO: A função principal agora exibe a memória livre e a lista de
    programas disponíveis no menu.
    """
    so = OperatingSystem()
    
    while True:
        # Pega a memória livre atual para exibir no menu
        free_mem = so.memory_manager.get_free_memory()
        total_mem = so.memory_manager.total_memory

        print("\n╔════════════════════════════════════════════════════════════╗")
        print(f"║ Memória Livre: {free_mem} MB / {total_mem} MB{' ' * (31-len(str(free_mem))-len(str(total_mem)))}║")
        print("╠═══════ Programas Disponíveis para Iniciar ══════════════╣")
        # Lista os programas que podem ser inicializados
        for name, mem_cost in AVAILABLE_PROGRAMS.items():
            print(f"║ -> {name:<25} (Requer: {mem_cost} MB){' ' * (15-len(str(mem_cost)))}║")
        print("╠═══════════════════════════ MENU ═══════════════════════════╣")
        print("║ 1. Iniciar um Programa                                     ║")
        print("║ 2. Finalizar um Processo                                   ║")
        print("║ 3. Simular e Analisar Deadlock                             ║")
        print("║ 4. Listar Processos Ativos                                 ║")
        print("║ 5. Sair                                                    ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            clear_screen()
            print("--- Iniciar Novo Programa ---")
            prog_name = input("Digite o nome do programa que deseja iniciar (ex: Navegador Web): ")

            if prog_name in AVAILABLE_PROGRAMS:
                memory_needed = AVAILABLE_PROGRAMS[prog_name]
                process = so.process_manager.create_process(prog_name, memory_needed)
                if not so.memory_manager.allocate(process):
                    so.process_manager.remove_process(process.pid)
            else:
                print(f"❌ [ERRO] Programa '{prog_name}' não encontrado na lista de programas disponíveis.")
            
            input("\nPressione Enter para continuar...")
            clear_screen()

        elif choice == '2':
            clear_screen()
            print("--- Finalizar um Processo ---")
            so.list_processes()
            if not so.process_manager.process_table:
                input("\nPressione Enter para continuar...")
                clear_screen()
                continue
            try:
                pid_to_kill = int(input("Digite o PID do processo a ser finalizado: "))
                so.terminate_process(pid_to_kill)
            except ValueError:
                print("❌ [ERRO] O PID deve ser um número inteiro.")
            input("\nPressione Enter para continuar...")
            clear_screen()

        elif choice == '3':
            clear_screen()
            so.simulate_deadlock()
            input("\nPressione Enter para continuar...")
            clear_screen()

        elif choice == '4':
            clear_screen()
            so.list_processes()
            input("\nPressione Enter para continuar...")
            clear_screen()

        elif choice == '5':
            print("Finalizando o simulador...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()