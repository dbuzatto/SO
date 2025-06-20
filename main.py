import tkinter as tk

AVAILABLE_PROGRAMS = {
    "Navegador Web": 256,
    "Editor de Texto": 128,
    "Player de Musica": 64,
    "IDE de Programacao": 384,
    "Jogo 3D": 512,
    "Calculadora": 32,
}

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
        return process, f"📢 [PROCESSO] Criado: {process}"
    
    def remove_process(self, pid):
        if pid in self.process_table:
            process = self.process_table[pid]
            del self.process_table[pid]
            return True, f"✅ Processo {process.name} (PID {pid}) removido."
        return False, f"❌ Processo com PID {pid} não encontrado."
    
    def remove_all(self):
        count = len(self.process_table)
        self.process_table.clear()
        return f"✅ Todos os {count} processos foram finalizados."

class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.allocations = {}

    def get_used_memory(self):
        return sum(p.memory_footprint for p in self.allocations.values())

    def get_free_memory(self):
        return self.total_memory - self.get_used_memory()

    def allocate(self, process):
        if process.memory_footprint > self.get_free_memory():
            return False, f"🧠 Memória insuficiente para alocar {process.memory_footprint} MB ao {process.name}."
        self.allocations[process.pid] = process
        return True, f"🧠 {process.name} alocado com {process.memory_footprint} MB."

    def free(self, process):
        if process.pid in self.allocations:
            del self.allocations[process.pid]
            return True, f"🧠 Memória liberada por {process.name}."
        return False, f"❌ Memória de {process.name} já estava liberada."

    def free_all(self):
        count = len(self.allocations)
        self.allocations.clear()
        return f"🧠 Memória liberada para todos os {count} processos."

class DeadlockDetector:
    def __init__(self, process_manager):
        self.process_manager = process_manager
        self.requests = {}

    def request_resource(self, process, resource):
        self.requests[process.pid] = resource

    def check(self):
        for pid1, req1 in self.requests.items():
            if pid1 not in self.process_manager.process_table: continue
            p1 = self.process_manager.process_table[pid1]
            for pid2, p2 in self.process_manager.process_table.items():
                if pid1 == pid2: continue
                if req1 in p2.resources_held:
                    req2 = self.requests.get(pid2)
                    if req2 and req2 in p1.resources_held:
                        return (p1, p2), f"🚨🚨🚨 Deadlock detectado entre '{p1.name}' e '{p2.name}'!"
        return None, "✅ Nenhum deadlock encontrado no momento."
    
    def clear_requests(self):
        self.requests.clear()

class OperatingSystem:
    def __init__(self):
        self.process_manager = ProcessManager()
        self.memory_manager = MemoryManager(1024)
        self.deadlock_detector = DeadlockDetector(self.process_manager)

    def list_processes(self):
        if not self.process_manager.process_table:
            return ["Nenhum processo ativo."]
        return [str(p) for p in self.process_manager.process_table.values()]

    def terminate_process(self, pid):
        if pid not in self.process_manager.process_table:
            return False, f"❌ Processo com PID {pid} não encontrado."
        process = self.process_manager.process_table[pid]
        freed, mem_msg = self.memory_manager.free(process)
        removed, rm_msg = self.process_manager.remove_process(pid)
        return True, f"🔪 {rm_msg}\n{mem_msg}"

    def terminate_all_processes(self):
        count = len(self.process_manager.process_table)
        self.process_manager.remove_all()
        mem_msg = self.memory_manager.free_all()
        return f"✅ Todos os {count} processos finalizados.\n{mem_msg}"

    def simulate_deadlock(self):
        nomes = sorted(AVAILABLE_PROGRAMS.items(), key=lambda x: x[1], reverse=True)
        prog1_name, prog1_mem = nomes[0]
        prog2_name, prog2_mem = nomes[1]

        p1, msg1 = self.process_manager.create_process(prog1_name, prog1_mem)
        p2, msg2 = self.process_manager.create_process(prog2_name, prog2_mem)

        ok1, mem_msg1 = self.memory_manager.allocate(p1)
        ok2, mem_msg2 = self.memory_manager.allocate(p2)

        msgs = [msg1, msg2, mem_msg1, mem_msg2]

        if not (ok1 and ok2):
            msgs.append("❌ Não há memória suficiente para simular deadlock.")
            if ok1:
                self.memory_manager.free(p1)
                self.process_manager.remove_process(p1.pid)
            if ok2:
                self.memory_manager.free(p2)
                self.process_manager.remove_process(p2.pid)
            return None, "\n".join(msgs)

        r1 = "Impressora"
        r2 = "Scanner"

        p1.resources_held.append(r1)
        p2.resources_held.append(r2)
        self.deadlock_detector.request_resource(p1, r2)
        self.deadlock_detector.request_resource(p2, r1)

        deadlock_info, deadlock_msg = self.deadlock_detector.check()
        msgs.append(deadlock_msg)

        return deadlock_info, "\n".join(msgs)

class OSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SO Simulado")
        self.os = OperatingSystem()

        self.log = tk.Text(root, height=15, width=70)
        self.log.pack(pady=5)

        self.mem_label = tk.Label(root, text="")
        self.mem_label.pack()

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Iniciar Programa", command=self.start_program).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Finalizar Processo", command=self.end_process).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Simular Deadlock", command=self.simulate_deadlock).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Listar Processos", command=self.list_processes).grid(row=0, column=3, padx=5)

        self.update_memory()

    def log_msg(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)

    def update_memory(self):
        used = self.os.memory_manager.get_used_memory()
        total = self.os.memory_manager.total_memory
        self.mem_label.config(text=f"Memória Usada: {used} MB / {total} MB")

    def start_program(self):
        popup = tk.Toplevel(self.root)
        popup.title("Selecionar Programa")
        tk.Label(popup, text="Escolha um programa para iniciar:").pack(pady=5)

        selected = tk.StringVar(popup)
        selected.set(list(AVAILABLE_PROGRAMS.keys())[0])
        dropdown = tk.OptionMenu(popup, selected, *AVAILABLE_PROGRAMS.keys())
        dropdown.pack(pady=5)

        def iniciar():
            prog = selected.get()
            mem = AVAILABLE_PROGRAMS[prog]
            proc, msg1 = self.os.process_manager.create_process(prog, mem)
            success, msg2 = self.os.memory_manager.allocate(proc)
            if not success:
                self.os.process_manager.remove_process(proc.pid)
            self.log_msg(msg1)
            self.log_msg(msg2)
            popup.destroy()
            self.update_memory()

        tk.Button(popup, text="Iniciar", command=iniciar).pack(pady=10)

    def end_process(self):
        popup = tk.Toplevel(self.root)
        popup.title("Finalizar Processo")

        tk.Label(popup, text="Digite o PID para finalizar ou clique em 'Finalizar Todos'").pack(pady=5)

        entry = tk.Entry(popup)
        entry.pack(pady=5)

        def finalizar_pid():
            try:
                pid = int(entry.get())
            except:
                self.log_msg("PID inválido")
                return
            ok, msg = self.os.terminate_process(pid)
            self.log_msg(msg)
            if ok:
                popup.destroy()
                self.update_memory()

        def finalizar_todos():
            msg = self.os.terminate_all_processes()
            self.log_msg(msg)
            popup.destroy()
            self.update_memory()

        tk.Button(popup, text="Finalizar PID", command=finalizar_pid).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(popup, text="Finalizar Todos", command=finalizar_todos).pack(side=tk.RIGHT, padx=10, pady=10)

    def simulate_deadlock(self):
        deadlock_info, msg = self.os.simulate_deadlock()
        self.log_msg(msg)
        self.update_memory()

        if deadlock_info:
            p1, p2 = deadlock_info
            self.ask_resolve_deadlock(p1, p2)

    def ask_resolve_deadlock(self, p1, p2):
        popup = tk.Toplevel(self.root)
        popup.title("Deadlock Detectado!")

        tk.Label(popup, text="Deadlock detectado entre:").pack(pady=5)
        tk.Label(popup, text=f"{p1}").pack(pady=5)
        tk.Label(popup, text=f"{p2}").pack(pady=5)
        tk.Label(popup, text="Escolha um processo para finalizar e resolver o deadlock:").pack(pady=5)

        def finalizar_processo(process):
            ok, msg = self.os.terminate_process(process.pid)
            self.os.deadlock_detector.clear_requests()
            self.log_msg(msg)
            self.update_memory()
            popup.destroy()

        btn1 = tk.Button(popup, text=f"Finalizar {p1.name} (PID {p1.pid})", command=lambda: finalizar_processo(p1))
        btn1.pack(side=tk.LEFT, padx=10, pady=10)

        btn2 = tk.Button(popup, text=f"Finalizar {p2.name} (PID {p2.pid})", command=lambda: finalizar_processo(p2))
        btn2.pack(side=tk.RIGHT, padx=10, pady=10)

    def list_processes(self):
        procs = self.os.list_processes()
        self.log_msg("\n--- Processos Ativos ---")
        for p in procs:
            self.log_msg(p)
        self.update_memory()

if __name__ == "__main__":
    root = tk.Tk()
    app = OSApp(root)
    root.mainloop()
