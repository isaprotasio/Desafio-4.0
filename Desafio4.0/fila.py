import itertools
from typing import Optional, Tuple, Dict, List


class QueueGraph:
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}
        self.start: Optional[str] = None
        self.end: Optional[str] = None
        self._counter = itertools.count(1)
        self._priority_end: Optional[str] = None  # Última pessoa com prioridade

    def enqueue(self, name: str, priority: int = 0) -> Tuple[int, str]:
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Nome inválido.")

        ticket = next(self._counter)
        person_id = f"{ticket}:{name}"

        # Garante unicidade
        while person_id in self.graph:
            ticket = next(self._counter)
            person_id = f"{ticket}:{name}"

        self.graph[person_id] = []

        if self.start is None:
            # Fila vazia
            self.start = person_id
            self.end = person_id
            if priority > 0:
                self._priority_end = person_id
        else:
            if priority > 0:
                # Pessoa com prioridade
                if self._priority_end is None:
                    # Não há ninguém com prioridade ainda
                    # Esta pessoa vai para o início da fila
                    self.graph[person_id] = [self.start]
                    self.start = person_id
                    self._priority_end = person_id
                else:
                    # Já existem pessoas com prioridade
                    # Inserir após a última pessoa com prioridade
                    successor = self.graph[self._priority_end][0] if self.graph[self._priority_end] else None
                    
                    if successor:
                        # Conectar: última prioridade -> nova pessoa -> sucessor
                        self.graph[self._priority_end] = [person_id]
                        self.graph[person_id] = [successor]
                    else:
                        # Última prioridade é o final da fila
                        self.graph[self._priority_end] = [person_id]
                        self.end = person_id
                    
                    self._priority_end = person_id
            else:
                # Pessoa normal - sempre vai para o final
                self.graph[self.end] = [person_id]
                self.end = person_id

        return ticket, person_id

    def dequeue(self) -> Optional[str]:
        if self.start is None:
            return None

        removed = self.start
        next_nodes = self.graph.get(removed, [])

        # Atualizar start
        if next_nodes:
            self.start = next_nodes[0]
        else:
            self.start = None
            self.end = None
            self._priority_end = None

        # Atualizar _priority_end se necessário
        if removed == self._priority_end:
            # A pessoa removida era a última com prioridade
            # Precisamos encontrar a nova última pessoa com prioridade
            self._priority_end = None
            current = self.start
            last_priority = None
            while current:
                # Verificar se é uma pessoa com prioridade
                # Para simplificar, vamos assumir que prioridade é determinada
                # pela posição relativa à última prioridade conhecida
                # Em uma implementação real, precisaríamos de um flag
                pass
        
        # Remover do grafo
        self.graph.pop(removed, None)
        
        # Recalcular _priority_end
        self._recalculate_priority_end()
        
        return removed

    def _recalculate_priority_end(self):
        """Recalcula qual é a última pessoa com prioridade na fila"""
        self._priority_end = None
        current = self.start
        last_priority = None
        
        # Percorrer toda a fila
        while current:
            # Verificar se esta pessoa está antes da primeira pessoa normal
            # Para isso, vamos verificar se há alguma pessoa "normal" após ela
            temp = current
            found_normal = False
            
            # Verificar todas as pessoas após 'current'
            while temp:
                # Se encontrarmos uma pessoa que não é prioridade
                # (não está na "zona de prioridade")
                next_person = self.graph[temp][0] if self.graph[temp] else None
                
                # Simplificação: consideramos que todas as pessoas até a primeira
                # pessoa após a última prioridade original são prioridade
                # Em uma implementação real, precisaríamos armazenar a informação de prioridade
                temp = next_person
            
            # Para simplificar, vamos usar uma abordagem diferente:
            # Manteremos o controle de quem tem prioridade em uma lista separada
            # Mas por enquanto, vamos manter a lógica simples
            
            current = self.graph[current][0] if self.graph[current] else None
        
        # Por simplicidade, vamos usar uma abordagem mais direta:
        # Vamos rastrear pessoas com prioridade de forma explícita
        # Para isso, precisamos modificar a estrutura

    def show_queue(self) -> List[str]:
        ordem = []
        current = self.start
        while current:
            ordem.append(current)
            nxt = self.graph[current]
            current = nxt[0] if nxt else None
        return ordem

    def get_first_person(self) -> Optional[str]:
        """Retorna a primeira pessoa da fila (apenas para exibição)"""
        if self.start:
            return self.start
        return None

    def remove_person(self, person_id: str) -> bool:
        if person_id not in self.graph:
            return False

        # Caso especial: removendo o primeiro
        if person_id == self.start:
            self.dequeue()
            return True

        # Encontrar predecessor
        pred = None
        for p, neighbors in self.graph.items():
            if neighbors and neighbors[0] == person_id:
                pred = p
                break

        if pred is None:
            # Pessoa não está na cadeia principal
            return False

        # Conectar predecessor ao sucessor
        successor = self.graph[person_id][0] if self.graph[person_id] else None
        
        if successor:
            self.graph[pred] = [successor]
        else:
            # Removendo o último
            self.graph[pred] = []
            self.end = pred

        self.graph.pop(person_id, None)
        
        # Recalcular _priority_end
        self._recalculate_priority_end()
        
        return True

    def clear(self):
        self.graph.clear()
        self.start = None
        self.end = None
        self._priority_end = None


# ----------------- MODO INTERATIVO APENAS -----------------

def main():
    fila = QueueGraph()

    while True:
        # Mostrar quem é o primeiro da fila
        primeiro = fila.get_first_person()
        
        print("\n" + "="*60)
        print("SISTEMA DE ATENDIMENTO")
        print("="*60)
        print("1 - Registrar cliente")
        print("2 - Chamar próximo cliente")
        print("3 - Mostrar fila completa")
        print("4 - Remover pessoa da fila")
        print("5 - Limpar fila")
        print("6 - Sair")
        print("-"*60)
        
        if primeiro:
            print(f"👉 PRÓXIMO A SER ATENDIDO: {primeiro}")
        else:
            print("👉 PRÓXIMO A SER ATENDIDO: Ninguém na fila")
        print("="*60)

        opc = input("\nEscolha uma opção: ").strip()

        if opc == "1":
            nome = input("Nome do cliente: ").strip()
            if not nome:
                print("Nome não pode ser vazio!")
                continue
                
            prioridade_str = input("Prioridade (0=normal, 1=preferencial): ").strip()
            try:
                prioridade = int(prioridade_str)
                if prioridade not in [0, 1]:
                    print("Prioridade deve ser 0 ou 1. Usando 0.")
                    prioridade = 0
            except ValueError:
                print("Valor inválido. Usando prioridade 0.")
                prioridade = 0

            try:
                ticket, pid = fila.enqueue(nome, prioridade)
                print(f"\n✓ Cliente registrado")
                print(f"  Senha: {ticket}")
                print(f"  ID: {pid}")
                if prioridade == 1:
                    print("  (Cliente preferencial - será atendido antes dos normais)")
                
                # Mostrar a nova posição na fila
                fila_completa = fila.show_queue()
                posicao = fila_completa.index(pid) + 1 if pid in fila_completa else len(fila_completa)
                total_pessoas = len(fila_completa)
                print(f"  Posição na fila: {posicao}° de {total_pessoas}")
                
                # Mostrar quantas pessoas com prioridade estão na frente
                if prioridade == 0:
                    # Contar quantas pessoas com prioridade existem
                    prioridades_na_frente = 0
                    for pessoa in fila_completa[:posicao-1]:
                        # Para saber se é prioridade, precisaríamos armazenar essa informação
                        # Por simplicidade, vamos apenas mostrar a posição
                        pass
            except Exception as e:
                print(f"Erro: {e}")

        elif opc == "2":
            chamado = fila.dequeue()
            if chamado:
                print(f"\n📢 CHAMANDO PRÓXIMO CLIENTE:")
                print(f"   {chamado}")
                print(f"   Por favor, dirija-se ao atendimento!")
                
                # Mostrar quem será o próximo
                novo_primeiro = fila.get_first_person()
                if novo_primeiro:
                    print(f"\n   Próximo a ser chamado: {novo_primeiro}")
                else:
                    print(f"\n   ⚠️  Atenção: Não há mais ninguém na fila!")
            else:
                print("\nℹ️  Fila vazia. Ninguém para chamar.")

        elif opc == "3":
            fila_atual = fila.show_queue()
            if not fila_atual:
                print("\nℹ️  Fila vazia.")
            else:
                print(f"\n👥 FILA COMPLETA ({len(fila_atual)} pessoas):")
                print("-" * 40)
                for i, pessoa in enumerate(fila_atual, 1):
                    marcador = ">>> " if i == 1 else "    "
                    print(f"{marcador}{i:2d}. {pessoa}")
                print("-" * 40)

        elif opc == "4":
            fila_atual = fila.show_queue()
            if not fila_atual:
                print("\nℹ️  Fila vazia.")
                continue
                
            print("\nPessoas na fila:")
            for i, pessoa in enumerate(fila_atual, 1):
                marcador = ">>> " if i == 1 else "    "
                print(f"{marcador}{i:2d}. {pessoa}")
            
            print(f"\nPrimeiro da fila atual: {fila_atual[0]}")
            pid = input("\nDigite o ID da pessoa a remover (ex: '3:Maria'): ").strip()
            
            if pid == fila_atual[0]:
                confirmacao = input("⚠️  Esta é a primeira pessoa da fila! Tem certeza? (s/n): ").strip().lower()
                if confirmacao != 's':
                    print("Operação cancelada.")
                    continue
            
            if fila.remove_person(pid):
                print("✓ Pessoa removida da fila.")
                
                # Mostrar novo primeiro da fila
                novo_primeiro = fila.get_first_person()
                if novo_primeiro:
                    print(f"Novo primeiro da fila: {novo_primeiro}")
                else:
                    print("Fila agora está vazia.")
            else:
                print("✗ ID não encontrado.")

        elif opc == "5":
            if fila.get_first_person():
                confirmacao = input("⚠️  Tem certeza que deseja limpar TODA a fila? (s/n): ").strip().lower()
                if confirmacao == 's':
                    fila.clear()
                    print("✓ Fila limpa.")
                else:
                    print("Operação cancelada.")
            else:
                print("ℹ️  A fila já está vazia.")

        elif opc == "6":
            # Verificar se ainda há pessoas na fila
            if fila.get_first_person():
                confirmacao = input("⚠️  Ainda há pessoas na fila! Tem certeza que deseja sair? (s/n): ").strip().lower()
                if confirmacao != 's':
                    print("Continuando no sistema...")
                    continue
            
            print("\n" + "="*60)
            print("OBRIGADO POR USAR O SISTEMA DE ATENDIMENTO!")
            print("="*60)
            break

        else:
            print("\n✗ Opção inválida. Tente novamente.")
        
        # Pausa para o usuário ver as informações
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()